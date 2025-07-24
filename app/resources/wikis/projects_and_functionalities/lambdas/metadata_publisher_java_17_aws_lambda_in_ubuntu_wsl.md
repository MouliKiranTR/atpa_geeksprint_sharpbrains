# Table of Contents
1. [Install Java 17](#install-java-17)
2. [Install Maven](#install-maven)
3. [Setup Maven](#setup-maven)
4. [template.yaml](#template.yaml)
5. [event.json](#event.json)
6. [Disable amazonSqs.deleteMessageBatch()](#disable-amazonsqs.deletemessagebatch())
7. [Invoke SAM Application](#invoke-sam-application)
8. [Debug Java lambda code in Idea](#debug-java-lambda-code-in-idea)

The process in the same as described in [plain-text-publisher Python 3.13 AWS Lambda in Ubuntu WSL](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/1075/plain-text-publisher-Python-3.13-AWS-Lambda-in-Ubuntu-WSL) with small changes:
1.  Install Java instead of Python
2.  Install and set up Maven
3.  Use different template yaml for Java project with different configuration and name `MetadataPublisherFunction`
4.  Other Json event objects for [SQS cp-dev-content](https://us-east-1.console.aws.amazon.com/sqs/v3/home?region=us-east-1#/queues/https%3A%2F%2Fsqs.us-east-1.amazonaws.com%2F401148645463%2Fa205159-cp-dev-content)
5.  Make small changes to code to not execute SQS remove from queue logic because events are not from SQS queue

During `wget/curl` downloads you may face certificate errors, use [instruction](https://thomsonreuters.service-now.com/nav_to.do?uri=%2Fkb_view.do%3Fsysparm_article%3DKB0042139).

# Install Java 17
There are several ways on how to install Java 17:
1.  Add official Amazon repo with Corretto 17 and install using `apt-get`, see [instruction](https://docs.aws.amazon.com/corretto/latest/corretto-17-ug/generic-linux-install.html)
2.  Use SDKMAN!:
    1.  [Execute installation script](https://sdkman.io/install) that need zip dependency, use `sudo apt-get install zip`
    2.  After installation script complete, read notes where mentioned on how to enable sdk command in already running terminal like `source "/home/dk_wsl/.sdkman/bin/sdkman-init.sh"`
    3.  Install Amazon Corretto 17 using `sdk install java 17.0.15-amzn`
3.  Use OpenJDK from Ubuntu repo, `sudo apt install openjdk-17-jdk`

# Install Maven
There are two options:
1.  Install from Ubuntu repo using `sudo apt-get install maven`, may not be latest or like used in Idea
2.  Using sdkman, `sdk install maven`

# Setup Maven
Copy your `settings.xml` from Windows, change `employee_id` with yours, `~/.m2` must exist or create it using `mkdir ~/.m2`
```
cp /mnt/c/Users/<employee_id>/.m2/settings.xml ~/.m2/
```
Then edit file and check if there are no Windows paths that may break build, for example in `<localRepository>`.

# template.yaml
Use updated file for Java and metadata-publisher
```
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: >
  metadata-publisher lambda local tester

  Created for execution of metadata-publisher with Java 17 runtime
Globals:
  Function:
    Timeout: 300

Resources:
  MetadataPublisherFunction:
    Type: AWS::Serverless::Function
    Properties:
      # take from AWS console in Lambda -> Code tab -> Runtime settings section -> Handler field
      Handler: com.trta.contenttech.metadatapublisher.MetadataPublisherHandler
      # take from AWS console in Lambda, Configuration tab -> Environment variables
      Environment:
        Variables:
          CONFIG_SERVER_URL: http://cpa-config-server.tr-tax-cp-preprod.aws-int.thomsonreuters.com
          ENVIRONMENT: dev
          HTML_PUBLISHER_LAMBDA: a205159-cp-dev-html-publisher
          MAIN_CLASS: com.trta.contenttech.metadatapublisher.MetadataPublisherApplication
          SPRING_PROFILES_ACTIVE: dev
      Runtime: java17
      Architectures:
        - x86_64
      # take from AWS console in Lambda, Configuration tab -> General configuration
      MemorySize: 1024
      EphemeralStorage:
        # take from AWS console in Lambda, Configuration tab -> General configuration
        Size: 512
```
# event.json
For new/update metadata use
```
{
  "Records": [
    {
      "body": "{\"bucket\":\"a205159-cp-content-dev\",\"contentSet\":\"ftlap\",\"documentId\":\"i166f181fd5814bc69bd7ddc359bda0bb\",\"action\":\"new\"}",
      "eventSource": "aws:sqs"
    }
  ]
}
```
For delete metadata use
```
{
  "Records": [
    {
      "body": "{\"bucket\": \"a205159-cp-content-dev\",\"contentSet\": \"ftlap\",\"documentId\": \"i166f181fd5814bc69bd7ddc359bda0bb\",\"action\": \"deleted\"}",
      "eventSource": "aws:sqs"
    }
  ]
}
```
It is possible to merge both Json in one event.json file but this will make not possible to check metadata changes using [Dev Swagger](https://cp-dev-cp-metadata-service.tr-tax-cp-preprod.aws-int.thomsonreuters.com/api/docs/cp-metadata-service/swagger-ui/index.html#/cp-metadata-service-controller/get_1) between events.

# Disable amazonSqs.deleteMessageBatch()
Because events data is not real SQS message that means that we do not need to notify AWS SQS that message was processed, that is why comment line with execution of `deleteMessagesByQueueUrl()` method in [MetadataPublisherFunction](https://github.com/tr/cp_metadata-publisher/blob/00f8d58fb092a935dacec6ee14017fe4366ce4c3/src/main/java/com/trta/contenttech/metadatapublisher/MetadataPublisherFunction.java#L72).

# Invoke SAM Application
First run
```
sam build
```
After each source code change rerun `build` command.
Login to `cloud-tool` and then use
```
sam local invoke MetadataPublisherFunction --event event.json
```
Or with `local_lambda_test` profile
```
sam local invoke MetadataPublisherFunction --profile local_lambda_test --event event.json
```

# Debug Java lambda code in Idea
Make sure that `cloud-tool` logged in and `sam build` executed.
To debug Java lambda using Idea do next steps:
1.  In Idea Open `Edit Configurations`
2.  Click `+` and select `Remote JVM Debug`
3.  Fill name like `WSL Java lambda debug` and click Ok applying default values, default values are:
    1.  Debugger mode - Attach to remote JVM
    2.  Transport - socket
    3.  Host - localhost
    4.  Port - 5005
    5.  Command line arguments for remote JVM - -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005
    6.  JDK 9 or later
    7.  Use module classpath - cp-metadata-publisher
4.  Put breakpoint in Idea, for example on first line of `MetadataPublisherFunction.apply()`
5.  Execute in WSL, `-d 5005` says to start debug session on port `5005` (the same as specified in `Port` field in `Remote JVM Debug`)  
    ```  
    sam local invoke MetadataPublisherFunction -d 5005 --event event_new.json  
    ```
6.  Wait until in WSL execution pauses with last message  
    ```  
    Picked up _JAVA_OPTIONS: -agentlib:jdwp=transport=dt_socket,server=y,suspend=y,quiet=y,address=*:5005 -XX:MaxHeapSize=2834432k -XX:+UseSerialGC -XX:+TieredCompilation -XX:TieredStopAtLevel=1 -Djava.net.preferIPv4Stack=true  
    ```
7.  Switch to Idea and click Debug for created `Remote JVM Debug` in `Edit Configurations`
8.  Execution in WSL will continue, wait when line with breakpoint is executed and then debugger session will become active in Idea