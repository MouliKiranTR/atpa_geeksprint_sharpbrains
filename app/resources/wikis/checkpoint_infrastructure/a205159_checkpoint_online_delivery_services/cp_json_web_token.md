1. Description

2. Repository Link

3. Libraries

4. Testing

5. Diagrams

6. Notes
Below Repos are using  json-web-token jar as a dependency in pom.xml.

- cp_news-processing-service(11)  

- cp_calendar-service(11)  

- cp_user-profile-service(11)  

- cp_content-service(11)  

- cp_news-processing-service(11)  

- cp_calendar-service-poc(11)  

- cp_calendar_service(11)  

- cp_intuitive-search(1.8)  

- cp_autosuggest_recommender(11)  

- cp_public_search_service(11)  

- cp_tam-runner(1.8)  

- cp_content-agent(17)  

- cp_metadata-publisher(17)  

- cp_search-rank-service(17)  

- cp_updates-service(17)  

- cp_export-service(17)  

- cp_public-search-service(17)  

- cp_autosuggest-recommender(17)  

- cp_notifications-service(17)  

- cp_content-processing-service(17)  

- cp_trta-search


If we are using latest jar , need to do some necessary changes in test cases. otherwise testcases are failed to run. 
I tested latest jar by using **cp_autosuggest-recommender** . Got the below error.

**Error**
[ERROR]   JwtAuthorizationTokenFilterTest.doFilterInternalTest_ExpiredToken:91 » WeakKey The verification key's size is 88 bits which is not secure enough for the HS256 algorithm. The JWT JWA Specification (RFC 7518, Section 3.2) states that keys used with HS256 MUST have a size >= 256 bits (the key size must be greater than or equal to the hash output size). Consider using the Jwts.SIG.HS256.key() builder to create a key guaranteed to be secure enough for HS256.

**Resolution for  above error :**
If we get the above error while we are using the latest jar we need to change the secret key to 32 bytes size.

**example**
In my case chaged Secret key from **test-secret** to  **test-secretKey-strong-secret-32bytes**. We will use this secret key while generating the token.

Reference PR [Hm-168109-Fix Critical and High Vulnerabilities. by HarmandeepTR · Pull Request #24 · tr/cp_autosuggest-recommender](https://github.com/tr/cp_autosuggest-recommender/pull/24/files)