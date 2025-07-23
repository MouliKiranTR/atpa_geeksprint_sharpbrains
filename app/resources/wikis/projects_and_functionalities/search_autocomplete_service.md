The search autocomplete project allows the application to provide typeahead suggestions to users in both Classic and Edge views. The autocomplete service is hydrated with search queries run by customers. Such queries are written into our log files so we can extract them and feed the service.

Even though the user interface does not call the autocomplete service directly —it uses the autosuggestV2 endpoint that complements the response with history entries—, most of the proposed search phrases come from the Autocomplete service.

![image.png](/.attachments/image-99152807-bb53-4d5f-a000-f426f37764b8.png).
![image.png](/.attachments/image-0bfdfbef-83b8-4522-9627-4e29e4dfbad9.png)

# High-level design [Current solutions]

![image.png](/.attachments/image-1fcf838c-5dcd-4510-ab2a-80fd7670a947.png)


The legacy solution uses a series of manual steps on on-premises resources. However, some of those resources were migrated in 2019 and the process was not reinitiated so new queries and terms are not currently fed into the service to populate the typeahead suggestions.

1. Logs from all environments are pulled from the Web App servers daily using a nightly batch process (runAll.bat) in the LogProcess server (c548kqncplog). Those logs are stored on a NAS server (ciscInt-e0897).
   - Note: Logs can manually pulled using the LogProcess UI application. For this process, only `userAct` logs can be fetched.
     ![image.png](/.attachments/image-220b566f-93c8-43a9-8472-5ad0e815db82.png)
2. Once logs are in the server, they need to be manually processed by running the `userSrch` process. That process takes the `userAction` logs from the previous step, parses them, and generates the "queries" report. That report looks like the following:
   ![image.png](/.attachments/image-a595f3f8-bf65-47f2-97aa-137deeab91d1.png)
   **Note:** This process is no longer run by anyone from the development team.
3. In the same LogProcess server, another batch process is manually run: the `stage1.bat` process. This process runs the `com.tta.checkpoint.searchauto.MainBuildSearchAutoCompleteData` application from the Search Autocomplete Data using the `serviceStage1` argument. The process validates search queries using a spellchecker, an inclusion list, and an exclusion list. As an output, it generates two files, a temporary query completion data and a queryCompletion Excel file.
   **Note:** This process is no longer run by anyone from the development team.
4. Once the previous step is complete, the development team uploads the queryCompletionUpdated.xls Excel file to a Sharepoint. Then, send an email to the Editorial team for them to review it.
   **Note:** This process is no longer done by anyone from the development team.
5. The Editorial team manually reviews the file. Check which new records should be included or ignored. Once this process is complete, they need to upload the new version of the excel file to the Sharepoint (renamed to queryCompletion.xls) and let the development know so they can run the next steps.
   **Note:** This process is no longer done by the Editorial team
6. The development team runs the `stage2.bat` process. This process runs the `com.tta.checkpoint.searchauto.MainBuildSearchAutoCompleteData` application from the Search Autocomplete Data using the `serviceStage2` argument. The process will take the temporary query completion data from point 3, and the Excel file from point 5 to generate the final result: the final queries per practice area in the form of a Trie data structure.
   **Note:** This process is no longer run by anyone from the development team.
7. Once the final files are generated from the previous step, the development team needs to manually push those files into the NAS storage server (cisclnt-e0076, cisclnt-e0075, cpsprod-f0401, or cpsprod-e0191) for the Search Autocomplete Service.
   **Note:** This process is no longer done by anyone from the development team.

8. The Search Autocomplete server takes the files from the NAS server and loads them so that the Web Application can get the typeahead suggestions.


![image.png](/.attachments/image-67a59518-6434-423e-a6f3-893d8debbb1a.png)

## Resources:
- Web App servers (log generators) - RHEL servers.
- Log Process Server - Windows Servers, connect using Remote Desktop with:
  - domain: c548kqncplog.ecomqc.tlrg.com
  - port: 5616
  - username: Ecomqc\srvcpdevops
- NAS Server, mounted to F: network drive  in Log Process Server
  - domain: ciscInt-e0897.int.thomsonreuters.com
- FTP Servers (Linux):
  Username: webappteam 
  - c803gqkcpprpb.int.thomsonreuters.com
  - c883wyscpprpb.int.westgroup.com
  - c006zuncptepb.int.westgroup.com
  - c571keqcpdvpb.int.westgroup.com
- NAS Server,  mounted in /searchdata in Search Autocomplete Server
  - DEV: cisclnt-e0076.int.thomsonreuters.com
  - QA: cisclnt-e0075.int.thomsonreuters.com
  - Preprod/Prod: cpsprod-f0401 and cpsprod-e0191

- Search Autocomplete Server - RHEL 7
  - username: asread or asadmin
  - port: 9001
  - NAS Storage mounted to `/searchdata`

| Environment | Service<br/>URL | Servers | NAS mount point |
|-------------|-----------------|---------|-------------|
| Dev          | [Link](http://dev.search.checkpoint.thomsonreuters.com/searchAutoComplete/JSP/queryComp.jsp) | c111jjhckpt.int.westgroup.com | cisclnt-e0076.int.thomsonreuters.com:/cb0074_chkpt_checkpointsearch_dev_snap/search |
| QA           | [Link](http://qa.search.checkpoint.thomsonreuters.com/searchAutoComplete/JSP/queryComp.jsp) | c111bmqckpt.int.westgroup.com<br>c111sbdckpt.int.westgroup.com | cisclnt-e0075.int.thomsonreuters.com:/cb0074_chkpt_checkpointsearch_qa_snap/search |
| PreProd/<br>Prod | [Link](http://search.checkpoint.thomsonreuters.com/searchAutoComplete/JSP/queryComp.jsp) | c111ypvckpt.westlan.com<br/>c111znsckpt.westlan.com<br/>c111cmqckpt.westlan.com<br/>c111ftkckpt.westlan.com | cpsprod-f0401:/chkpt_checkpointsearch_proda_snap/search<br/>cpsprod-f0401:/chkpt_checkpointsearch_proda_snap/search<br/>cpsprod-e0191:/cb0010_chkpt_checkpointsearch_prodb_snap/search<br/>cpsprod-e0191:/cb0010_chkpt_checkpointsearch_prodb_snap/search |

# Cloud proposal (Work In Progress)

# Proposal 1
![image.png](/.attachments/image-867f096c-5399-4cfb-b1cb-c3d4c14a6738.png)

## Proposal 2
![image.png](/.attachments/image-6e736130-c448-4db0-8e7a-44139f67416d.png)

# References

- [Lucid chart design diagram](https://lucid.app/lucidchart/aacbe96f-e231-4e47-bb5f-c62678b36805/edit?invitationId=inv_f226f83e-7315-42c7-9e5e-c62fe6320dd6&page=LUKw7~WeclK1#)
- [Search Autocomplete [Old CP Wiki]](http://cpwiki.int.westgroup.com/MillenniumProject/SearchAutoComplete)
- [LogProcess - [Old CP Wiki]](http://cpwiki.int.westgroup.com/LogProcess)
- [Sharepoint documentation 1](https://trten.sharepoint.com/sites/trta/sites/checkpoint/Shared%20Documents/Forms/AllItems.aspx?viewpath=%2Fsites%2Ftrta%2Fsites%2Fcheckpoint%2FShared%20Documents%2FForms%2FAllItems%2Easpx&id=%2Fsites%2Ftrta%2Fsites%2Fcheckpoint%2FShared%20Documents%2F0%2EPast%20Releases%2F9%2E4%20Documentation%2FQuery%20Completion%20Service&viewid=9877826d%2D7164%2D4409%2Db034%2D11e1302cd6af)
- [Sharepoint documentation 2 - Search enhancements](https://trten.sharepoint.com/sites/trta/sites/checkpoint/Shared%20Documents/Forms/AllItems.aspx?viewpath=%2Fsites%2Ftrta%2Fsites%2Fcheckpoint%2FShared%20Documents%2FForms%2FAllItems%2Easpx&id=%2Fsites%2Ftrta%2Fsites%2Fcheckpoint%2FShared%20Documents%2FSearch%20Enhancements&viewid=9877826d%2D7164%2D4409%2Db034%2D11e1302cd6af)
- Repositories:
  - [LogProcess [TFVC]](https://dev.azure.com/tr-tax-default/Checkpoint/_versionControl?path=%24/Checkpoint/Web/Tools/LogProcess)
  - [Search Autocomplete Data [ADO]](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_git/cp-search-auto-complete-data)
  - [Search Autocomplete Data [TFVC]](https://dev.azure.com/tr-tax-default/Checkpoint/_versionControl?path=%24/Checkpoint/Web/Tools/BuildSearchAutoCompleteData)
  - [Search Autocomplete Service [ADO]](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_git/cp-libraries?_a=contents&version=GBmaster&path=/SearchAutoComplete)
  - [Search Autocomplete Service [TFVC]](https://dev.azure.com/tr-tax-default/Checkpoint/_versionControl?path=%24/Checkpoint/Web/Libraries/SearchAutoComplete)
- Search Autocomplete application
  - [On-premises](http://c111jjhckpt.int.westgroup.com:9001/searchAutoComplete/JSP/queryComp.jsp)
  - [Cloud]()