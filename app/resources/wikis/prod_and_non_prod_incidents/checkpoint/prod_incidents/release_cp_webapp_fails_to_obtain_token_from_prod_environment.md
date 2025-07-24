[[_TOC_]]

## Overview
We ran into a PROD issue on the day (5th April 2024) of production deployment for the April release. Here, I outlined the details problem statement, the root cause of the problem, resolutions, troubleshooting steps, and recommendations to avoid this kind of issue in the future.

Here is a snapshot of the Network tab from Chrome's Developer Tools when I was accessing the Checkpoint application using one of the direct target servers:

![image.png](/.attachments/image-886eefe2-3182-4f20-8caa-87734a8999e0.png)

And here is the snapshot of the DataDog logs of the token obtain related problem.

![image.png](/.attachments/image-a376d102-636f-400c-b0c3-5049b2f86bab.png)

- **Problem Statement**: Checkpoint WebApp failed to obtain a token from CP-Auth-Service in the PROD environment.
- **Root cause of the Problem**: Incorrectly encrypted `client-id` was pushed in the `appBase.properties` file as a part of this pull request - https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_git/cp-web-app/pullrequest/13396.
- Resolution: Replacing the existing `client-id` with a properly encrypted `client-id` fixed the problem in the PROD environment.

## Problem Statement Details
Checkpoint WebApp failed to obtain a token from CP-Auth-Service in the PROD environment though the application has been working fine in the lower (DEV, QA, and PREPROD) environments with the code from the April release. As a result, the WebApp failed to make successful API calls to the following microservices:

- Publicly Exposed Microservices (toc, charts, calendar, and collaborative notes):
- Microservices called through WebApp Backend (profile, and notifications)

## How to Reproduce the Issue in the LOCAL Environment
- To reproduce the issue in the LOCAL environment, I checked out the April 2024 release-specific branches of Checkpoint WebApp, and CP-UI applications and ran the applications locally by hitting the PROD endpoint of cp-auth-service.
- To hit the PROD endpoint of the CP-Auth service, comment out these properties (`auth.service.token.signing.key`, `auth.service.token.client-id`, `auth.service.token.audience`, and `auth.service.client.base-url`) from `appDevData.properties` file and copy/paste the same set of properties from `appBase.properties` into the `appDevData.properties` file.

![image.png](/.attachments/image-37dc3189-f177-4c97-b3ac-34a542ff3af8.png)

- Then put debugging points in the `CPAuthClient.getAccessToken` and `CPJwtUtil.generateToken` methods as shown in the following screenshots and run the CP-UI and WebApp applications where CP-UI application was pointing to the locally running Checkpoint WebApp.

![image.png](/.attachments/image-addcc227-d1c1-4851-a81f-adc59249f79b.png)

![image.png](/.attachments/image-5868f62e-13c6-4223-8cd0-242e8f655763.png)

- During debugging through the WebApp code, I found that the `CPJwtUtil.generateToken` method threw an exception from the following line and hence the token obtain endpoint was failing.

     `String clientId = mgr.getProperty(CPAppProp.AUTH_TOKEN_CLIENT_ID, null);`

## How to fix the Root Cause of the Problem
Once we identified the problem, the fix was easier. We [replaced](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_git/cp-web-app/pullrequest/13627) the (auth.service.token.client-id) using a properly encrypted client-id and merged the changes to the production environment.

## Direct Target Servers
Each of the on-prem environments is balanced by the F5 load balancer. Depending on the environment, the underlying servers could vary from 2 to 16. Here is the current number of servers available in each on-prem environment. Details will be found in the [Checkpoint LinkMaster](http://cplink.int.westgroup.com/) portal.

- DEV environment: 2 servers
- QA environment: 8 servers
- PRE-PROD environment: 2 servers and
- PROD: 16 servers.

## Checkpoint WebApp Deployment Strategy in the Checkpoint PROD environment
We can access an underlying server using one of these ports (10401 or 10405). The DevOps team deploys the release code in one of the ports and we test out the latest code using one of the underlying servers. 

_Please note, that we need to be on the Zscaler, and requires a non-CIAM user to login to the Checkpoint application using the underlying server URL._

## Test out the Fix using Direct Target Servers before Releasing it to the Customer
We grabbed one of the direct target server URLs from LinkMaster and used a non-CIAM user to log in to the Checkpoint application. For example, here is the URL of a direct target server - http://c628muvcppdap.int.thomsonreuters.com:10401/app/.

While testing the client-id-specific fix in the production environment, we noticed that though the Profile and Notifications services were working as expected but the Checkpoint WebApp was still facing problems calling the publicly facing services (**toc, charts, notes, and calendar**) successfully.

We dug down further and noticed that the publicly exposed APIs were failing due to the configurations we applied for each of these microservices in the [cp-config-server](https://github.com/tr/cp_config-server). For example, we allowed the following three URLs in the `allowed-origin` section of the cp-calendar service for the PROD environment.

- https://checkpoint.riag.com
- https://checkpoint.thomsonreuters.com
- https://riacheckpoint.com

![image.png](/.attachments/image-010ea473-c8a9-4714-bb27-8000e418dbe1.png)

If we initiate a request from any other origin to the calendar service in the PROD environment, the API call will fail. In our case, we were trying to call the calendar service from the origin (c628muvcppdap.int.thomsonreuters.com:10401), as a result, the API call failed which is expected. The same thing happened for the toc, charts, and notes services as well.

**Note:** Please reach out to the Checkpoint CIAM Team (checkpointciamteam@thomsonreuters.com) to get a non-CIAM user for you.

## How to allow Cross Origin Requests from Direct Target Servers
To allow the calls from the origin (c628muvcppdap.int.thomsonreuters.com:10401) and two other direct target servers, we added 3 direct target server URLs in the `allowed-origin` section of the toc, calendar, charts, and notes services and deployed to the PROD environment.

![image.png](/.attachments/image-0cd522fd-6e2e-4f35-9b68-ec98d309f122.png)

**Important:** 
- Please note, that deploying the latest changes from cp-config-server is not enough to pick up the latest config changes. 
- We need to restart the underlying EC2 instances for the microservices. 
- Please contact the Checkpoint DevOps team to restart the EC2 instances. Also, please note that we don't restart the PROD EC2 instances during US hours. DevOps team restarts the PROD EC2 instances during midnight US hours (early IST hours).

Lastly, we didn't make these config changes directly in the release branch to deploy to the PROD environment. We made changes in the DEV environment first to replicate the PROD issue and tested it out. Once confirmed, we went ahead and made the config changes for the PROD environment.

Also, we rolled back the changes from the DEV and PROD environments after the testing was completed.

**Note: It's always better to be extra careful before pushing anything into the production environment.**

## Recommendations to Avoid Similar Kinds of Production Issues in the Future
We have been encrypting the credentials (`client-id`, `client-secret`) before using them in the properties file.  If we encrypt any PROD credentials and push them to the production environment without testing, we can't confirm that we didn't make any mistakes while encrypting the credentials.

During our development time, whenever we notice that we have different sets of credentials for different environments (1. for PROD and 2. another for non-PROD environment), it's recommended to test out the corresponding functionality using the PROD credentials before pushing the changes to the PROD environment. 

For example, we have two sets of credentials for the CIAM platform - 1. non-PROD and 2. PROD. We added the PROD-specific CIAM credentials in the `appDevData.properties` file and deployed the changes to the DEV environment for an hour or two to test out the corresponding functionality. We rolled back the changes after the testing was completed.

We followed the same approach for the News Room API work as well. If anyone has any questions on this, please feel free to reach out to the leads and/or architects for more information.

