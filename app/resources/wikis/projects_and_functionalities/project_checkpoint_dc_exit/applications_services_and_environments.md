[[_TOC_]]


# Checkpoint Web Application
- Repository: https://github.com/tr/cp_web-app
- CIAM SNow template: [SSO Change Request template](https://thomsonreuters.service-now.com/sp?id=sc_cat_item&sys_id=946b025a1b81e054b65c32a3cc4bcb8d)
### Environments

|  Environment  | On-Prem URI | Site-specific URIs | Region URI | Cloud URI |
|---------------|-------------|--------------------|--------------------|--------------------|
| CI / Dev      | https://dev.checkpoint.thomsonreuters.com/app | N/A | https://region-use1.checkpoint.ci.thomsonreuters.com/app | https://checkpoint.ci.thomsonreuters.com/app |
| Demo / QA     | https://qa.checkpoint.thomsonreuters.com/app | <ul><li>[site-use1c1](https://site-use1c1.checkpoint.demo.thomsonreuters.com)</li><li>[site-use1c2](https://site-use1c2.checkpoint.demo.thomsonreuters.com)</li></ul> | https://region-use1.checkpoint.demo.thomsonreuters.com/app | https://checkpoint.demo.thomsonreuters.com/app |
| QED / Preprod | https://preprod.checkpoint.thomsonreuters.com/app<br><small>* External<small> | <ul><li>[site-use1c1](https://site-use1c1.checkpoint.qed.thomsonreuters.com)</li><li>[site-use1c2](https://site-use1c2.checkpoint.qed.thomsonreuters.com)</li></ul> | https://region-use1.checkpoint.qed.thomsonreuters.com/app<br><small>* Direct target<small> | https://checkpoint.qed.thomsonreuters.com/app<br><small>* External (Cloudflare)<small> |
| Prod          | https://checkpoint.riag.com/app<br><small>* External<small> | <ul><li>[site-use1c1](https://site-use1c1.checkpoint.thomsonreuters.com/app)</li><li>[site-use1c2](https://site-use1c2.checkpoint.thomsonreuters.com/app)</li></ul> | https://region-use1.checkpoint.thomsonreuters.com/app<br><small>* Direct target<small> | https://checkpoint.riag.com/app |

#### How to reach Cloud Environments without region-specific URL
For example, to reach cloud environment over checkpoint.qed.thomsonreuters.com you can either:
1. For automated requests (synthetic checks, automated testing): add *request header* `X-AWS-Region: us-east-1`
2. Add in browser console (Application) the *cookie* `location=cloud`

**Note:** There will also be specific site URLs for the cloud. 

### Cumulus Pipeline
| Environment | AWS CodePipeline | Status |
|:-----------:|------------------|--------|
| Altogether | [Link](https://us-east-1.console.aws.amazon.com/codesuite/codepipeline/pipelines?region=us-east-1&pipelines-meta=eyJmIjp7InRleHQiOiJjcC13ZWJhcHAifSwicyI6eyJwcm9wZXJ0eSI6InVwZGF0ZWQiLCJkaXJlY3Rpb24iOi0xfSwibiI6MzAsImkiOjB9) ||
| CI          | https://us-east-1.console.aws.amazon.com/codesuite/codepipeline/pipelines/a200172-cp-webapp-ci-use1-pipeline/view | [Link](https://infratools-cp-ci-use1.5463.aws-int.thomsonreuters.com/status) |
| Demo        | https://us-east-1.console.aws.amazon.com/codesuite/codepipeline/pipelines/a200172-cp-webapp-demo-use1-pipeline/view | [TBD](https://infratools-cp-demo-use1.5463.aws-int.thomsonreuters.com/status) |
| QED         | https://us-east-1.console.aws.amazon.com/codesuite/codepipeline/pipelines/a200172-cp-webapp-qed-use1-pipeline | [TBD](https://infratools-cp-qed-use1.1434.aws-int.thomsonreuters.com/status) |
| Prod        | https://us-east-1.console.aws.amazon.com/codesuite/codepipeline/pipelines/a200172-cp-webapp-prod-use1-pipeline | [TBD](https://infratools-cp-prod-use1.1434.aws-int.thomsonreuters.com/status) |

**Note**: Please submit a request using this [form](https://thomsonreuters.service-now.com/sp?id=sc_cat_item&sys_id=20a076696f079280a24190754b3ee4f1) to get access to the Cumulus pipeline. Here is an example of the selected properties:
- Select a Service: **AWS**
- What is your application's Asset Insight Name? **Checkpoint Research**
- AWS Account Name: **tr-ras-cicd-prod (235790704225)**
- Roles to Access: **readonly** (to view the pipelines) or **PowerUser2** (to view and trigger the pipeline)
- Role Membership: **add your m account Id**

## Datadog | CMDB | ÜberGUI links

| Environment | Datadog Error Dashboard<br>trta-cp-prod | CMDB Link | CMDB view<br>Global Scope| ÜberGUI |
|:-----------:|:---------------------------------------:|-----------|:------------------------:|---------|
| CI          | [Link](https://trta-cp-prod.datadoghq.com/dashboard/qk9-4qw-3qy?fromUser=false&refresh_mode=sliding&view=spans) | [Link](https://infratools-cp-ci-use1.5463.aws-int.thomsonreuters.com/cmdb/verticals/attributes?targetName=webapp) | [Link](https://infratools-cp-ci-use1.5463.aws-int.thomsonreuters.com/cmdb/rest/v2/ServerProfileApplicationAttributes/applicationName=webapp&namespace=cp&location=use1c1&serverProfileName=cp&decryptFlag=false) | [Link](https://infratools-cp-ci-use1.5463.aws-int.thomsonreuters.com/ubergui) |
| Demo        | [Link](https://trta-cp-prod.datadoghq.com/dashboard/qk9-4qw-3qy?fromUser=false&refresh_mode=sliding&tpl_var_env%5B0%5D=demo-cp-use1&view=spans) | [Link](https://infratools-cp-demo-use1.5463.aws-int.thomsonreuters.com/cmdb/verticals/attributes?targetName=webapp) | [Link](https://infratools-cp-demo-use1.5463.aws-int.thomsonreuters.com/cmdb/rest/v2/ServerProfileApplicationAttributes/applicationName=webapp&namespace=cp&location=use1c1&serverProfileName=cp&decryptFlag=false) | [Link](https://infratools-cp-demo-use1.5463.aws-int.thomsonreuters.com/ubergui) |
| QED         | [Link](https://trta-cp-prod.datadoghq.com/dashboard/qk9-4qw-3qy?fromUser=false&refresh_mode=sliding&tpl_var_env%5B0%5D=qed-cp-use1&view=spans) | [Link](https://infratools-cp-qed-use1.1434.aws-int.thomsonreuters.com/cmdb/verticals/attributes?targetName=webapp) | [Link](https://infratools-cp-qed-use1.1434.aws-int.thomsonreuters.com/cmdb/rest/v2/ServerProfileApplicationAttributes/applicationName=webapp&namespace=cp&location=use1c1&serverProfileName=cp&decryptFlag=false) | [Link](https://infratools-cp-qed-use1.1434.aws-int.thomsonreuters.com/ubergui) |
| Prod        | TBD | [Link](https://infratools-cp-prod-use1.1434.aws-int.thomsonreuters.com/cmdb/verticals/attributes?targetName=webapp) | [Link](https://infratools-cp-prod-use1.1434.aws-int.thomsonreuters.com/cmdb/rest/v2/ServerProfileApplicationAttributes/applicationName=webapp&namespace=cp&location=use1c1&serverProfileName=cp&decryptFlag=false) | [Link](https://infratools-cp-prod-use1.1434.aws-int.thomsonreuters.com/ubergui) |

## Mobile - Web Application 

|Environment| URI | 
|-----------|-----|
| CI        |checkpoint.ci.thomsonreuters.com/app/mobile/login |
| Demo      |checkpoint.demo.thomsonreuters.com/app/mobile/login  |
| Preprod   |checkpoint.qed.thomsonreuters.com/app/mobile/login  |
| Prod      |checkpoint.riag.com/app/mobile/login  |

# CP UI
## Version

|Environment| Version |
|-----------|--------------------------------------------------------------|
| CI        | https://checkpoint.ci.thomsonreuters.com/static/version.html |
| Demo      | https://checkpoint.demo.thomsonreuters.com/static/version.html |
| QED       | https://checkpoint.qed.thomsonreuters.com/static/version.html |
| Prod      | https://checkpoint.riag.com/static/version.html |



# CUAS
- Repository: https://github.com/tr/cp_user-administration

### CUAS-API/UI
- CP Web App property name: `cuas.link`, `cuas.create.user.url.domain`

|  Environment  | URI | Internal Cloud URI (Cobalt Shared) | Internal Cloud URI (TR Tax) |
|---------------|-----|------------------------------------|-----------------------------|
| CI | https://cpadmin.ci.thomsonreuters.com/ | https://cpadmin-ci-use1.8101.aws-int.thomsonreuters.com/ | https://cpadmin-ci-use1.5463.aws-int.thomsonreuters.com/ |
| DEMO | https://cpadmin.demo.thomsonreuters.com/| https://cpadmin-demo-use1.8101.aws-int.thomsonreuters.com/ | https://cpadmin-demo-use1.5463.aws-int.thomsonreuters.com/ |
| QED | https://cpadmin.qed.thomsonreuters.com/ | https://cpadmin-qed-use1.04032.aws-int.thomsonreuters.com/ | https://cpadmin-qed-use1.1434.aws-int.thomsonreuters.com/ |
| UAT | https://cpadmin.uat.thomsonreuters.com/ | https://cpadmin-uat-use1.04032.aws-int.thomsonreuters.com/ | https://cpadmin-uat-use1.1434.aws-int.thomsonreuters.com/ |
| PROD | https://cpadmin.thomsonreuters.com/ | https://cpadmin-prod-use1.04032.aws-int.thomsonreuters.com/ | https://cpadmin-prod-use1.1434.aws-int.thomsonreuters.com/ |

#### CMDB for CUAS-API
| Environment | URI |
|-|-|
| CI | https://infratools-chkpnt-ci-use1.8101.aws-int.thomsonreuters.com/cmdb/verticals |
| DEMO | https://infratools-chkpnt-demo-use1.8101.aws-int.thomsonreuters.com/cmdb/verticals |
| QED | https://infratools-chkpnt-qed-use1.04032.aws-int.thomsonreuters.com/cmdb/verticals |
| UAT | https://infratools-chkpnt-qed-use1.04032.aws-int.thomsonreuters.com/cmdb/verticals |
| PROD | https://infratools-chkpnt-prod-use1.04032.aws-int.thomsonreuters.com/cmdb/verticals |

### CPREG-UI
- CPWeb App property name: `cuas.token.ipAuthentication.uri`

|  Environment  | URI | Internal Cloud URI |
|---------------|-----------|--------------------|
| CI | https://cpreg.ci.thomsonreuters.com/ | https://cpreg-ci-use1.8101.aws-int.thomsonreuters.com/ |
| DEMO | https://cpreg.demo.thomsonreuters.com/ | https://cpreg-demo-use1.8101.aws-int.thomsonreuters.com/ |
| QED | https://cpreg.qed.thomsonreuters.com/ | https://cpreg-qed-use1.04032.aws-int.thomsonreuters.com/ |
| UAT | N/A | N/A |
| PROD | https://cpreg.thomsonreuters.com/ | https://cpreg-prod-use1.04032.aws-int.thomsonreuters.com/ |

### OMCUAS-UI

|  Environment  | URI | Internal Cloud URI |
|---------------|-----------|--------------------|
| CI | https://omcuas.ci.thomsonreuters.com/ | https://omcuas-ci-use1.8101.aws-int.thomsonreuters.com/ |
| Demo | https://omcuas.demo.thomsonreuters.com/ | https://omcuas-demo-use1.8101.aws-int.thomsonreuters.com/ |
| QED | https://omcuas.qed.thomsonreuters.com/ | https://omcuas-qed-use1.04032.aws-int.thomsonreuters.com/ |
| UAT | https://omcuas.uat.thomsonreuters.com/ | https://omcuas-uat-use1.04032.aws-int.thomsonreuters.com/ |
| Prod | https://omcuas.thomsonreuters.com/ | https://omcuas-prod-use1.04032.aws-int.thomsonreuters.com/ |


# Search Autocomplete
- Repository: https://github.com/tr/cp_search-autocomplete
- App property name: `search.autocomplete.domain`
### Environments

|Environment| On-prem URI | Internal Cloud URI | 
|-----------|-------------|--------------------|
| CI        | http://dev.search.checkpoint.thomsonreuters.com/searchAutoComplete/JSP/queryComp.jsp | https://region-use1.checkpoint.ci.thomsonreuters.com/searchAutoComplete/JSP/queryComp.jsp |
| Demo      | http://qa.search.checkpoint.thomsonreuters.com/searchAutoComplete/JSP/queryComp.jsp | https://region-use1.checkpoint.demo.thomsonreuters.com/searchAutoComplete/JSP/queryComp.jsp|
| Preprod   | http://search.checkpoint.thomsonreuters.com/searchAutoComplete/JSP/queryComp.jsp | https://region-use1.checkpoint.qed.thomsonreuters.com/searchAutoComplete/JSP/queryComp.jsp |
| Prod      | http://search.checkpoint.thomsonreuters.com/searchAutoComplete/JSP/queryComp.jsp | region-use1.checkpoint.thomsonreuters.com/searchAutoComplete/JSP/queryComp.jsp  |


# Document Conversion
- Repository: https://github.com/tr/cp_doc-conversion
- App property name: `prismDocConv.url`
- Datadog: [Link](https://trta-cp-prod.datadoghq.com/logs?query=env%3Aci-cp-use1%20service%3Adocconv%20&cols=host%2Cservice&fromUser=true&index=%2A&messageDisplay=inline&refresh_mode=sliding&storage=hot&stream_sort=desc&viz=stream&from_ts=1712571660595&to_ts=1712658060595&live=true)
### Environments

|Environment| On-prem URI | Internal Cloud URI | 
|-----------|-------------|--------------------|
| CI        | http://dev.export.checkpoint.thomsonreuters.com/services/DocConversion?wsdl | https://region-use1.checkpoint.ci.thomsonreuters.com/services/DocConversion?wsdl |
| Demo      | http://qa.export.checkpoint.thomsonreuters.com/services/DocConversion?wsdl | https://region-use1.checkpoint.demo.thomsonreuters.com/services/DocConversion?wsdl |
| Preprod   | http://qa.export.checkpoint.thomsonreuters.com/services/DocConversion?wsdl | https://region-use1.checkpoint.qed.thomsonreuters.com/services/DocConversion?wsdl |
| Prod      | http://export.checkpoint.thomsonreuters.com/services/DocConversion?wsdl | https://region-use1.checkpoint.thomsonreuters.com/services/DocConversion?wsdl |


# TRTA Search
- Repository: https://github.com/tr/cp_trta-search
- App property name: `cobalt.domain`
- Datadog: [tr-contentandresearch-prod](https://tr-contentandresearch-prod.datadoghq.com/logs?query=service%3Acheckpointussearch&agg_m=count&agg_m_source=base&agg_t=count&cols=host%2Cservice&fromUser=true&messageDisplay=inline&refresh_mode=sliding&storage=hot&stream_sort=desc&viz=stream&from_ts=1729632409659&to_ts=1729633309659&live=true)
### Environments

|Environment| On-prem URI | Cloud URI (Cobalt Shared) | Cloud URI (TR Tax) | CMDB (Cobalt Shared) |
|-----------|-------------|-----------|-----------|------|
| CI        | [Link](http://trtacheckpointus-ci.int.thomsonreuters.com/) | https://trtacheckpointus-ci-use1.8101.aws-int.thomsonreuters.com/CheckpointUSSearch/v1/resourcecheck | https://trtacheckpointus-ci-use1.5463.aws-int.thomsonreuters.com/CheckpointUSSearch/v1/resourcecheck | [Link](https://infratools-chkpnt-ci-use1.8101.aws-int.thomsonreuters.com/cmdb/verticals) |
| Demo      | [Link](http://trtacheckpointus-demo.int.thomsonreuters.com/) | https://trtacheckpointus-demo-use1.8101.aws-int.thomsonreuters.com/CheckpointUSSearch/v1/resourcecheck | https://trtacheckpointus-demo-use1.5463.aws-int.thomsonreuters.com/CheckpointUSSearch/v1/resourcecheck | [Link](https://infratools-chkpnt-demo-use1.8101.aws-int.thomsonreuters.com/cmdb/verticals) |
| QED       | [Link](http://trtacheckpointus-qed.int.thomsonreuters.com/) | https://trtacheckpointus-qed-use1.04032.aws-int.thomsonreuters.com/CheckpointUSSearch/v1/resourcecheck | https://trtacheckpointus-qed-use1.1434.aws-int.thomsonreuters.com/CheckpointUSSearch/v1/resourcecheck | [Link](https://infratools-chkpnt-qed-use1.04032.aws-int.thomsonreuters.com/cmdb/verticals) |
| Prod      | [Link](http://trtacheckpointus.int.thomsonreuters.com/) | https://trtacheckpointus-prod-use1.04032.aws-int.thomsonreuters.com/CheckpointUSSearch/v1/resourcecheck | https://trtacheckpointus-prod-use1.1434.aws-int.thomsonreuters.com/CheckpointUSSearch/v1/resourcecheck | [Link](https://infratools-chkpnt-prod-use1.04032.aws-int.thomsonreuters.com/cmdb/verticals) |

# GIS
- Repository: https://github.com/tr/TRTA_GIS_SERVICES
- App property name: `gis.host`
- Datadog (traces): [Link](https://tr-contentandresearch-prod.datadoghq.com/apm/traces?query=service%3Atrtagisgisservices&agg_m=count&agg_m_source=base&agg_t=count&cols=core_service%2Ccore_resource_name%2Clog_duration%2Clog_http.method%2Clog_http.status_code&fromUser=false&historicalData=false&messageDisplay=inline&sort=desc&spanType=all&storage=hot&view=spans&start=1750433862954&end=1750434762954&paused=false)
### Environments

|Environment| On-prem URI | Cloud URI (Cobalt Shared) | Cloud URI (TR Tax) |
|-----------|-------------|---------------------------|--------------------|
| CI        | [Link](https://trtagis.ci.thomsonreuters.com/gis/api/v1/ResourceCheck) | https://trtagis-ci-use1.8101.aws-int.thomsonreuters.com/gis/api/v1/ResourceCheck | https://trtagis-ci-use1.5463.aws-int.thomsonreuters.com/gis/api/v1/ResourceCheck |
| Demo      | [Link](https://trtagis.demo.thomsonreuters.com/gis/api/v1/ResourceCheck) | https://trtagis-demo-use1.8101.aws-int.thomsonreuters.com/gis/api/v1/ResourceCheck | https://trtagis-demo-use1.5463.aws-int.thomsonreuters.com/gis/api/v1/ResourceCheck |
| Preprod   | [Link](https://trtagis.qed.thomsonreuters.com/gis/api/v1/ResourceCheck) | https://trtagis-qed-use1.04032.aws-int.thomsonreuters.com/gis/api/v1/ResourceCheck | https://trtagis-qed-use1.1434.aws-int.thomsonreuters.com/gis/api/v1/ResourceCheck |
| Prod      | [Link](https://trtagis.thomsonreuters.com/gis/api/v1/ResourceCheck) | https://trtagis-prod-use1.04032.aws-int.thomsonreuters.com/gis/api/v1/ResourceCheck | https://trtagis-prod-use1.1434.aws-int.thomsonreuters.com/gis/api/v1/ResourceCheck |

# Novus

## Environments

|   Region  | Novus Client environment| Novus Prod environment |
|:---------:|------------|----------|
| :warning: <span style="color:red">Eagan</span> | CLIENT | PROD |
| us-east-1 | NOVUSAWS:CLIENT | NOVUSAWS:PROD |
| us-east-2 | NOVUSAWSUSE2:CLIENT | NOVUSAWSUSE2:PROD |

## Easel

|   Region  | Client URL | Prod URL |
|:---------:|------------|----------|
| :warning: <span style="color:red">Eagan</span> | https://easelclt.thomson.com/easel/ | https://easel.thomson.com/easel/ |
| us-east-1 | https://easelro-novus-client-use1.67223.aws-int.thomsonreuters.com/easel/ | https://easelro-novus-prod-use1.67223.aws-int.thomsonreuters.com/easel/|

## Novus Publishing GUI

|   Region  | Client URL | Prod URL |
|:---------:|------------|----------|
| :warning: <span style="color:red">Eagan</span> | https://publishingclt.int.westgroup.com/pubgui/ | https://publishing.int.westgroup.com/pubgui/ |
| us-east-1 | https://pubgui-client.1667.aws-int.thomsonreuters.com/pubgui | https://pubgui-prod.1667.aws-int.thomsonreuters.com/pubgui |
| us-east-2 | https://pubgui-client-use2.1667.aws-int.thomsonreuters.com/pubgui | https://pubgui-prod-use2.1667.aws-int.thomsonreuters.com/pubgui/ |

# Checkpoint/CUAS PostgreSQL Database and Data Replication


## Environments
- Database: checkpointdb
- Schema: checkpoint

|Environment| Host                                                                                        | Cluster | AWS Account |
|:---------:|---------------------------------------------------------------------------------------------|---------|-------------|
| CI        | a203669-checkpoint-research-ci-us-east-1.cluster-coahfs6xirdx.us-east-1.rds.amazonaws.com   | https://us-east-1.console.aws.amazon.com/rds/home?region=us-east-1#database:id=a203669-checkpoint-research-ci-us-east-1;is-cluster=true | tr-cobalt-shared-preprod (744501378101) |
| Demo      | a203669-checkpoint-research-demo-us-east-1.cluster-coahfs6xirdx.us-east-1.rds.amazonaws.com | https://us-east-1.console.aws.amazon.com/rds/home?region=us-east-1#database:id=a203669-checkpoint-research-demo-us-east-1;is-cluster=true | tr-cobalt-shared-preprod (744501378101) |
| Preprod   | a203669-checkpoint-research-qed-us-east-1.cluster-c8cik2zlbtiq.us-east-1.rds.amazonaws.com  | https://us-east-1.console.aws.amazon.com/rds/home?region=us-east-1#database:id=a203669-checkpoint-research-qed-us-east-1;is-cluster=true | tr-cobalt-shared-prod (999437604032) |
| Prod      | a203669-checkpoint-research-prod-us-east-1.cluster-c8cik2zlbtiq.us-east-1.rds.amazonaws.com | https://us-east-1.console.aws.amazon.com/rds/home?region=us-east-1#database:id=a203669-checkpoint-research-prod-us-east-1;is-cluster=true | tr-cobalt-shared-prod (999437604032) |

## Flyway
- Flyway repository: https://github.com/tr/cp_web-app-dbchange/
- IaC repository: https://github.com/tr/a203669_trtacheckpoint-rds-iac
- **[Deprecated]** AWS CodePipeline (all env): https://us-east-1.console.aws.amazon.com/codesuite/codepipeline/pipelines/a203669-trtadb-cumulus-db-flyway-pipeline/view?region=us-east-1
- **[New]** AWS codepipeline: [https://us-east-1.console.aws.amazon.com/codesuite/codepipeline/pipelines/a203669-trtadb-cp-cuas-cumulus-db-flyway-pipeline/view?region=us-east-1](https://us-east-1.console.aws.amazon.com/codesuite/codepipeline/pipelines/a203669-trtadb-cp-cuas-cumulus-db-flyway-pipeline/view?region=us-east-1 "https://us-east-1.console.aws.amazon.com/codesuite/codepipeline/pipelines/a203669-trtadb-cp-cuas-cumulus-db-flyway-pipeline/view?region=us-east-1")
  **Note:** Access to the human-role/a200172-PowerUser2 role in the tr-ras-comm-cicd-prod (084375544766) account is required.
  **Note:** Approvals to upper environments with Pavankumar Pusukuri, Venkat Dangeti, or Dinesh Talapala (Platform CM & CSS teams)
- AWS CodeBuild (logs): 
  - CI/Demo: https://us-east-1.console.aws.amazon.com/codesuite/codebuild/744501378101/projects/a203669-trtadb-cumulus-db-change-project?region=us-east-1
  **Note:** You need to [raise a request](https://thomsonreuters.service-now.com/sp?id=sc_cat_item&sys_id=20a076696f079280a24190754b3ee4f1) in the asset _Legal Shared Cobalt Services_ for the _human-role/206645-ReadOnly_ role from the _tr-cobalt-shared-preprod (744501378101)_ AWS account to have access to the Build logs.
  - QED/Prod: https://us-east-1.console.aws.amazon.com/codesuite/codebuild/999437604032/projects/a203669-trtadb-cumulus-db-change-project?region=us-east-1 
  **Note:** You need to [raise a request](https://thomsonreuters.service-now.com/sp?id=sc_cat_item&sys_id=20a076696f079280a24190754b3ee4f1) in the asset _Legal Shared Cobalt Services_ for the _human-role/206645-ReadOnly_ role from the _tr-cobalt-shared-prod (999437604032)_ AWS account to have access to the Build logs.

## Data Replication
The on-prem (Oracle) and cloud (Postgres) databases need data synchronization. To accomplish that, we follow these approaches depending on the environment:

1. AWS Data Migration Service (DMS)
   - Responsible: [Dev DBA team](https://dev.azure.com.mcas.ms/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/776/Teams-and-POCs?anchor=dev-dba-%5Boracle-db-support%2C-postgres-integration%2C-hvr-preps%5D)

   |Environment| Link     |
   |:---------:|----------|
   | CI        | [Link]() |
   | Demo      | [Link]() |

2. High Volume Replicator (HVR)
   - Responsible: https://dev.azure.com.mcas.ms/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/776/Teams-and-POCs?anchor=high-volume-replicator-(hvr)-%5Bdata-synchonization%5D

   |Environment| HVR Hub Server              | Account                              |
   |:---------:|-----------------------------|--------------------------------------| 
   | Preprod   | a203669-tr2-qed-hvrhub-ASG  | tr-cobalt-shared-prod (999437604032) |
   | Prod      | a203669-tr2-prod-hvrhub-ASG | tr-cobalt-shared-prod (999437604032) |

# CP Developer/DevOps Tools Migration (Wiki, LinkMaster)
- MoinMoin Old CP Wiki site
  Link: https://infratools-cp-ci-use1.5463.aws-int.thomsonreuters.com/wiki
- LinkMaster
  Repository: https://github.com/tr/cp_linkmaster
  Link: TBD

# Microservices Checkpoint DB (205159)
- In the Checkpoint Cloud Services AWS account we have an RDS Aurora Postgres DB used for all cloud microservices
- Login credentials:
	- DEV: https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/120/RDS-Aurora-DEV_Passwords
	- Test: https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/130/RDS-Aurora-Test_Passwords
	- QED/PROD reach out to West-Dev DBA

### Auth Service
- The Auth service relies on DMS task to replicate entries from the Checkpoint & CUAS DB (either on-prem Oracle or cloud Postgres) to the 205159 RDS DB
- Lucid: https://lucid.app/lucidchart/2178baf5-0280-4cc1-862c-fdff03ed25ff/edit?invitationId=inv_562dd334-8320-48e0-b13a-5dc17e9eef90&page=0_0# ![image.png](/.attachments/image-bb36bb61-1936-424e-a44b-3062d09ccc34.png)
- DMS tasks:

| **_Environment_** | **_Status_** | **_DMS Task_**                        | **_Source Endpoint_** |
| ----------------- | ------------ | ------------------------------------- | --------------------- |
| DEV               | Running      | a205159-cp-auth-dev-migration-task    | Oracle                |
| Test              | Running      | a205159-cp-auth-test-migration-task   | Oracle                |
| QED               | _STOPPED_    | a205159-checkpoint-qed-authentication | Oracle                |
| QED               | Running      | a205159-cp-authentication-shared-qed  | Postgres              |
|                   |              |                                       |                       |

## CUAS User Creation Flow
- ![CP DB Flows.png](/.attachments/CP%20DB%20Flows-f9ad53a0-f9e9-4e7f-998f-8eba2f79a941.png)
- When we create a user in cloud CUAS a DB entry is added to the cloud Postgres DB. However, since HVR is not enabled in lower envs, this entry is never copied over to the Oracle DB, and therefore the DMS task does not sync this new user over to the Auth service DB, and the user is not able to be found.
- For all other cases, the sync should operate properly as expected