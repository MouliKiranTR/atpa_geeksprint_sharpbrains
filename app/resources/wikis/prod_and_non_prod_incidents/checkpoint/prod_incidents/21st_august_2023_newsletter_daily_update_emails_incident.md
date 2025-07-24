**Short description**
The regular daily email updates to checkpoint users did not get sent out on the morning of 21st August, 2023. 

**Detailed explanation**

After investigation with Jamaica from DevOps and Hong Tu, the following problem was identified-

- Active Build (which can be set manually on the admin page) was not updated to the correct (ie current) version of cp-web-app.  
- The active version was _20230802_ instead of the current version of _20230811_. This caused the batch process to go into the state of "**_DO PROMOTE_**" that indicates version mismatch. 
- This caused the batch jobs that run these newsletters to fail, because when they run they require at least half the usage to be on that active version.  
- Since the old 20230802 version was just turned off on 21st August, as part of the release steps (it was drained on Friday, 18th August and turned off on Monday, 21st August) – this was a problem.

**Resolution**
- Update the active build manually from the cpadmin page.
- This was done for QA, preprod and prod.

**Root cause analysis**
- For QA and preprod deployment, the problem was within a downstream Jenkins job that is responsible to set the active build. 
1. From the console output from [QA](https://cpjenkins.int.westgroup.com/job/Checkpoint/job/Deploy/job/Qa/job/deploy2QA/976/console) and [preprod](https://cpjenkins.int.westgroup.com/job/Checkpoint/job/Deploy/job/ASE/job/Preprod/job/deploy2Preprod/116/console) deployment we can see that the active_build and current_build was not set properly-

preprod console out sample-

```
++ wget -q -O- --user=******** --password=*************--no-check-certificate https://preprod.checkpoint.thomsonreuters.com/app/adminservlet/CPBuildServlet
++ grep -i 'value="build_'
++ awk -F '"' '{ print $2 }'
++ awk -F = '{ print $4 }'
+ active_build=
++ wget -q -O- 'http://preprod.checkpoint.thomsonreuters.com/app/sessionless?jsp=%2Fv10%2Fjsp%2FservInfo.jsp'
++ grep -i 'build name'
++ awk '{ print $NF }'
++ tr -d '</td>'
++ tr -d '\r'
+ current_build=20230811
+ '[' '!' '' = '' -a '!' 20230811 = '' ']'
+ subject='***ERROR*** Unable to get active_build or current_build.
```

However, this step is not identified as one of the critical steps to pass/fail a deploy job and hence the deployment was deemed successful. 

The takeaways identified from this was- 
1.	fix the user Jenkins is utilizing to update the builds (hopefully just a pw rotation will resolve this)
2.	update the deploy jobs so that they fail when the active does not update

**Update-**
The credentials for these Jenkins jobs did not rotate for some reason with the last rotation, which is why they got into a bad state and stopped updating the active build.  It has been fixed, and DEVOPS will be double checking that they get updated with each rotation going forward.

However, the Prod environment is different as it does not actively set the active build within the deploy job.  For Prod there is a separate job to set the active build that is in the CHG ticket for the ASEs, this job was  missed when going over the CHG tickets. To summarize, – the active build gets set within the deploy job for qa/preprod – but for prod it gets set within a totally different Jenkins job that gets run after the deploy.
