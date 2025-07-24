[[_TOC_]]

## Project Resources:
- ADO Area Path: _Checkpoint\Checkpoint CoCounsel_
- [Stories Backlog](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_backlogs/backlog/House%20Tyrrell/Stories)
- [Features Backlog](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_backlogs/backlog/House%20Tyrrell/Features)
- [Template feature](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_workitems/edit/166346)
- [Template story](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_workitems/edit/166328)
- [Milestone 1 query](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_queries/query/af449445-3227-458f-aa79-220c39e5bbca/)
- Teams Site:  [Checkpoint Gen AI | General | Microsoft Teams](https://teams.microsoft.com/l/team/19%3AUs-PfZOlxvWEzZ2Q1ad6RRY2acAwYIhflbxBG7kLMzw1%40thread.tacv2/conversations?groupId=69d15602-4a12-41d4-af45-5909f8e7abd1&tenantId=62ccb864-6a1a-4b5d-8e1c-397dec1a8258)
  - We are using the same Teams site being use for all the Checkpoint AI work.
- Teams Channel:  [Checkpoint Gen AI | AI Assistant | Microsoft Teams](https://teams.microsoft.com/l/channel/19%3Ae6cafec385ee44ab9ab4f496a41536ba%40thread.tacv2/AI%20Assistant%20MFE?groupId=69d15602-4a12-41d4-af45-5909f8e7abd1&tenantId=62ccb864-6a1a-4b5d-8e1c-397dec1a8258)
- Teams tech folder:  [AI Assistant](https://trten.sharepoint.com/:f:/r/sites/CheckpointGenAI635/Shared%20Documents/General/Architecture%20%26%20Dev?csf=1&web=1&e=QDD1lV)
  - Note the folder is under Documents → General → Architecture & Dev
- [Project Plan](https://trten.sharepoint.com/:x:/r/sites/CheckpointGenAI635/_layouts/15/Doc2.aspx?action=editNew&sourcedoc=%7B6627393e-76a9-4254-885f-26235404338a%7D&wdOrigin=TEAMS-MAGLEV.teamsSdk_ns.rwc&wdExp=TEAMS-TREATMENT&wdhostclicktime=1724961593262&web=1)
  - [Example of CP Gen AI Project Plan 2024](https://trten.sharepoint.com/:x:/r/sites/CheckpointGenAI635/Shared%20Documents/General/Roadmaps(inc.%20RAID%20log),%20Estimates,%20Planning%20Artifacts/Project%20Plan%20-%20Checkpoint%20Gen%20AI%202024.xlsx?d=w6a449680ad7c458f9ae318cef1a8c2d4&csf=1&web=1&e=bc7FDf)

## CoCounsel
- CoCounsel 2.0 Atrium Site
- CoCounsel PROD- https://cocounsel.thomsonreuters.com/work
- CoCounsel CI- https://cocounsel-ci.thomsonreuters.com/work
- CoCounsel INT- https://cocounsel-int.thomsonreuters.com/work
- CoCounsel QA- https://cocounsel-qa.thomsonreuters.com/work

## Tech Resources
- [CARI Skill API’s Atrium Page](https://trten.sharepoint.com/sites/CaRSOperations/SitePages/RAS/CARI%20Skill%20API.aspx#overview)- good overview of skill servers with links to other documentation
- [Architecture Diagram](https://lucid.app/lucidchart/ab069a25-3b5c-4625-bd32-3a2bae9d6c8e/edit?viewport_loc=-791%2C-329%2C2153%2C1140%2CtUMYdnBc.HzV&invitationId=inv_14b42940-c74a-4df1-9215-aeba9cb235c7) – draft, tab labeled “AI Assistant Architecture”
- [CaRS Logical Architecture Diagram](https://lucid.app/lucidchart/d2ecce87-b27a-4f00-ac1b-3a5764c7faba/edit?viewport_loc=-227%2C-8082%2C2779%2C1291%2Cqlnjn0KbYBPF&invitationId=inv_4b7f71d8-287f-4c6a-8431-1970549d20e3)
- [Tech Estimate](https://trten.sharepoint.com/:x:/r/sites/CheckpointGenAI635/_layouts/15/Doc.aspx?sourcedoc=%7BB3EEB8BB-ECF8-42A8-B7A7-02E644F3F09E%7D&file=CP%20AI%20Assistant%20Skill%20Estimate.xlsx&action=default&mobileredirect=true)
- [WL / PL Figma](https://www.figma.com/design/8K892LYLbAaTS1wubdh6na/PL%2FWL%2FCoCounsel-Integration-Alignment?node-id=98-69732&t=qyYW4PVbm5i8zOaj-0) (AI Assistant)
- [Practical Law – CoCounsel: Frontend Architecture](https://lucid.app/lucidchart/a31a6b90-bb33-4ffd-b22d-73979007febc/edit?view_items=aKabp6qNLpt0&invitationId=inv_cff73d6f-5f50-4727-968d-cf9fdc193011)
	- While the title of the chart is PL / CoCounsel the integration approach is the pattern for WL and Checkpoint.
- [cars-shared_pipeline-templates](https://github.com/tr/cars-shared_pipeline-templates?tab=readme-ov-file)
	- Documentation for creating and deploying a container – the starting point for building a Skill API.
	- Documentation is for CaRS Tech Suite.  For the Skills API the tech suite is CARI.
- [cari-shared_pipeline-parameters](https://github.com/tr/cari-shared_pipeline-parameters/tree/main/project-configs/a208625-skill-apis)
- [https://github.com/tr/.github/tree/main](https://github.com/tr/.github/tree/main) - TR GitHub Organization Actions-based Workflows
- [tr/cars-shared_java-api-template](https://github.com/tr/cars-shared_java-api-template) – A Java API template with a basic Hello World endpoint, with security requiring a GCS authentication token
- [CICD self-service portal](https://self-service.cicd.int.thomsonreuters.com/) – used to subscribe to CICD patterns and create PR for GitHub workflows
- [cari_skill-api-read-write · tr Team](https://github.com/orgs/tr/teams/cari_skill-api-read-write) – team with read/write access to CARI Skill API repos (request access to join this team which will grant write access to all CARI Skill API related repos)
- [tr/cari-skill-api_caretaker-repo - Caretaker repo for CARI skill API related repositories](https://github.com/tr/cari-skill-api_caretaker-repo) (including rotating shared credentials)
- Cumulus
	- Cumulus is a deployment solution maintained by Platform Engineering, and developed by contributors across Thomson Reuters
	- [Cumulus documentation](https://github.com/tr/cumulus_python-cumulus-cli/blob/develop/README.md)
	- [Atrium page](https://trten.sharepoint.com/sites/intr-cumulus)
	- [Hands-on lab](https://trten.sharepoint.com/sites/intr-cumulus/SitePages/Cumulus-Training-Materials--Hands-on-lab.aspx)
- [API Documentation](https://developerportal.thomsonreuters.com/research-skills/swagger_openapi_document/ai-assisted-legal-research/18248/001#/) for CARI skill APIs
	- You need to login to the developer portal for the link to work (may need to click on it twice).
	- For AALR and Ask PL the APIs paths are the same, however, the payloads are different, and I don’t think they are captured in the documentation.
- CARI skills repos:
	- [cari-skill_ai-assisted-legal-research](https://github.com/tr/cari-skill_ai-assisted-legal-research)
	- [cari-skill_askpl](https://github.com/tr/cari-skill_askpl)
        - [cari-skill_corss-cutting](https://github.com/tr/cari-skill_cross-cutting) - A library of functionality to be reused across CARI skills
- CARI MFE repos:
	- [tr-cobalt-aalr-mfe](https://github.com/tr/tr-cobalt-aalr-mfe)
	- [tr-cobalt-askpl-mfe](https://github.com/tr/tr-cobalt-askpl-mfe)
	- [tr-cobalt-components](https://github.com/tr/tr-cobalt-components) (for shared components between WL AALR and PL AskPL
- Resources from CoCounsel team:
	- [Documentation for contract between an application and AI Assistant MFE](https://trten-my.sharepoint.com/:w:/g/personal/ark_roy_thomsonreuters_com/EUrBemoWTDFHui5i_QEwYPABl_m3h4CV7OBD4E8GMr6ztg?e=VnD7qM)
	- [Sample skill](https://github.com/tr/coco-skill-server-example)
	- [Skills Integration Guide](https://github.com/tr/ai-assistant-doc/blob/update-skills-section/02_integration_guide/skills.md)
	- These documents are provided for reference – our implementation will follow the CaRS pattern.
- [API Documentation](https://developerportal.thomsonreuters.com/cari-capability-api) for CARI capability APIs
	- You need to login to the developer portal for the link to work (may need to click on it twice).
	- “auth-access-mgmt” under REST documents contains documentation for CARI Auth API
- Auth Token Flows
	- [AI Assistant High Level Vision - Auth Token Flows](https://lucid.app/lucidchart/504954ed-91f0-4985-b7d5-da50d2e84612/edit?invitationId=inv_4ec2cfab-4f31-4511-8da4-caa470cde3a7&page=q-v77X5RKCky)
	- [API Authorization: OAuth Patterns in CIAM and their OnePass Equivalents](https://lucid.app/lucidchart/5c620807-88cf-4df7-8f97-aee43a1c99a2/edit?invitationId=inv_cef5f3e2-7bdd-4c37-aa34-b2991ba03a9c&page=frPy1-L_EPIL)
	- [Developer portal: Checkpoint Edge Search API Authentication](https://developers.thomsonreuters.com/pages/api-catalog/f0ffe0b4-899e-455f-af3b-73e554cb5f10#Authentication)
	- [CIAM Platform Atrium](https://trten.sharepoint.com/sites/Platform-CIAM?xsdata=MDV8MDJ8fDU3ZTMxNmI0NWZiMjQ3M2IxZTY2MDhkY2QyYTRiM2I5fDYyY2NiODY0NmExYTRiNWQ4ZTFjMzk3ZGVjMWE4MjU4fDB8MHw2Mzg2MTY4NTIwMTE0OTA5MTh8VW5rbm93bnxWR1ZoYlhOVFpXTjFjbWwwZVZObGNuWnBZMlY4ZXlKV0lqb2lNQzR3TGpBd01EQWlMQ0pRSWpvaVYybHVNeklpTENKQlRpSTZJazkwYUdWeUlpd2lWMVFpT2pFeGZRPT18MXxMMk5vWVhSekx6RTVPakl3TnpCaVpUZ3lMVEkyWlRjdE5HUmpPQzFoTWpBMExUQXlOVE14WVdObVptWmpNMTlqWkdRMk5XRmxaaTA0WlRrNUxUUXpPVEF0WVdRNE5pMWxZalk0TURrMFl6QmxNREpBZFc1eExtZGliQzV6Y0dGalpYTXZiV1Z6YzJGblpYTXZNVGN5TmpBNE9EUXdNREUxT1E9PXxmNzFmY2I5OGFkYmY0NDgwYmMwZTA4ZGNkMmE0YjNiNnwxNTMwNGYzNDdmMjc0NjFjOGQ3ZmQ3MDMzZWU1YTEzYQ%3D%3D&sdata=S0NRWTVaZEVNLzdTSkdhU1dDL0pvZ2d1bWJIN1JTZEpUYitmUlIrMUpYdz0%3D&ovuser=62ccb864-6a1a-4b5d-8e1c-397dec1a8258%2Cjosh.schmidt%40thomsonreuters.com&OR=Teams-HL&CT=1726499760592&clickparams=eyJBcHBOYW1lIjoiVGVhbXMtRGVza3RvcCIsIkFwcFZlcnNpb24iOiI0OS8yNDA4MDIxMjAxMSIsIkhhc0ZlZGVyYXRlZFVzZXIiOmZhbHNlfQ%3D%3D)

## Checkpoint AI Assisted Research (existing Gen AI implementation for CP Research Application)
- [Architecture diagram](https://lucid.app/lucidchart/ab069a25-3b5c-4625-bd32-3a2bae9d6c8e/edit?viewport_loc=-1303%2C-515%2C4992%2C2319%2C0_0&invitationId=inv_14b42940-c74a-4df1-9215-aeba9cb235c7) – tab labeled “Architecture”
- Checkpoint Gen AI Demo by Ravi
	- [Diagram](https://lucid.app/lucidchart/1a3f7bbf-d46d-4322-9c17-2e211bd44ce4/edit?viewport_loc=-19%2C51%2C4039%2C1876%2C9R-7exwcr6h5&invitationId=inv_492f8c33-5f9c-4a9f-b801-ebfcddc399d5)
	- [Recording](https://trten-my.sharepoint.com/:v:/r/personal/mostafijur_rahman_thomsonreuters_com/Documents/Recordings/Bi-Weekly%20Tech%20Meeting-20240830_100215-Meeting%20Recording.mp4?csf=1&web=1&e=xFVZu0&nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D)
- [[INT] RAS Content Access Novus APIs](https://content-access-int.plexus-ras1-ppuse1.5771.aws-int.thomsonreuters.com/swagger-ui/index.html)
- [[DEV] Swagger - CP API (AI Assistant)](https://dev.checkpoint.thomsonreuters.com/app/api/swagger-ui.html#/AI_Assistant_Controller) – first need to sign into [CP application](https://checkpoint.ci.thomsonreuters.com/app)
- [[CI] Swagger - RAS AI Conversations](https://ai-conversations-ci.plexus-ras1-ppuse1.5771.aws-int.thomsonreuters.com/docs)
- [[QA] Swagger - RAS LLM Proxy](https://llm-proxy-qa.plexus-ras1-ppuse1.5771.aws-int.thomsonreuters.com/docs#/)
- [Checkpoint GAIL Service](https://github.com/tr/cp-gail_service) - RESTful API repo for Checkpoint GAIL (Generative AI and LLM)
- [API Documentation](https://developerportal.thomsonreuters.com/checkpoint-search-api/getting_started/authentication) for CP Search API Authentication
	- You need to login to the developer portal for the link to work (may need to click on it twice).
