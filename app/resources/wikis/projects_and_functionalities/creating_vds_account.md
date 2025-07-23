# Table of Contents
1. [What are Virtual Directory Services (VDS)](#what-are-virtual-directory-services-(vds))
2. [Why s.VDS.WEBAPP.DEV was created](#why-s.vds.webapp.dev-was-created)
3. [Steps to create VDS account](#steps-to-create-vds-account)
4. [How VDS account used in Web App](#how-vds-account-used-in-web-app)

# What are Virtual Directory Services (VDS)

Virtual Directory Services (VDS) is used for Identity management and attribute delivery. When identity information is stored in many different locations, VDS provides a common correlated source for the identity data.

What VDS provides:
1. Enables applications to more easily consume identity data through common interfaces such as LDAP and REST
2. Enables secure access to identity attributes
3. Aggregates all identity stores like standard Active Directory (AD), Database servers, LDAP servers, etc. to give applications a single, logical point of access, and a single version of the truth

For more info see [article](https://identity.int.thomsonreuters.com/content/%2Ftopics%2Fdirectory_services%2F/page/about_vds).

# Why s.VDS.WEBAPP.DEV was created
New VDS account is needed to replace usage of s.VDS.CUAS.PROD in web app, because it was locked several times on incorrect password attempts if one of developers not properly configured credentials, and it affected Prod environment because this account is shared between web app and CUAS.

# Steps to create VDS account

In [ticket](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_workitems/edit/164582/) was created new VDS account s.VDS.WEBAPP.DEV for web app.

Please review [instruction](https://identity.int.thomsonreuters.com/content/topics/directory_services/page/vds_app_integration) on how to create VDS account that contain latest information, later HCL-GAM team shared [Request_Service_account_and_functionalities.pdf](/.attachments/Request_Service_account_and_functionalities-9e9dd35d-e095-43d8-8813-e8884fd660a7.pdf) that contain info on how to create/enable/disable/unlock account and change password.
Next instructions contain basic steps on how to create new VDS account with examples from creation of s.VDS.WEBAPP.DEV:
1. Create name of VDS account and open [Onboarding applications to VDS](https://thomsonreuters.service-now.com/com.glideapp.servicecatalog_cat_item_view.do?v=1&sysparm_id=58cb09571b0fefc4059562007e4bcb5c) request.
Name may be like s.VDS.WEBAPP.DEV in format S.VDS.AppName.Environment.Number(optional), see examples

| Environment | Example |
|-------------|------------------|
| Pre-Prod\QA | S.VDS.SCOM.QA |
| Pre-Prod\QA | S.VDS.SCOM.QA.2 |
| Production | S.VDS.SSO.PROD |
| Production | S.VDS.DCAG.PROD.1 |

For [Onboarding applications to VDS](https://thomsonreuters.service-now.com/com.glideapp.servicecatalog_cat_item_view.do?v=1&sysparm_id=58cb09571b0fefc4059562007e4bcb5c) use next examples [s.VDS.WEBAPP.DEV](https://thomsonreuters.service-now.com/sp?sys_id=e7f5e4211b685614777bec23604bcbde&view=sp&id=form&table=sc_req_item), [s.VDS.CUASAPI.PROD.1](https://thomsonreuters.service-now.com/sp?id=ticket&table=task&sys_id=e8d00d658757ca947204a60d3fbb358c&record=%5Bobject%20Object%5D), [S.VDS.CUAS.PROD](https://thomsonreuters.service-now.com/sp?id=ticket&table=task&sys_id=f60fa2db1beef454531e975a234bcb24). For field "TLS version details if used any" you need to connect to server that will use your VDS account, read item 4 of current instruction on how to connect to server and run openssl s_client -connect vds.int.thomsonreuters.com:636

2. Create new VDS account.
Go to [SailPoint IdentityIQ form](https://iga.int.thomsonreuters.com/), left menu -> Non-Standard Account Management -> Account Create
![image.png](/.attachments/image-fab876cc-1b95-4528-8f57-f544d3079193.png)
fill and submit request, for details see instruction. For creation of s.VDS.WEBAPP.DEV for web-app was used:
```
Account Type: Service
System: Enterprise Active Directory (EAD)
Do you have existing account in any other Domain?: No
Account First Name: VDS
Account Last Name: WEBAPP.DEV
Account Name: s.VDS.WEBAPP.DEV
Managed Unit Name: Checkpoint U.S.
Managed Unit Owner: 0050354, automatically filled based on Managed Unit Name field
Application Tier: This account will be required for application authentications and authorizations.
Business Description: This account will only be used to Bind to and search specific VDS directories for application.
Primary Account Owner: Elle Mason
Password Custodian: Sam Lewis
Account Expiration: automatically filled, 365 days from request creation date
```
3. Add created VDS account to appropriate EAD Domain Group.
For s.VDS.WEBAPP.DEV it is Pre-Prod\QA: -DL-T1-Operators-VDS-EnterpriseAD-QA-RO (check [instruction](https://identity.int.thomsonreuters.com/content/topics/directory_services/page/vds_app_integration)for most relative info), the data that accessed is the same for prod and non-prod EAD Domain Group:
a. In [SailPoint](https://iga.int.thomsonreuters.com/) Manage Access -> Manage My Access (in instruction written Manage User Access but In my scenario there was no such menu item)
![image.png](/.attachments/image-1bcdd689-b41f-49da-b1b8-d79b4f1a38f6.png)
b. Select Find Users' Access in left dropdown, that have value Search By Keywords
![image.png](/.attachments/image-1bb02cac-36dc-4e80-a87f-05f7ad41aa13.png)
c. Select your account (s.VDS.WEBAPP.DEV) in dropdown and click Apply
d. If there is No Search Results then you not have proper permissions, try to ask password custodian or primary account owner that were filled in VDS creation form and follow item 3 of instruction
4. item 4, 5, 6 of [instruction](https://identity.int.thomsonreuters.com/content/topics/directory_services/page/vds_app_integration) perform checks on servers, nslookup, telnet, certificates in java certificate store and openssl check that will be used later, you can ask DevOps for help or try to do checks by yourself:
a. Need to find AWS instance ID, for example it may be found in datadog logs, narrow search for specific service and environment and check Host column in logs table for instance id
![image.png](/.attachments/image-e1500edf-8269-4527-9f7f-d050fe5aac24.png)
b. Go to [AWS EC2 instances](https://us-east-1.console.aws.amazon.com/ec2/home?region=us-east-1#Instances:v=3;$case=tags:true%5C,client:false;$regex=tags:false%5C,client:false) and search by Instance id, check needed item and click Connect
![image.png](/.attachments/image-57b4a968-43fb-4738-af41-43334fd65af9.png)
c. Open Session Manager tab and click Connect.
Request additional permissions on permissions error, to do it, check instance name like a200172-cp-webapp-ci-use1c1, f it contains 200172 then create [Service Now request](https://thomsonreuters.service-now.com/sp?sys_id=ebd785e81ba8de1464d45574604bcb79&view=sp&id=form&table=sc_req_item), for 205159 create [Service Now request](https://thomsonreuters.service-now.com/sp?sys_id=e01632301b2d0e10386b63d3604bcbdd&view=sp&id=form&table=task) and log in to AWS with needed role, web app preprod (qed) and prod need additional permissions and better to ask DevOps if you need to connect to this servers
![image.png](/.attachments/image-71d7ed23-fe16-4e45-9805-0a237d05780f.png)
d. Execute all needed commands
e. Save output of openssl s_client -connect vds.int.thomsonreuters.com:636, used for Onboarding applications to VDS Service Now request
5. Change VDS account password.
You need to be password custodian to change VDS password.
In [instruction](https://identity.int.thomsonreuters.com/content/topics/directory_services/page/vds_app_integration#ldap-integration-example) it is suggested to contact HCL-GAM
![image.png](/.attachments/image-84f070f3-7184-48c8-9658-64b7579f8353.png)
As the result [Request_Service_account_and_functionalities.pdf](/.attachments/Request_Service_account_and_functionalities-9e9dd35d-e095-43d8-8813-e8884fd660a7.pdf) was shared in [ServiceNow request](https://thomsonreuters.service-now.com/sp?sys_id=8cbeec851b7c1ed00f272068b04bcb4c&view=sp&id=form&table=task), see section How to change password for Service Account.

# How VDS account used in Web App

In [context.xml](https://github.com/tr/cp_web-app/blob/main/CPWar/web/META-INF/context.xml#L35) specified Realm that uses VDS account. Realm definition from [Realm Configuration How-To](https://tomcat.apache.org/tomcat-9.0-doc/realm-howto.html#What_is_a_Realm?)
> A Realm is a "database" of usernames and passwords that identify valid users of a web application (or set of web applications), plus an enumeration of the list of roles associated with each valid user. You can think of roles as similar to groups in Unix-like operating systems, because access to specific web application resources is granted to all users possessing a particular role (rather than enumerating the list of associated usernames). A particular user can have any number of roles associated with their username

Used Combined Realm and VDS account Realm is a second sub realm, first sub realm uses Management account, Combined Realm info from [Realm Configuration How-To](https://tomcat.apache.org/tomcat-9.0-doc/realm-howto.html#CombinedRealm)
> Using CombinedRealm gives the developer the ability to combine multiple Realms of the same or different types. This can be used to authenticate against different sources, provide fall back in case one Realm fails or for any other purpose that requires multiple Realms

In [web.xml](https://github.com/tr/cp_web-app/blob/main/CPWar/web/WEB-INF/web.xml#L1124) specified several <security-constraint> elements that maps URL with Roles from Active Directory through Management or VDS account, next info taken from [Specifying Separate Security Constraints for Various Resources (The Java EE 6 Tutorial) (oracle.com)](https://docs.oracle.com/cd/E19798-01/821-1841/bncbl/index.html)
> You can create a separate security constraint for various resources within your application. For example, you could allow users with the role of PARTNER access to the GET and POST methods of all resources with the URL pattern /acme/wholesale/* and allow users with the role of CLIENT access to the GET and POST methods of all resources with the URL pattern /acme/retail/*

For more description on VDS account in web app see [Bi-Weekly Tech Meeting-20240621_100309-Meeting Recording.mp4](https://trten-my.sharepoint.com/personal/mostafijur_rahman_thomsonreuters_com/_layouts/15/stream.aspx?id=%2Fpersonal%2Fmostafijur%5Frahman%5Fthomsonreuters%5Fcom%2FDocuments%2FRecordings%2FBi%2DWeekly%20Tech%20Meeting%2D20240621%5F100309%2DMeeting%20Recording%2Emp4&referrer=StreamWebApp%2EWeb&referrerScenario=AddressBarCopied%2Eview%2E45f1fa5b%2D47ea%2D4329%2D9a94%2D4e3ca63387ef) (first topic is about VDS).

For list of roles see <security-role> elements in [web.xml](https://github.com/tr/cp_web-app/blob/main/CPWar/web/WEB-INF/web.xml#L1121), roles name starts from:
1. P-West-TTA_CPAdmin_ for MGMT Domain, accessed using Management account
2. S-West-TTA_CPAdmin_ for TLR Domain, accessed using VDS account


First Management account Realm used for prod users, second VDS Realm used for developer users.
For example my account have all four S-West-TTA_CPAdmin_ roles that are accessed using VDS account, lookup using Management account return no data.
Each role has two names, one for MGMT domain, second for TLR domain and each protected URL check roles in pairs for both domains:
1. Webapp security role:
    * P-West-TTA_CPAdmin_Webapp.r
    * S-West-TTA_CPAdmin_Webapp
2. CMSSupp security role:
    * P-West-TTA_CPAdmin_CMSSupp.r
    * S-West-TTA_CPAdmin_CMSSupp
3. TechSupp security role:
    * P-West-TTA_CPAdmin_TechSupp.r
    * S-West-TTA_CPAdmin_TechSupp
4. NewsFlash security role:
    * P-West-TTA_CPAdmin_NewsFlash.r
    * S-West-TTA_CPAdmin_NewsFlash

Next URL patterns may be accessed if user have needed Role:
* /admin
* /admin/secure
* /adminNewsFlash
* /adminservlet/*
* /cpadmin/CMSSupp/*
* /cpadmin/NewsFlash/*
* /cpadmin/TechSupp/*
* /cpadmin/Webapp/*
* /cpapp
* /updates

For latest Roles mapping check [web.xml](https://github.com/tr/cp_web-app/blob/main/CPWar/web/WEB-INF/web.xml#L1124).

Here are several URLs that are using VDS or Management account to get user data and roles:
1. http://localhost:8080/app/admin
2. http://localhost:8080/app/adminservlet/CPViewLogServlet
3. http://localhost:8080/app/cpadmin/TechSupp/CPUserAdmin.jsp

If to put breakpoint in JNDIRealm.authenticate(String username, String credentials) and open any protected URL from <security-constraint>:
1. Authenticate() called twice, because we have Combined Realm with two sub Realms, one for Management account and second for VDS account
2. For my developers account using Management account lookup next line return no data
``` this.getUser(context, username, credentials) ```
but with VDS account lookup returned user info with roles list, that are used to determine if it is allowed to visit specific URL or not
3. Authenticate() method called only during access to protected URL and not during tomcat startup or deployment and not during authentication on login page