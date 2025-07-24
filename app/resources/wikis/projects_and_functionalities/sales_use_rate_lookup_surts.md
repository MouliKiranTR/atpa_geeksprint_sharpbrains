**About Surts:**
http://cpwiki.int.westgroup.com/SURTS?highlight=%28surts%29

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Jenkins Job and ADO Details:**

	Jenkins: https://cpdevops-jenkins.tr-tax-cp-preprod.aws-int.thomsonreuters.com/job/pipelines/job/Checkpoint/job/cp-surts-dtr-client/job/master-build/

	jFrog: https://tr1.jfrog.io/ui/repos/tree/General/libs-release-local/checkpoint-release/com/tr/checkpoint/cp-surts-dtr-client

	ADO: https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_git/cp-surts-dtr-client

**To make surts tool work in local:**

	1. Change the surts.dtr.webproxy.enable=false in appBase/appLocal.properties
	2. Change the weproxy.hostname=webproxy.westlan.com in appBase/appLocal.properties
	3. Finally change the nonProxyHosts.properties  by adding |*.hostedtax.thomsonreuters.com and update *.int.thomsonreuters.com to *.thomsonreuters.com

4. Below is the my local nonProxyHosts.properties
		

		http.nonProxyHosts=sndoitsvc017v.riaqa.loc|sat-gosystemrs.fasttax.com|localhost|tlr.thomson.com|tlr.thomson.com:389|mgmt.tlrg.com|mgmt.tlrg.com:389|*.ecomqc.tlr.com|*.ecom.tlrg.com|*.tlr.thomson.com|*.westgroup.com|***thomsonreuters.com**|cpadmin*.thomsonreuters.com|*.int.westgroup.com|*.westlan.com|*.taxpartners.com|*.westlaw.com|*.bit-co.com|*.onesourcetax.com|*.contractexpress.com|***.hostedtax.thomsonreuters.com**
		
		nonProxyHosts=sndoitsvc017v.riaqa.loc|sat-gosystemrs.fasttax.com|localhost|tlr.thomson.com|tlr.thomson.com:389|mgmt.tlrg.com|mgmt.tlrg.com:389|*.ecomqc.tlr.com|*.ecom.tlrg.com|*.tlr.thomson.com|*.westgroup.com|***thomsonreuters.com**|cpadmin*.thomsonreuters.com|*.int.westgroup.com|*.westlan.com|*.taxpartners.com|*.westlaw.com|*.bit-co.com|*.onesourcetax.com|*.contractexpress.com|***.hostedtax.thomsonreuters.com**

		
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


**How to generate the client jar:**

- These are needed to support the client side code which helps in creating the contract ( wsdl ) to make communication to the server.
- Steps that will be helpful in creating the jar as follows:
	1. Attached the pom.xml which contains the apache-cfx plugin to generate the required jars.
	2. Copy pom.xml and edit the pom.xml whenever there is change in "wsdl". In this case we will have 2 different environments for dev/qa and preprod/prod. 
	3. See the lines in pom.xml 25 and 26 which contains the wsdl location.
	4. Just run mvn clean install to build the required jars.
	5. Attaching pom.xml here: 
	6. [pom.xml](/.attachments/pom-54f3adfb-ef09-4d19-ac83-0717d9bd99e8.xml)
	

**Additional Notes:**
1. Download the soap-ui tool for testing the new endpoints.
		
	
2. Notes from loading the app properties:
		It's calling database with server id to fetch the properties once.
			Dev: 
			surts.dtr.pw	TRWel@111222333!99	reload	db.override_props.45187
			surts.dtr.url.tax.rate	Show 70 chars	reload	db.override_props.45187
				https://onesource-idt-det-amer-int.hostedtax.thomsonreuters.com/sabrix/services/taxrateservice/2014-06-30/taxrateservice?wsdl
			surts.dtr.url.zone.lookup	Show 70 chars	reload	db.override_props.45187
				https://onesource-idt-det-amer-ws.hostedtax.thomsonreuters.com/sabrix/services/zonelookupservice/2011-09-01/zonelookupservice?wsdl
			surts.dtr.username	^tr.checkpoint.surts.prod.AMB		
			
			QA:
			surts.dtr.pw	k7S20!zb4x	reload	db.override_props.Qa
			surts.dtr.url.tax.rate	Show 70 chars	reload	db.override_props.Qa
				https://checkpoint-uat.hostedtax.thomsonreuters.com/sabrix/services/taxrateservice/2014-06-30/taxrateservice?wsdl
			surts.dtr.url.zone.lookup	Show 70 chars	reload	db.override_props.Qa
				https://checkpoint-uat.hostedtax.thomsonreuters.com/sabrix/services/zonelookupservice/2011-09-01/zonelookupservice?wsdl
			surts.dtr.username	surts	 	 
		
Changes done in Dev Admin Portal to servers:
			48850 changes from this server applied to other servers

**NOTE**: These properties are removed from the database in both the tables (WEB_APP_PROPERTY and WEB_APP_PROPERTY_DEFAULT) as it's hard to maintain the properties at two different places.
