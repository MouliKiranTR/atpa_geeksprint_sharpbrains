[User Story 167416](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_workitems/edit/167416): [Discovery] Spike - Manually Passing Auth Token in Postman.

*Author:* @<DE58388A-475B-68F7-A222-1DD0000B6525> 
___

In order to call API endpoints in cp-webapp you need to provide a cookie which includes an authentication token. This can be retrieved from any valid session to Checkpoint. Steps for retrieving and using to make requests:

1. Sign into Checkpoint web application ([https://checkpoint.ci.thomsonreuters.com/](https://checkpoint.ci.thomsonreuters.com/))
2. Open developer tools in your browser
3. Perform any action that makes a request to app/api/
   - Example: navigate to the AI Assistant, enter a query, and hit search
4. Find the request in developer tools network tab
   - Example: there should be a start POST request visible to app/api/aiAssistant/v5/conversation/start
5. Under the request, select the "Headers" tab and find "Cookie" value under "Request Headers" section
   - ![Image](https://dev.azure.com/tr-tax-checkpoint/c60acdc5-4ee0-4039-9a00-61975bbd5dfe/_apis/wit/attachments/2db6c24c-b78e-4d02-ab2a-16b6bf6a640f?fileName=image.png)  
6. You can then use this "cookie" value in Postman like so:
   - ![Image](https://dev.azure.com/tr-tax-checkpoint/c60acdc5-4ee0-4039-9a00-61975bbd5dfe/_apis/wit/attachments/bc00080b-5633-4de6-84ac-736365f3c13e?fileName=image.png)

If desired, you can add the cookie value to the variables for your collection so its re-used across all requests in that collection.