## **Objectives:**
The goal of this document is to set up maven in the local environment.

## Setup Steps:
- Please download and configure maven using following the [link](https://maven.apache.org/install.html).
- In the Windows machine, browse to the `%USERPROFILE%\.m2` folder and add the server entries into the `server.xml` file using the file - [settings.xml](/.attachments/settings-847efb25-11af-4a3d-ba3e-1c5a72c52dc6.xml)
- Please make sure you log in to the [jFrog](https://tr1.jfrog.io) repository using SAML SSO and click on your employee id and then Edit Profile.

![image.png](/.attachments/image-0dc4914b-1404-43b7-baf0-579939d699a2.png)

- Copy the API key and use it as a password for each section into the settings.xml file.

![image.png](/.attachments/image-42f8c898-80ed-4a12-a80b-1f8ce95c37d5.png)

![image.png](/.attachments/image-a6c4234d-5da9-4f96-9cef-a5daa8640cb4.png)

- Fork and checkout a microservice (for example, `[cp-auth-service](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_git/cp-auth-service)`) from the repository using the [link](https://docs.github.com/en/get-started/quickstart/fork-a-repo).
- Open the project using IntelliJ. Usually, IntelliJ pops up an option to enable auto imports at the right bottom corner while downloading the dependencies. 
- Please enable it and Maven will download all the required dependencies for the microservice.
- If there are still dependency errors, please use `mvn clean install`.