# Table of Contents
1. [Install WSL or Update WSL](#install-wsl-or-update-wsl)
2. [Optional, sudo not ask for password](#optional%2C-sudo-not-ask-for-password)
3. [Install Python3](#install-python3)
4. [Install Python 3.13 of lambda runtime version](#install-python-3.13-of-lambda-runtime-version)
5. [Install AWS CLI](#install-aws-cli)
6. [Install AWS SAM CLI (Serverless Application Model)](#install-aws-sam-cli-(serverless-application-model))
7. [Install Docker using the repository](#install-docker-using-the-repository)
8. [Mandatory step, make Docker run without sudo](#mandatory-step%2C-make-docker-run-without-sudo)
9. [Install cloud-tool](#install-cloud-tool)
10. [Quick SAM Application overview](#quick-sam-application-overview)
11. [template.yaml](#template.yaml)
12. [SAM build](#sam-build)
13. [Event.json](#event.json)
14. [Invoke SAM Application](#invoke-sam-application)
15. [Testing process](#testing-process)

In [User Story 174902](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_workitems/edit/174902/) it is needed to upgrade Python from 3.7 to 3.13 for [a205159-cp-dev-plaintext-publisher](https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/functions/a205159-cp-dev-plaintext-publisher?subtab=general&tab=code) Lambda.
During `wget/curl` downloads you may face certificate errors, use [instruction](https://thomsonreuters.service-now.com/nav_to.do?uri=%2Fkb_view.do%3Fsysparm_article%3DKB0042139).
Next steps describe how to test locally [a205159-cp-dev-plaintext-publisher](https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/functions/a205159-cp-dev-plaintext-publisher?subtab=general&tab=code) using Ubuntu WSL with Docker and Python 3.13:

# Install WSL or Update WSL
Open Command line with admin rights and [Install WSL](https://learn.microsoft.com/en-us/windows/wsl/install#install-wsl-command) using
```
wsl --install
```
You may want to [update WSL](https://learn.microsoft.com/en-us/windows/wsl/basic-commands#update-wsl) if already installed
```
wsl --update
```
You may also review [Basic commands for WSL | Microsoft Learn](https://learn.microsoft.com/en-us/windows/wsl/basic-commands).
After install it will be suggested to reboot VDI.
After reboot In Start menu search for WSL and run it.
Follow all instructions and as the result you will have installed Ubuntu with created user and password, password is needed for sudo command but this may be disabled and described in 2nd item by adding of your user to sudoers file.
Drive c: from VDI is mounted to `/mnt/c` by default, for example folder in VDI `C:\checkpoint\cp_plain-text-publisher` may be accessed by
```
cd /mnt/c/checkpoint/cp_plain-text-publisher
```
  
# Optional, sudo not ask for password

Adding of your user to sudoers file is not necessary but may be convenient, note that when you enter password for sudo once the password will not be asked second time in the same session.
First run
```
sudo visudo
```

Enter password of your user that was specified during user creation and text editor will be opened, in my scenario it is GNU Nano but long time before it was vi or vim.
Add next lines to file almost at the end of file before @includedir /etc/sudoers.d, **not forget to replace your user name**
```
# Allow my user to use sudo without password
{replace_with_your_user_name} ALL=(ALL) NOPASSWD:ALL
```

And save using `CTRL + O`, then Enter and `CTRL + X` to exit.

# Install Python3

Update repositories indexes and install Python3 with dependencies
```
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv
```

This will install currently available 3rd version of Python from Ubuntu repositories.
`Python3-pip` is needed for lambda dependencies installation using SAM from requirements.txt and cloud-tool.
`Python3-venv` is needed for cloud-tool in virtual environment.
After installation is done run to check installed version of Python
```
python3 --version
```

In my situation was installed `3.12.3`.
  
# Install Python 3.13 of lambda runtime version
Python3 installed version `3.12.3` but lambda need to use `3.13` and SAM build command will reject to execute if in `template.yaml` specified `Runtime: python3.13` version of Python and there is no python3.13 in PATH.
Need to add external ppa repository with compiled python versions, if there is no version that you need probably you may try to compile it from sources and create
your own package
```
sudo add-apt-repository ppa:deadsnakes/ppa
```

Had long time wait util description was loaded and then pressed enter, you may also need to update repositories index if add repository not done it and install Python 3.13
```
sudo apt-get update
sudo apt-get install python3.13
```

And check if python3.13 is installed
```
python3.13 --version
```

# Install AWS CLI
Find Linux section and [install AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) using any of available options, I used snap because it is only one command and not 5 steps if using installer and worked locally without issues.

# Install AWS SAM CLI (Serverless Application Model)
Find Linux section and [install AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) using downloadable installer, wget <installer_url> may be used to download installer to current directory.
Also install unzip utility that is executed by user during installation and not installed by default
```
sudo apt install unzip
```

# Install Docker using the repository
Use instructions that are provided in [documentation](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository), while writing this doc found another way [using convenience script](https://docs.docker.com/engine/install/ubuntu/#install-using-the-convenience-script) that was not used by me.
After installation is done make sure you verified installation
```
sudo service docker start
sudo docker run hello-world
```

# Mandatory step, make Docker run without sudo
If not to do this step then SAM cli will not see Docker if executed without sudo
```
Error: Running AWS SAM projects locally requires Docker. Have you got it installed and running?
```

To make Docker run without sudo do next steps
```
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
```

And check results by running of docker without sudo
```
sudo service docker start
docker run hello-world
```

# Install cloud-tool
[Cloud tool](https://techtoc.thomsonreuters.com/non-functional/cloud-landing-zones/aws-cloud-landing-zones/command-line-access/cloud-tool-quickstart/) needs Python and pip that are already installed and described in item 3 Install Python3.

# Quick SAM Application overview
You may review [Develop your serverless application with AWS SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/chapter-create-application.html).
High level process looks like:
1.  Create configuration template.yaml
2.  Build sam application
3.  Run sam application specifying input/event data and optionally aws profile

As written in [documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/using-sam-cli-init.html) it is possible to create SAM application using sam init, questions will be asked about your application and as the result will be created separate project folder where you need to put sources and configuration as standalone application.
Using sam init it is good global approach but for first run was chosen lightweight/easier version, it is good idea to discuss later if more enterprise-like approach make sense but for first try it is good to understand and focus on basics and then discuss next steps.
Why lightweight/easier approach is used for first try:
1.  Easy to set up and works fine with minimal configuration
2.  Easier to understand and focus on basic features
3.  A lot of extra function like tests and gateways are not used, not set up and not mentioned in document, used only what is required
4.  Do not need to copy anything in separate SAM project folder like sources and requirements.txt
5.  Approach may be extended later after discussion

Template.yaml created by sam init use templates from [git](https://github.com/aws/aws-sam-cli-app-templates/blob/master/python3.13/hello/%7B%7Bcookiecutter.project_name%7D%7D/template.yaml).
  
# template.yaml
Each SAM application needs template.yaml and it may change depending on what you are testing and other criteria.
In this section shown `template.yaml` for `cp_plain-text-publisher`.
In project folder create template.yaml file near pom.xml and requirements.txt, in my situation it is `/mnt/c/checkpoint/cp_plain-text-publisher/template.yaml`, for cp_plain-text-publisher it looks like:
```
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: >
  plaintext_publisher.py lambda local tester

  Created for execution of plaintext_publisher.py with Python 3.13 runtime
Globals:
  Function:
    Timeout: 3

Resources:
  PlaintextPublisherFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: src.plaintext_publisher.lambda_handler
#      Environment:
#        Variables:
#          ENVIRONMENT: dev
      Runtime: python3.13
      Architectures:
        - x86_64
      MemorySize: 192
      EphemeralStorage:
        Size: 512
```
Notes on template.yaml configuration:
1.  `Handler`, take from AWS console in Lambda -> Code tab -> Runtime settings section and Handler field and specify full path relative to template.yaml file if no CodeUri property is specified like in described case, if handler is in src directory then use src.plaintext_publisher.lambda_handler
2.  `Runtime`, specify python3.13 if you want to run lambda using python 3.13, docker image will be selected based on this parameter and SAM build will use python3.13 that must be on PATH
3.  `Environment`, sometimes it is needed to specify environment variables
4.  `MemorySize` and `EphemeralStorage.Size`, take from AWS console in Lambda, Configuration tab -> General configuration

Use [a205159-cp-dev-plaintext-publisher](https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/functions/a205159-cp-dev-plaintext-publisher?subtab=general&tab=code) lambda as example.
Refer to [documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/chapter-create-application.html) for more info.

# SAM build
You may review [Build your application with AWS SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-building.html).
After template.yaml is created and configured just run next command in project directory, in my situation it is `/mnt/c/checkpoint/cp_plain-text-publisher`
```
sam build
```

Check log and if there are no errors, like:
1.  `Needed python version not found`, just check that python3.13 --version is working fine or other version depending on Runtime configuration in template.yaml
2.  `Error installing dependencies from requirements.txt`, faced this error because in python3.13 there are problems with `regex==2020.1.8`, `ERROR: Failed to build installable wheels for some pyproject.toml based projects (regex)`, updated regex version and this solved my problem. You also may try to install dependencies from requirements.txt in venv using `pip3 install -r requirements.txt` and check if it is working fine outside of sam build
3.  `Not possible to copy files`, check filesystem permissions and if all files are readable and destination folder is writable, try to delete destination folder like .aws-sam and then use sam build that will create new folder, as last measure may try to use sudo sam build but it is not recommended

# Event.json
`Event.json` file contain input/event data for lambda, for example for cp_plain-text-publisher it looks like
```
{
    "objectMetaData": {
        "guid": "iPPCCAR:2021d734e5069a7ef83",
        "publication": "ppccar",
        "status": ""
    },
    "bucketName": "a205159-cp-content-dev",
    "eventName": "ObjectCreated:Put",
    "key": "html/ppccar/iPPCCAR:2021d734e5069a7ef83.html"
}
```
Create event.json files in project directory like `/mnt/c/checkpoint/cp_plain-text-publisher` and this data may be used during lambda execution.

Lambda may be triggered by different mechanisms like s3, invoked from Java code and others.
[a205159-cp-dev-plaintext-publisher](https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/functions/a205159-cp-dev-plaintext-publisher?subtab=general&tab=code) lambda not have triggers associated (like s3) and that means that it is triggered differently.
On [Content Pipeline](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/587/Content-Pipeline) diagram specified that plain text publisher lambda is called from [json publisher](https://github.com/tr/cp_json-publisher/blob/main/src/main/java/com/trta/checkpoint/jsonpublisher/JsonPublisherHandler.java#L269).
It is also possible to analyze .py file and get info on used fields and probably find logs with data or full event that may be viewed in [CloudWatch](https://us-east-1.console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups/log-group/$252Faws$252Flambda$252Fa205159-cp-dev-plaintext-publisher/log-events/2025$252F02$252F27$252F$255B$2524LATEST$255D569dad71531d4d26a814dd257cb8cfda).

# Invoke SAM Application
If python lambda is using aws resources like s3 then it is needed to log in cloud-tool first using
```
cloud-tool login
```

Or if you want to use specific aws profile like local_lambda_test then use
```
cloud-tool -p local_lambda_test login
```

Then go to project directory like `/mnt/c/checkpoint/cp_plain-text-publisher` where `template.yaml` file and `event.json` files and execute with default aws profile
```
sam local invoke PlaintextPublisherFunction --event event.json
```

Or with `local_lambda_test` profile
```
sam local invoke PlaintextPublisherFunction --profile local_lambda_test --event event.json
```

`PlaintextPublisherFunction` is specified in `template.yaml`.
Do not try to use this command with sudo or may have problems with aws even if cloud-tool is logged in
`An error occurred (InvalidAccessKeyId) when calling the GetObject operation: The AWS Access Key Id you provided does not exist in our records`.

If docker is failing with message
```
Error: Running AWS SAM projects locally requires Docker. Have you got it installed and running?
```

Then finish item 8 and make docker run without sudo and this will resolve problem, running sam invoke with sudo will also remove docker error but this is not an option.
See results example:
```
Invoking src.plaintext_publisher.lambda_handler (python3.13)
Local image is up-to-date
Using local image: public.ecr.aws/lambda/python:3.13-rapid-x86_64.

Mounting /mnt/c/checkpoint/cp_plain-text-publisher/.aws-sam/build/PlaintextPublisherFunction as /var/task:ro,delegated, inside runtime container
START RequestId: f7bdde1f-bc46-4b3d-9113-ec0145b8d03c Version: $LATEST
/var/task/src/plaintext_publisher.py:58: SyntaxWarning: invalid escape sequence '\s'
  text = re.sub("\s+", " ", text)
[INFO]  2025-03-07T13:25:05.472Z                Found credentials in environment variables.
[INFO]  2025-03-07T13:25:05.686Z        04e2868b-1f97-4213-bcd2-998b0c95bab6    {"objectMetaData": {"guid": "iPPCCAR:2021d734e5069a7ef83", "publication": "ppccar", "status": ""}, "bucketName": "a205159-cp-content-dev", "eventName": "ObjectCreated:Put", "key": "html/ppccar/iPPCCAR:2021d734e5069a7ef83.html"}
[INFO]  2025-03-07T13:25:05.686Z        04e2868b-1f97-4213-bcd2-998b0c95bab6    bucket_name: a205159-cp-content-dev
[INFO]  2025-03-07T13:25:05.686Z        04e2868b-1f97-4213-bcd2-998b0c95bab6    input_key: html/ppccar/iPPCCAR:2021d734e5069a7ef83.html
[INFO]  2025-03-07T13:25:05.686Z        04e2868b-1f97-4213-bcd2-998b0c95bab6    event_name : ObjectCreated:Put
[INFO]  2025-03-07T13:25:05.686Z        04e2868b-1f97-4213-bcd2-998b0c95bab6    plaintext_publisher extract try for bucket: a205159-cp-content-dev key: html/ppccar/iPPCCAR:2021d734e5069a7ef83.html
[INFO]  2025-03-07T13:25:05.963Z        04e2868b-1f97-4213-bcd2-998b0c95bab6    plaintext_publisher load successfull for bucket: a205159-cp-content-dev key: text/ppccar/iPPCCAR:2021d734e5069a7ef83.txt
END RequestId: 04e2868b-1f97-4213-bcd2-998b0c95bab6
REPORT RequestId: 04e2868b-1f97-4213-bcd2-998b0c95bab6  Init Duration: 0.03 ms  Duration: 1279.00 ms    Billed Duration: 1280 ms        Memory Size: 192 MB     Max Memory Used: 192 MB
{"ResponseMetadata": {"RequestId": "KX151MGCQ5MYA3JK", "HostId": "qa9Xeje7lc4yGxVR4mlG8CyKC93IAK0/ZC+hK5RkS1MRLtvDoxu7LuIOYtNtHKj+LLlEJC3Tk0g=", "HTTPStatusCode": 200, "HTTPHeaders": {"x-amz-id-2": "qa9Xeje7lc4yGxVR4mlG8CyKC93IAK0/ZC+hK5RkS1MRLtvDoxu7LuIOYtNtHKj+LLlEJC3Tk0g=", "x-amz-request-id": "KX151MGCQ5MYA3JK", "date": "Fri, 07 Mar 2025 13:25:06 GMT", "x-amz-server-side-encryption": "AES256", "etag": "\"a3269526e2998c5d898c36e18f682109\"", "x-amz-checksum-crc64nvme": "W4Bh0uKpiZI=", "x-amz-checksum-type": "FULL_OBJECT", "content-length": "0", "server": "AmazonS3"}, "RetryAttempts": 0}, "ETag": "\"a3269526e2998c5d898c36e18f682109\"", "ServerSideEncryption": "AES256"}
```
After run you may check results, in my situation results are:
1.  Lambda executed without errors and as the result have `200 http code`
2.  Used python 3.13 Docker image `public.ecr.aws/lambda/python:3.13-rapid-x86_64`
3.  All logs that I excepted are printed
4.  New file saved in s3 bucket in text directory by lambda
5.  Have one `SyntaxWarning: invalid escape sequence '\s' for line text = re.sub("\s+", " ", text)` that needs to be investigated
6.  Lambda is finished with updated dependency `regex==2024.11.6`
7.  Need to analyze all use cases for this lambda










# Testing process


[Test Guide - cp-plaintext-publisher Lambda Function.pdf](/.attachments/Test%20Guide%20-%20cp-plaintext-publisher%20Lambda%20Function-5d4702b1-70a1-4f83-a1fd-420a08aca9ad.pdf)

[Test Guide - cp-plaintext-publisher Lambda Function.md](/.attachments/Test%20Guide%20-%20cp-plaintext-publisher%20Lambda%20Function-494cabe7-b898-4b08-9e21-161c87366ddf.md)
