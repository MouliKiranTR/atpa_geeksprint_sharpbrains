[[_TOC_]]

## Resources
- [Good overview on CARS](https://trten.sharepoint.com/sites/CaRSOperations/SitePages/CARS%20Operations.aspx)
- [Good overview on CARI Skill APIs](https://trten.sharepoint.com/sites/CaRSOperations/SitePages/RAS/CARI%20Skill%20API.aspx)
- [CARS Shared Pipeline Templates Documentation](https://github.com/tr/cars-shared_pipeline-templates/blob/main/readme-docs/cicd-setup-instructions.md)
- [Overall CaRS Logical Architecture Lucid Chart](https://lucid.app/lucidchart/d2ecce87-b27a-4f00-ac1b-3a5764c7faba/edit?invitationId=inv_4b7f71d8-287f-4c6a-8431-1970549d20e3&page=qlnjn0KbYBPF#)
- [CaRS API Routing Lucid Chart](https://lucid.app/lucidchart/2408b51e-f93a-4a98-9aac-cce9c6ec9287/edit?invitationId=inv_9606720f-10c7-4203-8620-58602ad1183a&page=vaPey8.gV-nC#)
- [CaRS API Repos Lucid Chart](https://lucid.app/lucidchart/d0696e1f-aeb6-4c32-9336-06d96a13f10c/edit?invitationId=inv_4f7fcc25-6d2d-44c6-9c00-75c59fd772d6&page=bWpRtFPSdS1I#)

## Steps to Create Cumulus Pipeline Deployment and IAC
- The main source of documentation for this process is in the `cars-shared_pipeline-templates` repo: https://github.com/tr/cars-shared_pipeline-templates/blob/main/readme-docs/cicd-setup-instructions.md
1. The first step is to add create a repository and add GitHub Workflow actions
	1. You can use the [CARS Java API Template Repository](https://github.com/tr/cars-shared_java-api-template) or [CARS Python API Template Repository](https://github.com/tr/cars-shared_python-api-template) as a starting point
	2. The GitHub actions can then be added by subscribing to the IHN patterns using the [CICD Self Service Portal](https://self-service.cicd.int.thomsonreuters.com/)
	3. You enter your GitHub credentials, specify the repo, and it will open a PR with the required files for CICD workflows
3. The next step is adding your projects configuration to the parameters repo
	1. There are pipeline parameters repositories for CARI, VARS, RAS, and GCS
	2. For CARI the repo is [cari-shared_pipeline-parameters](https://github.com/tr/cari-shared_pipeline-parameters)
	3. In this repo you need to add the config for your project under `project-configs`
	4. Create a PR adding project config
4. Next, there are modifications needed to the generated GitHub Workflows
	1. This is listed under step (d)
	2. The main step here for the CICD pipelines us adding the execution of the shared pipeline parameters repository as the third step of the repo
	3. Details for this can be found in the specific pipeline parameter repo for the tech suite you are using (in this case CARI so the `cari-shared_pipeline-parameters` repo)
	4. You also need to create an empty `cicd` directory which will be populated with the generated spec files from the Cumulus pipeline execution
	5. Create and check in PR for these changes to your microservice repo
5. Next, update the IaC configuration to create resources in AWS
	1. [cari-skill_shared-iac](https://github.com/tr/cari-skill_shared-iac) repository holds the IaC files
	2. Create a PR adding IaC for your microservice
	3. Once the PR is checked in the CodePipeline in AWS will execute and create the resources using AWS CodeBuild
6. Once the resources are created and pipeline stood up then there are some changes needed to the microservice application itself, in this case the Java app created from the [CARS Java API Template Repository](https://github.com/tr/cars-shared_java-api-template)
	1. Some of the changes involve updating ARN for IAM roles as well as server endpoints (Plexus Hosted Zone Name) now that the infrastructure is created
	2. Create and check in PR for these changes to your microservice repo
7. Lastly, Cumulus needs to be installed into the account (if not already), and then deployed using the merge and deploy scripts
	1. Steps to use the merge util can be found [here](https://github.com/tr/cars-shared_pipeline-templates/blob/main/readme-docs/using-merge-util.md)
	2. Merge util repo: [ras_cumulus-template-replace-action](https://github.com/tr/ras_cumulus-template-replace-action)
7. Additionally, the service must be added to the CARI Shared API Router
    - Repository: [cari-shared_api-router](https://github.com/tr/cari-shared_api-router)
    - Acts as configuration for the gateway that manages and routes traffic to services within the plexus cluster
    - It has been needed because of CoCounsel 1.0 not being on the internal TR network and having to call CARI skills via ADN (API Delivery Network). ADN requires separate configurations for each host/subdomain to be setup so only QA and Prod configurations were put in place. It also does not support wildcard configurations.
    - We added this shared router to have a single entry point for QA and Prod CARI Skills (in addition to the service-specific direct hosts). This router then takes the request and passes it along to the skill-specific Kubernetes service.

### Example PR's for AATR (AI Assisted Tax Research)
1. PR for adding CICD workflow templates to the `cari-skill_ai-assisted-tax-research` repo: https://github.com/tr/cari-skill_ai-assisted-tax-research/pull/1
2. PR for adding Cumulus config to the `cari-shared_pipeline-parameters` repo adding the project configuration: https://github.com/tr/cari-shared_pipeline-parameters/pull/67
3. PR for creating IAC resources in `cari-skill_shared-iac`: https://github.com/tr/cari-skill_shared-iac/pull/31
4. PR with modifications to the `cari-skill_ai-assisted-tax-research` repo for GH Actions workflow to include the shared pipeline parameters execution as well as updating ARN for IAM roles: https://github.com/tr/cari-skill_ai-assisted-tax-research/pull/24
5. PR for adding values for AI assisted tax research skill in `cari-shared_api-router`: https://github.com/tr/cari-shared_api-router/pull/34


## CARS Shared Pipelines
- Repo: [cars-shared_pipeline-templates](https://github.com/tr/cars-shared_pipeline-templates?tab=readme-ov-file)
- Documentation for creating and deploying a container- the starting point for building a Skill API
- Documentation is for the CaRS Tech Suite. For the Skills API the tech suite is CARI
- This repo acts as a framework for Cumulus pipeline templates (framework for microservice CICD operations)
- Creating project config files:
	- Adam Peterson will help do your first microservice and walk through the steps
	- project config files get stored in respective parameters repository based on the tech suite you are working in (CARI, VARS, RAS, GCS)
- Parameter Repositories Using This Action
	- [CARI Parameters](https://github.com/tr/cari-shared_pipeline-parameters)
	- [VARS Parameters](https://github.com/tr/vars-shared_pipeline-parameters)
	- [RAS Parameters](https://github.com/tr/ras-shared_pipeline-parameters)
	- [GCS Parameters](https://github.com/tr/gcs-shared_pipeline-parameters)
- [Lucid Chart Diagram](https://lucid.app/lucidspark/64022cff-750f-4692-8103-8555cd271ab4/edit?viewport_loc=-300%2C-578%2C4520%2C2069%2C0_0&invitationId=inv_e1082df5-3a39-4624-83cf-861cf9dbd633): ![Pasted image 20240904121600.png](/.attachments/Pasted%20image%2020240904121600-a73db2d5-c69e-4f83-b920-9282fbead4a8.png)
- For us, we will likely need to create a config file for our project under https://github.com/tr/cari-shared_pipeline-parameters/tree/main/project-configs/a208625-skill-apis

## AWS & Cloud Hosting
- Sample request: https://thomsonreuters.service-now.com/sp?id=request&table=sc_req_item&sys_id=60f47415870d5a905551319d3fbb358d
- Application Insight Name: CARI Skill APIs (AIID: 208625)
- ![image.png](/.attachments/image-9d4a9264-9fdb-4446-8a02-def53bb24064.png)

### AWS Accounts
- tr-cari-cicd-prod (041993746908)
    - Deployment pipelines
- tr-cari-apis-preprod (511927825172)
    - Additional resources created via Cloud IAC for use in the CI and INT environments
    - Use for local DD logging
    - Also used by CodeBuild for test suite
- tr-cari-apis-prod (533267099881)
    - Additional resources created via Cloud IAC for use in the QA and PROD environments
- tr-cari-service-mesh-preprod (580275797328)
    - Plexus/Kubernetes resources (deployments, etc.) for the CI and INT environments
- tr-cari-service-mesh-prod (208183779110)
    - Plexus/Kubernetes resources (deployments, etc.) for the QA and PROD environments

## Snyk
- Request access to this role: ![Pasted image 20241011130759.png](/.attachments/Pasted%20image%2020241011130759-a6dddc53-7fb5-4ba9-b418-3e51cce48bd9.png)
- instructions to get started in Snyk: https://trten.sharepoint.com/sites/intr-application-security/SitePages/Getting-Started-in-Veracode.aspx