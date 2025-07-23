You can use ado-projects-tagger (Python script) if you can't add tag to ADO repo manually using ADO UI for any reason like:
- tag length is more than 40 symbols;
- number of tags in repo more than 15. 


**1. Learn more on tag formats for ADO repos:** 
- Link to AIID: https://techtoc.thomsonreuters.com/pattern-library/azure-devops-repo-tagging/
- Exclude from Snyk scanning: https://techtoc.thomsonreuters.com/non-functional/security/application-security/exception-mitigation/

**2.Get your Personal Access Token for ADO repo using next steps:**
-   Go to ADO repo and press Settings icon
![ADO PAT, Step 1.jpg](/.attachments/ADO%20PAT,%20Step%201-a212892d-de2a-4f7e-a195-8ccb2f9c1e0e.jpg)
-   Select menu item "Personal access token"
![ADO PAT, Step 2.jpg](/.attachments/ADO%20PAT,%20Step%202-9f0205be-4174-4b13-ba99-92930a411e1c.jpg)
- Press "New Token" button
![ADO PAT, Step 3.jpg](/.attachments/ADO%20PAT,%20Step%203-bc3d0f79-56f4-45a3-bfa6-67c00acef597.jpg)
- Enter the name and select "full access" in the Scopes section.
![b270e61b-a1d6-4fa2-9c8c-55f52be911d7.png](/.attachments/b270e61b-a1d6-4fa2-9c8c-55f52be911d7-88d09e49-3cd8-4751-ba07-138795667b4c.png)
- Press "Create" button and then copy your token. Save this token somewhere.
![6a137275-65de-4498-b4a8-b713a9b1d714.png](/.attachments/6a137275-65de-4498-b4a8-b713a9b1d714-b05cb8b8-ffae-41fe-934a-bbe99e592830.png)

**3. Use your ADO Personal Access Token with the ado-projects-tagger (Python script)** 
- Clone the repo. 
GitHub repo: https://github.com/tr/prodsec_snyk/tree/main
- After you have cloned the project, you can open the project through the IDE or not, since all actions will take place through the console.
- **Set Environment Variable:** Set the AZURE_TOKEN environment variable with your Azure Devops API token. To do this, paste this "Edit environment variables for your account" into the windows search. Press "New" and fill in the fields and press "OK" button.
![9f28811d-7a20-4716-8da9-6aec2969e7d2.png](/.attachments/9f28811d-7a20-4716-8da9-6aec2969e7d2-d2eacf99-3a99-4e30-bd80-ac36ef996203.png)
-**Install Dependencies:** Open the command prompt (cmd), go to the folder "ado-projects-tagger" and run this command "pip3 install requirements.txt"
**Note** If this command does not work, add "-r" => " pip3 install -r requirements.txt"
- Add tag: command line for adding tags: 
1) python ado_tagger.py add my-org my-project --tags my_repository:206398
2) python ado_tagger.py add my-org my-project --tags my_repository:206398,my_repository2:208426
3) python3 ado_tagger.py add my-org my-project --tags @file-containing-tags

**Example of filled in fields:** "python ado_tagger.py add tr-tax-checkpoint Checkpoint --tags cp-web-app:no-code-scanning".
After you have filled in all the fields, paste this command into the command prompt and run.

**Note** After --tags, you can specify a list of tags separated by commas, or specify a file with @filename
- Remove tag: command line for removing tags: 
1) python ado_tagger.py remove my-org my-project --tags my_repository:206398
2) python ado_tagger.py remove my-org my-project --tags my_repository:206398,my_repository2:208426
3) python3 ado_tagger.py remove my-org my-project --tags @file-containing-tags

**Example of filled in fields:** "python ado_tagger.py remove tr-tax-checkpoint Checkpoint --tags cp-web-app:no-code-scanning".
After you have filled in all the fields, paste this command into the command prompt and run.
