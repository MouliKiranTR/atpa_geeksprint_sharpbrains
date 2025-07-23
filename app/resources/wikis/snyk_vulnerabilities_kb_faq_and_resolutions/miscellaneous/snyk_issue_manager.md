## Overview:
This project offers several options for teams to manage the issues reported in Snyk effectively. Currently, teams can perform the following actions.

- Fetch issues from the backend, using filters available.
- Enrich issues with metadata available in the UI.
- Mark issues to be ignored according to a set of filters.
- Ignore issues of interest (e.g., false positives or non-applicable vulnerabilities).
- Format issues to generate an Excel workbook for reporting.

Details on specific commands for each of the operations will be added later.

References:
Snyk Issue Manager: https://github.com/tr/prodsec_snyk_issues_manager

## Setup
- Install python (For time of editing version 3.12)
- clone repository https://github.com/tr/prodsec_snyk_issues_manager
- install pip packages: (pip generally is getting installed while installing python )
  - Go to project root directory and run:
     ```pip install -r requirements.txt```
  - If necessary create virtual environment:
https://docs.python.org/3/library/venv.html
- Set SNYK_TOKEN environment variable
  - Get your snyk token from account settings:
![image.png](/.attachments/image-0d2afac1-7437-4d32-badd-e3b15a8f216e.png)
  - Copy and set value to SNYK_TOKEN environment variable based on your operating system. You can check token with ```echo $SNYK_TOKEN``` command in terminal.
- Set SNYK_COOKIE environment variable. You will need this while executing extend operation. 
IMPORTANT: value of SNYK_COOKIE should be following: snyk.id=<your snyk.id here>
You can find it in snyk.id cookies on browser:
![image.png](/.attachments/image-65bcf66c-cc23-4b66-8d84-1a2f6d0ecae7.png)

## Operations
- In case of every operation it is necessary to run python file with relevant parameters. We can imagine operation as one of the parameter. There are 5 operations:
  - retrieve
  - extend
  - filter
  - ignore
  - format
- It is important to know org_id since it is required for most commands. You can find org_id here:
![image.png](/.attachments/image-8019c601-44bb-48f0-a5a9-f9bf731fc088.png)
## retrieve
- For retrieve operation we need 2 parameters: org_id, and json file where we define filters.
  - Filter json file should be constructed according to ```filters.retrieve_issues.schema.json``` file that is included in repo.
  - We can create json file named ```filters-file.json```:
```{
    "projects": ["56b0c863-57fe-4bf4-b0ec-56ea26a092c1"],
    "issues": {
        "type": "code",
        "effective_severity_level": "high",
        "ignored": false,
        "status": "open"
    }
}
```
In the "projects" field we need to specify array of project ids, which can be found in url:
![image.png](/.attachments/image-6c0a49ec-4e73-4533-b546-32dfe3f2b3d1.png)
In the "issues" we can see fields that can be used as filters. Other fieleds that can  be used for filtering is specified in ```filters.retrieve_issues.schema.json```
In this case we will retrieve issues that has high severity level, open status ",
type of "code" and those which are not ignored.
- Now we can run command that will retrieve issues and generate json file containing array or snyk issues (-o options is for org_id):
```python snyk-issees-manager.py retrieve -o 60149f90-f5e7-4fae-9424-a616e4a1f514 --filter filters-file.json```
This will retrieve issues from snyk and generate json file (file name format - snyk_issues_{CURRENT_DATE}.json).
NOTE: json file can have empty array if there is no issues with specified filters.
![image.png](/.attachments/image-fd484646-3150-4c5b-a9a7-6eddc91290b1.png)


## extend
- retrieve command does not give all information about snyk vulnerabilities, therefore we need to use extend command.
IMPORTANT: you need to set SNYK_COOKIE in order to execute this command, please check setup section.
- we can execute following command:
```
python snyk-issues-manager.py extend -o 60149f90-f5e7-4fae-9424-a616e4a1f514 --input snyk_issues_20240913.json
```
IMPORTANT: This command may result TimeoutError, if project is big and has many vulnerabilites. In this case you may want to increase timeout of request in snyk.py. At the time of editing this document original timeout value was 5 seconds:
![image.png](/.attachments/image-e9308a05-9eb8-45e1-b2c6-49cece3d0c58.png)
-o (organization) option is mandatory. --input options is file that was generated from retrieve command, which is also mandatory.
![image.png](/.attachments/image-0bb801de-22f3-4a6c-82ef-f4a61ccb821d.png)
After running command we should get new file named ```snyk_issues_extended_{CURRENT_DATE}.json``` in this case ```snyk_issues_extended_20240913.json```
In this file we will have same json which have one additional field ```METADATA```
![image.png](/.attachments/image-07fffc5a-e0fe-4594-9464-847ca6fda58c.png)

## filter
- After fetching metadata about each snyk issue, now we can mark object with a filed ```SHOULD_BE_IGNORED: true```
- Before executing filter command we need to setup filters.py:
```
IGNORE_FILTERS = [{
    "name": "Ignore all issues",
    "reason": "The reported issue represents a false positive given the validation and sanity checks performed by the development team.",
    "fn": lambda x: ignore_filter(x)
}]

def ignore_filter(issue):
    
    file_path = "CPWar/web/cpadmin/TechSupp/logincookies.jsp"
    isNotPresent = "METADATA" not in issue or "RESULT" not in issue["METADATA"] or "locations" not in issue["METADATA"]["RESULT"]
    if isNotPresent:
        return False

    file_location = issue["METADATA"]["RESULT"]["locations"][0]["physicalLocation"]["artifactLocation"]["uri"]
    if file_location == file_path:
        return True
```
We can have several ```IGNORE_FILTERS``` objects, but most important part is ```fn```. This is filter function that will mark specific json object with ```SHOULD_BE_IGNORED: true``` if ```True``` is returned from ```ignore_filter(issue)``` function. parameter ```issue``` is single object from array that is stored in ```snyk_issues_extended_{CURRENT_DATE}.json``` in this case ```snyk_issues_extended_20240913.json```


In this particular case ignore function will mark issues with ```SHOULD_BE_IGNORED: true``` which are in file ```CPWar/web/cpadmin/TechSupp/logincookies.jsp```

-Let's run command:
```
python snyk-issues-manager.py filter -o  60149f90-f5e7-4fae-9424-a616e4a1f514 --input snyk_issues_extended_20240913.json
```
org_id and input file generated from extend command are mandatory.
command will generate file ```snyk_issues_filtered_{CURRENT_DATE}.json```.

We can see on snyk ui that there are 2 issues related to logincookies.jsp file.
![image.png](/.attachments/image-42761097-cc77-4452-8754-4fb83a7ab124.png)
And two issues were marked with ```SHOULD_BE_IGNORED: true``` in json file:
![image.png](/.attachments/image-2b1af095-50ca-400a-b6dd-9e0f1f775803.png)

In order to make sure that marking went correctly we can compare ```KEY``` attribute of  each json entry (snyk issue) to snyk ui.
![image.png](/.attachments/image-1f6c136d-1257-4f22-9599-d3c84f6ef16b.png)
![image.png](/.attachments/image-aeade949-10d7-4940-8afd-e3645a044924.png)

In conclusion we can identify json object which were marked with ```SHOULD_BE_IGNORED: true``` and compare ```KEY``` values to snyk ui. In this way we can make sure that filtering went as we intended and we did not make any mistakes.

## format 
- We can format issues as excel document
``` 
python snyk-issues-manager.py format --input snyk_issues_extended_20240913.json --config configuration.py
```
This will generate new .xlsx file. Configuration of formatting can be found in ```configuration.py```
configuration object is most important because this declares what we want to generate in .xlsx file. configuration object is constructed based on  
```configuration.schema.json```

![image.png](/.attachments/image-3c007a0d-a9a8-43c5-bfc2-df408c389c6f.png)


## ignore
- please refer to readme for this operation
https://github.com/tr/prodsec_snyk_issues_manager?tab=readme-ov-file#ignore-issues
IMPORTANT: This operation allows to ignore issues flagged as candidates for ignore within the ```SHOULD_BE_IGNORED``` field. In order to avoid errors and not ignore other snyk issues unintentionaly,  it is good idea to consult with security team first before executing this command.

