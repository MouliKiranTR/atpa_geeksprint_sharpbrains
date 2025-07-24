## Scenario: 
There was a requirement to override the checkpoint user subscriptions in order to hide certain functionalities in the application. The initial request was to hide the ability to search and navigate in Toc structure the source EY Green Tax Tracker (ODS GTRKEY) for KPMG users then It was extended to KPMG TaxNewsFlashes (ODS KPMGTNF).

## Implementation:
In order to achieve this effort, application and microservice work was done.
There was a decision to create a configuration file to handle the override of user entitlements, Given some rules then the user entitlements(ODSES, OFSES) could be impacted.
![entitlements override rules.png](/.attachments/entitlements%20override%20rules-c34d6663-5315-4a8b-bd33-44126d79c3dd.png)

**Content and Publishing work:** just the creation of the new OFS which will control the turn on/off the feature from CUAS.
US for reference: [KPMG TaxNewsFlashes Account Feature Work: Create new OFS ](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_workitems/edit/143372)

**Microservices Work:**
Some areas like table of contents in search screen consumes information regarding user entitlements from cp-auth-service, also the notifications page to handle the displays of notifications based on the user entitlements.

PR'S :
[Added implementation for EY Green Tax Tracker and Account Feature Work -- Microservices](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_git/cp-auth-service/pullrequest/12265)
[Add Implementation for account Ofs ](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_git/cp-auth-service/pullrequest/12343)
[Removed null check for accounts ofses](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_git/cp-auth-service/pullrequest/12349)
[added override rules in configuration file in order to remove KPMG Content](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_git/cp-auth-service/pullrequest/12620)

Table of contents- Search screen consumes user entitlements from the auth service in order to handle the display of toc nodes which is subscription sensitive.
![image.png](/.attachments/image-a3505479-b47a-48d6-b5ac-7c3ccc2e24ef.png)

The notifications page- Notifications can be released filtered by odses or ofses.
When releasing new content a notification is created with ods filter, only users subscribed to an specific ods or ofs can get the notification.

This is an example of creating a notification filtered by ods only, used for the Ey Green Tax Tracker content release.
![image.png](/.attachments/image-a5d70683-70e4-4d74-9a5a-ae11d2bcfab7.png)
DEV: https://cp-dev-admin-notification-ui.tr-tax-cp-preprod.aws-int.thomsonreuters.com/
QA: https://cp-test-admin-notification-ui.tr-tax-cp-preprod.aws-int.thomsonreuters.com/

**NOTE:** In lower environments almost all the users has the ODS id "ALL"
 as part of their subscription. 
![image.png](/.attachments/image-0ef1f461-8689-42f8-8a13-2d7f592e145d.png)
for testing the Notifications system make sure the ods id "ALL" is removed for the user. It is confirmed that ods id "ALL" is not available for production users.



**Application Work:** 
-The user entitlements are modified based on the override rules available in the file [entitlementsOverrideRules.xml](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_git/cp-web-app?path=/CPWar/web/WEB-INF/data/entitlementsOverrideRules.xml&_a=contents&version=GBmaster) 

This is how it was implemented before:
[US135376-EY Green Tax Tracker and Account Feature Work](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_git/cp-web-app/pullrequest/12154)
[update logic to remove green tax tracker ods Id](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_git/cp-web-app/pullrequest/12167)

Then a refactored version:
[Refactored the implementation for entitlements override rules , replicated logic from cp-auth-service](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_git/cp-web-app/pullrequest/12662)

**NOTE:** for new account feature work and the requirement is to alter the user entitlements we just need to add new entries in 
https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_git/cp-web-app?path=/CPWar/web/WEB-INF/data/entitlementsOverrideRules.xml&_a=contents&version=GBmaster

**cp-web-app**
[entitlementsOverrideRules.xml](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_git/cp-web-app?path=/CPWar/web/WEB-INF/data/entitlementsOverrideRules.xml&_a=contents&version=GBmaster)

**cp-auth-service**
[entitlements-override-rules.yml](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_git/cp-auth-service/pullrequest/12620)

**Account Feature Work for non ODS related items**
Some Account feature work such as folders, notes, and tax calendar are not tied to an ODS.

For this work there is a quick process involved. Following the steps in [this PR](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_git/cp-web-app/pullrequest/12743)

1. Create the OFS in the OFS table, this will take part in the daily builds so may not be available until the next day
2. Add the boolean value to this object in cp-web-app CPUserFeatureItems
3. Return from the UserFeaturesServiceImpl
4. Depending on where you need this value, in example cp-ui
   a. Update user-feature.reducer.ts to include the initial state
   b. Update userfeature.model.ts with your new value
   c. Use this selector to hit the endpoint with your web app changes - this.userFeatureItems$ = this.store.select(selectLoggedUserFeatureState);