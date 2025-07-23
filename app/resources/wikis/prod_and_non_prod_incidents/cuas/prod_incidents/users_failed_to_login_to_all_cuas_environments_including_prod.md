# Issue
Network Credential Users locked out of CUAS-API across all environments including Production for 60 minutes with a frequency of 2-3 times a day

# Root Cause
CUAS-API makes use of a VDS Service account for LDAP authentication for Internal users that login with their network credentials (ex: C280..., it is the TR employee id)
A Login issue was faced across all CUAS-API environments including Production for these network credential users where the users were not able to login and get through to the application landing page, this happened because the VDS service account that CUAS-API uses was locked out because of 5 or more invalid password attempts by a recent code change in CP-WEB-APP (codebase for Checkpoint application)
CP-WEB-APP is also using this service account (this is not recommended) for LDAP authentication for their administrative login on the /app/admin path 
A recent code change removed the password which was hardcoded in the codebase and replaced it with a property accessor variable which was supposed to pick up the password value from catalina.properties file
Deployed Checkpoint applications worked fine as all of them had this file with correct value stored for this property accessor variable but some developers who were working on a local server of Checkpoint missed out on adding this property and its value to the local catalina.properties file and this made calls to the VDS service with invalid password and this being done by multiple developers caused service account lockout which locked out all CUAS Internal users from logging in to the application for at least 60 minutes including Production

# Short Term Fix
The code change that replaced the hard coded password for the LDAP VDS Service account in CP-WEB-APP was reverted to prevent developers from causing this issue again by mistakenly launching a local server of Checkpoint without the password in their catalina.properties file

# Long Term Fix
The long term fix (and future prevention) for this issue is to not allow sharing of VDS Service account across applications
Work items have been created for the following action items and will be taken up by CUAS and Checkpoint Teams:
- Request a new VDS Service account for Checkpoint and replace the shared VDS Service account being used currently (Checkpoint Team)
- Request a new VDS Service account for CUAS Production (CUAS Team)

## Root Cause Code Change - https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_git/cp-web-app/pullrequest/13889