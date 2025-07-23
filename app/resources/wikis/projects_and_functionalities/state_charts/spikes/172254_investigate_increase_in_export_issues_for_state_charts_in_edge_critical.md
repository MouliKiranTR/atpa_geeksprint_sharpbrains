# Basic information

*   Spike Title: SPIKE: Investigate increase in export issues for State charts in Edge (Critical)
*   @<BD53ED6B-D73D-627F-A090-FF19100E6D93> 

# Contents

[[_TOC_]]

# References and Resources 


### Repositories

* [cp_web-app](https://github.com/tr/cp_web-app)
* [cp_ui](https://github.com/tr/cp_ui)

# Purpose

### Problem Statement
State Charts Export takes much more time than expected when user chose several states, tax and chart types. It may take more than 10 minutes.

### Objectives
*   Investigate, what leads to export delay.
*   Learn export process
*   Identify the problem (and provide possible solution)


# Investigation Details

Technical Analysis

### Research Findings

We thought that it takes a lot of time to process the request on the backend, but its [export controller](https://github.com/tr/cp_charts-service/blob/2f559c51799e5e72c8d6f59607d496c251e056db/src/main/java/com/tr/checkpoint/charts/controller/ChartsController.java#L218) runs in a normal speed. Meanwhile, web profiling showed that the main delay was due to cp_ui's [downloadChart method](https://github.com/tr/cp_ui/blob/d977d7d02a47d12c625d8e0caa66f9b514039081/src/app/shared/services/charts.service.ts#L132).
It uses [JsZip](https://stuk.github.io/jszip/) to send compressed data to backend, and this library may work slower with "too big" files. Also, here ZIP64 files are supported if they fit within 32-bit integer limits due to JavaScript's number handling.
[Limitations of JSZip](https://stuk.github.io/jszip/documentation/limitations.html).
\
This is performance of all requests from pressing button 'Generate' to receiving formed XML file.
\
![{C91F61E2-D392-4C5F-91E0-77CF37D0F577}.png](/.attachments/{C91F61E2-D392-4C5F-91E0-77CF37D0F577}-b20c5395-5bdc-4582-92f6-bff46822bbc9.png)
\
We see that the load appears only at the beginning, middle and end of the request. More than half of the time is spent waiting.
\
Arrows lead from JS functions that call a method with a timer set to functions that end the timer and call the next function.
First timer was run with [downloadChart method](https://github.com/tr/cp_ui/blob/d977d7d02a47d12c625d8e0caa66f9b514039081/src/app/shared/services/charts.service.ts#L132)
\
Table showing the relationship between the size of html (the amount of information processed) and its average execution time:
![image.png](/.attachments/image-0ffddf9c-da05-4a1b-b945-728f908fef06.png)
\
![image.png](/.attachments/image-d6037a46-7554-413a-9760-fec89b8b7901.png)
After ~200,000 characters, execution time increases sharply.

*   [Note any blockers encountered]

## Implementation Details


### Required Changes
   * Check the minimum size of document that will lead to response delay;
   * Check another library for zipping files with "large" data;

### Example Implementation

[downloadChart method](https://github.com/tr/cp_ui/blob/d977d7d02a47d12c625d8e0caa66f9b514039081/src/app/shared/services/charts.service.ts#L132):
![{23F59903-EB25-40FF-B371-CAEE5B820B33}.png](/.attachments/{23F59903-EB25-40FF-B371-CAEE5B820B33}-0e99dde1-8480-4cc0-9789-dfdcc3588812.png)

# Results

### Conclusions

The problem is related to cp_ui's library limitation.
Update data zipping mechanism.