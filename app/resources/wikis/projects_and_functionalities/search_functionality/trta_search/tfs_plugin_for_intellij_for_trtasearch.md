Please follow the following steps to connect your local TRTASearch project with th eTFS repo for TRTASearch using IntelliJ-
1. First install "Azure DEVOPS" plugin for IntelliJ.
2. Get from VCS.
3. Select "Azure DevOps TFVC" from drop down.
4. Click 'clone'.
5. Select "Azure DevOps Services" Tab and click sign in.
6. A pop up window will come up with a Code for use in microsoft authentication process.
7. You can login using SSO after putting in the code in the link provided in the pop up wondow.
8. After completing authentication you will be presented with a list of repositories within cobalt. 
9 Select 'Core Search' to connect to the repository and create a workspace.

You will need the following to set up the TFVC-
1. Go to https://github.com/JetBrains/team-explorer-everywhere/releases and download and extract TEE-CLC-14.135.3.zip (your version may be different)
2. In the unzipped folder you will find tf.cmd which you will need to link in IntelliJ. Go to Poject Settings -> Version Control -> Azure DevOps Services /TFS (You need to install this plugin from IntelliJ marketplace) 
