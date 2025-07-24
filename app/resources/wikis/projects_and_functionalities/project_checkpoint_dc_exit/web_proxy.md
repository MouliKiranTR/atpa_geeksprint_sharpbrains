For DC Exit project, when running CP in the cloud we want to disable all uses of the web proxy. [Following changes made by platform engineering](https://trten.sharepoint.com/sites/intr-cloud-conversion/SitePages/Platform-Engineering--Important-Key-Dates-Impacting-Network-Services.aspx?xsdata=MDV8MDJ8fDRjNGI0ODIzNTUyZDRmOGY0ZWY5MDhkYzg0MGI2ODA1fDYyY2NiODY0NmExYTRiNWQ4ZTFjMzk3ZGVjMWE4MjU4fDB8MHw2Mzg1MzA0MzE3MDQ0NTI4NTd8VW5rbm93bnxWR1ZoYlhOVFpXTjFjbWwwZVZObGNuWnBZMlY4ZXlKV0lqb2lNQzR3TGpBd01EQWlMQ0pRSWpvaVYybHVNeklpTENKQlRpSTZJazkwYUdWeUlpd2lWMVFpT2pFeGZRPT18MXxMMk5vWVhSekx6RTVPbTFsWlhScGJtZGZUbnByTTA1NlZYbFBWMDEwVDFSbk5FMURNREJaVkVGNVRGUm5NMDVVUVhSYVZGVjVUbnBLYkU5RVpHdE9la1pxUUhSb2NtVmhaQzUyTWk5dFpYTnpZV2RsY3k4eE56RTNORFEyTXpZNU1qY3p8YWZhOWE0YjBhY2ZkNDZhMjRlZjkwOGRjODQwYjY4MDV8NzMxYWU4NWRjMGI5NGIzNmFhNTg3YWI0ODZmNjc1ZTY%3D&sdata=RWpGamJHT0Uycmt3WDFZWWZTSmoxb2ZQS2c2ei9hSGsxVGJWcUN6Q21WST0%3D&ovuser=62ccb864-6a1a-4b5d-8e1c-397dec1a8258%2CLuke.Houge%40thomsonreuters.com&OR=Teams-HL&CT=1718211474938&clickparams=eyJBcHBOYW1lIjoiVGVhbXMtRGVza3RvcCIsIkFwcFZlcnNpb24iOiI0OS8yNDA1MDMwNzYxNyIsIkhhc0ZlZGVyYXRlZFVzZXIiOnRydWV9), after May 31st 2024 any calls to the proxy from outside services (like webapp in Cloud AWS) will be restricted.

The following user story and PR added a property flag (`webproxy.enabled`) to control enabling/disabling the web proxy in all places where it is not already enabled/disabled by another property flag: 
- #164257
- !13879
- Bold/italic entries in table below reflect changes added in the above PR

## Properties
- ***Proxy host property values:***
	- `proxy = webproxy.int.westgroup.com`
	- `webproxy.hostname = webproxy.e.corp.services`
- ***Proxy flag properties:***
	-  `akkadia.service.client.webproxy.enabled`
	-  `apigarden.webproxy.enable`
	-  `auth.service.proxy.enabled`
	-  `calendar.service.client.proxy.enabled`
	-  `ce.client.webproxy.enabled`
	-  `ciam.sdk.proxy.enabled`
	-  `feature.flag.client.proxy.enabled`
	-  `gcs.es.service.client.webproxy.enabled`
	-  `neota.use.proxy`
	-  `surts.dtr.webproxy.enable`
## Proxy usage and ways to turn off:
### Usages of `webproxy.hostname`

|     **_Class Using Proxy_**      |     **_Controlling Property Flag_**     |
| :------------------------------: | :-------------------------------------: |
|      CPGCSEntitlementClient      | gcs.es.service.client.webproxy.enabled  |
|        FeatureFlagConfig         |    feature.flag.client.proxy.enabled    |
|      CPSingleSignOnService       |         ***webproxy.enabled***          |
| AuthenticationControllerProvider |         ciam.sdk.proxy.enabled          |
|       CPTrSecClientAdaptor       |        apigarden.webproxy.enable        |
|           CPAuthClient           |       auth.service.proxy.enabled        |
|         CPCalendarClient         |  calendar.service.client.proxy.enabled  |
|         CPCIAMAuthClient         |         ciam.sdk.proxy.enabled          |
|     CPContractExpressClient      |       ce.client.webproxy.enabled        |
|         CPNewsroomClient         |         ciam.sdk.proxy.enabled          |
|       CPPrivacyDataClient        |         ***webproxy.enabled***          |
| CPPrivacyDataOneTrustTokenClient |         ***webproxy.enabled***          |
|         CPAkkadiaClient          | akkadia.service.client.webproxy.enabled |
|         CPSurtsDtrClient         |        surts.dtr.webproxy.enable        |

### Usages of PROXY:

| **_Class Using Proxy_** | **_Controlling Property Flag_**  |
| :---------------------: | :------------------------------: |
|      CPHttpClient       | ***ANDed with webproxy.enable*** |
|      CPAppService       | ***ANDed with webproxy.enable*** |
|     CPProxyService      | ***ANDed with webproxy.enable*** |
|     CPHtmlPageUtil      | ***ANDed with webproxy.enable*** |
|      CPNeotaClient      |         neota.use.proxy          |

### Properties to set in Cloud CMDB:
*All should be set to `false`*
- `akkadia.service.client.webproxy.enabled`
- `apigarden.webproxy.enable`
- `auth.service.proxy.enabled`
- `calendar.service.client.proxy.enabled`
- `ce.client.webproxy.enabled`
- `ciam.sdk.proxy.enabled`
- `feature.flag.client.proxy.enabled`
- `gcs.es.service.client.webproxy.enabled`
- `neota.use.proxy`
- `surts.dtr.webproxy.enable`
- `webproxy.enabled`