# Objective
This is a copied and enhanced list from CP Wiki page.

It describes the existing login types on Checkpoint Web App and how they are covered by Checkpoint Auth Service.

 

# Login types

```
Some login types are not supported in Checkpoint Auth service.

It doesn't mean they cannot/wouldn't be supported with Auth service in place. It means Checkpoint Web App will have to cover it.

However, if we assume we need to migrate to SPA/PWA and remove the Web App, it will become an issue.
```



```
All the below mappings of login types to Auth service are applicable to Authorization Code Grant only because it's the only supported grant flow that actually initiates authentication.


See details on flow: Checkpoint OAuth Flows 

See details on authentication: Checkpoint OAuth - Authentication
```
 

|Login Type| Description from CP Wiki | In Checkpoint Auth service |
|--|--|--|
|Normal   | User enters user name and password on login screen. Screen is posted using https to server.  | Covered by authentication during Authorization Code Grant. |
|Normal - Cookie  |User previously entered user name and password and checked the “Save Name/Password” checkbox. The web app sets a “secure” cookie with the username and password on a login path. And Sets another cookie on the main path indicating there is a cookie on the login path so the server will redirect to it in the future.  |Auth service supports this in a similar way -- a remember-me cookie is issued if user checked the checkbox during log in. Next time, when the user is back to Checkpoint and is redirected to /authorize endpoint, the cookie is passed along with request and the request is authorized immediately, without prompting user's credentials. |
|Registration/Seamless  | Check IP address at login if no cookie or user name and password. If IP matches one in list, redirect the user to CUAS registration server for their account. User registers and is sent an email with a new or existing CP User id and password. With a successful login, the web app saves user id and password in a cookie.  | Not supported. |
|Walkin user   | User clicks on an URL provided by the School/University that contains a location id. The web app checks if the location id matches the IP addresses in the list for it. If it does the user is given an user from a pool of users. For these users there is no persistent data saved like options, history or folder information | Not supported. |
|Speedlink   | Speedlink provides you with access to key features of Checkpoint® in one easy to use tool. It makes searching for information faster by bypassing the need to log in each time you want to perform a search or move to a related area. Speedlink resides in your desktop System Tray for convenient access. | Not supported. |
| Corporate Token Authentication  | Customer installs creates a component on one of their corporate servers that is accessed by users for a link to Checkpoint. The user clicks on a link in their Intranet which calls their component. Their component calls a CUAS authentication service with its user id. The service validates the IP address is in the list for the requester. The auth service looks up for an existing user for the id, if not there allocates one from an existing pool and assigns the user to it. The auth service then responds with an URL to Checkpoint that includes a temporary token. The corporate server redirects the user to the Checkpoint URL. Checkpoint validates the token is still valid and logs the user in. Optionally setting a cookie for few hours or days.  | Not supported. |
| 3rd Party Software Authentication  |Software is registered for that registration service and a pool of users with their products are created. The software is provided with a token to include in a header to call to the registration service. The service validates the token and selects a user from the pool and creates a token for login the user into CP.  | Not supported. |
|Client Network SSO using Ping Federate Account Mapping  | Customer uses a SAML connection to redirect to the TRTA PingFederate service and pass along their client network user id. PingFederate validates the customer is who they say they are and redirects the request to Checkpoint. Checkpoint queries the database for a CP user mapped to the client network user id and logs in the user. If the user does not exist, the CP Registration service is called to create the user. | Covered during authorization request in Auth Code grant. The /authorize endpoint supports SSO opentoken. The identity is extracted from the token and exchanged for Checkpoint's identity. Replicated tables USER_CLIENT_INFO and ACCOUNT_AUTH_TYPE are used. **Note:** the SSO integration has not been promoted to production. However, this should only be a configuration change |
|Client Network SSO using Ping Federate Account Linking   | (As of April 2013 this is not being used yet)...Customer uses a SAML connection to redirect to the TRTA PingFederate service and pass along their client network user id. Ping checks to see if there is an existing account link between the client network id and Checkpoint; if not it redirects to the Checkpoint account link page. The user enters their Checkpoint credentials and Checkpoint redirects back to Ping. From then on, whenever that user tries to log in again, Ping will look up the account link information and pass the Checkpoint credentials on to Checkpoint via a redirect.  | Covered during authorization request in Auth Code grant. The /authorize endpoint supports SSO opentoken. The Checkpoint's identity is extracted from the token. The account linking is supported at /ssoAccountLinking with the same interface. **Note:** the SSO integration has not been promoted to production. However, this should only be a configuration change. |
| Application SSO using Ping Federate Account Mapping |Customer's credentials are passed via PingFederate and browser redirects from another TRTA application and used directly to log the user into Checkpoint.   |Covered during authorization request in Auth Code grant. The /authorize endpoint supports SSO opentoken. The identity is extracted from the token and exchanged for Checkpoint's identity. Replicated tables USER_CLIENT_INFO and ACCOUNT_AUTH_TYPE are used. **Note:** the SSO integration has not been promoted to production. However, this should only be a configuration change.  |
| Application SSO using Ping Federate Account Linking  | Customer's credentials are passed to PingFederate using a browser redirects from another TRTA application (source). Ping checks to see if there is an existing account link between the source application and Checkpoint; if not it redirects to the Checkpoint account link page. The user enters their Checkpoint credentials and Checkpoint redirects back to Ping. From then on, whenever that user tries to log in again, Ping will look up the account link information and pass the Checkpoint credentials on to Checkpoint via a redirect. |Covered during authorization request in Auth Code grant. The /authorize endpoint supports SSO opentoken. The Checkpoint's identity is extracted from the token. The account linking is supported at /ssoAccountLinking with the same interface. **Note:** the SSO integration has not been promoted to production. However, this should only be a configuration change.  |
| API Gateway connection  | -- |See detailed description on Checkpoint API - Integration with API Gateway  |




