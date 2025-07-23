# Description
The Content Agent is a Spring Boot application that allows to run various content-related tasks on the CPS servers from command line. While all of the commands available in the Content Agent can be executed manually, some of them are part of automated processes. For example, the CPS `prepilot` and `postpilot` Perl scripts trigger the Content Agent multiple times but with different commands.

Remember that the Checkpoint Publishing System (CPS) regular process, runs the following commands per database in that order:
1. generate-metadata (prepilot.pl)
2. generate-manifest (postpilot.pl)
3. datasync (postpilot.pl)
4. datasync-status (postpilot.pl)

##Available commands

|**Command**             | **Triggered from** |
|------------------------|--------------------|
| `cpa-orchestrator`     | Manually triggered |
| `datasync`             | prepilot.pl (3) |
| `datasync-status`      | postpilot.pl  |
| `generate-manifest`    | prepilot.pl (2) |
| `generate-metadata`    | prepilot.pl (1) |
| `promote-chart`        |  |
| `promote`              | CPS |
| `promote-content`      |  |
| `promote-cp-tools`     |  |
| `promote-orchestrator` |  |
| `promote-toc`          |  |
| `test-light`           | Test Light script |

## Content Agent Development and Deployment 
Repository: https://github.com/tr/cp_content-agent

The project has its own Jenkins pipeline. The pipeline, if successful, will create a new JAR version in the JFrog Artifactory.

Note that this Jenkins job will not automatically deploy the JAR to the CPS servers. If you need to deploy a different version of the Content Agent, you have to request the deployment to the DevOps team and specify the version and the environment to deploy (INT for Dev).

Remember that some of the Content Agent commands require connectivity to AWS services. The application properties keep configurations regarding the AWS Credentials. Take this into consideration whenever the application fails to communicate with AWS services.

## Content Agent Execution

There are multiple ways available to run the Content Agent. You can find the steps for each one below: 

1. Running Developer scripts in the CPS server

   Login to the CPS server to run the following commands there. See the instructions to login in: https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/585/Checkpoint-Publishing-System-(CPS).

    - Light script:

      Shell script to run the content agent using the test-light command. This command will only publish manifest in the given mode to the s3 bucket. To use it, execute the following command:
      `$ /checkpoint/fs/content-agent/scripts/test-datasync-light.sh <database> <mode>`

      Where: 
      * `<database>`= Publication to run written in lowercase.
      * `<mode>`= The mode to run the publication. I.e. `full` or `incremental`.

    - Complete script:

      Shell script to run the content agent using the commands: `generate-manifest`, `datasync`, and `datasync-status`. This will trigger AWS DataSync of DMS (XMLs) and Metadata folders      and then send over the manifest to s3.  To use it, execute the following command:
      `$ /checkpoint/fs/content-agent/scripts/test-datasync-complete.sh <database> <mode>`

      Where: 
      * `<database>`= Publication to run written in lowercase.
      * `<mode>`= The mode to run the publication. I.e. `full` or `incremental`.
    - Content Pipeline Developer Tool script:
      Shell script that allows us to run multiple options, including the scripts mentioned above. Besides the capability to run content agent commands, it allows verification of the DMS REST API and restarts it when needed. To use it, execute the following command:
      `$ /checkpoint/fs/content-agent/scripts/content-pipeline-tool.sh`

      ![image.png](/.attachments/image-3379304d-d3cc-4eaf-9fed-f07510436b0f.png)

2. Running the `content-agent` JAR directly in the server
**Note:** Replace the variables below with:

   _{profiles}_:

   | Environment | profiles            |
   |-------------|---------------------|
   | dev         | int,aws-nonprod     |
   | qa          | int,aws-nonprod     |
   | preprod     | preprod,aws-nonprod |
   | prod        | prod,aws-prod       |

   _{database}_: The publication name with lowercase.

   _{mode}_: Optional. Either **full** or **incremental** values. The default mode is set in the content-agent-config.xml file and used if not defined.

   _{snapshotID}_: SnapshotID name that will be sent to the Kinesis stream. Usually, set with the current date.

   ### Commands

   - Generate Metadata
`$ /checkpoint/fs/java/java8/bin/java -Dspring.profiles.active={profiles} -DconfigFile=/checkpoint/fs/content-agent/content-agent-config.xml -jar /checkpoint/fs/content-agent/content-agent*.jar generate-metadata -p {database}`

   - Generate Manifest
`$ /checkpoint/fs/java/java8/bin/java -Dspring.profiles.active={profile} -DconfigFile=/checkpoint/fs/content-agent/content-agent-config.xml -jar /checkpoint/fs/content-agent/content-agent*.jar generate-manifest -p {database} -md /checkpoint/cm/work/contentAgent/{database} [-m mode]`

     Note: It creates a manifest file in `/checkpoint/cm/work/contentAgent/{database}` path.

   - Create Datasync Task
`$ /checkpoint/fs/java/java8/bin/java -Dspring.profiles.active={profile} -DconfigFile=/checkpoint/fs/content-agent/content-agent-config.xml -jar /checkpoint/fs/content-agent/content-agent*.jar datasync -p {database} -lpd /checkpoint/cm/work/contentAgent/{database}`

   - Datasync Status Check and Manifest publishing to S3
`$ /checkpoint/fs/java/java8/bin/java -Dspring.profiles.active={profile} -DconfigFile=/checkpoint/fs/content-agent/content-agent-config.xml -jar /checkpoint/fs/content-agent/content-agent*.jar datasync-status -p {database} -lpd /checkpoint/cm/work/contentAgent/{database}`

   - Promote Event:
`$ /checkpoint/fs/java/java8/bin/java -Dspring.profiles.active={profile} -DconfigFile=/checkpoint/fs/content-agent/content-agent-config.xml -jar /checkpoint/fs/content-agent/content-agent*.jar promote-content -s {snapshotID}`

3. Locally using IntelliJ

   **Note:** When running locally you need to comment the following line in the `ContentAgentService` class: 
   `restTemplate.setRequestFactory(getClientHttpRequestFactory()); // Need proxy to call content service`

   1. Ensure you have Java 8 installed in your local machine.
   2. Fork the project from `https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_git/content-agent` and clone it to your local.
   3. Open the project in IntelliJ and resolve the Maven dependencies.
   4. Verify the profiles section in your `settings.xml` file.
   5. Open the Run/Debug configurations and set them as follows:

      ![image.png](/.attachments/image-b43abedb-b227-48d5-b0f5-271d24418e31.png)


      - The application runs with program arguments:
        - The first element is the command to run. E.g. `datasync`, `generate-metadata`, etc.
        - The second element is usually the content set that we want to run preceded by `-p`.
        - Take point number 2 as a reference for any other options needed.

      At this step, you are gonna be able to run the content agent successfully.

## Visualize the Content Agent Logs

Once you are on the CPS server machine you need to go to the `/checkpoint/cm/logs/` directory where the logs are saved:

1. `content_agent*.log`. Logs for the `generate-metadata` and `generate-manifest` commands.
2. `content_agent_datasync*.log`. Logs for the `datasync` and `datasync-status` commands.
3. `notify_elasticsearch_drv_prodop_*.log`. Promote event logs.
4. `dmsrestapi_prodop*.log`. Logs of the DMS Rest API.
5. `<processor+ID>.event.newlog`, `<processor+ID>.err.newlog`. CPS Processors logs. E.g. `PR1.event.newlog`.
   Where
   - processor = PR (preprocessing), PO (Postprocessing), LO (left-over) 
   - ID= the process ID that goes from 1 to 10.