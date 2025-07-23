- **POST /api/v1/auth/api/token**
  - Special token obtain endpoint for API Gateway (see Checkpoint API - Integration with API Gateway), so DevOps could whitelist it only for the gateway use.
  - Sample request
    ```
    POST /api/v1/auth/api/token HTTP/1.1
    Host: https://cp-dev-services.tr-tax-cp-preprod.aws-int.thomsonreuters.com
    Content-Type: application/x-www-form-urlencoded
    grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer&assertion=<encoded assertion token>
    ```


- **POST /api/v1/auth/token**
  - Token obtain endpoint.
  - Sample request for Client Credential Grant-
    
    ```
    POST /api/v1/auth/token HTTP/1.1
    Host: https://cp-dev-services.tr-tax-cp-preprod.aws-int.thomsonreuters.com
    Content-Type: application/x-www-form-urlencoded
    grant_type=client_credentials&client_id=99deb97e00177c8293074f2d37f17ea5.dev.cp-news- 
    service&client_secret=**
    ```


- **GET /api/v1/auth/authorize**
  - Authorize endpoint. This is the entry point for [Auth Code Grant](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/919/Checkpoint-OAuth-Flows). If request doesn't possess valid Remember-me cookie, the endpoint always redirects to configured Login page (currently, it is a built-in login page). During redirect, the given parameters are encoded in "auth_target_path" parameter to maintain initial state.
This is done to keep Auth server stateless. The default Spring Security implementation creates HTTP session when redirecting to Login page. This is not too bad, but still we would want to keep the server stateless as much as possible. Current redirect implementation keeps initial request's state in query param, and Auth server does not create session at any request at any time.
  - Sample request-

    ```
    GET /api/v1/auth/authorize?response_type=code&client_id=cp- 
    spa&redirect_uri=https://dev.checkpoint.thomsonreuters.com/app/edge/ HTTP/1.1
    Host: https://cp-dev-services.tr-tax-cp-preprod.aws-int.thomsonreuters.com
    ```


- **POST /api/v1/auth/token/validate**
  - Token validation endpoint for those resources that cannot validate JWT signature. The only param is "token".
- **GET /api/v1/auth/keys**
  - Lists current public keys, aka Well Known JSON Web Key Set.
  - See Keys rotation for details.
- **GET /api/v1/auth/login**
  - Auth server's built-in login page for Auth Code Grant. 
Accepts query param "auth_target_path", which is propagated back to authorization endpoint on submitting the login form.
  - Sample request:

    ```
    GET /api/v1/auth/login?&auth_target_path=/api/v1/auth/authorize?response_type=code%26client_id=cp- 
    spa%26redirect_uri=https://dev.checkpoint.thomsonreuters.com/app/edge/ HTTP/1.1
    Host: https://cp-dev-services.tr-tax-cp-preprod.aws-int.thomsonreuters.com
    ```


- **POST /api/v1/auth/login**
  - Login processing endpoint. This is the URL login page must be submitted to.
After successful authentication, the request is forwarded to URL from "auth_target_path" param. This could be either /authorize or /ssoAccountLinking.
If authentication fails, the request is redirected back to configured login page with "error" param.
  - Sample request-

    ```
    POST /api/v1/auth/login HTTP/1.1
    Host: https://cp-dev-services.tr-tax-cp-preprod.aws-int.thomsonreuters.com
    Content-Type: application/x-www-form-urlencoded
    username=mikhail.chen-len-son&password=**&auth_target_path=/api/v1/auth/authorize? 
    response_type=code%26client_id=cp-spa%26redirect_uri=https://dev.checkpoint.thomsonreuters.com/app/edge/
    ```


- **POST /api/v1/auth/logout**
  - This is intended to be used by UI in Auth Code Grant Flow and Web App Experimental integration enabled.
  - Invalidates HTTP session at Checkpoint Web App if corresponding cookie is provided.
- **GET /api/v1/auth/entitlements/***
  - Entitlements endpoints providing subscriptions assigned to users.
  - See [Checkpoint Access Control (Subscriptions)](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/926/Checkpoint-Access-Control-(Subscriptions)).
- **POST /api/v1/auth/ssoAccountLinking**
  - SSO account linking endpoint. Establishes relation between Checkpoint user and external identity at Ping Federate.
    1. The flow is initiated on Ping's side.
    1. When the external user's context is retrieved, Ping is expected to call /ssoAccountLinking endpoint.
    1. Since account linking endpoint requires full authentication (just like /authorize endpoint), it will redirect user to the login page.
    1. After successful authentication, the request is forwarded back to account linking endpoint.
    1. The service encodes Checkpoint user identifier in a token for Ping Federate and redirects to Ping to resume the process on their side.
  - See Account linking related login types in [Checkpoint Login types](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/925/Checkpoint-Login-types).