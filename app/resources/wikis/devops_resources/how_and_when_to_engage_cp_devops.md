The below link can be used to raise a webform request to cp-devops@thomsonreuters.com team.
http://devops.tr-tax-cp-preprod.aws-int.thomsonreuters.com/.

Here are some details we have shared, please go through this before reaching cp-devops@thomsonreuters.com team


1.	AWS account access: User should have M-account. We have 2 environments, tr-tax-cp-preprod & tr-tax-cp-prod. Also mention the type of access you need ReadOnly or PowerUser2 

2.	To create M-account, please go through this pdf https://identity.int.thomsonreuters.com/documents/spgm-ad-group-membership-request.pdf


3.	Azure repo access:
https://dev.azure.com/tr-tax-checkpoint/Checkpoint <b>(Create web-form request if you are unable to access) </b>

4.	Datadog access:
https://app.datadoghq.com/account/login/id/27626c51d <b>(Create web-form request if you are unable to access) </b>

5.	Jenkins access:
https://devops-jenkins.tr-tax-cp-preprod.aws-int.thomsonreuters.com <b>(Create web-form request if you are unable to access) </b>
https://cpbuild.int.westgroup.com/ (no need to raise ticket through web form, it is opened to all TR employees)

6.	Checkpoint environments: <b>CP DevOps Not maninting the User access</b> 
To get the access to checkpoint environments and facing any login issues, Please raise the request using the below SNOW link
https://thomsonreuters.service-now.com/sp/?id=sc_cat_item&sys_id=727c7d2613ebf6049c89b53a6144b006 </br>
Below are the environments</br>
DEV: https://dev.checkpoint.thomsonreuters.com/app/ 
QA: https://qa.checkpoint.thomsonreuters.com/app/ 
PREPROD: https://preprod.checkpoint.thomsonreuters.com/app/ 
PROD: https://checkpoint.riag.com/app/



7.	Checkpoint environments with admin tool access:
DEV: https://dev.checkpoint.thomsonreuters.com/app/admin
QA: https://qa.checkpoint.thomsonreuters.com/app/admin
PREPROD: https://preprod.checkpoint.thomsonreuters.com/app/admin
PRODUCTION: https://checkpoint.riag.com/app/admin

Note: if you are facing content issue or folder issue then must reach the TLR-RIACheckpointEaganDev@thomsonreuters.com.

| Environemnts | Raise request                                                                                                                                                | User Should be part of the below groups                                                                                                      | Assignment group | Reference Tickets                                  |
|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|------------------|----------------------------------------------------|
| Non Prod     | https://thomsonreuters.service-now.com/sp?id=sc_cat_item&sys_id=71bb146613e67a009c89b53a6144b0eb                                                             | ten\S-West-TTA_CPAdmin_TechSupp,  ten\S-West-TTA_CPAdmin_CMSSupp, ten\S-West-TTA_CPAdmin_Webapp, ten\S-West-TTA_CPAdmin_NewsFlash            | HCL-GAM          | RITM2477289                                        |
|              |                                                                                                                                                              |                                                                                                                                              |                  |
| Production   | https://thomsonreuters.service-now.com/nav_to.do?uri=%2Fcom.glideapp.servicecatalog_cat_item_view.do%3Fv%3D1%26sysparm_id%3D2e246fb213e67e00f05c7e276144b026 | mgmt\P-West-TTA_CPAdmin_CMSSupp.r, mgmt\P-West-TTA_CPAdmin_NewsFlash.r, mgmt\P-West-TTA_CPAdmin_TechSupp.r, mgmt\P-West-TTA_CPAdmin_Webapp.r | NA               | RITM2477296, RITM2477303, RITM2477310, RITM2477325 |
|              |                                                                                                                                                              |                                                                                                                                              |                  |



8.	Before onboarding new service for checkpoint microservices, we need the following information
We should request the developer to send below information before onboarding the service:</br>
<b>Where should the application run (EC2/Lambda/Fargate)?
Please give brief description of the application.
This application will be deployed under shared ALB - Is that ok? (if not please provide justification)
Should this application made available publicy ? If yes - provide the specific endpoints.
Are customers going to access this service via apigee gateway ? If yes please provide if proxy should be created as internal (restricted to TR network) / external (open to the world) and make sure openapi spec is added to root of codebase as swagger.json.
What is the endpoint to validate health-check ?
Are there any additional specifications required to on-board this app ?
Timeline:
Please provide more information around timeline for release:</br>
DEV date?
QED date?
PreProd date?
PROD date? </b>

9.	If cps tool is down due to the below error or if you are seeing it is due to some DB issues, then please reach oracle team ORACLE-SUPPORT-TR@thomsonreuters.com.
`![cpsdb.png](/.attachments/cpsdb-31267f9a-f10c-4c18-addf-8f0a61b3bf01.png)

10. To see the logs for cp-webapp you can use the below datadog links for respective environments.


| Environment |   |
|-------------|---|
|  Checkpoint Dev           | [logs](https://app.datadoghq.com/logs?query=host%3A%28c501meycpdvap.int.thomsonreuters.com%20OR%20c681gsxcpdvap.int.thomsonreuters.com%29&cols=core_host%2Ccore_service&index=&messageDisplay=expanded-md&stream_sort=desc&from_ts=1644966208182&to_ts=1645052608182&live=false)  |
|   Checkpoint QA          | [logs](https://app.datadoghq.com/logs?query=host%3A%28c221yubcpqaap.int.thomsonreuters.com%20OR%20c222atmcpqaap.int.thomsonreuters.com%29&cols=core_host%2Ccore_service&index=&messageDisplay=expanded-md&stream_sort=desc&from_ts=1644695430352&to_ts=1644868230352&live=false)  |
|      Checkpoint Preprod       | [logs](https://app.datadoghq.com/logs?query=host%3A%28c302egecpqaap.int.thomsonreuters.com%20OR%20c384xzqcpqaap.int.thomsonreuters.com%29&cols=core_host%2Ccore_service&index=&messageDisplay=expanded-md&stream_sort=desc&from_ts=1644966208182&to_ts=1645052608182&live=false)  |
|      Checkpoint Production       |  [logs](https://app.datadoghq.com/logs?query=host%3A%28c151xfccppdap.int.thomsonreuters.com%20OR%20c054uepcppdap.int.thomsonreuters.com%20OR%20c162nptcppdap.int.thomsonreuters.com%20OR%20c193yytcppdap.int.thomsonreuters.com%20OR%20c224stccppdap.int.thomsonreuters.com%20OR%20c309ssacppdap.int.thomsonreuters.com%20OR%20c365ppxcppdap.int.thomsonreuters.com%20OR%20c488xkpcppdap.int.thomsonreuters.com%20OR%20c560anycppdap.int.thomsonreuters.com%20OR%20c649attcppdap.int.thomsonreuters.com%20OR%20c667uqccppdap.int.thomsonreuters.com%20OR%20c716wagcppdap.int.thomsonreuters.com%29&cols=core_host%2Ccore_service&index=&messageDisplay=expanded-md&stream_sort=desc&from_ts=1644172200000&to_ts=1644344940000&live=false) |

 Note: Please filter with the respective date.

11. Checkpoint application login issue:

![image.png](/.attachments/image-25696961-e46f-4234-9c79-5bf5c7e18372.png)

DEV: https://dev.checkpoint.thomsonreuters.com/app/ 
QA: https://qa.checkpoint.thomsonreuters.com/app/ 
PREPROD: https://preprod.checkpoint.thomsonreuters.com/app/ 
PROD: https://checkpoint.riag.com/app/ 

When individual users have login issue (Due to subscription deactivate), please raise the request using the below SNOW link
https://thomsonreuters.service-now.com/sp/?id=sc_cat_item&sys_id=727c7d2613ebf6049c89b53a6144b006

If all the users facing the same login issue please raise a web form request by using the below link. DevOps team will take care. 
http://devops.tr-tax-cp-preprod.aws-int.thomsonreuters.com/

12. To Request the Access for Checkpoint Databases.
https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/571/How-to-Request-for-checkpoint-Database

13. How to do [Microservices deployment](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/656/Microservices-Deployment) for lower evns