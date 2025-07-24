# 1. a205159 services information

>- The complete list of services can be found [here](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/1175/Swagger-links) 

# 2. Extra services

- [Akkadia Services](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/1079/Project-Setup-Shared-Folders-for-localhost)
- [News API](https://cp-prod-services.tr-tax-cp-prod.aws-int.thomsonreuters.com/api/docs/news/swagger-ui.html)
- [Platform Config Service](https://cp-dev-cp-platform-config-service.tr-tax-cp-preprod.aws-int.thomsonreuters.com/swagger-ui/index.html)
- Search Service, no Swagger configured
- Spellcheck Service, no Swagger configured
- Usage Metrics Pendo, no Swagger configured



# 3. Swagger UI Endpoint
The standard Swagger UI endpoint for a service is `<host>/api/docs/<service-name-from-application-properties>/swagger-ui.html`. Most of the services have had their Swagger UI endpoints updated to adhere to this standard. For any developer working on a service, it would be preferable if the Swagger UI endpoint is updated as well if it does not adhere to the standard for existing services and if it is the case that a new service is created then this convention should be followed.
