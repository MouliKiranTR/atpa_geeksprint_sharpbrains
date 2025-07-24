In this document you will find all the CUAS CMDB Properties that works directly or indirectly in CIAM Migration of users. 

- **ciam.createNewUser** : Boolean 
1. This Property works in conjuction with another CMDB Property **ciam..accounts.createNewUser**
As the name suggest, while creating new users through CUAS-UI application, if this property is find to be true, CUAS app creates or updates user's existing CIAM Profile for the newly created CUAS user provided the user mets given below conditions. 
    - User is not a ciam restricted user. For example: Users from Ciam Restricted Account Linking ( see table **ciam_restrict_acct_linking** Accounts, CIAM Restricted G7 Accounts ( see table: **ciam_restrict_g7_users**, a walkin traffic user. 
    - User is not a Walkin Traffic user
    - If cuas has received request from **CPREG** application to create this new user and the **ciam.createNew.CPRegUser** CMDB Property is set to true

2. New DEMO users will be migrated to CIAM at the time of their creation, if the property is set to **true**.

3. If the newly created CUAS users have been migrated to CIAM, they receive CIAM pertaining Welcome Email, otherwise they receive Legacy Welcome Email. The CUAS app uses same logic as stated in point 1, to determine what email it should send to the newly created user.

4. Any new users created through OMCUAS application would also consider this CMDB Property to determine if the user has to be migrated to CIAM during its creation. 


- **ciam.accounts.CreateNewUser**: List of accountIds separated by comma
      If you want to enable CIAM Migration for new users of a Customer, you need to enter the Customer Account's ID in the above CMDB Property list. Once the accountId is in the list any new user that will be created through the CUAS-UI application will be migrated to CIAM at the same time of its creation.
      This property works in conjunction with **ciam.createNewUser** CMDB Property as described under that property. 


- **ciam.createNew.CPRegUser** : Boolean
    If this CMDB property is set to **true**, they any request from **CPREG** application to cuas-api to create a new user, would make **cuas-api** to create a new CIAM Profile or update user's existing CIAM Profile in case there already exists a CIAM Profile for the user, at the time of the user creation. 
   This property works in conjunction with **ciam.creatNewUser** CMDB Property.


- **ciam.createNew.RegisterViaIpUser** : Boolean 
   Register Via IP User will receive CIAM related Welcome Email when the property value is set to true, otherwise they receive legacy Welcome Email with temporary username and password. 

- **+ciam.dataMigration.pickupAccount.bufferTime** : Encrypted Integer
This CMDB Property is used by **CiamMigrationAccountReadinessJob**. This job randomly picks first 1000 accounts and test their eligibility for CIAM Migrations, if it finds an account is eligible for migration, it inserts a record for that account in **ciam_account_migration** table with **status_code** set to 1 ( READY FOR MIGRATION) and **migration_started_on** date set to current_date + **ciam.dataMigration.pickupAccount.bufferTime**. 

  **CiamMigrationBulkMigRATEjob** only picks those accounts for which the **status_code** is set to 1 ( READY FOR MIGRATION) and **migration_started_on** date is set to any date within last 7 days from its execution date.

  Which means when an account is marked as READY FOR MIGRATION by the **CiamMigrationAccountReadinessJob**, the account will be picked for migration by the **CiamMigrationBulkMigrateJob** after **ciam.dataMigration.pickupAccount.bufferTime** number of days.

- **ciam.dataMigration.accountMapping.enabled** : Boolean 
This property is used by **CiamMigrationBulkMigrateJob** to determine if an Account Mapping Account is eligible for CIAM Migration prior to its migration. 
Note: if we don't turn on this property and run the Batch job for an Account Mapping Customer, the job would consider the Account as a Normal Account and thus all users in that account must have ciamEmailAddress in **ciam_user** table for the account to be eligible for migration. However, for an Account Mapping customer only normal active users needs to have ciamEmailAddress, sso users are not necessarily required to have ciamEmailAddress value in **ciam_user** table. For SSO users, the bulk migration job will use their notification_email_address to create their CIAM Profile.


- **ciam.updateAccountMappingUser.enabled** : Boolean
   When **true**, it turns on CIAM Migration for new users that are provisioned through Account Mapping Login flow. Note: It enables Account Mapping Flow for all Account Mapping Customers. 

- **ciam.createNewSeamlessByWebServiceUser**: Boolean
  Setting this property to false, hides the **Seamless By Webservice** Create solution button from the Configure SSO Page of CUAS-UI. 
  When property set to true: 
![image.png](/.attachments/image-eccf883f-19c7-4673-8cc8-eb2a6a18eddd.png)
  When Property set fo false:
![image.png](/.attachments/image-ac2e3375-3061-4e0f-a31c-019b04f539bc.png)




- **ciam.notification**: 
