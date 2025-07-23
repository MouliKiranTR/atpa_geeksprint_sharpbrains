**Prerequisites**

Please check out this article [OAuth, OIDC, Authentication and Authorization](https://dev.to/engincanv/what-are-oauth-2-0-and-oidc-openid-connect-with-endpoints-25kd) for better understanding of OAuth principles.

And just to remind:


```
In OAuth and OIDC, the initiator is always makes an authorization request.

As part of the authorization request in OIDC only, the initiator may additionally ask for authentication information to be conveyed in the authorization response.

There is no authentication request defined in either OAuth or OIDC.
```

**Authentication and Identities**

Despite the fact that OAuth is NOT about authentication, the Checkpoint Auth service does provide AuthN capabilities-

- User authentication via Form login
  - If request to /authorize endpoint doesn't posses Remember-me cookie, the server initiates authentication request and redirects user to Login page (currently configured to use static page served by Checkpoint Auth at /login).
  - User's password is checked against the database (BCrypt encryption is used) with a help of cp-password lib to stay consistent with Checkpoint Web App.
- Client authentication (when applicable)
  - Usually, every time a token is requested by an OAuth Client, that client's identity must be validated, therefore, client's secret is also required.
  - However, there are two exceptional cases:
    - Public clients (aka browser-based applications) can't store secrets securely, hence, should not pass it during the token request. See [Section 9.2](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-browser-based-apps-00#section-9.2) of OAuth specification for details.
    - Trusted clients that are utilizing other trust relationship (signature validation supported). Since assertion token is required in this flow, we validate the client's identity by validating the assertion token.
 

**User identities management**

Users identities are managed via CUAS application and are available in a shared Checkpoint Oracle database.
To maintain bounded context in Auth service, AWS Database Migration Service was set up. All auth related tables are continuously replicated to Auth database.

 

Replicated tables related to identification/authentication-


```
ACCOUNT

RIA_USER

USER_ADMIN
```


Replicated tables related to subscriptions-

A_PACKAGE


```
ODS

OFS

ODS_PACKAGE

OFS_PACKAGE

ODS_AVAILABILITY

OFS_AVAILABILITY

A_ORDER

USER_ORDER
```


Replicated tables related to SSO-


```
USER_CLIENT_INFO

ACCOUNT_AUTH_TYPE
```


**Client identities management**

All client identities are managed via externalized configuration at https://github.com/tr/cp_config-server/tree/main/cp-auth-service (property security.oauth2.default-clients).

Clients details are loaded from configuration during Auth service startup and are stored in-memory by default.

By setting security.oauth2.clients-store=jdbc you can enable storing the data in database (currently enabled on DEV), so it could be managed from outside of the service.


```
Alternatively, we could wipe out the client details from the configuration and only manage client details through DB storage on all environments (clients' secrets are encrypted with BCrypt, so you would still be able to manage it securely).

 
However, I couldn't find an elegant way to promote new clients to production without having a direct access to production database cause client details should be environment specific.
```

