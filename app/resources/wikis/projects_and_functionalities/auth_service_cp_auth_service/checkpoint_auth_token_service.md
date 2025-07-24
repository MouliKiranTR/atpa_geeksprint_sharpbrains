## Purpose
Creates a authToken for login to checkpoint when given username and password.

This service is being used by Speedlink and Hofbrau as of 1/25/2017.

## Request

POST app/rest/authToken
## Request: Entity Body

Content-Type: application/x-www-form-urlencoded

username=LKondragunta&password=password

## Response: Status Codes



| Code |Meaning  | Returned When |
|--|--|--|
| 401 | Unauthorized |The resource could not be created because the client submitting the request either has not provided authentication credentials, or authentication failed (e.g. due to an invalid username or password) after such credentials were provided.  |
| 500 | Internal Server Error | A service error prevented the resource from being created. |


## Response: Content-Type
application/json

## Response: Entity Body (on Success)
"A VERY LONG STRING TO BE USED AS TOKEN TO LOGIN TO CHECKPOINT"

## Response: Entity Body (on Error)
Invalid Login

 

Once we get the authToken, we can use it on urls like this-

**/app/goto?checkpointAuthToken=</value>** 