# Summary
Users are unable to get to the login screen of CUAS. 

**Owner:** @<1EEF89FE-A95B-429D-8940-CDDFCF32AD59> 
**Contributors:** @<0ED19A06-8ED7-6233-8278-DD84CD11EBEE>, @<DAA2D016-8969-418B-9137-24EC1D57A506>, @<74694AFB-AB97-6599-B071-C877D06F82DF>,  @<2B24B1EC-0C3E-6D78-8168-4BBC94754190>, @<0543612D-CDD7-6D3A-93D9-009AEA1EA850>, Venkat Dangeti (CSS), Jason Rodlund (CSS), Sushma Mahesh (CSS), Abhishek Jain (CSS)
**Reported By:** Aldric Rowe
**Incident:** [INC6669317](https://thomsonreuters.service-now.com/sp?id=ticket&table=incident&sys_id=bf46c4861bd45e1064d45574604bcb2a) (Separate from the DB issue)
**Related Support Request:** [RITM4210773](https://thomsonreuters.service-now.com/sp?id=ticket&table=task&sys_id=66d1c4c61b5856940f272068b04bcb03)

## Root Cause
When setting up the Production Cloud environments for CUAS we needed to update CMDB URLs to be able to test it with internal URLs before the cut-over to prod. Flipping these values back to the the public prod domain should have been part of the CUAS cut-over runbook. This item was missed and thus was missed during the cut-over activities. This issue was avoidable.

## Investigation 
1. The customer has had their browser cache and cookies clear and that is no help.
1. Looking at the screenshot it _isn't a CUAS error_. It is an error getting returned prior to CUAS
1. @<1EEF89FE-A95B-429D-8940-CDDFCF32AD59> found that the CMDB did not have the Prod URL values changed back to `https://cpadmin.thomsonreuters.com`
   1. There were a number of URLs that had not been moved back to the Prod domain name.
   1. This then impacted multiple different CUAS features including login.
1. I also looked at the Checkpoint application properties in Prod and verified that the CUAS URLs are correct. We are all good from a Checkpoint front. This is a CUAS only incident.

## Impact: 
1. All external users logging into CUAS. 
   1. The CMDB property tells CUAS what to send to CIAM as a login callback
   1. Once the user logs in through CIAM the CIAM platform uses that login callback to redirect the user back to CUAS.
   1. The CMDB property is for an internal URL which customer's can't access.
   1. So, a customer is redirected after login to a site they can't access: `https://cpadmin-prod-use1.04032.aws-int.thomsonreuters.com`
<br/>
   * Only 13 customers called in reporting the issue
   * This is only an issue with External Customers and does not impact Internal users as we have access to the private URLs while we are on the TR network or on zScaler.
<br/>
1. External users who login on the TR network doesn't work either and it can be seen that the URL the user is brought back to is incorrect with the value of `https://cpadmin-prod-use1.04032.aws-int.thomsonreuters.com`
   * This is not a common use case.
   * This is what prevented this from being caught on CUAS cloud cut-over.
<br/>
1. Seamless by Web Service returned incorrect the internal CPReg URL of `https://cpreg-prod-use1.04032.aws-int.thomsonreuters.com`
   * New users from CliftonLarsonAllen could not register
   * This is the only customer on Seamless by WebService.
   * This login method will be decommissioned after migration of CliftonLarsonAllen to SAML.
<br/>
1. The Walk-in and Remote Walk-in strings we share with customers were broken and displaying `https://cpreg-prod-use1.04032.aws-int.thomsonreuters.com`
   * If these links were shared or emailed to customers on August 28th or August 29th those links will be incorrect.
   * To our knowledge this did not occur.
<br/>
1. The BigMachines calls returned the incorrect OMCUAS URL of: `https://omcuas-prod-use1.04032.aws-int.thomsonreuters.com`
   * Sales reps could still get to OMCUAS-UI but they saw an error message about the Wijmo grid license.
   * This gave the sales reps issues and support request: [RITM4210773](https://thomsonreuters.service-now.com/sp?id=ticket&table=task&sys_id=66d1c4c61b5856940f272068b04bcb03)

## Resolution Steps 
| Order | Task | Owner | Ticket | Status |
|-------|------|-------|--------|--------|
|1| Submit CMDB ADO ticket | @<1EEF89FE-A95B-429D-8940-CDDFCF32AD59> | [ADO #2068783](https://dev.azure.com/TR-Legal-Cobalt/Cobalt%20TFS%20Central/_workitems/edit/2068783) | Complete |
|2| Request Change ticket to be created by Platform CM | @<1EEF89FE-A95B-429D-8940-CDDFCF32AD59> || Complete |
|3| Emergency Change Ticket creation | Jason Rodlund | [CHG1726928](https://thomsonreuters.service-now.com/nav_to.do?uri=%2Fchange_request.do%3Fsys_id%3Dd96b204a875852d4cef3a93e3fbb3588%26sysparm_stack%3D%26sysparm_view%3D) | Complete | 
|4| Complete Emergency Chain Questionnaire | @<1EEF89FE-A95B-429D-8940-CDDFCF32AD59> | | Complete |
|5| Change got approve for the evening of 08/29 | Cobalt Services Support(Jason Rodlund) | | Complete |
|6| Update CMDB Prod Properties | Cobalt Services Support(Sushma Mahesh) | | Complete |
|7| Redeploy CUAS-API in Cloud Prod | Cobalt Services Support(Abhishek Jain) | | Complete |
|8| Verify deployment and emergency fixes | @<1EEF89FE-A95B-429D-8940-CDDFCF32AD59>, @<DAA2D016-8969-418B-9137-24EC1D57A506>, @<74694AFB-AB97-6599-B071-C877D06F82DF> | | Complete |
|9| Close Change and Incident | Cobalt Services Support(Abhishek Jain) | | Complete |

## Change Request Verification
1. An external user can login.
1. Emails sent to users have the correct CUAS prod URLs.
1. Validate that a Seamless by WebService call returns the correct URL.
1. Validate that the Override token URLs in SSO setup are correct.

## Emergency Change Approval Questionnaire Response
**Summary of what the change is:**
This is a CMDB property value change. The CUAS URLs configured in the CMDB properties are currently pointed to the wrong URL and is pointing internally. This impacts login to CUAS and the Seamless by WebService registration process.

**Why is it needed?**
Some external Customers are unable to login to CUAS.

**What is the current impact without the change implemented?**
Some customers will not be able to access the application which they use to manage their Checkpoint users. 1 customer will not be able to register new users.

**What applications are impacted?**  
CPAdmin-UI and CPReg-UI are both impacted. The CMDB change is applied to CUAS-API (Checkpoint User Administration System). This will thusly impact the CPAdmin-UI and CPReg-UI as a result.

**Who are the customers affected?** 
13 customer and growing
 
**What are the risks of implementing the change?**  
Limited risk. If the implementation of this change is unsuccessful it doesn’t impact the customer any more than it does right now.
 
**What are the risks we face if the change is not implemented at the requested time?** 
Some customers will continue to have this error. Customer support will have to continue to tell the customers they cannot access or use this application.
 
**Has this change been tested in a lower environment?** 
No, these are production environment specific settings. These values will not work in a lower environment and just cause that application to no longer allow users to login. 
 
**What checkout/verification procedures do we have and who performs them?**  
We need to verify: 
* An external user can login.
* Emails sent to users have the correct CUAS prod URLs.
* Validate that a Seamless by WebService call returns the correct URL.
* Validate that the Override token URLs in SSO setup are correct.
 
**Why it is implemented as an Emergency Change?** 
Because we have customers that cannot access the application and we need to get this resolved quickly to give our customers access to the application.
 
**Was there any TechM dependency?** 
No

**If yes, please elaborate.** 
 
**If no, then why the change is assigned to COBALT-SERVICES-SUPPORT?**
This has been assigned to COBALT-SERVICES-SUPPORT as they will perform the CMDB update and redeploy of the CUAS-API application.
 
**Are there any related Incidents for this change? And any downtime included during the deployment?** 
Yes, INC6669317
The changes should be applied to servers on a rolling bases so there is no downtime.
 
**Any TR network or infra-side applications be impacted (TR-owned or any 3rd Party application) due to this change?**
No
 
**Director(s) who have approved**: Pending
<br/>
<br/>
## Screenshots of Error Reproduction
Recreation of the external customer issue. This must be done from a computer off the TR Network.

![image.png](/.attachments/image-9fa6d748-3a31-48b5-b609-67a35311be06.png)

Recreation of Seamless by Web Service

![image.png](/.attachments/image-0d2aca12-314b-43f5-af4b-fa4a55db8908.png)

Recreation with "external user" on the TR Network. This is what happens once you get redirected back to CUAS after a login through CIAM. 
1. It does not log you in
1. It has the incorrect URL

![image.png](/.attachments/image-fd0a1af1-1952-4600-8ad2-d2f0c50d463a.png)


Recreation of the registration links being incorrect.

![image.png](/.attachments/image-2251da24-1f8a-4514-a6e0-5968d5cd63be.png)
