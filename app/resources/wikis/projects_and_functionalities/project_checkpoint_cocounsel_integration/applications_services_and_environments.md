[[_TOC_]]


# CARI Skill Server - AI Assisted Tax Research (AATR)
- Repository: https://github.com/tr/cari-skill_ai-assisted-tax-research

## Environments

| Environment | URI |
|--|--|
| CI | https://ai-assisted-tax-research-ci.plexus-cari-ppuse1.97328.aws-int.thomsonreuters.com/skill/ai-assisted-tax-research/ |
| INT | https://ai-assisted-tax-research-int.plexus-cari-ppuse1.97328.aws-int.thomsonreuters.com/skill/ai-assisted-tax-research/ |
| QA | TBD |
| PROD | TBD |

## Cumulus Pipeline (AWS CodePipeline and CodeBuild)
- Account:  tr-cari-cicd-prod (041993746908)
- [a208625-skill-api-ai-assisted-tax-research-cumulus](https://us-east-1.console.aws.amazon.com/codesuite/codepipeline/pipelines/a208625-skill-api-ai-assisted-tax-research-cumulus/view?region=us-east-1#)
- [a208625-skill-api-ai-assisted-tax-research-cumulus-Bake](https://us-east-1.console.aws.amazon.com/codesuite/codebuild/041993746908/projects/a208625-skill-api-ai-assisted-tax-research-cumulus-Bake/history?builds-meta=eyJmIjp7InRleHQiOiIiLCJzdGF0dXMiOiIifSwicyI6e30sIm4iOjIwLCJpIjowfQ&region=us-east-1#)
- [a208625-skill-api-shared-iac-cumulus-iac](https://us-east-1.console.aws.amazon.com/codesuite/codepipeline/pipelines/a208625-skill-api-shared-iac-cumulus-iac/view?region=us-east-1#) (shared IAC Cumulus pipeline for all CARI Skill APIs)
- [a208625-cari-cloud-iac-codebuild](https://us-east-1.console.aws.amazon.com/codesuite/codebuild/041993746908/projects/a208625-cari-cloud-iac-codebuild?region=us-east-1&builds-meta=eyJmIjp7InRleHQiOiIiLCJzdGF0dXMiOiIifSwicyI6e30sIm4iOjIwLCJpIjowfQ)

## AWS Elastic Container Registry (ECR)
- Account:  tr-cari-cicd-prod (041993746908)
- [a208625/skill-api/ai-assisted-tax-research](https://us-east-1.console.aws.amazon.com/ecr/repositories/private/041993746908/a208625/skill-api/ai-assisted-tax-research?region=us-east-1)

## Plexus Cluster
- Accounts:
  - *Preprod*: tr-cari-service-mesh-preprod (580275797328)
  - *Prod*: tr-cari-service-mesh-prod (208183779110)
- The Plexus Cluster is hosted using AWS Elastic Kubernetes Service (EKS)
- ***PreProd Cluster:*** [a208219-preprod-cari-useast1-plexus-cluster](https://us-east-1.console.aws.amazon.com/eks/home?region=us-east-1#/clusters/a208219-preprod-cari-useast1-plexus-cluster)
- Connecting locally
  - To connect locally you must have [cloud-tool](https://techtoc.thomsonreuters.com/non-functional/cloud-landing-zones/aws-cloud-landing-zones/command-line-access/user_guide/#windows-install) and [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) installed
  - Then, login to the CARI Service Mesh AWS account using `cloud-tool login` and selecting the correct role
  - Next, you can connect to the EKS cluster using the following AWS CLI command: 
    - `aws eks --region us-east-1 update-kubeconfig --name a208219-preprod-cari-useast1-plexus-cluster`
    - *Note:* this command is for connecting to the preprod cluster, update as needed to connect to any other clusters
   - This will update the Kube config on your system which will allow you to connect to the cluster

## Swagger Documentation
- [CI](https://ai-assisted-tax-research-ci.plexus-cari-ppuse1.97328.aws-int.thomsonreuters.com/skill/ai-assisted-tax-research/swagger-ui/index.html)
- [INT](https://ai-assisted-tax-research-int.plexus-cari-ppuse1.97328.aws-int.thomsonreuters.com/skill/ai-assisted-tax-research/swagger-ui/index.html)

## Overview of API's
- **POST /v1/conversation**
  - _Milestone 1_
  - Used to initiate a conversation based on user's query 
  - **Request** contains user query (passed through the POST request body)
  - **Response** contains conversation ID and conversation entry ID if it was initiated successfully
- **GET /v1/flows/{id}/status**  
  - _Milestone 1_
  - Used to retrieve the status of a conversation
  - **Request** contains the conversation ID and _(optionally)_ a conversation entry ID (if provided returns status of a specific entry of the conversation, if left blank returns status of the whole conversation)
    - id is path parameter, and required
    - entry_id is a query parameter, and optional
  - **Response** contains status information such as the status and progress (percent complete)
- **GET /v1/flows/{id}**
  - _Milestone 2_
  - Used to retrieve information and details of a conversation
  - **Request** contains the conversation ID and _(optionally)_ a conversation entry ID (if provided returns information/details of a specific entry of the conversation, if left blank returns information/details of the whole conversation)
    - id is path parameter, and required
    - entry_id is a query parameter, and optional
  - **Response** contains details of the conversation, including response output and citations
- **PUT /v1/conversation/{id}**
  - _Milestone 2_
  - Used to continue an existing conversation by submitting a new follow-up query 
  - **Request** contains user query (passed through the PUT request body) and ID of the conversation (required path parameter)
  - **Response** contains conversation entry ID if it was initiated successfully along with index of the entry in the conversation

## Datadog
- Datadog logs can be found under the `tr-contentandresearch` organizations
- [AATR service page](https://tr-contentandresearch-preprod.datadoghq.com/apm/services/ai-assisted-tax-research/operations/servlet.request/resources?dependencyMap=qson%3A%28data%3A%28telemetrySelection%3Aall_sources%29%2Cversion%3A%210%29&deployments=qson%3A%28data%3A%28hits%3A%28selected%3Aversion_count%29%2Cerrors%3A%28selected%3Aversion_count%29%2Clatency%3A%2195%2CtopN%3A%215%29%2Cversion%3A%210%29&env=ci&errors=qson%3A%28data%3A%28issueSort%3AFIRST_SEEN%29%2Cversion%3A%210%29&fromUser=true&groupMapByOperation=null&infrastructure=qson%3A%28data%3A%28viewType%3Apods%29%2Cversion%3A%210%29&logs=qson%3A%28data%3A%28indexes%3A%5B%5D%29%2Cversion%3A%210%29&panels=qson%3A%28data%3A%28%29%2Cversion%3A%210%29&resources=qson%3A%28data%3A%28visible%3A%21t%2Chits%3A%28selected%3Atotal%29%2Cerrors%3A%28selected%3Atotal%29%2Clatency%3A%28selected%3Ap95%29%2CtopN%3A%215%29%2Cversion%3A%211%29&summary=qson%3A%28data%3A%28visible%3A%21t%2Cchanges%3A%28%29%2Cerrors%3A%28selected%3Acount%29%2Chits%3A%28selected%3Acount%29%2Clatency%3A%28selected%3Alatency%2Cslot%3A%28agg%3A95%29%2Cdistribution%3A%28isLogScale%3A%21f%29%2CshowTraceOutliers%3A%21t%29%2Csublayer%3A%28slot%3A%28layers%3Aservice%29%2Cselected%3Apercentage%29%2ClagMetrics%3A%28selectedMetric%3A%21s%2CselectedGroupBy%3A%21s%29%29%2Cversion%3A%211%29&traces=qson%3A%28data%3A%28%29%2Cversion%3A%210%29&start=1728920171113&end=1729524971113&paused=false)