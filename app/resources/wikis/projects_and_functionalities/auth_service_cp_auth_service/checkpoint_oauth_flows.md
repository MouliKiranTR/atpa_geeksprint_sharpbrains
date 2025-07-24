Below we go through the flows that are effectively used in Checkpoint Auth service.

 

# JWT Profile Grant for Web App
**Consider use case:** Checkpoint Web App wants to obtain access tokens from Checkpoint Auth service.

**Problem:** user is already authenticated by the Web App and we don't want to prompt for their credentials once again.

**Solution:** Utilize JWT Bearer Authorization Grant ([RFC 7523](https://datatracker.ietf.org/doc/html/rfc7523))


```
Luckily we are, OAuth is all about delegation. It allows a client application to ask resource owner (a user) for permission to access a protected resource (an HTTP API) on their behalf. It is a delegation protocol.

How do we keep request acting on the user’s behalf? How do we do this securely without prompting the user's credentials?
```


From the specification, the JWT Bearer Authorization Grant is:



[A way for] a JWT Bearer Token can be used to request an access token when a client wishes to utilize an existing trust relationship, […] without a direct user-approval step at the authorization server.
[RFC 7523 - Section 1](https://datatracker.ietf.org/doc/html/rfc7523#section-1)



This authorization grant is most suited towards swapping tokens and assertions issued by a different authorization server/identity provider, for tokens issued by our authorization server (impersonation).

 

In this flow Auth service considers user pre-authenticated, therefore, only validates the user's status without checking credentials.

![JWT Profile Grant Flow.png](/.attachments/JWT%20Profile%20Grant%20Flow-009f2dd3-e9db-4173-b259-8413e27ee26c.png)

 

Checkpoint Auth authenticates this impersonate request by validating the assertion token (see [RFC 7523 - Section 2.1](https://datatracker.ietf.org/doc/html/rfc7523#section-2.1)).

**Assertion token**

```
{
  ..
  "aud": "b8a9abb6130d63a3066166c97d7363ef.test.cp-auth-service,
  "iss": "e5614b6f48a8daf4144763b3b0348903.test.cp-edge-ui,
  "sub": "4717969",
  ..
}
```

This is a sample assertion token payload (other typical non-relevant JWT claims are removed).

Here,

- Audience claim contains the integration key of Checkpoint Auth (also known as client ID),
- Issuer claim contains the integration key of Checkpoint Web App (also known as client ID),
- and Subject claim contains the Checkpoint User ID.
 

# JWT Profile Grant for API Gateway
Another case for use of JWT Profile Grant is integration with API Gateway-
![JWT Profile Grant Flow (API Gateway).png](/.attachments/JWT%20Profile%20Grant%20Flow%20(API%20Gateway)-17496f69-d6be-4396-9d12-8d62355a10f0.png)


Same situation: API Gateway already authenticated request and wants to obtain access token on behalf of the user.


 

# Client Credentials Grant
There are multiple cases when protected resource needs to be accessed without user's interaction (for example, by a scheduled job).


```
You need to understand that not every protected resource could be accessed without a user context.

Usually, a resource wants to inspect user's identity to understand their subscriptions and access level as to maintain row-level security.

 

So, the use of Client Credentials flow is quite limited and in each case we should have a specific endpoint, which is ensured not to inspect user info.

It is a good practice to protect this endpoint with a meaningful scope and grant your client access to this scope as to fail fast and properly if accidental call happens.
```


The flow is very simple:

![Client Credentials Flow.png](/.attachments/Client%20Credentials%20Flow-8bb578b5-d0e9-4cb9-aaaa-bda16ef06588.png)

Obtained access token in this flow is "client only token" -- it doesn't contain any user information.

 

# Authorization Code Grant (with Proof-Key for Code Exchange, or PKCE)
This is a preferred grant flow for Single Page Applications.

It is configured to be used by CP-Edge-UI but is not used effectively, however.


```
OAuth 2.1 makes PKCE required for Authorization Code Grant.

Currently, Checkpoint Auth service supports PKCE but doesn't enforces its use following OAuth 2.0 specification.
```


This flow is a bit complicated since it is a three legged redirect-based flow.

1. Client redirects user to /authorize endpoint (then user optionally authenticates)
1. Auth redirects back to client with Authorization Code.
1. Client obtains access token with the given Authorization Code.
 

The comprehensive sequence looks like this-

![Sequence Diagram.png](/.attachments/Sequence%20Diagram-09c9bee4-b469-418d-9080-5aba9bc3cced.png)

 

Access token obtain data flow diagram-

![Auth-Code-Grant-Flow.png](/.attachments/Auth-Code-Grant-Flow-5c1a81b2-bef4-4a93-a926-82e2786d2f9b.png)