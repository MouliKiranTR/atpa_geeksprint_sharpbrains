[[_TOC_]]

**Original issue**
Starting from the beginning of February production instances of Checkpoint web application periodically are crashed with OutOfMemoryException.
Related bug is #174842 

This article describes the investigation of the problem. 

## Heap dump analysis

Eclipse Memory Analyzer [MAT](https://eclipse.dev/mat/) has been used for heap dump analysis. Additionally following plugin has been installed - [MAT Calcite plugin](https://github.com/vlsi/mat-calcite-plugin) that allows to use syntax close to SQL for executing analysis queries.

DevOps team provided several dumps. All of them has the same problem - a big amount of java.lang.ref.Finalizer instances. This class is responsible for execution of finalize method in classes that have it.

![Screenshot 2025-05-29 181642.png](/.attachments/Screenshot%202025-05-29%20181642-4655baad-26f7-49ec-a34b-f177c837bb46.png)

Object finalization is executed after the phase when object was already processed and collected by garbage collector (GC). If object has finalize() method it will be put into specific queue. This queue is processed by java.lang.ref.Finalizer that correctly finalize the object lifecycle (for example flush buffers on disk, correctly close files, etc). Finalizer is single thread object, and it is not possible to process objects from queue in parallel.

Using Calcite plugin and the next query 

```
select f.referent['@className'] clsName, sum(shallowSize(f.referent)) shallow, sum(retainedSize(f.referent)) retained, count(*) cnt from "java.lang.ref.Finalizer" f group by f.referent['@className'] order by retained, cnt desc
```

there were collected information about objects that are waiting the finalization in queue. Additionally, query collected amount of shallow memory size, retained memory size and number of objects

| clsName                                                           |    shallow |      retained  |    cnt  |
|-------------------------------------------------------------------|-----------:|---------------:|--------:|
| sun.security.ssl.SSLSocketImpl                                    |  7,351,200 |  8,599,838,768 | 102,100 |
| org.htmlparser.lexer.Page                                         |    175,584 |  5,657,834,976 |   5,487 |
| com.westgroup.novus.message.ResponseIterator                      |  1,389,056 |    279,292,968 |  21,704 |
| org.apache.cxf.jaxws.JaxWsClientProxy                             |    102,816 |    220,473,168 |   3,213 |
| com.sun.xml.bind.v2.runtime.unmarshaller.UnmarshallerImpl         |    396,984 |    212,448,536 |   7,089 |
| com.westgroup.novus.message.AsyncClient                           |  1,742,208 |    101,483,616 |  18,148 |
| java.util.zip.ZipFile$CleanableResource$FinalizableResource       |  4,840,512 |     89,147,528 | 151,266 |
| org.postgresql.jdbc.PgConnection                                  |     73,600 |     55,666,432 |     575 |
| com.sun.mail.smtp.SMTPTransport                                   |    110,880 |      7,148,320 |     660 |
| javax.imageio.stream.FileCacheImageOutputStream                   |     13,120 |      1,390,720 |     164 |
| java.util.concurrent.Executors$FinalizableDelegatedExecutorService|     24,096 |        877,464 |   1,506 |
| sun.net.www.http.KeepAliveStream                                  |    400,000 |        518,944 |   6,250 |
| split.org.apache.http.impl.conn.PoolingHttpClientConnectionManager|         32 |        158,328 |       1 |
| com.sun.jndi.ldap.LdapSearchEnumeration                           |      2,592 |        146,736 |      36 |
| org.apache.http.impl.conn.PoolingHttpClientConnectionManager      |      1,696 |        141,304 |      53 |
| org.apache.tomcat.util.http.fileupload.disk.DiskFileItem          |      5,888 |         99,360 |      92 |
| com.sun.jndi.ldap.LdapCtx                                         |      6,016 |         78,488 |      47 |
| com.sun.jndi.ldap.LdapClient                                      |      1,472 |         59,304 |      46 |
| org.apache.commons.fileupload.disk.DiskFileItem                   |         64 |         31,808 |       1 |
| com.sun.net.ssl.internal.ssl.Provider                             |        104 |         21,080 |       1 |
| java.util.Timer$1                                                 |        464 |         19,464 |      29 |
| javax.imageio.spi.SubRegistry                                     |        160 |         11,048 |       5 |
| com.westgroup.novus.messenger.MQPool                              |        160 |          2,304 |       4 |
| datadog.trace.agent.core.CoreTracer                               |        200 |          1,680 |       1 |
| com.amazonaws.auth.InstanceProfileCredentialsProvider             |         24 |          1,672 |       1 |
| javax.imageio.spi.IIORegistry                                     |         16 |            320 |       1 |
| org.apache.xml.resolver.readers.TR9401CatalogReader               |         32 |            152 |       1 |
| jnr.ffi.provider.jffi.AbstractX86StubCompiler$PageHolder          |         80 |             80 |       2 |
| Total: 28 entries                                                 | 16,639,056 | 15,226,894,568 | 318,483 |
-------------------------------------------------------------------------------------------------------------

We can make the conclusion that most problematic objects in queue are instances of sun.security.ssl.SSLSocketImpl. 
At first glance, the analysis and searching information about potential problem shows that until Java 12 there is no bounded limit to number of SSL sessions stored in SSL cache. 
Additionally, the analysis was executed to get information about hosts that SSL sessions belong to. For collecting this information, the following query has been executed:

```
select t.peerHost, sum(t.shSize) shallow, sum(t.retSize) retained, count(*) cnt from (
	select toString(s.peerHost) peerHost, shallowSize(s.this) shSize, retainedSize(s.this) retSize from "sun.security.ssl.SSLSocketImpl" s
) as t group by t.peerHost order by retained, cnt desc
```

| peerHost                                                                                   |   shallow |      retained |     cnt |
|--------------------------------------------------------------------------------------------|----------:|--------------:|--------:|
| cp-prod-cp-doc-recommendation-service.tr-tax-cp-prod.aws-int.thomsonreuters.com            | 1,538,424 | 2,071,363,672 |  21,367 |
| cp-prod-services.tr-tax-cp-prod.aws-int.thomsonreuters.com                                 | 1,505,880 | 2,039,128,360 |  20,915 |
| cp-prod-cp-notifications-service.tr-tax-cp-prod.aws-int.thomsonreuters.com                 | 1,354,320 | 2,236,778,600 |  18,810 |
| trtacheckpointus-prod-use1.04032.aws-int.thomsonreuters.com                                |   846,648 |   303,466,288 |  11,759 |
| site-use1c2.checkpoint.thomsonreuters.com                                                  |   592,632 |   118,322,192 |   8,231 |
| cp-prod-cp-user-profile-service.tr-tax-cp-prod.aws-int.thomsonreuters.com                  |   346,176 |   573,078,496 |   4,808 |
| cpa-prod-autosuggest-recommender.tr-tax-cp-prod.aws-int.thomsonreuters.com                 |   343,656 |   469,916,624 |   4,773 |
| auth.thomsonreuters.com                                                                    |   196,056 |   141,914,952 |   2,723 |
| ai-conversations-prod.plexus-ras-use1.3772.aws-int.thomsonreuters.com                      |   131,904 |   110,271,056 |   1,832 |
| cp-prod-cp-spellcheck-service.tr-tax-cp-prod.aws-int.thomsonreuters.com                    |   106,848 |   131,766,032 |   1,484 |
| onesource-idt-det-amer-int.hostedtax.thomsonreuters.com                                    |   103,032 |    77,976,408 |   1,431 |
| cp-prod-cp-snapshots-service.tr-tax-cp-prod.aws-int.thomsonreuters.com                     |    77,472 |   106,385,584 |   1,076 |
| a203669-checkpoint-research-prod-us-east-1.cluster-c8cik2zlbtiq.us-east-1.rds.amazonaws.com|    56,952 |    23,142,968 |     791 |
| cp-prod-cp-tools-service.tr-tax-cp-prod.aws-int.thomsonreuters.com                         |    47,664 |    65,687,400 |     662 |
| a205159-akkadia-prod-use1.tr-tax-cp-prod.aws-int.thomsonreuters.com                        |    34,344 |    44,195,176 |     477 |
| cp-prod-cp-metadata-service.tr-tax-cp-prod.aws-int.thomsonreuters.com                      |    30,384 |    53,739,680 |     422 |
| events.split.io                                                                            |    14,184 |     5,300,144 |     197 |
| us-checkpoint.contractexpress.com                                                          |     6,624 |     8,468,152 |      92 |
| cp-prod-cp-toc-service.tr-tax-cp-prod.aws-int.thomsonreuters.com                           |     5,400 |     8,484,712 |      75 |
| trtagis-prod-use1.04032.aws-int.thomsonreuters.com                                         |     3,888 |     4,850,536 |      54 |
| cp-prod-cp-export-service.tr-tax-cp-prod.aws-int.thomsonreuters.com                        |     3,528 |     2,277,600 |      49 |
| sdk.split.io                                                                               |     1,944 |       402,016 |      27 |
| api.thomsonreuters.com                                                                     |       936 |     1,246,680 |      13 |
| cpadmin.thomsonreuters.com                                                                 |       504 |       676,872 |       7 |
| entitlement.gcs.thomsonreuters.com                                                         |       504 |       428,296 |       7 |
| a207947-novus-prod.ldap.1667.aws-int.thomsonreuters.com                                    |       432 |        53,072 |       6 |
| cobaltservices-use1-prod.dataroom-prod.aws-int.thomsonreuters.com                          |       144 |       244,072 |       2 | 
| api.draftable.com                                                                          |       144 |        93,008 |       2 |
| api.int.thomsonreuters.com                                                                 |       144 |        25,720 |       2 |
| b-87a985b1-13b8-4873-a3b9-134e81f8add3-1.mq.us-east-1.amazonaws.com                        |        72 |           216 |       1 |
| sso-auth.thomsonreuters.com                                                                |        72 |        12,568 |       1 |
| b-86bb644e-aad7-4c20-86e6-ef7e98887b25-1.mq.us-east-1.amazonaws.com                        |        72 |        14,328 |       1 |
| trtasso-service.thomson.com                                                                |        72 |        12,088 |       1 |
| dtxp-eform-prod-api.int.thomsonreuters.com                                                 |        72 |        94,400 |       1 |
| vds-qa.int.thomsonreuters.com                                                              |        72 |        12,144 |       1 | 
| trtasso.thomson.com                                                                        |        72 |        21,728 |       1 |
| Total: 36 entries                                                                          | 7,351,272 | 8,599,851,840 | 102,101 |
------------------------------------------------------------------------------------------------------------------------------------

The result of query shows that most of connections are related to Checkpoint services, but it still not clear why finalizer do not execute the logic effectively for finalize() method for SSL connection.

## Analyzing of JVM collected events

It was decided to collect additional information using runtime tooling. For collecting runtime information Java Flight Recorder has been used. It is embedded tool of JVM that allows to collect different JVM events and save them to files or collect in runtime and then visualize in Mission Control. Mission control has highlighted problem with Socket read operations. 

![Screenshot 2025-05-30 195439.png](/.attachments/Screenshot%202025-05-30%20195439-952d5018-b939-489b-8f67-64f22071d42f.png)

After finding related JVM socket event it was identified that Finalizer waits 10 minutes on the operation to read bytes from host trtacheckpointus-prod-use1.04032.aws-int.thomsonreuters.com.

![Screenshot 2025-05-29 234803.png](/.attachments/Screenshot%202025-05-29%20234803-241b71da-0f9f-4e75-af86-d6c4e61c7bac.png)

Stacktrace of stacked operation showed that code sends SSL close_notify event to server and waiting for the same event from server to correctly finish communication in duplex mode for SSL session. But server did not send this event. 

```
int java.net.SocketInputStream.read(byte[], int, int, int)	
int java.net.SocketInputStream.read(byte[], int, int)
int java.net.SocketInputStream.read()
void sun.security.ssl.SSLSocketInputRecord.deplete(boolean)
void sun.security.ssl.SSLSocketImpl$AppInputStream.readLockedDeplete()
void sun.security.ssl.SSLSocketImpl$AppInputStream.deplete()
void sun.security.ssl.SSLSocketImpl.bruteForceCloseInput(boolean)
void sun.security.ssl.SSLSocketImpl.duplexCloseOutput()
void sun.security.ssl.SSLSocketImpl.close()
void sun.security.ssl.BaseSSLSocketImpl.finalize()
void java.lang.System$2.invokeFinalize(Object)
void java.lang.ref.Finalizer.runFinalizer(JavaLangAccess)
void java.lang.ref.Finalizer$FinalizerThread.run()
```

Making the analysis of Java code it was identified that timeout of http client used for connection to Cobalt domain is configured for 10 minutes, while timeouts for http clients of first top 3 domain from previous table are configured for 1 minute.

| host                                                                            | timeout in milis |
|---------------------------------------------------------------------------------|-----------------:|
| cp-prod-cp-doc-recommendation-service.tr-tax-cp-prod.aws-int.thomsonreuters.com |           60,000 |
| cp-prod-services.tr-tax-cp-prod.aws-int.thomsonreuters.com                      |           60,000 |
| cp-prod-cp-notifications-service.tr-tax-cp-prod.aws-int.thomsonreuters.com      |           60,000 |
| trtacheckpointus-prod-use1.04032.aws-int.thomsonreuters.com                     |          600_000 |

Analysis of calls to domain trtacheckpointus-prod-use1.04032.aws-int.thomsonreuters.com in DataDog showed that connection does not exceed 10 seconds during the search activities.


## Follow up steps.

Here is list of follow up steps to improve the situation with finalization of work for SSL sessions.

### Optimize timeout of http client used for connection to TRTA Search

The following steps are suggested to introduce and test changes safely for application.

1. Modify and extract http client timeout value into configurable property. Assign by default exist value - 10 minutes.
2. During the release cycle configure this property for one of the production instance to 1 minute and enable JFR to record runtime events for follow up analysis
3. Collect JFR recording files and review whether Finalizer is stacked on closing connection to TRTA Search domain
4. If results of analysis are positive configure property through CMDB for all instances.
5. If results of testing changes are positive apply 1 minute timeout as default value for connection to TRTA Search domain.

### Optimize a number of SSL sessions in cache
We can decrease a number of SSL session that are located in cache. There is [article](https://access.redhat.com/solutions/2682761) on RedHat support portal that explains the problem with cache. The size of cache could be modified by adding JVM parameter javax.net.ssl.sessionCacheSize through CMDB. SSL session connection is unbounded by default until JDK 11. Starting from JDK 12 default value is 20480
