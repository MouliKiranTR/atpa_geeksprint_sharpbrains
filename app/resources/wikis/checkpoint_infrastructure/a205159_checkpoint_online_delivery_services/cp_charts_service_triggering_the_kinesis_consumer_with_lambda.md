Triggering the **Kinesis** consumer with **Lambda** for **Local Testing** of cp_charts-service:

**1.**  Add this parameter in your IDEA to **environment variable** for running the cp_charts-service to ensure that the CI stream is not affected by the local instance you are running:  
    `aws.kinesis.bindings.content.applicationName=a205159-cp-dev-charts-kinesis-local-<your id or any random string>`

**2.**  Add these lines to application-local.yml to ensure that you block out the majority of the Kinesis logs which will spam the console.
YAML(dont push this changes to git, it's just for local testing)
```yaml
logging:
  level:
    root: INFO
    software.amazon.kinesis: WARN
``` 
**3.** After running the application(don't forget to log in to cloud-tool with **'cloud-tool login'** before run the app), wait for the following logs(after application starts - it needs in general **approximately 2-10 minutes** to be shown) to appear before sending data into the lambda test, as the Kinesis connection may not be ready. In case you do not see the logs below, you can still send the data if the wait time has been longer than 10 mins.

![image (2).png](/.attachments/image%20(2)-edcad446-3234-45e5-a8e6-6d734b4ed3e8.png)

P.S if logs are not shown on picture clearly - they look like:

```
[Kinesis] Initializing record processor ....... 
[Kinesis] Initializing record processor ....... 
[Kinesis] Initializing record processor .......
```
 
**4.** Log in to ([AWS TR Sign In](https://mfs.thomsonreuters.com/adfs/ls/IdpInitiatedSignon.aspx))
Use Username Like: MGMT\MC301135 (change with your m account username)
Get password of M account from: https://pam.int.thomsonreuters.com/PasswordVault/v10 (Vault Users)
(P.S Use the same credentials for cloud-tool)

**5.** From the roles, select the role used in cloud-tool or human-role/a205159-PowerUser2 as this role has the necessary permissions.

![Picture1.png](/.attachments/Picture1-c3f86fc3-98f2-4f6b-b23e-c1c032881367.png)

**6.** In the dashboard search for **'Lambda'**:

![Picture2.png](/.attachments/Picture2-33480049-fc0b-46e6-b134-337cbf2c384f.png)


**7.** In the lamda search fo**r cp-dev-plaintext-publisher** (it may look like **a205159-cp-dev-plaintext-publisher**) p.s make sure that you are in **us-east-1** region(without this you may not be shown cp-dev-plaintext-publisher function).

![Picture3.png](/.attachments/Picture3-f18ba4a4-9c33-4b2f-aea3-93aee83a0153.png)

**8.** In the lambda dashboard go to **Test tab** and enter the input into the **Event JSON text area**.

![Picture4.png](/.attachments/Picture4-abdf642f-525f-4505-aed1-9ef41f4833c5.png)

Specifically for cp_charts-service, make sure that the publication is either: **slexanam** or **slexannw** ([as specified from this configuration](https://github.com/tr/cp_charts-service/blob/main/src/main/resources/publications.json "https://github.com/tr/cp_charts-service/blob/main/src/main/resources/publications.json")).

For example, in **Event JSON text are** you can paste this json value and then click **'Test button'** to send the input to lambda:

```json
{  
"objectMetaData": {  
   "guid": "ib79e6f35dc5969f8ca77be532ebc5281",  
   "publication": "slexanam",  
   "status": ""  
},  
"bucketName": "a205159-cp-content-dev",  
"eventName": "ObjectCreated:Put",  
"key": "html/slexanam/ib79e6f35dc5969f8ca77be532ebc5281.html"  
}
```

After that return to your IDEA(where your cp_chars-service is running and wait approximately 2-5 minutes to appear the new logs):
The logs should be like: 

```
2025-07-10 16:32:15.560  INFO [X-Request-ID= | build-version=] 5836 --- [dProcessor-0001] c.t.c.m.consumer.KinesisConsumer         : [Kinesis] Processing 1 records from shardId-000000000010  
2025-07-10 16:32:15.571  INFO [X-Request-ID= | build-version=] 5836 --- [dProcessor-0001] c.t.c.c.config.KinesisConfiguration      : AWS Kinesis 'Content' event starts: [status=PUT, id=ib79e6f35dc5969f8ca77be532ebc5281, publication=slexanam]  
2025-07-10 16:32:16.101  INFO [X-Request-ID= | build-version=] 5836 --- [dProcessor-0001] c.t.c.c.service.CPMetadataServiceImpl    : Retrieved document metadata for ib79e6f35dc5969f8ca77be532ebc5281  
2025-07-10 16:32:16.101  INFO [X-Request-ID= | build-version=] 5836 --- [dProcessor-0001] c.t.c.o.logging.aspect.CPProfilerConfig  : Total run time - method:CPMetadataServiceImpl.getDocumentMetadata(..) in 118ms  
2025-07-10 16:32:16.351  INFO [X-Request-ID= | build-version=] 5836 --- [dProcessor-0001] c.t.c.c.helper.ChartEntryDataHelper      : Deleted 1 chart entries for document id: ib79e6f35dc5969f8ca77be532ebc5281  
2025-07-10 16:32:16.458  INFO [X-Request-ID= | build-version=] 5836 --- [dProcessor-0001] c.t.c.c.service.CPMetadataServiceImpl    : Retrieved document metadata for ib79e6f35dc5969f8ca77be532ebc5281  
2025-07-10 16:32:16.458  INFO [X-Request-ID= | build-version=] 5836 --- [dProcessor-0001] c.t.c.o.logging.aspect.CPProfilerConfig  : Total run time - method:CPMetadataServiceImpl.getDocumentMetadata(..) in 106ms  
2025-07-10 16:32:21.405  INFO [X-Request-ID= | build-version=] 5836 --- [dProcessor-0001] c.t.c.c.helper.ChartEntryDataHelper      : Persisted 26 links for GUID ib79e6f35dc5969f8ca77be532ebc5281  
2025-07-10 16:32:21.811  INFO [X-Request-ID= | build-version=] 5836 --- [dProcessor-0001] c.t.c.c.helper.ChartEntryDataHelper      : Persisted 1 chart entries for GUID ib79e6f35dc5969f8ca77be532ebc5281  
2025-07-10 16:32:21.997  INFO [X-Request-ID= | build-version=] 5836 --- [dProcessor-0001] c.t.c.c.config.KinesisConfiguration      : Content id: ib79e6f35dc5969f8ca77be532ebc5281 took 6432 ms  
2025-07-10 16:32:21.998  INFO [X-Request-ID= | build-version=] 5836 --- [dProcessor-0001] c.t.c.m.consumer.KinesisConsumer         : [Kinesis] Time taken to process 1 records: 6.438 seconds
```

**There should not be exceptions, errors or there should not be written that the S3 document is empty(or something like that)**

**9.** Now you can remove this from application-local.yml file and stop the application:
```yml
    logging:  
    level:  
       root: INFO  
       software.amazon.kinesis: WARN
```