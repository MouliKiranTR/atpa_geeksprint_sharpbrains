[cloud-tool](https://github.com/tr/enterprise-cloud_cloud-tool) is a Python CLI tool which facilitates authenticated access to Amazon AWS; enables SSH access to AWS hosted resources via the Bastion Service; and helps users manage their local configuration for the AWS CLI. Access to TR assets in AWS is restricted for security purposes, and cloud-tool is the approved mechanism for accessing them via the command line.

There are two links under the **Get Started** section of this [Atrium](https://trten.sharepoint.com/sites/intr-plat-eng/SitePages/Cloud-Tool.aspx) document. Follow the instructions from the **Cloud-Tool Installation** section of the [first](https://techtoc.thomsonreuters.com/non-functional/cloud-landing-zones/aws-cloud-landing-zones/command-line-access/cloud-tool-quickstart/) document or use the following steps to install cloud-tool if you are using a Windows machine:

- Cloud-Tool is currently compatible with Python versions 3.7.x through 3.9.x. So use any version such as 3.8.0 or 3.9.7.
- Click on the Add Python 3.x to PATH option when installing Python on Windows.
- Create a directory in your home (C:\Users\UXXXXXXX or C:\Users\CXXXXXXX) directory called pip.
- Add the following lines in the pip.ini file:

```
[global]
extra-index-url=https://<employee-id>:<APIKey>@tr1.jfrog.io/tr1/api/pypi/pypi-local/simple
```

- Replace <employee-id> using your employee id. Make sure to use only the numeric part of your employee id.
- Login to the [jFrog repository](https://tr1.jfrog.io/ui/login/) using SAML SSO option.
- Get the API key from the Edit Profile section.

![image.png](/.attachments/image-13f35ee3-ee51-482e-bab8-42bc05671e61.png)

- Generate a new API key if it doesn't exist.

![image.png](/.attachments/image-e6bb9a49-e54f-44b2-be6a-e88c406facfe.png)

- Copy the API key and replace the <APIKey> section in the second line of the pip.ini file.
- Save the changes and close the pip.ini file.
- Open a command prompt and check the python version.
- Execute the command - **pip install --upgrade cloud-tool** to install the latest cloud-tool version.
- Or use this command - **pip install --upgrade cloud-tool==<version>** to install a specific version of it. For example **pip install --upgrade cloud-tool==7.2.0**
- Use **cloud-tool --version** command to check the installed cloud-tool version.
- Then follow the instructions from **Cloud-Tool Configuration** section of this [document](https://techtoc.thomsonreuters.com/non-functional/cloud-landing-zones/aws-cloud-landing-zones/command-line-access/user_guide/).
- Try to execute the following commands if you find the below error: ![image.png](/.attachments/image-977bed8d-f106-465d-96a0-21b5e03aa368.png)

export jfrog_url=https://<artifactoryUsername>:<artifactoryToken>@tr1.jfrog.io/tr1/api/pypi/pypi-local/simple

pip install --upgrade --extra-index-url $jfrog_url cloud-tool

**Note: if none of the above steps work for you, please try out the following steps to install cloud-tool in your machine.**

- Use Command "pip install --upgrade --index-url https://<artifactoryUsername>:<artifactoryToken>@tr1.jfrog.io/tr1/api/pypi/pypi-local/simple cloud-tool"
Replace your username with <artifactoryUsername> and Api-Key from JFrog with <artifactoryToken>
- And if says to upgrade the psutil to specific version use command "pip install --upgrade --index-url https://pypi.org/simple psutil=<version>
- And further if you encounter error that says pywin32 is not present or could not be found, use  command "pip install  --upgrade --index-url https://pypi.org/simple pywin32"
- And then use Command "pip install --upgrade --index-url https://<artifactoryUsername>:<artifactoryToken>@tr1.jfrog.io/tr1/api/pypi/pypi-local/simple cloud-tool", this would help you install cloud-tool. 

![image.png](/.attachments/image-5cbed016-8a55-43d4-8f2b-df9b95a04cbe.png)
[[_TOC_]]

- Once the configuration is completed, you can use cloud-tool to login to the AWS from the command prompt.
- Use **cloud-tool login** command to log in to the AWS.
- Get the one-time password from [Password Vault] (https://pam.int.thomsonreuters.com/PasswordVault/v10/logon) and use it to login to AWS using cloud-tool.

![image.png](/.attachments/image-6b58ccc4-e239-4f25-939e-b372a0ce591d.png)

**References:**
- Cloud-Tool - https://trten.sharepoint.com/sites/intr-plat-eng/SitePages/Cloud-Tool.aspx
- Cloud Tool User Guide - https://techtoc.thomsonreuters.com/non-functional/cloud-landing-zones/aws-cloud-landing-zones/command-line-access/user_guide/
- Cloud-Tool Quick Start Guide - https://techtoc.thomsonreuters.com/non-functional/cloud-landing-zones/aws-cloud-landing-zones/command-line-access/cloud-tool-quickstart/





