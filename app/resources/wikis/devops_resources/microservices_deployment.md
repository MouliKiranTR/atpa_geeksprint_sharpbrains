This document will provide you with the steps for deploying microservices in DEV and Test (QA) environments.
1.	Login into the [Jenkins server](https://cpdevops-jenkins.tr-tax-cp-preprod.aws-int.thomsonreuters.com/job/dev-utilities/job/app_deploy/)

2.	Now go to the [app_deploy](https://cpdevops-jenkins.tr-tax-cp-preprod.aws-int.thomsonreuters.com/job/deployment-utilities-GitHub/job/app_deploy/) job

![DevDeployJob.PNG](/.attachments/DevDeployJob-5f2ab582-fbad-4542-9914-0cf679287189.PNG)

3.	In the above job, click on build with Parameters and pass the build parameters as shown below


|Paramter Name| Description |
|--|--|
| serviceEnv | Please choose the deployment environment for the microservice |
| serviceName | Please designate the microservice for deployment |
| serviceVersion | Please select the microservice version for deployment. We can get the microservice from many ways, for example go to AWS EC2 Section and search for microservice in AMI’s sub section it will display all available for versions  |
|  deployerVersion|  [cp_aws](https://github.com/tr/cp_aws) repository bundle version. This bundle will consist for all cp-devops code. Namely cloudformation templates, Ansible Playbooks etc. we can use default value (**latest**) for this parameter |

![AMIList.PNG](/.attachments/AMIList-80fb60f9-bec5-41e7-9b5d-e75d83d83cd8.PNG)

4.	After passing the above three parameters, click on build and this build will runs for approximately 20mins. If it’s crossing 20mins please check with cp-devops team

![DevBuildWithParameter.PNG](/.attachments/DevBuildWithParameter-67f33d17-509a-4467-8e2e-38a4f2295437.PNG)

5.	If you are facing any issues with deployment any access issues or if you didn’t find any microservice name from the drop down, please check with cp-devops team (cp-devops@thomsonreuters.com



