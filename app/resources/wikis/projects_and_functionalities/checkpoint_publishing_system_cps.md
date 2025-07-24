# CPS process and workflow

Please refer to this file: [LINK](/.attachments/KT%20Document%201-8597e405-8b2a-48c6-b2ba-18f268a80e53.doc) there you are gonna find very useful information about CPS.
## CPS Tool
You can request access to the CPS tool from Terri Ganssley.

| Environment | Link |
|-------------|------|
|INT          |http://cps-int-app.int.thomsonreuters.com:8888/CPS.Tool/|
|QA           |http://cps-qa-app.int.thomsonreuters.com:8888/CPS.Tool/|
|Preprod      |http://cps-preprod-app.int.thomsonreuters.com:8888/CPS.Tool/|
|Prod         |http://cps-prod-app.int.thomsonreuters.com:8888/CPS.Tool/|

_Repository:_ https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_git/cp-publishing?path=/CpsCore2.0/ContentProcessing/CPS.Tool

### How to schedule a database to run through the Checkpoint Publishing System Tool platform

See the section above and check if you have access to the platform. Follow the next steps:


1. Go to Requesting DB for processing:
![image.png](/.attachments/image-dbf8ee55-29e4-468b-ae87-bc6c52ff146d.png)
2. Request the database that you want to process:
![image.png](/.attachments/image-9f18190d-9519-43fc-b7a4-2ef49bd20621.png)
3. Submit the request.

**Note:** If you want your database to be processed for the next day, you need to request it with your current date build on "Select a build for the database request" and make sure to request it before the cut-off at **11:00 AM EST**.

## How to access the CPS Server

You can access the servers using ssh with the following servers:


| Environment | Server |
|--|--|
| INT | ssh [user]@cps-int-app.int.thomsonreuters.com |
| QA  | ssh [user]@cps-qa-app.int.thomsonreuters.com |
| Preprod | ssh [user]@cps-preprod-app.int.thomsonreuters.com |
| Prod | ssh [user]@cps-prod-app.int.thomsonreuters.com |


**Note:** Ask for credentials to DevOps our your lead.

### 1. Putty
Host: cps-int-app.int.thomsonreuters.com
Port: 22
Connection Type: SSH

### 2. Console

- Login
`$ ssh <user>@cps-int-app.int.thomsonreuters.com`

- Copy a file from the server
`$ scp <user>@cps-int-app.int.thomsonreuters.com:<path_to_file_in_server> <local_path>`

- Copy a file to the server
`$ scp <local_path> <user>@cps-int-app.int.thomsonreuters.com:<path_to_file_in_server>`

## Other documentation
- [CPS - KT Document - 2010.doc](/.attachments/CPS%20-%20KT%20Document%20-%202010-f6152c66-c8ee-4f5d-9596-d15def54c76b.doc)