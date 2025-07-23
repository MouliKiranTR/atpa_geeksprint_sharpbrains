## Background and References
- ***Summary:*** LogProcess is a helper application that downloads and processes Checkpoint server log files and creates summary error reports and log stats report. These usage files ultimately are used to provide data via the [Usage Report Tool](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/845/CP-Usage-Logs?anchor=checkpoint-usage-report-tool%3A).
- This document was created as part of research into the LogProcess application for [User Story 164345](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_workitems/edit/164345): [Usage Processing Logs][LogProcess-1 ] Deep Dive Code to Understand Scope and Changes Needed for Implementing LogProcess Changes 
- LogProcess repo: https://github.com/tr/cp_developer-tools/tree/main/LogProcess
- LogProcess Wiki: https://infratools-cp-ci-use1.5463.aws-int.thomsonreuters.com/wiki/LogProcess

### Checkpoint Logging
- A list of the various types of log files created by Checkpoint and what they are used for:
- *Note:* * = date/version/port placeholder, e.g. - `analysis13_01_24_9.9.49_10405.log`

| Name              | File Name Pattern             | Description                                                               |
| ----------------- | ----------------------------- | ------------------------------------------------------------------------- |
| Analysis          | analysis*.log                 | Detailed timing information                                               |
| Browser Info      | browserInfo*.log              | For each user login, what are their browser specs                         |
| Checkpoint Access | checkpoint_*_access.log.*.txt | Tomcat access log                                                         |
| Cite Alert        | CiteAlert*.log                | Track It process                                                          |
| CP                | CP_*.log                      | Checkpoint application debug/warning/error messages                       |
| GC                | gc_*.log                      | Garbage collection logs                                                   |
| News Email        | newsEmail*.log                | Newsletter process                                                        |
| Processes         | processes.log                 | Process Dump? How is this triggered?                                      |
| Requests          | requests*.log                 | All requests to Checkpoint application                                    |
| Schedule Search   | scheduleSearch*.log           | Logging of scheduled search processing                                    |
| System Out/Error  | sysErr_*.log                  | Tomcat (catalina.out) log is directed here                                |
| TA Summary        | taSummary*.log                | ?                                                                         |
| Time Errors       | time_errs*.log                | Checkpoint requests that took longer than expected                        |
| User Action       | userAction*.log               | Detailed analysis of user actions used by R&amp;D for search enhancements |

## Server
- Runs on server: `c548kqncplog.ecomqc.tlrg.com:5616`
	- user: `Ecomqc\srvcpdevops`
	- password: check with Miguel or Luke
	- Windows server
	- Can connect using "Remote Desktop Connection" with above credentials
- On the server, Windows Task Scheduler runs the batch processes nightly
- LogProcess is configured to output the reports, and zipped log files to `F` drive
- `F` drive on the server is mapped to NAS at `cisclnt-e0897.int.thomsonreuters.com/checkpointlogprocess`

### Task Scheduler
- The Windows Task Scheduler is configured by DevOps to run LogProcess nightly for each environment: ![Pasted image 20240703084625.png](/.attachments/Pasted%20image%2020240703084625-04b10e06-bd2a-4d54-8e62-11820055fffa.png)

## Batch Processes
- Batch processes are defined in `.bat` files
- All use `CONFIG_FILE=process_data.xml`, so you need to rename one of the config files by removing the env you would like to use

### `runUi.bat`
- Calls `com.tta.checkpoint.logProcess.LogProcessApp`
- Opens window like this: ![Pasted image 20240628105946.png](/.attachments/Pasted%20image%2020240628105946-4ea370dc-6ae8-427b-a689-8c09a6484971.png)
- Allows you to select different config files to use, and input the date (0 referenced from current date) you want logs for (ex: -1 is yesterday)
- Zip into sub directory tells the output to be grouped by server in sub directories
- Servers/files tab allows you to select servers to get logs for, which file types to get logs for
- Processes tab allows you to get specialized reports (such as error report, GC summary, etc.)

### `RunErrUi.bat`
- Calls `com.tta.checkpoint.errorReader.ErrReaderApp`
- Can upload zip file of `CP_Err_{date}.zip` and it will show all errors from the zip file
- Allows you to group and read errors

### `RunAll.bat`
- Calls `com.tta.checkpoint.logProcess.BatchAllApp`
- Set config file in the `runAll.bat` file as either the `process_data.xml` or the `process_data_prod.xml`
- This is generally used in production
- Runs every night on the `c548kqncplog` server

## Config Files
- In the root directory of LogProcess there are numerous config files prefixed with `process_data_` followed by the environment
- These are used to specify, for each environment, what servers to download logs from, and the different log files to download as well as some additional configurations
- The top of these XML files contains good usage documentation on how the file is structured
- Ex:
	```xml
	<directories>  
	    <zipDir del="-20" date="yyyy_MM_dd">dummy:\LogProcess\devData</zipDir>  
	  
	    <!-- Dev App-->  
	    <inDir proc="N"  id="c111xjwcpdvap" dm="dev"  env="dev"  deploy="_" type="tomcat" pw="Chkpntdv">asread@c111xjwcpdvap:/appserver/tomcat</inDir>  
	    <inDir proc="Y"  id="c501meycpdvap" dm="dev"  env="dev"  deploy="_" type="tomcat" pw="CheckpointDev123">asread@c501meycpdvap.int.thomsonreuters.com:/appserver/tomcat</inDir>  
	</directories>  
	<files>  
	    <file id="CP" dl="Y" req="Y" date="yy-MM-dd">CP_(date).log</file>  
	    <file id="news" dl="Y" req="N" date="yy_MM_dd">newsEmail(date).log</file> 
	</files>
	```

### Servers
- Servers are specified under `directories` and uses `inDir` field
- for each there is an ID, env, type, password, etc.

### Files
- Log files to process are under `files` using `file` tag
- for each there is id, date format, and the name of the log file
- **List of files (from DEV config):**
	- CP = CP_(date).log
	- access-web = access_log.(date)
	- access = _access_log.(date).txt
	- access-http = access_log_checkpoint.(date)
	- analysis = analysis(date).log
	- news = newsEmail(date).log
	- citeAlert = CiteAlert(date).log
	- trSec = TrSecApi(date).log
	- restApi = RestClientApi(date).log
	- secure = security(date).log
	- request = requests(date).log
	- timer = time_errs(date).log
	- userAct = userAction_(date).log
	- gc = gc.log
	- server = server.log
	- browserInfo = browserInfo(date).log

### Processes
- These are specialized reports that are generated from the downloaded log files, and where the bulk of LogProcess logic is contained
- For purposes of this work, assuming we get the log files downloaded and zipped in the format it's expecting, there *should* be **NO** changes needed to this portion of the code (but the format needs to match exactly)
- For each one of these, they have a specific root XML element for each (listed below before the =, for example `errReport` and `extReq`)
- Each of these also defines a `fileId` attribute, which points to one of the above log files by its ID (for example `extReq` uses `request` file ID, which is mapped above to `requests(date).log`)
- Each one of these also has an output directory specified (for example: `errReport` output is `f:/ErrReport/LogErrData`)
- **List of processes (and the log file ID they use):**
	- browserReport = browserInfo
	- emailLinkStat = request
	- emailNewsLetterStat = access
	- errReport = CP
	- extReq = request
	- gcSum = gc
	- logStat = analysis
	- userAction = userAct
	- webStat = access

## Output
- The output of LogProcess is various reports for each process defined above, with the output for each a location on the NAS mounted to F drive (`cisclnt-e0897.int.thomsonreuters.com/checkpointlogprocess`)

### NAS Output Directories
- zipDir (f:/LogProcess/prodData)
	- is the directory to put the zipped log files in
- rptDir (F:/LogProcess/prodRpts)
	- this is the location to place reports that are not specified with absolute path
- **Directories for processes (where to output the resulting process output)**
	- logStat (f:/logstat)
	- errReport (f:/ErrReport/LogErrData)
	- webStat (f:/ftp/WebStat/Prod)
	- gcSum ({rptDir}/gc)
	- userAction (f:/ftp/UserActions/prod)
	- userSrch (f:/LogProcess/prodUserSrch)
	- servProc ({rptDir}/servProc)
	- extReq ({rptDir}/reqs)
	- longHttpReq ({rptDir}/http)
	- wrongServerReq ({rptDir}/http)
	- browserReport ({rptDir}/browser)

### CPS Datawarehouse Output
- The `userAction` process has property `useSFTP` which can be set to true
- If true, it sends the output files from the `userAction` process to the CPS Datawarehouse servers configured in the config file under `sftpServers` XML element
	- c006zuncptepb.int.westgroup.com (Test)
	- c571keqcpdvpb.int.westgroup.com (Dev)
	- c883wyscpprpb.int.westgroup.com (Prod)
	- c803gqkcpprpb.int.thomsonreuters.com (QED)
	- ![Pasted image 20240702152708.png](/.attachments/Pasted%20image%2020240702152708-8c12fb97-d088-4e17-8454-b1a2c1687f6c.png)
- This data that is outputted to the DW server's is then used to provide data via the Usage Tool


## `BatchAllApp` Code Flow
- Class to run batch process to download and process log files
- Runs with one arg: `file=%CONFIG_FILE%`, which is set to `process_data.xml` in the batch script
- First, `parseParms` takes the arguments and turns into a hash map
- Then, `loadCriteriaFile` uses the name of the criteria file passed in from program args, and reads the associated config file by parsing it into a type `CriteriaFile`
	- This contains TreeMap's with list of files and servers
	- Next, it gets the day from params. If null it uses the days from the Criteria File (set to -1)
	- It then uses this `day` value to offset from the current date (in this case -24 hours from current time) and uses this to set the file name for each of the files in the Criteria file (ex: for key `news` the `fileName` becomes `newsEmail24_06_27.log`)
	- Next, it gets the `zipDir` from params if present, otherwise also from the Criteria file
- Next, it checks the current status of `ZipFiles`
	- `updateWithExistingZipFiles` looks in the zip directory for the zip files and log files within them to verify which ones are already processed
	- It uses the criteria file, and the current date to read the zip directory for all zip files with the current criteria date
	- It then loops over every file in `list` (which is just files in the zip dir), and if desired file is located it sets in the `FileData` object of the `Server` object `lastRun` equal to current date. If not found then set `lastRun` to null
- Next, it checks if zip files are already present in local cache
	- `checkZipFiles` loops through all the servers and checks if the file is there
	- If so it adds to list of files, if not it sets flag to have it loaded
	- It indicates the file should be loaded again by setting `lastRun=null`
	- It does this for all files on each server with double for loop (loops over server, and over files in each server)
- Next, it gets the files according to server type
	- Three types:
		- `wasServers`
			- WebSphere servers
			- Uses `ZipWasFiles.downLoadWasFiles`
		- `tomcatServers`
			- Uses `ZipTomcatFiles.downLoadTomcatFiles`
		- `httpServers`
			- Uses `ZipWasFiles.downLoadHttpFiles` and `ZipTomcatFiles.downLoadHttpFiles`
	- Inside of `downLoadHttpFiles`, we download all the files from all the HTTP servers defined in the criteria. Criteria holds what files and servers to process (loaded previously from the config XML file), and `httpServers` is list of servers to process, each containing list of files to process on that server
	- It uses this information and some checks to build list of servers, which is sent to `getHttpFiles` and `getLinuxFiles`
- After all the files have been downloaded to ZIP files we again reload the Zip file info
- Then, call `ProcessData.doProcesses` which calls `runIt`, an interface to run the process with various implementations for each process type (see [Processes](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/843/LogProcess?_a=edit&anchor=processes) for list)
	- For each one of these implementations, the general structure is that it iterates over list of servers obtained from `criteria.getServerList()`, and for each server checks if it should be processes
	- Then, it reads the saved ZIP files and processes them using custom logic in each implementation
	- The report is then written out to the directory specified in the process config
- After this, it determines if the output files should be sent over SCP to the server
	- This is set to false for all processes but user action
	- For user action, its specified using property with id `useSFTP` in the config file
	- For the prod config, its specified to SFTP the files to `c006zuncptepb.int.westgroup.com` which is a CPS Datawarehouse server
- Finally, we update the status, check for errors or notes, and email any errors