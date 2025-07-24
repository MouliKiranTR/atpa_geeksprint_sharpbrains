Apigee is a platform for developing and managing application programming interfaces (APIs). When deploying to Apigee, we create what Apigee calls a reverse proxy. This proxy routes the requests sent to Apigee to your API. When the API responds to Apigee, Apigee will then route the response back to the user.

[[_TOC_]]
___

## Resources/References
- [Atrium Page on Apigee API Gateway Onboarding](https://trten.sharepoint.com/sites/Platform-API/SitePages/Apigee-API-Gateway-%26-Automation.aspx)
- [How to get Access to Apigee](https://trten.sharepoint.com/sites/Platform-API/SitePages/How-to-get-Access-to-Apigee-.aspx)

## Getting Access to Apigee
- Follow the guide on Atrium [here](https://trten.sharepoint.com/sites/Platform-API/SitePages/How-to-get-Access-to-Apigee-.aspx) to submit SNOW request
  - [Service now request form](https://thomsonreuters.service-now.com/sp?id=sc_cat_item&sys_id=793735b71b519010b65c32a3cc4bcb4c)
  - [Sample request](https://thomsonreuters.service-now.com/sp?sys_id=504165271b295ad4c774eb58b04bcb64&view=sp&id=form&table=sc_req_item)
- Select asset ID according to the API Proxy you want to access
  - [a200172 - Checkpoint Research AIID](https://assets.int.thomsonreuters.com/Technology/Application/200172)
  - [a203669 - CUAS AIID](https://assets.int.thomsonreuters.com/Technology/Application/203669)
  - Proxies without AIIDs are really old as they were created before the AIID naming standard that is now implemented
- Once permission is granted you can access Apigee at the following locations:
  - *Non-prod:* https://thomson-reuters-nonprod.apigee.com/edge
  - *Prod:* https://thomson-reuters.apigee.com/edge

## Apigee API Proxy Configurations
### Environments
- *Non-prod:* tr-api-cloud-qa
  - dev
  - test
- *Prod:* tr-api-cloud
  - uat
  - trexternal (prod)
  - trinternal (prod)

### TR External Prod Proxies (available outside TR network)
| **Proxy Name**                              | **Status**  |
| ------------------------------------------- | ----------- |
| a200172-checkpoint-metadata-service-v1      | Not Running |
| Checkpoint-Authorization                    | Running     |
| a200172-checkpoint-search-v2                | Running     |
| a203669-CUAS-Entitlements-API - Not running | Not Running |
| a200172-checkpoint-search-v1                | Running     |
| a200172-checkpoint-privacy-api-v1           | Running     |
| a200172-checkpoint-news-api-v1              | Running     |
| Checkpoint-Documents                        | Running     |
| 200172-checkpoint-privacy-api               | Running     |


### TR Internal Prod Proxies  (available inside TR network only)
| **Proxy Name**                         | **Status**  |
| -------------------------------------- | ----------- |
| a200172-checkpoint-metadata-service-v1 | Running     |
| Checkpoint-Authorization               | Running     |
| a200172-checkpoint-search-v2           | Not Running |
| a203669-CUAS-Entitlements-API          | Running     |
| a200172-checkpoint-search-v1           | Not Running |
| a200172-checkpoint-privacy-api-v1      | Running     |
| a200172-checkpoint-news-api-v1         | Not Running |
| Checkpoint-Documents                   | Not Running |
| 200172-checkpoint-privacy-api          | Not Running |

## Using Apigee
- Once you are logged into Apigee there are a few key locations to be aware of
### The **Proxy** page
- ![image.png](/.attachments/image-99020990-84f2-4013-8c49-0dbe0985ecaa.png)
- Access from "Develop → API Proxies"
- Lists all the API proxy configurations, organized by environment (dropdown next to search bar)
- You can click on any one of these to view more details: ![image.png](/.attachments/image-2795facb-c2be-4ac5-8f9e-b33ab2da32a7.png)
- From the details page you can click the "Develop" tab to view complete implementation: ![image.png](/.attachments/image-853b6492-6d23-46b0-803e-8a0579280edc.png)
- In this example for CP Authorization you can see various "policies" with code attached to them. In this particular policy we are defining a POST request to an endpoint in CP Auth Service to retrieve a token

### The **target servers** page
- ![image.png](/.attachments/image-2157b189-5226-41b7-818a-08fe7aaa3a19.png)
- Access from "Admin → Environments → Target Servers"
- Provides configurations of servers, for example in the above screenshot for the CP Authorization policy `SC-GetCheckpointToken` it references `<Server name=CheckpointAuth"/>` which is defined on this page

### The **Key Value Maps** page
- ![image.png](/.attachments/image-e71cff74-47ed-4818-bb09-2372d4221662.png)
- Access from "Admin → Environments → Key Value Maps"
- Provides access to keys/secrets to be used in the Proxy configuration
- In the above example you can see the item with name "auth-checkpoint" has three keys under it for `audience`, `client_id`, and `private_key`
- These values are then consumed in the `KVM-GetServiceKey` policy under Checkpoint Authorization API Proxy: ![image.png](/.attachments/image-53186f64-ae3c-47fd-ba9f-c6de2651e409.png)

## Contacts
For questions on Apigee, check with the following team members who have Apigee access/experience:
- @<1EEF89FE-A95B-429D-8940-CDDFCF32AD59> 
- @<DE58388A-475B-68F7-A222-1DD0000B6525> 
- @<5D859739-32D0-62AD-8D9B-670A89B07CEA> 