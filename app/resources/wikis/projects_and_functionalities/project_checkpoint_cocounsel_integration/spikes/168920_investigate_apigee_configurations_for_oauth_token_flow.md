[User Story 168920](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_workitems/edit/168920): [Authentication] SPIKE #2 – Investigate Apigee Configurations for OAuth Token Flow

*Author:* @<DE58388A-475B-68F7-A222-1DD0000B6525> 

[[_TOC_]]

___

## References and Resources
- [Lucid chart on AI Assistant ("Auth" tab)](https://lucid.app/lucidchart/ab069a25-3b5c-4625-bd32-3a2bae9d6c8e/edit?invitationId=inv_14b42940-c74a-4df1-9215-aeba9cb235c7&page=mQsi-~FgsXEm#)
- [Lucid chart on CP Search API](https://lucid.app/lucidchart/b878afd7-f13c-4c21-939b-ee278f02b993/edit?invitationId=inv_90ba6fdf-ceb6-48f8-8f2e-d804da53a460&page=yZA9au-ejUWY#)
- [CP Wiki - Integration with API Gateway](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/928/Checkpoint-API-Integration-with-API-Gateway)
- [Checkpoint Edge Search API Authentication Documentation](https://developers.thomsonreuters.com/pages/api-catalog/f0ffe0b4-899e-455f-af3b-73e554cb5f10#Authentication)
- [Atrium Page on Apigee API Gateway Onboarding](https://trten.sharepoint.com/sites/Platform-API/SitePages/Apigee-API-Gateway-%26-Automation.aspx)
- [How to get Access to Apigee](https://trten.sharepoint.com/sites/Platform-API/SitePages/How-to-get-Access-to-Apigee-.aspx)
- CP Auth Service API Swagger Documentation
  - [DEV/CI](https://cp-dev-services.tr-tax-cp-preprod.aws-int.thomsonreuters.com/api/docs/auth/swagger-ui/index.html#)
  - [TEST/DEMO](https://cp-test-services.tr-tax-cp-preprod.aws-int.thomsonreuters.com/api/docs/auth/swagger-ui/index.html)
  - [QED/PreProd](https://cp-qed-services.tr-tax-cp-preprod.aws-int.thomsonreuters.com/api/docs/auth/swagger-ui/index.html)
- [Checkpoint Auth Service GitHub repo](https://github.com/tr/cp_auth-service)

---
## Apigee
- See Wiki page [Apigee API Gateway](/Projects-and-Functionalities/Apigee-API-Gateway) for more details

### Checkpoint Authorization Proxy
- **_Links to Proxy configuration in Apigee:_**
  - [Non-prod](https://thomson-reuters-nonprod.apigee.com/platform/tr-api-cloud-qa/proxies/a200172-Checkpoint-Authorization/overview/14)
  - [PROD](https://thomson-reuters.apigee.com/platform/tr-api-cloud/proxies/Checkpoint-Authorization/overview/6)
- **_Deployments:_**
  - These are all of the configured deployments/URI's, requests to these will be routed to Apigee and then to the Checkpoint Authorization API Proxy
  - **dev**
    - http://tr-api-cloud-qa-dev.apigee.net/checkpoint/oauth2
    - https://api-dev.thomsonreuters.com/checkpoint/oauth2
    - https://api-dev.int.thomsonreuters.com/checkpoint/oauth2
  - **test**
    - http://tr-api-cloud-qa-test.apigee.net/checkpoint/oauth2
    - https://api-test.thomsonreuters.com/checkpoint/oauth2
    - https://api-test.int.thomsonreuters.com/checkpoint/oauth2
  - **uat (prod account)**
    - http://tr-api-cloud-uat.apigee.net/checkpoint/oauth2
    - https://api-uat.thomsonreuters.com/checkpoint/oauth2
    - [https://api-uat.int.thomsonreuters.com/checkpoint/oauth2](https://api-uat.int.thomsonreuters.com/checkpoint/oauth2)
  - **trinternal prod (prod account)**
    - https://empty.thomsonreuters.com/checkpoint/oauth2
    - https://empty.thomsonreuters.com/checkpoint/oauth2
    - https://api.int.thomsonreuters.com/checkpoint/oauth2
  - **trexternal prod (prod account)**
    - http://tr-api-cloud-trexternal.apigee.net/checkpoint/oauth2
    - https://api.thomsonreuters.com/checkpoint/oauth2
    - https://empty.thomsonreuters.com/checkpoint/oauth2
- _**Proxy Endpoint:**_
  - There is one endpoint configured for the Checkpoint Authorization proxy
  - `/checkpoint/oauth2/token`
- _**Policies:**_
  - In Apigee, policies are modules that provide common API management functionalities
  - They are used to control and manage the behavior of APIs
  - Policies can be easily applied to API proxies to handle various aspects like security, traffic management, transformation, etc.
  - **`SC-GetCheckpointToken`**
    - This policy is responsible for obtaining a Checkpoint Token
    - Does this by making a POST request to `/api/v1/auth/api/token` in `CheckpointAuth` server
    - The `CheckpointAuth` server is defined in the "Target Servers" page, see [here](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/988/Apigee-API-Gateway?anchor=the-**target-servers**-page) for more details on how this is setup
    - Target Servers - CheckpointAuth
      - dev (non-prod account): not set
      - test (non-prod account): test-checkpoint.5463.aws.thomsonreuters.com
      - uat (prod account): qed-checkpoint.5463.aws.thomsonreuters.com
      - trinternal prod (prod account): checkpoint.1434.aws.thomsonreuters.com
      - trexternal prod (prod account): checkpoint.1434.aws.thomsonreuters.com
    - ![image.png](/.attachments/image-b3161479-2353-4b40-a0cf-00488ab1960d.png)
  - **`JWT-GenerateAuthBearer`**
    - This policy generates a JWT bearer token and stores in output variable `public.security-serice-jwt` which is passed to the Auth Service token endpoint in the above `SC-GetCheckpointToken` policy
    - ![image.png](/.attachments/image-d952f6ee-42e5-4fda-8b2e-ee06f1b51b67.png)
- _**Secrets:**_
  - Secrets for this proxy are stored in the "Key value maps" page
  - See [this page](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/988/Apigee-API-Gateway?anchor=the-**key-value-maps**-page) for more information
  - In the case for the Checkpoint Authorization proxy, there is key value map "auth-checkpoint" which contains the `audience`, `client_id`, and `private_key` values used by the policies when generating a token
  - ![image.png](/.attachments/image-0397a51d-9c46-4c38-835e-56c35c5a7f3e.png)

---
## Flow for Creating an API User
- See [Lucid chart on AI Assistant ("Auth" tab)](https://lucid.app/lucidchart/ab069a25-3b5c-4625-bd32-3a2bae9d6c8e/edit?invitationId=inv_14b42940-c74a-4df1-9215-aeba9cb235c7&page=mQsi-~FgsXEm) for visual representation of this flow
- See [report for SPIKE #168919](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/967/168919-Investigate-API-User-Setup-and-Entitlements-Flow) for more details on the API user setup and entitlements flow

### Prerequisites:
1. An API user setup with entitlements created in CUAS for the customer (these are the entitlements that will be used by the search API)
2. When this is setup in CUAS it calls Apigee to create a Client Company and Client App.
    - These get custom values assigned to them
      - Customer Account ID
      - API User ID
3. These are then displayed in the developer portal.
    - The dev portal is just a public UI for Apigee configuration data.

### Auth Flow:
1. Auth Call
      1. Client calls the Auth endpoint specified in our Apigee configuration.
         1. This endpoint accepts a client key and client secret.
      2. Apigee then takes custom values from the Dev Portal and makes an auth request to the CP Auth Service
          1. The values that are pulled from the Dev Portal are:
             1. Customer Account ID
             2. API User ID
          2. This returns a CPAuthToken for this customer and user ID
      3. Apigee stores the CPAuthToken in cache.
      4. Apigee returns a ClientToken (not the CPAuthToken). This value maps to the CPAuthToken
          1. The ClientToken is the key
          2. The CPAuthToken is the value
2. Search Call
    1. Client takes the ClientToken and puts it into the authorization header
    2. Client makes a call to the CP Search Service
    3. The request hits Apigee
    4. Apigee looks at the ClientToken and checks if it is expired
    5. Apigee exchanges the ClientToken for the CPAuthToken
    6. The request is sent to the CP Search Service
    7. The CP Search Service then validates the CPAuthToken
       1. I believe this is done through the Auth Client Lib
    8. The CP Search Service then gets the entitlements of the API User
    9. Then CP Search Service then calls the WebApp using the CPAuthToken as an authorization header.
    10. The WebApp endpoint validates the CPAuthToken
    11. The WebApp processes the request.
    12. WebApp returns result to CP Search Service
    13. CP Search Service returns to Apigee
    14. Apigee returns to the Client.

---
## CP Auth Service
- CP Auth Service GitHub repo: https://github.com/tr/cp_auth-service
- The controller `ApiTokenController` extends `org.springframework.security.oauth2.provider.endpoint.TokenEndpoint`
  - All logic contained in `TokenEndpoint.class` is from the `spring-security-oauth2` library
- `ApiTokenController` contains two endpoints:
	- GET `/api/v1/auth/api/token`
	- POST `/api/v1/auth/api/token`
	- The GET and POST both end up calling `org.springframework.security.oauth2.provider.endpoint.TokenEndpoint#postAccessToken`
- `postAccessToken` method takes in principal and map of parameters
	- `principal` is derived from the `Authorization` header containing the Bearer token
		- `java.security.Principal` is an interface, and in this case `principal` variable is instance of `org.springframework.security.core.Authentication` interface
		- `principal` is used to extract the client ID (which is set in Apigee to value of `private.checkpoint-client-id`)
	- `parameters` are populated from the payload of the request from Apigee
		- Apigee payload:
			- **Key**: `grant_type`
			- **Value**: `urn:ietf:params:oauth:grant-type:jwt-bearer`
	- The method checks `principal` is of type `Authentication` and verifies the client id, validates the scope, checks the grants, and generates a token
- Description of the `ApiTokenController` class:
  - Dedicated token obtaining endpoint specially for API Gateway.
  - To successfully obtain a token caller must:
     - Provide JWT token (token is expected in standard request header ("Bearer"). Parameter is not supported).
     - Token must be signed and the signature must verifiable with public key stored in Auth service.
     - Token must have expiration date.
     - Token must have client ID. Now, only API Gateway is allowed to obtain tokens through this endpoint.
   - Sample token payload:
		```Json
		{
		  "TR_CHECKPOINT_SERVICE_ACCOUNT_ID": "112233",
		  "TR_CHECKPOINT_ACCOUNT_ID": "1700",
		  "exp": 10000000000,
		  "client_id": "api-gateway",
		  "scope": ["trust"]
		}
		```
---
## Summary of Findings
- In Apigee, the API Proxy a200172-Checkpoint-Authorization is setup and mapped to endpoint `/checkpoint/oauth2/token`
- In this proxy configuration, there are policies for the following:
    - `JWT-GenerateAuthBearer` - uses the private key, subject, issues, audience, and claims to generate a JWT token
    - `SC-GetCheckpointToken` - makes POST request to `/api/v1/auth/api/token` passing in the JWT token as Bearer in the Authorization header
- The `/api/v1/auth/api/token` endpoint in the CP Authorization issues an OAuth 2.0 access token. It checks whether the client is authorized to request a token, validates the scope, and ensures that the grant type is supported. It does not perform any Authentication.

