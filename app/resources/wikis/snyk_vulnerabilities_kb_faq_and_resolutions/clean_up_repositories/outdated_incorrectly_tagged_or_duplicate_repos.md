**Outdated repo:**
This category of repo will not be deployed to Dev/QA/PreProd/Prod (code in repos was changed long time ago and will not be changed)  or used to deploy code to Dev/QA/PreProd/Prod
In this case you need to:
•	Archive outdated Repo in ADO or GitHub (if it will not be used for any purposes).

**Wrong tagged repo with Asset Insight ID (AIID):**
You may meet situation when your repo is tagged with 2 or more AIID or just wrong one. First of all you need to identify the correct AIID and then:
•	Remove wrong tag(s)/topic(s) for repo in ADO or GitHub
•	Add correct tag/topic for repo in ADO or GitHub (if needed)
**Note:** Please learn more on tag/topic format policy for AIID: https://techtoc.thomsonreuters.com/pattern-library/azure-devops-repo-tagging/ 

**Duplicate repo:**
If you have duplicate repo in ADO or GitHub please check if it still actual and will be used to deploy to Dev/QA/PreProd/Prod.
If it is not, you can: 
•	Archive outdated Repo in ADO or GitHub (if it will **not** be used for any purposes).
•	Add tag “no-code-scanning” in ADO or GitHub (if it will be used for any purposes).
**Note:** Please learn more on tag format policy for excluding repo from Snyk scanning: https://techtoc.thomsonreuters.com/non-functional/security/application-security/exception-mitigation/ 

**Personal repo:**
If you have repo in ADO or  GitHub (for personal use, POC, etc) that will be used for personal purposes only and will not be deployed to Dev/QA/PreProd/Prod (code in repos was changed long time ago and will not be changed)  or used to deploy code to Dev/QA/PreProd/Prod
In this case you need to: 
•	Add tag “no-code-scanning” in ADO or GitHub (if it will be used for any purposes).
**Note:** Please learn more on tag format policy for excluding repo from Snyk scanning: https://techtoc.thomsonreuters.com/non-functional/security/application-security/exception-mitigation/ 

