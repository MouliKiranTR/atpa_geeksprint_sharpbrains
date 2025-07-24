How to run cp-tools-service.

You need to have already setUp cloud-tool. If you dont have it follow this link
[Cloud-Tool](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/258/Accessing-CP-Amazon-Web-Services-Amazon-DynamoDB-using-AWS-CLI-and-Configuring-Spring-Boot-to-connect-with-Amazon-DynamoDB?anchor=accessing-to-amazon-dynamodb-locally-using-aws-cli%3A)
Under "Accessing to Amazon DynamoDB locally using AWS CLI:" you will find how to install it.

After you have clone cp-tool-service, do the next:
*Resolve the dependencies.
*Follow the screenshot to see the configuration to run

![image.png](/.attachments/image-d12b7202-da83-4d6d-a341-f5479d64025e.png)

In order to work locally cp-web-app and cp-tools-service, you need to point to your 
tools.service.client.base-url = http://localhost:9998

Log in to http://localhost:8080/app/admin and follow the next:
Server Admin/This server/ View Configuration/ View loaded app.properties

Under update property
Selec the correct name in this case it would be "tools.service.client.base-url".
Add the new value.
Check "This server Only".
Click Submit.
![image.png](/.attachments/image-57d41447-3918-4fd7-be77-5e356495fbe2.png)

If you don't have access follow this link [Admin_Access](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/287/Admin-Site-Checkpoint)

Another option It would be to add into appLocal.properties
tools.service.client.base-url = http://localhost:9998
build and run.