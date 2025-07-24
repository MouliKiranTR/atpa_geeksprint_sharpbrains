Elasticsearch Cluster information can be found on relevant config servers

- **[DEV](http://cpa-config-server.tr-tax-cp-preprod.aws-int.thomsonreuters.com/cp-displaycards-service/dev)**
- **[TEST/QA](http://cpa-config-server.tr-tax-cp-preprod.aws-int.thomsonreuters.com/cp-displaycards-service/test)**
- **[QED/PreProd](http://cpa-config-server.tr-tax-cp-preprod.aws-int.thomsonreuters.com/cp-displaycards-service/qed)**

- **[PROD](http://cpa-config-server.tr-tax-cp-prod.aws-int.thomsonreuters.com/cp-displaycards-service/prod)**

**ES Index Policies -** 
- Incremental Index - 5 shards and 1 replica, to have higher speed of data ingest
- Live Index - 1 shard and 2 replicas, to have higher speed of queries. Number of replicas to be adjust in case of change in number of data nodes change in our Elasticsearch cluster. Currently we have 3 datanodes so using 1 shard and 2 replicas for querying performance.


[Link to Elasticsearch Index creation scripts](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_git/cp-displaycards-service?path=%2Fsrc%2Fmain%2Fresources%2Fes)