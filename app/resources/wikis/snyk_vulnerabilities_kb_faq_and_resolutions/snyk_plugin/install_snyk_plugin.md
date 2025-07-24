To Install Snyk in our local IntelliJ IDE., Go to Settings --> Plugins. Search for Snyk and install Snyk plugin as shown :

![image (1).png](/.attachments/image%20(1)-7b8e7ed2-7e3d-4d18-8891-73b21ff60c56.png)

Once installed, Restart IDE.

Snyk would now be installed as shown and we shall proceed for the setup.

![image (2).png](/.attachments/image%20(2)-224c683d-04e7-4111-b97e-9dca3c061755.png)

Make sure you have access to https://app.snyk.io/ . If you need support, please check https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/553/Snyk-Vulnerabilities-KB-FAQ-and-resolutions?anchor=requesting-access-to-snyk
Now in the IDE click on Trust Project and Scan as shown above, it opens your default browser as attached below. Click on Grant Access. 

![image (3).png](/.attachments/image%20(3)-7eb3c506-877c-4c1f-9249-87b52f574061.png)

Once when we are back to IDE, it starts Snyk Analysis 

![image (4).png](/.attachments/image%20(4)-531cab1d-4329-4be5-affd-a351d6ded105.png)

When we restart IDE, the analysis would not be stored we may have to run again by clicking the play button or Run Scan option as shown :

![image (5).png](/.attachments/image%20(5)-44bf8a79-92e1-4996-8fd9-05bf332c07f8.png)

Common Issues Faced while running Snyk Analysis on web-app: 

- Out of Memory Issue
- Snyk keeps analyzing for so long 

More details can be found at - [Known issues](/Snyk-Vulnerabilities-KB-%2D-FAQ-and-resolutions/Snyk-Plugin/Known-issues)

These issues are commonly seen in newer versions of IntelliJ and can be overcome by 

- Either running only the sub-directory where we want analysis, since web-app is a single repo and larger project
- Or we can install another downgraded version(2020.3.4) of IntelliJ IDE which uses lower version of Snyk(2.4.64) shown below :

![image (6).png](/.attachments/image%20(6)-f24407cb-c18c-4153-bc3b-7ade2d45b6d5.png)

![image (7).png](/.attachments/image%20(7)-a390f32f-2168-426e-9021-38f5e382dcae.png)

- When we downgraded, this is how Snyk runs analysis locally :

![image (1).png](/.attachments/image%20(1)-84e51d1b-00e0-4060-8eb2-548f3e82a3e3.png)