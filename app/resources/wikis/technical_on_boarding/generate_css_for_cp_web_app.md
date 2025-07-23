
If the UI is not displaying correctly when running locally, for example, History/Notifications/..., you may need to generate a CSS file.

- In order to resolve the dependencies needed for building CSS we need to create a .npmrc file (if not already done)
  1. Get your JFrog API Key from [Jfrog](https://tr1.jfrog.io/ui/#/home) in the Edit profile option of the top right bar and in the API Key section. To authenticate use the SAML SSO option.
  2. Get your secret key with the API Key of the previous step by running the following command: `curl -u <User>:<API Key> https://tr1.jfrog.io/tr1/api/npm/auth`
  3. Update the .npmrc file with the following information:
      ```
      registry = https://tr1.jfrog.io/tr1/api/npm/npm/
      _auth = <your-secret-key>
      always-auth = true
      email = <your-username>@thomsonreuters.com
      ```
- Install GitHub CLI from the following link: [https://cli.github.com](https://mcas-proxyweb.mcas.ms/certificate-checker?login=false&originalUrl=https%3A%2F%2Fcli.github.com.mcas.ms%3FMcasTsid%3D15600&McasCSRF=6ad64f07344157a44eeaf57b148f2a2069098450c609bf2e332bb61706a266e2).
- Run the following command in PowerShell to authenticate to your GitHub TR account: **gh auth login**
Note: this command would not work properly in Git Bash due to the interactive authentication process. However, once you’re logged in to GitHub, you can use Git Bash for the next steps.
- Run the following command to pull the latest CP UI release artifact: **gh release -R tr/cp_ui download --pattern artifact.zip**
- If you have the CP Web App running locally, stop it before proceeding with the next steps.
- Delete the “CPWar/web/ngCPDist” folder from your CP Web App working directory.
- Extract the Zip file and copy the “ngCPDist” folder into the “CPWar/web/” folder of your project.
- Repeat steps 3-6 every time you need to get the latest changes from the UI project (Checkpoint Edge) to run within the Web app.
- For local, run the Ant script `localBuildCss`
  - ![image.png](/.attachments/image-12915b9e-e8dc-4638-9a89-5b59df1cccd0.png)
- Expected
![image.png](/.attachments/image-d9a45ba1-0d85-4c31-b651-c8803d40c893.png)


## ERRORS:
- when you run `gulp buildCss` -> primodials error
  - ![image.png](/.attachments/image-7495ce0a-ad63-433b-9977-2bd824c12dc3.png)
- **FIX:** Use these versions to run `gulp buildCss`
  - gulp 3.9
  - ~~node 10~~
    - *Note:* changes made to `package.json` in [PR #13939](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_git/cp-web-app/pullrequest/13939) updated the required Node version to 16. If you experience issues try running with Node v16.
