# How to set up Shared Folders on cp-web-app project?
- Configure cp-web-app:
  1. Go to **appDev.properties**, search for _akkadia.service.client.base-url_ and _akkadia.service.apikey.encrypted_ and assign these values: 
     - https://a205159-akkadia-ci-use1.tr-tax-cp-preprod.aws-int.thomsonreuters.com
     - "QTY+JqXOvHbNppG33rcZCP5dIp0vMK3dpEyMDD33U2WrGAkEZjDUBh91AMZcjq5WvOlGpluQv/ge1u8GnZMzW5H2bexczaLr6FPz18rH3tBI3uz6+uDA4d7fs9Nxqo9w7Qp22vWbbnd5mK5h5xjVAWhkJtKJA1+ebZsJEWfWcRK4SqeGnPRQrSxaIZt4rRhAL96Vm42ihO7vd1B4LO3Oa8H+hF+FuKWg01H+dOwEX3FEoEZj1ie5bRM++gmHORVdmhpSHY1vbj8H3yClVwRwMeSQz8hvqp93ylzFW3dicF3cTm1ik+68YfCa18AmTVOi/kXJtJsR+TY/PK5Go84X3Pp4ENJPEprs0OeE6xeyUdg="
![image.png](/.attachments/image-2206b2c6-6afe-4f4f-8d2b-ae5d4db7e3f8.png)

  2. Go to **CPAkkadiaClient.java** and change the following lines code:
     - Method _createFolders_, line 380. Set the version value to 3.
![image.png](/.attachments/image-334ee954-30b2-49c1-a6c8-39995eb8eefb.png)

     -  Method _getFolders_, line 430. Set the version value to 5.
![image.png](/.attachments/image-abfcba87-970c-47bc-a491-dc75fdf42bd7.png)

     - Method _getSharedFoldersItems_, line 448. Set the version value to 5.
![image.png](/.attachments/image-f8523d01-44d9-4966-8a19-b231b56e6f58.png)

     - Method _getSharedFoldersItemsCount_, line 751. Set the version value to 3.
![image.png](/.attachments/image-b8646146-3e35-4474-8d90-c6ce2337851f.png) 

  3. Go to **SharedFolderResponse.java**, after _applicationTags_. Add the next 2 lines:
       @ApiModelProperty("copyState")  
private String copyState;
![image.png](/.attachments/image-772ee42b-dacf-4f11-8881-8407b64c241f.png)

  With this changes, the Shared Folders section will appear:
![image.png](/.attachments/image-5b765a45-73b7-43d5-af1a-b450b2bc7637.png)

**Note**: Please be aware that this steps are to show the Shared Folders in localhost, actions like move, copy or delete can throw errors as the test of configuration is not finish yet.
