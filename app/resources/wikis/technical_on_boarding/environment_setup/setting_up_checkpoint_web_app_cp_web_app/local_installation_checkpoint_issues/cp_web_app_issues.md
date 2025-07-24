Here you can find issues that developer have faced during the development in local environment for cp_web-app application

# Local user authentication

| Issues description (attach screenshot to demonstrate problem if it is possible) | Stacktrace if it is avaialable (add only valueable information from stacktrace) | Analysis of problem | Solution of problem |
|---|---|---|---|
| Taking long time for user Authentication and After some time it is showing eror message.(Login Error!Your User ID and Password are valid.You cannot login because your subscription has not been activated or it has expired.Please contact your web administrator, or contact Technical Support at 1-800-431-9025 or by e-mailing Technical Support)| Machine: USCDEVPW110115#080:ce314a.f<br>Severity: Non-Fatal<br>Error ID: CPTOCService.getTOCNodesForClass.Ex<br>UserID: firstname.lastname<br>Novus m/c,<br>env: ,novusaws:client<br>Novus Coll (D,T): trtaintset:trtaintset<br>Text: App Setup Error name=ODS<br><br>Stack Trace: com.tta.checkpoint.servlet.CPException<br> at com.tta.checkpoint.servlet.CPTOCService.getTOCNodesForClass(CPTOCService.java:1899)<br>Caused by: com.westgroup.novus.productapi.NovusException: Search Controller timed out waiting for engine.<br>at com.westgroup.novus.productapi.SearchImpl.getProgress(SearchImpl.java:990)|As per  error logs it seems Novus cloud issue. |  |

