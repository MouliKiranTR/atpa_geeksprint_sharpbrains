# Dinkytown calculators update process

**Document Link** https://infratools-cp-ci-use1.5463.aws-int.thomsonreuters.com/wiki/Calculators_-_General
**licensing related problem in the CI environment -** It is displaying error in calculator "KJE Calculator License Not Found for: checkpoint.ci.thomsonreuters.com".
**Solution:** Set the following b=j.kujaleip;b=false; in KJE.js file. This solution provided in the above document.

**Exsiting Updates**
The formulas for some of the calculators change on a regular basis due to things like tax rate changes. Therefore, just prior to each quarterly Checkpoint release, someone must e-mail Karl (ebert@dinkytown.net) to inquire about any changes made during that quarter. We have given Karl our yearly quarterly release schedule so he will hopefully have our changes ready 2 weeks in advance of code freeze/QA.

Karl will generally reply with a summary of the calculators that have changed and why. He will also send a download page URL containing a Download update.exe link. Update Only/DownloadKJECalc.exe link is a self extracting executable which downloads javascript/CSS/html file updates.

**Steps for Quarterly Update of Dinkytown calculators:**

**1**.Download anytime from: http://www.dinkytown.net/downloads/991791c, User id: 991791c, Password: tut67etr

**2**.Download Update Only files to separate folder. These files are limited to KJE.css, KJE.js, and calculator specific *.js.

**3**.**Note:** files KJESiteSpecific.css, KJESiteSpecific.js, and *.html files will not be included in Update Only since they are user specific customizable files.

**4**.Update changed: v10\css\extern\calcGeneral\CSS file (use e.g. WinMerge to compare downloaded files in separate folder to existing Checkpoint files)

**5**.Update changed: v10\js\extern\calcGeneral\JS files (use e.g. WinMerge to compare downloaded files in separate folder to existing Checkpoint files)

**6**.CSS needs to be minimized (e.g. https://cssminifier.com/) and checked into Checkpoint\Web\Application\main\CPWar\web\v10\cssmin\extern\calcGeneral. Non minimized version should be checked into Checkpoint\Web\Application\main\CPWar\web\v10\css\extern\calcGeneral. At some point in future, may want to look into modify build to automatically minimize changed extern CSS files from vendors.

**7**.**Note:** Not all files in the KJEUpdate.zip are updated, some of the .js might still be the same as the previous version. If they are the same then don't update them.

**8**.Set the following b=j.kujaleip;b=false; in KJE.js file. Re: Bug 122519: [Prod] College of Charleston: All calculators in Checkpoint Edge are giving the message "KJE Calculator License Not Found for: checkpoint-riag-com.nuncio.cofc.edu"

**Note:** web\WEB-INF\data\calculatorsGen.xml is a configuration file containing calculator name, hover-over, title description, and ofs-id information. Some of this information came from static *.html files from Dinkytown (e.g. <calc-desc> contains title description of calculator). Since this information is static, all references to dates have been removed, e.g. Tax/Estate Tax Planning and Tax/Payroll Deductions calculators had references to current year and 2017 Tax Cuts and Jobs Act. At times, may want to make sure static titles have not changed drastically.