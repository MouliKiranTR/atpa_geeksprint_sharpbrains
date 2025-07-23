1. Architecture 

- [General Infrastructure Diagram](https://lucid.app/lucidchart/9aeb4fc0-5c66-4039-b206-824c0a6d6ddd/edit?invitationId=inv_cd8a8f63-048d-47f2-a008-652ebb79f5ef&page=zc3.hlhYJ5ST#)

- [Lambdas Infrastructure Diagram](https://lucid.app/lucidchart/638e1911-0caf-4c76-8873-d12d0b37e775/edit?invitationId=inv_2a9e69ec-3d38-4e04-a442-46645a1cc73f&page=0_0#)

2. Testing 

- [Swagger URLs](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/1175/Swagger-links)



## 3. Services


- [cp-auth-service](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/1120/cp_auth-service)
- [cp_autosuggest-loader](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/1121/cp_autosuggest-loader)
- [cp_autosuggest-recommender](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/1123/cp_autosuggest-recommender)
- [cp_cm-classifier](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/1125/cp_cm-classifier)
- [cp_charts-service](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/1126/cp_charts-service)
- [cpa-content-processing-service](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/1128/cp_content-processing-service)
- [cap-content-service](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/1130/cp_content-service)
- [cp_doc-compare-service](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/1132/cp_doc-compare-service)
- [cp_doc-recommendation-service](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/1133/cp_doc-recommendation-service)
- [cp_export-service](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/1135/cp_export-service)
- [cp_feature-generation-service](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/1124/cp_feature-generation-service)
- [cp_folder-service](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/1137/cp_folder-service)
- [cp_gdp-classifier](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/1138/cp_gdp-classifier)
- [cp_history-service](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/1140/cp_history-service)
- [cp_intuitive-search](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/1141/cp_intuitive-search)
- [cp_metadata-service](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/1143/cp_metadata-service)
- [cp_newsletter-subscription-service](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/1145/cp_newsletter-subscription-service)
- [cp_notes-service](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/1146/cp_notes-service)
- [cp_notifications-service](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/1148/cp_notifications-service)
- [cp_search-rank-service](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/1149/cp_search-rank-service)
- [cp_search-service](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/1150/cp_search-service)
- [cp_snapshots-service](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/1152/cp_snapshots-service)
- [cp_toc-service](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/1154/cp_toc-service)
- [cp_tools-service](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/1156/cp_tools-service)
- [cp_updates-service](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/1157/cp_updates-service)
- [cp_usage-service](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/1159/cp_usage-service)
- [cp_user-profile-service](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/1161/cp_user-profile-service)
- [cp_calendar-service](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/1163/cp_calendar-service)
- [cp_json-web-token](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/1176/cp_json-web-token)


## 4. RDS

- Aurora Databases

1. Clusters by environment

>- CI  

>>- `a205159-cpeshared01s-cpedge-ci-use1.cluster-cu3yrxjpblsu.us-east-1.rds.amazonaws.com` 
>>- `a205159-cpeshared02s-cpedge-ci-use1.cluster-cu3yrxjpblsu.us-east-1.rds.amazonaws.com`

>- Demo  

>>- `a205159-cpeshared01s-cpedge-demo-use1.cluster-cu3yrxjpblsu.us-east-1.rds.amazonaws.com` 
>>- `a205159-cpeshared02s-cpedge-demo-use1.cluster-cu3yrxjpblsu.us-east-1.rds.amazonaws.com`

>- QED  

>>- `a205159-cpeshared01s-cpedge-qed-use1.cluster-cu3yrxjpblsu.us-east-1.rds.amazonaws.com` 
>>- `a205159-cpeshared02s-cpedge-qed-use1.cluster-cu3yrxjpblsu.us-east-1.rds.amazonaws.com`

>- Prod  

>>- `a205159-cpeshared01s-cpedge-prod-use1.cluster-ccytwsqd6qzd.us-east-1.rds.amazonaws.com` 
>>- `a205159-cpeshared02s-cpedge-prod-use1.cluster-ccytwsqd6qzd.us-east-1.rds.amazonaws.com` 

 

2. Databases

>- **cpeshared01s**

  | Schemas            |
  |---------           |
  | onersource         |
  | checkpoint_answers |
  | chartsservice      |
  | docrecservice      |
  | notification       |
  | silver             |
  | tools              |
  | updates            |

>- **cpeshared02s**

  | Schemas            |
  |---------           |
  | authentication     |
  | folder             |
  | history            |
  | newsletter         |
  | newsservice        |
  | notes              |
  | ria_web            |
  | search             |

