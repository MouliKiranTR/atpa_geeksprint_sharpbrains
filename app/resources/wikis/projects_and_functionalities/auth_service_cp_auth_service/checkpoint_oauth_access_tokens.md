

# Prerequisites
Here you can find a good explanation of the terms used below: [What is JWT, JWS, JWE, and JWK?](https://medium.com/@goynikhil/what-is-jwt-jws-jwe-and-jwk-when-we-should-use-which-token-in-our-business-applications-74ae91f7c96b)

 

# JWT vs Opaque
Whether you should validate access tokens locally (JWT is self-contained) or remotely (by calling validate endpoint) is a question of how much security you need.

The biggest downside to validating a token locally is that your token is, by definition, stale. It is a snapshot of the moment in time when Auth server generated the token.

The biggest benefit is that protected resources don't have to make an HTTP call to validate the token.

 

## Pros of JWT:

- Self-contained. Verification is stateless. No synchronous calls across services. Horizontal scaling is easier.
- No database table.
- Can trust Auth server (if not using dynamic token key obtaining).
 

## Cons of JWT:

- Becomes heavy if entitlements are added to payload (entitlements can take up to 150KB at the moment).
- Can't revoke token (force user logout). Must wait until it's expired. Refresh token is used as a trade-off.
- If payload contains sensitive data it can be exposed through headers logging.
- If Auth server's private key is compromised, the entire system is broken.
- As a mitigation for the point above, we must implement keys rotation (not a big deal actually if using JWKs).
- Can't see active sessions. Therefore, can't push messages to active users.
 

**It was decided to try living in two worlds**: use JWT for authentication and provide entitlements on demand with a dedicated endpoint.

`Before the decision was finalized, we tested both options. Opaque token strategy is still available at Auth service with a configuration property: security.oauth2.token-store. Supported values: jdbc, jwt.`

# Keys rotation
Like was said above, one of the cons of using JWT is that if a private key used to sign tokens is compromised, the entire system is broken. We need to be able to rotate the key and do it gracefully, without having to update all the protected resources. Regular key rotation can prevent the risk and if the risk has actually occurred we can rotate it immediately.

 

Here comes JWKs endpoint. It allows us sharing the public key with resource servers. Every time a resource server starts up it will load the current public key(s) from Auth server and then it will be using the given key(s) to validate tokens. If JWKs endpoint returns two public keys it means the key pair rotation is in progress.

The token's header contains the key identifier ("kid" claim), which must used by resource server to determine, which public key to use when validating it. 

 

Why we would want to return two keys? Why not just replacing old key with a new one?

Two reasons-

1. Although all new tokens are signed by the key from the newly added pair, there still could be a token issued before the rotation started, which is not expired yet and therefore should be validated properly.
1. Because we cannot guarantee that all instances of Auth server will be updated at a time. If one instance is not updated yet and is still returning the old key, then all instances must be also returning that key, so the resource servers could validate tokens properly.
 

You can find the JWKs endpoint at **/v1/auth/keys**.

 

The technology is quite mature. For example, Spring Security supports JWKs handling (on resource server side) out of the box with a little configuration.

 

If a resource server cannot handle JWKs handing, developers still can download the keys and manually add it to the service's configuration getting all the benefits of using JWT token verification strategy. However, they will have to keep in mind that they will also be responsible to update the configuration every time the key is rotated. Another option is to simply fall back to opaque token verification strategy and validate tokens via /v1/auth/token/validate endpoint (that is what is done NodeJS lambdas for simplicity).

 

# Overview of token flows in Checkpoint

![Token Flow.png](/.attachments/Token%20Flow-0b8a2cc7-41c3-4b6e-9130-7a2b9569c46a.png)
 

# CP-Auth-Client library
The library was created in order to simplify the process of onboarding a microservice to Checkpoint Auth.

It covers auto-configuration for token validating on protected endpoints.

Full documentation is available in its [README](https://github.com/tr/cp_auth-client/blob/main/README.md).