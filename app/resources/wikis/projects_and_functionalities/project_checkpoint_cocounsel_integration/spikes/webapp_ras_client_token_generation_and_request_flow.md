[User Story 168652](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_workitems/edit/168652): [Authentication] SPIKE #4 – Investigate CP WebApp RAS Client Token Generation and Request Flow

*Author:* @<5D859739-32D0-62AD-8D9B-670A89B07CEA> 

[[_TOC_]]
___

## The token generation in the RAS client
The Checkpoint application get access token with  grant type: `client_credentials`
Once the service user is created, it will be associated with a `client_id` and `client_secret`. These credentials can be used to generate a JWT token using the Entitlement POST API.
[Global Content Services Swagger UI](https://entitlement-qa.gcs.int.thomsonreuters.com/swagger-ui/index.html#/)
### Entitlement POST API
- **Method**: POST
- URL
  - [entitlement-qa (all non-prod)](https://entitlement-qa.gcs.int.thomsonreuters.com/v1/token)
  - [entitlement-prod](https://entitlement.gcs.thomsonreuters.com/v1/token)

The request body should be in `x-www-form-urlencoded` format and include the following information:
- `client_id`: Your service user's client ID.
- `client_secret`: Your service user's client secret.
- `grant_type`: `client_credentials`

As per RAS standards, only authorized users can access any endpoint. To implement authorization in the server-side code, use one of the following libraries:
- **GCS Authorization Library** (for cp web app):
  - Maven dependency: `com.tr.gcs:gcs-authorization:xx.xx.xx-RELEASE`
- **CARS Dynamic Authorization Library** (for microservice):
  - Maven dependency: `com.tr.da:cars_dynamicauthorization-java`

### Authorization Headers
To access the APIs, the user should pass the correct JWT token in the authorization header. Here is an example of how to include the JWT token in the request headers:
- Authorization: Bearer <your_jwt_token>
- **Expiration**: Expiration time of token 30 minutes.

### How to get a GCS Token manually
You can use your GCS Token for calls in other tools (Developer Portal, Postman, etc) that requires GCS authentication.
- Login to the QA or Prod content console
  - [QA](https://contentconsole-qa.int.thomsonreuters.com/)
  - [Prod ](https://contentconsole.thomsonreuters.com/)
- Go to the Chrome developer tools in your browser.
  - For chrome: right click > click inspect > Find the Application tab on top of the Console menu > On the left In Storage, expand Local Storage > click on the Content Console URL.
![image.png](/.attachments/image-ba58502e-581a-4c5e-b7ce-e3ea7298fd24.png)
- Find the AccessToken Key and copy the value. This is your GCS Token (without the quotes)

---
## The RAS token contains properties
The [GCS (Global Content Services) application](https://github.com/tr/gcs-access-management_entitlement-service/blob/f492c2b8fe19458b93c9cab1ce4e0bb22bb7c1f6/src/main/groovy/com/tr/gcs/entitlement/token/OauthAccessTokenResponseView.groovy) returns a token object with the following fields.
The [Oauth 2 Access Token response](https://www.oauth.com/oauth2-servers/access-tokens/access-token-response/)
- `access_token` (required) The access token string as issued by the authorization server.
- `token_type` (required `Bearer`) The type of token this is, typically just the string “Bearer”.
- `expires_in` (recommended) If the access token expires, the server should reply with the duration of time the access token is granted for.
- `refresh_token` (optional) If the access token will expire, then it is useful to return a refresh token which applications can use to obtain another access token. However, tokens issued with the implicit grant cannot be issued a refresh token.
- `scope` (optional) If the scope the user granted is identical to the scope the app requested, this parameter is optional. If the granted scope is different from the requested scope, such as if the user modified the scope, then this parameter is required.

---

##  The RAS request flow for CIAM and non-CIAM users
It depends on the `grant type` passed in the request body to [Global Content Services](https://github.com/tr/gcs-access-management_entitlement-service/blob/f492c2b8fe19458b93c9cab1ce4e0bb22bb7c1f6/src/main/groovy/com/tr/gcs/entitlement/token/TokenController.groovy#L62)
### For a CIAM user
- [client_credentials](https://www.oauth.com/oauth2-servers/access-tokens/client-credentials/)
see The RAS token contains properties
### For a non-CIAM user
- Raising a Request for Service User Creation or Update
  - [Raise a Request](https://contentconsole.thomsonreuters.com/access-management/requests): Use the request portal 
to create or update a service user.,
  - Defining the Request:
    - Title: Provide a clear and concise title for your request.
    - Purpose: Define the purpose of the service user. Clearly state the requirement and the specific rights needed for the service user.
    - [example](https://contentconsole.thomsonreuters.com/access-management/requests/3486)
  - Submit the Request:
    - After filling in the required information, submit the request.
    - The team will create or update the service user with the correct rights.
  - Validation and Confirmation:
    - Once the service user is created or updated, you will need to validate and confirm the details.
    - After validation, the team will close the raised request.
- [authorization_code](https://www.oauth.com/oauth2-servers/access-tokens/authorization-code-request/)
  - `grant_type`(required) parameter must be set to “authorization_code”.
  - `code`(required) This parameter is the authorization code that the client previously received from the authorization server.
  - `redirect_uri` (possibly required) If the redirect URI was included in the initial authorization request, the service must require it in the token request as well. The redirect URI in the token request must be an exact match of the redirect URI that was used when generating the authorization code. The service must reject the request otherwise.
  - `code_verifier` (required for PKCE support) If the client included a `code_challenge` parameter in the initial authorization request, it must now prove it has the secret used to generate the hash by sending it in the POST request. This is the plaintext string that was used to calculate the hash that was previously sent in the `code_challenge` parameter.
  - `client_id`(required if no other client authentication is present) If the client is authenticating via HTTP Basic Auth or some other method, then this parameter is not required. Otherwise, this parameter is required.

### CIAM user is sent to RAS in the request
- The Checkpoint application uses Grant Type: `Client_credentials` for get access token from GCS service.
The Client Credentials grant is used when applications request an access token to access their own resources, not on behalf of a user.
 ```curl --location 'https://entitlement-qa.gcs.int.thomsonreuters.com/v1/token' \
      --header 'Content-Type: application/x-www-form-urlencoded' \
      --data-urlencode 'grant_type=client_credentials' \
      --data-urlencode 'client_id={replace the client id}' \
      --data-urlencode 'client_secret={replace client secret}'


