The document highlighting functionality is realized by the standard Elasticsearch functionality. All the parameters are set using a search template which can be found in the [git repository](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_git/cp-elasticsearch?path=%2Ftrta-highlight-template.mustache)
The search template as input takes a list of document id and the search phrase that is used to highlight the terms.
The search is exposed in cp-search-service as a separate endpoint:
```
curl --location --request GET 'https://cp-dev-services.5463.aws.thomsonreuters.com/api/search/highlight?q=tax%20law&ids=iSLOMAM:95154.1,ib1f43a2a821e4d11e937d34c93e57a4a' \
--header 'Authorization: Bearer $access_token'
```