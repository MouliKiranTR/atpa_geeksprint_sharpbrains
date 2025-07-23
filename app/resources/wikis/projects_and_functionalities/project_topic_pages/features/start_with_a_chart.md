### Start with a Chart (SWAC)
The SWAC widget contains charts to State Chart, Nexus Assistant and Payroll Chart.  The links are curated by Editors for each subtopic and then shared the actual API payload information with the team who will be responsible for creating the container information.

#### List of steps to extract API Payload info in JSON format:
Here is a list of steps that Editorial uses to extract the State Chart/Nexus Assistant/Payroll payload information in json format.
##### Step 1
Login to Checkpoint application https://riacheckpoint.com/
Generate the Nexus Assistant Chart by click on the generate button.

![image.png](/.attachments/image-01b1bb9e-140b-43ab-9cd1-b936dae50c9f.png)

##### Step 2
After clicking on the “Generate” button, the chart is generated.

![image.png](/.attachments/image-0e649e80-a882-47fc-b880-d55b974f0352.png)

##### Step 3
After chart is generated, we need to logout the Checkpoint and re-login, once you are in Checkpoint, click on the “History” icon, you will see the history for the Nexus Assistant chart.  Now mouseover the link, you will see the status at the bottom of browser’s status bar.  See screenshot below for more details.

![image.png](/.attachments/image-ef880d88-9376-49a5-adbb-09e86e00dcdc.png)

##### Step 4
Find the HistID and ItemID value from the Nexus Assistant link, once you know the HistID and ItemId for the link, we will use the values to extract the Nexus Assistant Chart data.

The value for HistID is 39 and ItemId is 3, we will use these values in our next step.

##### Step 5
Extract the data by substitute the HistId and ItemId in the History API Endpoint, for example If the HistId is 39 and ItemId 3 then the API URL would be https://riacheckpoint.com/app/api/v1/history/39/items/3

![image.png](/.attachments/image-ff22ea78-254e-4f71-be6a-11bf4031e91e.png)

Example of extracted Nexus Assistant Chart Payload:

```
{
  "parType": "NEXUS",
  "chartCriteria": [
    {
      "taxType": "CORP",
      "chartTypes": [
        "65410"
      ]
    }
  ],
  "states": [
    "CT",
    "NJ",
    "NY"
  ]
}
```
