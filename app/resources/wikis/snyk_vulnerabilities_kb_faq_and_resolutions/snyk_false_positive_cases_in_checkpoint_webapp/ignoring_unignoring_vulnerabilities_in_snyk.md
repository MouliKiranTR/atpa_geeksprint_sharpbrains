If Snyk flags false positive cases, we can ignore them in Snyk Portal, which would later be reviewed by the team, the Custodians can accept or reject the request.

**Ignoring Snyk Vulnerability**
- Visit https://app.snyk.io/ and navigate to your project.
- You can view all the Open Vulnerabilities under Code Analysis as shown :

![Ignore1.png](/.attachments/Ignore1-36622535-be0f-4322-ba1f-2717c0ebc3f1.png)

- Left hand side you can see the ignored count as 13. Click on Ignore button if the vulnerability is false positive.

![Describe_Vulnerability.png](/.attachments/Describe_Vulnerability-3ada6101-689d-4e41-8705-a1a349e6be4b.png)

- When you _Ignore_ please specify reason from the drop-down: Not Vulnerable, Ignore Temporarily, Ignore Permanently.

- In Ignore Comment : Specify and describe the reason why you have to _Ignore_ the vulnerability. 
- Select Expiration if required and Click Confirm. The vulnerability is now Ignored.

- When you check the status of Ignored in left-hand filters, the count would increase from 13 to 14, since we ignored one vulnerability as shown.

![Check_Ignored.png](/.attachments/Check_Ignored-58e2c337-4085-483b-9111-281f67785bf2.png)

**Unignoring Snyk Vulnerability**

- From the above image, you would see options Unignore, Edit Ignore. 
- If there's some change in Ignoring details, click on Edit Ignore and edit respective fields.
- If there is a proper fix available and we have ignored the request, just click on the Unignore button.
- Once Unignore button is clicked the count in the left-hand filters would change again from 14 to 13 as shown.

![Ignore1.png](/.attachments/Ignore1-08ab6806-8642-4386-9320-3b5f09e272d2.png)

