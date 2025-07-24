[[_TOC_]]

# Test Plans
[Automation Regression Test Plans (ADO)](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_queries/folder/?path=Shared%20Queries/QA/Full%20Regression%20Automation%20Test%20Cases)
[Manual Regression Test Plans (ADO)](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_queries/folder/?path=Shared%20Queries/QA/Manual%20Regression%20Test%20Cases)

# Tools & Tools Documentation
[Report Portal](https://cr-reportportal.1129.aws-int.thomsonreuters.com/ui/#checkpoint/dashboard)
[JDI Light Framework](https://jdi-docs.github.io/jdi-light/#documentation)
[Split Feature Flags](https://app.split.io/org/104390f0-fce3-11e9-a909-0a2317b5aaf8/ws/1049f990-fce3-11e9-a909-0a2317b5aaf8/splits) - Access to Split is limited, if you need help with checking a feature flag please reach out to team members for assistance
[Datadog](https://trta-cp-prod.datadoghq.com/apm/home)

# Testing-related Process Links
[Synthetic Tests on Datadog](https://trta-cp-prod.datadoghq.com/synthetics/tests?query=-env%3Aqed%20-env%3Aprod%20-env%3Atest%20-env%3Adev%20-env%3Aprod-cp-use1%20-env%3Aqed-cp-use1%20-env%3ADevelopment%20-env%3ATEST%20-env%3ACI%20-env%3APREPROD%20-env%3ADEV%20-env%3APROD%20-type%3Aapi-ssl%20-type%3Aapi&cols=monitorStatus%2Ctype%2Cname%2Cdomain%2Ctags%2Cenvs%2Cuptime&page_index=0&from_ts=1742325801593&to_ts=1742329401593&live=true)
[Deleting Shared Folders in Lower Environments (WIP)](https://trten.sharepoint.com/:b:/r/sites/TRTAKSCheckpointAnswers/Shared%20Documents/House%20of%20Lannister/Projects/Regression%20Test%20Improvements/Shared%20Folder%20Script/Deleting%20Shared%20Folders/Documentation%20for%20the%20Process%20of%20Deleting%20Shared%20Folders%20in%20Lower%20Environments.pdf?csf=1&web=1&e=hCCv3l) - First draft Documentation for the Process of Deleting Shared Folders in Lower Environments

# Data for Testing
[Top Searches](https://trten.sharepoint.com/:f:/r/sites/TRTAKSCheckpointAnswers/Shared%20Documents/QA%20Team/Checkpoint%20Most%20Searched%20Terms?csf=1&web=1&e=oPxzfZ) - Last updated in 2023

# Tips & Tricks
- News Homepage & Main Document Page
   - Press Shift + Ctrl + X to open a secret menu -> click "Show XML" to validate information on articles/documents
- Admin Page Access
   - Go to checkpoint.[env].thomsonreuters.com/app/admin
   - Enter TR account credentials
![image.png](/.attachments/image-2232dd1e-8880-46cf-9d33-2ca86a65ba3b.png)

# Helpful Information
- Document Compare
   - Federal Rulings does not amend the same document name between Current Document and Related Document(s). New cases are created and Document Compare for Federal Rulings essentially becomes history. It is normal behavior if you see completely different document names/numbers within the Document Compare modal for Federal Rulings specifically.
- Report Portal
   - If Report Portal launches show both normal and interrupted instances, it may be due to an additional dependency creating a listener. Ensure the main "agent-java-testng" dependency is in the pom.xml file, and remove other dependencies like agent-java-junit, agent-allure-junit, or agent-allure-testng to prevent dual instances and launch issues.
      