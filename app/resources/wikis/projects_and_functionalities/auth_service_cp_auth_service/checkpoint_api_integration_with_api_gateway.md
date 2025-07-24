# Purpose
As TR pushes more-and-more APIs into the 3rd-party marketplace, we MUST use standards-based approaches for API access management; in short, this means using OAuth2. The purpose of this document is to walk through the proposed design, that is standards-based from end-to-end. This discussion is purely technical and may be disconnected from business imperatives and constraints.

# Scenario
The Checkpoint API provides research materials, news updates, marketing resources.

 

A typical use-case is where a Tax Professionals Firm or a TR Product wants to include Checkpoint Content into their applications.


|Name|Description  |
|--|--|
|Tax Professionals Firm  | An organization with 1 or more Tax Professionals (e.g. PwC). |
| Tax Professional | A person at a Tax Professionals Firm who wants information from the Checkpoint Content. |
| Tax Professionals Firm's Application | An application, produced and owned by the Tax Professionals Firm. It has many features, one of which is the ability to provide tax updates. |
|TR Product / TR Platform  | Thomson Reuters Product (e.g. Onvio). |
|TR Application  |Application produced and owned by TR Product (e.g. Onvio Advisory).  |
| Checkpoint API | An API, produced and owned by TR that provides programmatic access to tax updates. Part of the Checkpoint Product. |

# Use case
What we want is the ability for the Tax Professionals Firm's Application or TR Application to make API calls against the Checkpoint API.

 

# OAuth Solution Outline
 

## OAuth: Establish OAuth Roles
To get started with OAuth, it helps to first figure out who is playing what role, from an OAuth perspective. Luckily, there are only 4 roles that OAuth recognizes: Resource Owner, Client, Authorization Server and Resource Server.


|Name| OAuth Role |
|--|--|
|Tax Professionals Firm, TR Product  | No OAuth role in this scenario. |
| Tax Professional | 	No OAuth role in this scenario. |
| Tax Professionals Firm's Application, TR Application | Client |
| Checkpoint API | Resource Server |
| Checkpoint Auth | Authorization Server |

## OAuth: Establish OAuth Grant
With the actors mapped to OAuth roles, we can then move to figure out which OAuth grant is appropriate for this use case. Luckily there are only 4 main grants to choose from: Client Credential Grant, Implicit Grant, Resource Owner Password Credentials grant and Auth Code Grant (with or without PKCE). The art of OAuth is picking the right grant to use for the use case; I won't cover the rationale in this article, but the recommended grant is the Client Credential Grant.

### Client Credential Grant
In generic terms, here's how this flow would look-
![Client Credentials Grant.png](/.attachments/Client%20Credentials%20Grant-21260ef6-2316-4048-9d04-596fa5311309.png)

## Enhancement: Row-level security via Checkpoint Subscriptions Framework
The main problem we have is that Checkpoint's content only available by subscriptions. And the subscriptions only assigned to Checkpoint users. In other words, from Checkpoint's perspective there couldn't be anonymous or user-less access to the content. Data access always requires a user subscribed to a product, which grants access to the sub-set of data. 

 

That means our flow (Client Credentials Grant) is still missing one more OAuth role - Resource Owner.

 

Luckily we are, OAuth is all about delegation. It allows a client application to ask resource owner (a user) for permission to access a protected resource (an HTTP API) on their behalf. It is a delegation protocol. So, what happens when a client application communicates with a protected resource that itself then needs to inspect user's identity to understand what data that user is subscribed to? How do we keep this request acting on the user’s behalf? How do we do this securely without prompting the user's credentials?

 

### JWT Bearer Authorization Grant (RFC 7523)
From the specification, the JWT Bearer Authorization Grant is:

[A way for] a JWT Bearer Token can be used to request an access token when a client wishes to utilize an existing trust relationship, […] without a direct user-approval step at the authorization server.
[[RFC 7523 - Section 1](https://datatracker.ietf.org/doc/html/rfc7523#section-1)]

This authorization grant is most suited towards swapping tokens and assertions issued by a different authorization server/identity provider, for tokens issued by our authorization server (impersonation).

 

### Enhancement: API is "behind" Apigee API Gateway
In this case, the Checkpoint API is actually behind the Apigee API Gateway. As explained in OAuth Series: API Gateways, in this case the Resource Server is composed of both the API Gateway and the API itself.

 

## Full solution
Combining the enhanced requirements for row-level security based on Checkpoint user's subscriptions and the use of an API Gateway, we begin to see the complete solution as follows-
![OAuth Data Flows In Checkpoint.png](/.attachments/OAuth%20Data%20Flows%20In%20Checkpoint-3201b1fa-6d1b-4106-962c-d3730e377425.png)

From Client's perspective the flow is still Client Credentials Grant. Behind the scenes, the client's identity is impersonated to the Checkpoint's identity, which is then used to check subscriptions.

Checkpoint Auth authenticates this impersonate request by validating the assertion token (see [RFC 7523 - Section 2.1](https://datatracker.ietf.org/doc/html/rfc7523#section-2.1)).

 

### Assertion token

```
{
  ..
  "aud": "43c91f07499be34bf9590fb2e0ec8c50.dev.cp-auth-service",
  "iss": "3dc0724680e3a164b169d257d3ab8160.dev.api-gateway",
  "sub": "4717969",
  ..
}
```

This is a sample assertion token payload (other typical non-relevant JWT claims are removed).

Here,

- Audience claim contains the integration key of Checkpoint Auth (also known as client ID),
- Issuer claim contains the integration key of API Gateway (also known as client ID),
- and Subject claim contains the Checkpoint User ID.
 

The assertion token is expected to be signed by RSA private key. Using assymetric algorithm to generate signatures is convenient when you want to rotate the keys regularly, as it doesn't require the keys to be exchanged out of band (ensuring a secure communication channel), and manually updated on client (Checkpoint Auth, in our case).

 

# Wrap-up
Hopefully that's a pretty thorough walkthrough of the proposed solution. This doc should be updated as the implementation progresses.
