[User Story 168919](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_workitems/edit/168919): [Authentication] SPIKE #1 – Investigate API User Setup and Entitlements Flow

*Author:* @<5D859739-32D0-62AD-8D9B-670A89B07CEA> 

[[_TOC_]]
___

## Need to get access
### Access to Apigee
- See Wiki page [Apigee API Gateway](/Projects-and-Functionalities/Apigee-API-Gateway) for more details
### Access to CUAS
- See [CUAS Access for Tech Staff](https://trten.sharepoint.com/sites/TRTAKSCheckpointAnswers/Shared%20Documents/Forms/AllItems.aspx?id=%2Fsites%2FTRTAKSCheckpointAnswers%2FShared%20Documents%2FCCUAS%2Fdocs%2FDOC%2D2815553%20%2D%20CUAS%20Access%20for%20Tech%20Staff%20%28Employees%20%26%20Contactors%29%20%5F%20The%20Hub%2Ehtml&parent=%2Fsites%2FTRTAKSCheckpointAnswers%2FShared%20Documents%2FCCUAS%2Fdocs) for more information
![image.png](/.attachments/image-861a8dec-36ef-4afc-a450-f13dbd395df8.png)
- If you got access to the Non-Prod CUAS environments, then go to the specific instance you want to login to and enter your Network ID (Employee ID) and Password. This is the same username and password that you use when accessing something through eSSO.
  - CI (CP Dev): https://cpadmin.ci.thomsonreuters.com/
  - DEMO (CP QA): https://cpadmin.demo.thomsonreuters.com/
  - QA1 (No CP): https://cpadminqa1.qed.thomsonreuters.com/
  - QA2 (No CP): https://cpadminqa2.qed.thomsonreuters.com/
  - QED (CP PreProd): https://cpadmin.qed.thomsonreuters.com/
- Add-on Roles
Allows you to access the control menu
![image.png](/.attachments/image-eb29f343-ff5e-4e71-a9db-37e286e4db04.png)![image.png](/.attachments/image-29cc9346-eade-47a8-9d4d-e15cda1877a2.png)
Additionally, there are the add-on roles. Add-on roles alone will not allow a user to login. They must be assigned at least one of the major roles in order to login and use that add-on functionality. These add-on roles were introduced as they are very targeted to a specific piece of functionality.
![image.png](/.attachments/image-883e71de-74a6-45a3-a4a0-90440ab330f5.png)
- summarizing: 2 requests to the [SailPoint](https://iga.int.thomsonreuters.com/home.jsf) for the preprod environments developer
  - **REST-S-WEST-TTA_USERADMIN_ROOT**
  -  **-DG-TLR-REST-S-WEST-TTA_USERADMIN_DEV_ADMIN**

### Access to Developer Portal
- See [Developer Portal Access](https://trten.sharepoint.com/:w:/r/sites/intr-idt-product-engineering/_layouts/15/Doc.aspx?sourcedoc=%7B261C5FC0-9B41-46CE-B97F-8CA990D16C73%7D&file=Know%2BHow_%2BDeveloper%2BPortal%2BAccess.doc&action=default&mobileredirect=true&DefaultItemOpen=1) for more details

- **Iimportant:_** the menu in the developer portal will be invisible. To access it, need to add roles.
<IMG  src="https://dev.azure.com/tr-tax-checkpoint/c60acdc5-4ee0-4039-9a00-61975bbd5dfe/_apis/wit/attachments/bb426d36-fb1b-4a10-89ed-d3a71f6b6050?fileName=image.png"  alt="Image"/>
The roles that are necessary for managing companies, apps, and members are:
  - Internal Admin
  - Content Manager
  - Member Manager
  - Internal Content
  - External Content
  - Checkpoint Content

---
## Developer portal and Apigee
- The developer portal is making API calls to the Apigee management APIs.
A data in the developer portal is stored inside of Apigee.
The developer portal is just a UI facade.
- [Documentation on creating a new Apigee Proxy](https://trten.sharepoint.com/:w:/r/sites/intr-pl-enhancements/_layouts/15/Doc.aspx?sourcedoc=%7b4B1AA598-C5EF-4B4B-ACDB-9670A1CB2745%7d&file=New%20Apigee%20proxy%20creation%20process.docx&action=default&mobileredirect=true)

### CUAS Setup Process 
  - Login to CUAS 
  - Proceed to the customer’s account details
    **account id** and **account prefix** important details
![image.png](/.attachments/image-37ecf454-b610-4ccf-9e63-c90aaba5451a.png)
  - Create a new user with Role: API
![image.png](/.attachments/image-9db26167-19d0-4481-8b4c-d5cf04d2c5cb.png)
### TR Developer Portal Setup Process
  - Navigate to the [TR Developer Portal](https://developerportal.thomsonreuters.com)
#### Manage Client Company
  - Navigate to Company > Manage API Gateway Companies
![image.png](/.attachments/image-a05ec7f4-411c-4ab5-960e-c7999c368c92.png)
  - Select the Gateway necessary (cloud-qa = CI, Dev, QA and cloud = PreProd, Prod)
![image.png](/.attachments/image-8b7da115-f011-48d0-9a3b-a921ae58e4ef.png)
  - `Manage API Gateway Companies` button if the company is already created or `Create Company` to create it
  - Search for the customer’s **account prefix** from CUAS. Or create with required parameters
![image.png](/.attachments/image-0b64721f-f3af-48bb-9574-c4932c325882.png)
`TR_CHECKPOINT_ACCOUNT_ID` update **account id** value from CUAS customer’s account.
**Name***: Give the company a readable name.
#### Manage Client App
  - Navigate to Company > Manage Company Apps
![image.png](/.attachments/image-b5eb52a0-9cce-46d8-92ff-856c8e3c0cd3.png)
  - Select the Gateway necessary (cloud-qa = CI, Dev, QA and cloud = PreProd, Prod) and the name of the API Gateway Company and click the “Manage Company Apps” button
![image.png](/.attachments/image-28ddd89a-7cf3-4aa3-8b9a-07962daf70b8.png)
  - On the “Manage Company Apps” page, you may see an automatically created “APP NAME” called **account id** or any different name. Click the Operation icon to edit the Company App
![image.png](/.attachments/image-cc8dbdd8-3233-4690-b784-9b272426b262.png)
  - The `TR_CHECKPOINT_SERVICE_ACCOUNT_I` value can be matched and verified in CUAS. In this case, it is **"API User ID"**
#### Manage Members & Roles
  - Navigate to Company > Manage Members & Roles
![image.png](/.attachments/image-5466b240-5373-4506-be10-cd9dc8e67963.png)
  - Select the Gateway necessary (cloud-qa = CI, Dev, QA and cloud = PreProd, Prod) and the name of the API Gateway Company and click the “Manage members & roles” button
![image.png](/.attachments/image-1433c9e2-44b6-4637-84e9-cf009e2b887a.png)
  - Email of the customer employee email address that should have access to the API in the TR Developer Portal. 
  - Select if they can be a Company Admin (this means that user can then invite any other person to get access to the API. Note: Not sure we want to allow this because they could give access to anyone in their company or outside their company. So far, we have not given company admin access to any customer employees.) 
  - Click the Invite button
![image.png](/.attachments/image-77b9e9d2-79fa-433c-85b1-64013061c3c6.png)
  - If they already have a TR Developer Portal user, they will now have access to the API keys. If this is the case you will have to grant them access to Checkpoint Content so they can view the API documentation. 
  - Navigate to Members 
![image.png](/.attachments/image-c9ca453d-ab74-4401-9d72-4b9cdf3606a0.png)
  - Enter the email address of the user that was invited and click apply 
![image.png](/.attachments/image-e8169f8a-c46d-480a-9efe-810529b93521.png)
  - Click the Edit button for the user.
    Expand the Roles section and select “Checkpoint Content” and click Save
![image.png](/.attachments/image-4e5c4180-5d93-4d3f-8fef-48caa0fe029f.png)
  - The user can now login to the [Developer Portal](https://developerportal.thomsonreuters.com/) and they will be able to see the Checkpoint API documentation and the API Keys
![image.png](/.attachments/image-17761204-c53f-4b2f-a532-0f884c1151aa.png)
  - My Keys
![image.png](/.attachments/image-dbc9c9fa-8ab7-42ab-a048-951d4333ef93.png)

