If Internal users try to login Checkpoint application (Any environment) but it is guiding, you to CPREG URL then please follow the below process.

![image.png](/.attachments/image-112f7b29-31a1-4c81-91a3-9761630624db.png)

Use the below URL, you will get IP address 
URL - https://cpreg.environment.thomsonreuters.com/#/checkip (CI, Demo and QED)

 ![image.png](/.attachments/image-ad58d11e-9db1-44bc-9268-920dd66b5a44.png)

Login to CUAS application with Network credentials

In search bar enter the IP address and, in the dropdown select “IP Address” and click on search on Tab.

 ![image.png](/.attachments/image-341b2a47-59c1-4b12-a2b3-70ead5478b9f.png)

Search results display the information of Account in which your IP Address is added.

Click on the Unit Number- it displays the information of all the users in that account.

On the Top right you will find Show more (3 dots). Click on show more and select “Configure SSO”

 ![image.png](/.attachments/image-9ea274d4-36f5-44e0-8d7d-81e63abb35eb.png)

Now you will find “IP Address” Tab Click on that it displays the list of IP address.

 ![image.png](/.attachments/image-40d7022b-c4e9-494d-924f-c08dc3d16cc1.png)

Now select your IP address by check box now Delete IP Address will be highlighted. 

Click on Delete IP address Tab and then a pop displays to Acknowledge and then click on Delete. Now your IP address will not show in that list of IP address.

Once the above process is completed, we need to refresh the Transparent IP address in the CUAS Admin portal. 
Note:- IP Address will get auto refreshed, but that will take some time. So below are the steps to manually refresh IP address through Admin portal. By following these steps issue will be resolved instantly.

Use the below link to access Admin portal 
URL - https://environment.checkpoint.thomsonreuters.com/app/admin  (Dev, QA and Preprod)

Use your network credentials to login Admin portal.

 ![image.png](/.attachments/image-f24b2b92-db2b-4799-be3b-66713e25d982.png)
 

Server Admin  This Server  Update Server Data  Goto Updated Menu  View/ Reload Misc  View and reload Transparent IP account.

Now its displays all IP address 

Click on reload IP account which is on the Top left.

By doing this process your IP will be removed from Portal.

Now please try to open Check Point application, the issue will be resolved, and this will land in CP login screen.
