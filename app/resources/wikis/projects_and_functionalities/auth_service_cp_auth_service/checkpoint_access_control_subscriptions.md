# Overview of domain
In Checkpoint, resource servers usually operate with ODS/OFS entities to check access level of a current request. Each ODS/OFS represents minimum unit or piece of data (ODS) or functionality (OFS) that if available for user. The users get assigned to ODS/OFS via subscriptions.

 

Here is how they are connected-
![Checkpoint Subscriptions.png](/.attachments/Checkpoint%20Subscriptions-f082443d-af7e-45a7-8711-39f7d9292335.png)


 

# Current User Entitlements API
Checkpoint Auth server provides entitlements API, so that resource servers that need to check user access level could obtain the lists of ODS/OFS for current user. Auth server provides the following endpoint for retrieving current user's subscriptions:

- GET /api/v1/auth/entitlements
- GET /api/v1/auth/entitlements/odses
- GET /api/v1/auth/entitlements/odses/{odsName}
- GET /api/v1/auth/entitlements/ofses
- GET /api/v1/auth/entitlements/ofses/{ofsId}

```
ODSes are operated with their names, OFSes -- with their IDs.

This is to maintain their historical usage in Checkpoint Web App.
```


## Users Entitlements API
Entitlements provided by the endpoints above are scoped to current user (the current access token is issued to). If a service wants to inspect entitlements of other users (typically, this is needed when a scheduled job runs in user-less context), the request should be sent to one of the following endpoints:

- GET /api/v1/users/{userId}/auth/entitlements
- GET /api/v1/users/{userId}/auth/entitlements/odses
- GET /api/v1/users/{userId}/auth/entitlements/ofses
**Note:** in this case access token must be scoped to "urn:tr:checkpoint:api:userinfo:read". See Client Credentials Grant and Client identities management sections for details.

 

# Entitlements caching
Apparently, a big demand of entitlements data if expected, since many resources need to maintain row-level security and other access control. In response to that entitlements endpoints (not all, only /auth/entitlements -- the full subscriptions data, which is typically required) are optionally backed by Redis cluster.

 

The caching strategy chosen is Cache-Aside (or Lazy Loading), which is the most convenient in our case due to AWS DMS setup (Auth server is in read-only mode for subscriptions data).

 

Couple of notes on cache implementation:

- Time-to-live by default is 2 hours.
- Due to Redis cluster availability issues identified, the connection to Redis is wrapped with a circuit breaker, which fails silently (as if it's a cache miss). Circuit breaker configuration is available at hystrix.command.default property.
 

Thus, we expect to be having cache misses at initial request, when user signs in to Checkpoint, and every two hours (configurable) during the session. This setup should let us maintain reasonable cache size.

 

So the disadvantages are:

- Data is loaded to cache only after a cache miss -- first request in session takes longer (which might affect log in time).
- Cached data could be stale (subscription is updated meanwhile) and there is no way to invalidate it before time-to-live expires.

```
Actually, there is an endpoint for cache entries invalidation, but it is only for developers and QAs manual use:

- DELETE /api/v1/auth/redis/users/{userId}/entitlements
```


```
Write-through option is also possible, but requires complicated implementation -- we need to catch AWS DMS events and process them as to update entitlements data in cache.

And if we do want the cache to be cost effective (sized reasonably), then the only benefit of Write-through is having the cache always up-to-date (see stale data disadvantage above).
```


# Next steps
The only reason why entitlements API is residing within Auth server is AWS DMS setup. To avoid setting up another DMS configuration, it was decided to add subscriptions related tables to the existing configuration and expose Entitlements API from Auth server.

 

However, it is recommended to separate it out from the Auth concern, so it would become yet another resource server. The APIs implementation is not coupled with authentication part and should be easily extractable.