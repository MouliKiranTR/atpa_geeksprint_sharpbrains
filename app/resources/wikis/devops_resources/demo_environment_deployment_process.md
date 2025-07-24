Demo Environment Deployment Process
===================================

Overview
--------

*   Daily deployment of `cp_web-app` to DEMO happens automatically at **7:00 AM IST**.
    
*   Branch used depends on the code freeze status:
    *   **Outside code freeze:** deploy from **main** branch.
        
    *   **During code freeze/HotFix:** deploy from **release** branch.
        
    
**Important!**   DevOps manually switches the deployment branch by enabling/disabling the scheduler job.
    

Checking Deployed Version
-------------------------

*   Check deployed version here:  
    DEMO environment [https://infratools-cp-demo-use1.5463.aws-int.thomsonreuters.com/cmdb/verticals](https://infratools-cp-demo-use1.5463.aws-int.thomsonreuters.com/cmdb/verticals "https://infratools-cp-demo-use1.5463.aws-int.thomsonreuters.com/cmdb/verticals")
    QED endvironment [https://infratools-cp-qed-use1.1434.aws-int.thomsonreuters.com/cmdb/verticals](https://infratools-cp-qed-use1.1434.aws-int.thomsonreuters.com/cmdb/verticals "https://infratools-cp-qed-use1.1434.aws-int.thomsonreuters.com/cmdb/verticals")
    
*   Version names:
    *   **Main branch:** `yy.mm.dd.nn` format.
![==image_0==.png](/.attachments/==image_0==-6f5886ed-f023-4f80-bb75-a27c98a79f3d.png) 
        
    *   **Release branch:** contains the word `release`.
![==image_0==.png](/.attachments/==image_0==-34d4853f-ec8d-4947-b9d8-65a8f98db777.png) 
        
You can also check for the GitHub Action to see from which branch the builds are happening GitHub Actions for build info: [https://github.com/tr/cp_web-app/actions](https://github.com/tr/cp_web-app/actions "https://github.com/tr/cp_web-app/actions") 
    ``
    

On-demand Deployment (handled by DevOps)
-----------------

*   If an urgent deployment to DEMO is required **before the daily scheduled job**, you can request a **manual deployment** by contacting the DevOps team.
    
**Important!** Deployments from the **main** branch are **not allowed during the code freeze period**