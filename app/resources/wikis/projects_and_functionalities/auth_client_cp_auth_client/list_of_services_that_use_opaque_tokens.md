      

cp_auth-client provides support for 3 verification strategies –

·         JWT + JWK
·         JWT + Key
·         Opaque token

Out of these 3, JWT + JWK is the most frequently used by checkpoint microservices. The JWT + Key strategy is not being actively used anywhere, and the opaque token strategy is used by the following services –

·         cp_folder-service
·         cp_notes-service
·         cp_newsletter-subscription-service
·         cp_feature-flag-service (Nodejs AWS Lambda)
·         cp_privacydata-service (Nodejs AWS Lambda)

The Nodejs AWS lambdas make a direct call to cp_auth-service and do not involve cp_auth-client.