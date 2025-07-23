# **Scenario/Overview**
On Oct 13 2024,  we noticed that there was significant slowdown on Prod TRTA search endpoint,  checking this issue further,  we have noticed that there was surge in request from a single Webapp instance which eventually caused the high GC time and slowdown on TRTA search service. 
Webapp instance caused the surge in requests and all the below requests were from a single trace **trace_id:5232820986826151696**.
If you look the same trace (trace_id:5232820986826151696) on Webapp side we can see there was around 235K requests to search endpoint triggered by a single user.

## Analyses
It's confirmed from Product side that this user and firm doesn't have access to Search API's.
![Screenshot 2024-12-10 111114chat.png](/.attachments/Screenshot%202024-12-10%20111114chat-7aba180e-1478-4aee-b2b4-67caf0459360.png)
![image.png](/.attachments/image-7fea6655-3453-42f0-ba79-54a77f10170a.png)

So to trigger this much requests there is only two ways
1. User grabbed the HTTP request, used an automation tools and initiated massive number of requests.
2. It was a glitch in the server during that particular time


By analyzing logs from DataDog side we can see some points.
First as the requests were 235k we cannot check all of them ,but what we can notice is that a lot of requests contain this document Id  **idaf1dd12183411dc9de1c7f8ee2eaa77*,
so possibly we can assume that user executed search which returned  ([this document](https://checkpoint.riag.com/app/main/doc?DocID=idaf1dd12183411dc9de1c7f8ee2eaa77 "https://checkpoint.riag.com/app/main/doc?docid=idaf1dd12183411dc9de1c7f8ee2eaa77")).

,we can see that all the requests are more or less than within same time interval,
![Screenshot 2024-12-06 143900issuelog3.png](/.attachments/Screenshot%202024-12-06%20143900issuelog3-f6bd9313-41fe-43cb-afb7-d9c39ba3544e.png)


 as well as there are found header **user-agent: Jakarta Commons-HttpClient/3.1** , after checkinng multiple sources it indicates that _this user agent string belongs to Jakarta Commons HttpClient, which is a library used to perform HTTP requests (more often, in the automatic mode as a web crawler or bot)._
So we can assume that user done requests by using some automatic tool.
## **Run requests with automation tool**
To reproduce same behavior I have tried to copy cookies from browsers developer tool and to execute automated requests with any runner(I have tried Postman Runner).
So to do this we can copy request as CURL 
[![Screenshot 2024-11-28 at 11.28.34.png](/.attachments/Screenshot%202024-11-28%20at%2011.28.34-cbb6faae-d81b-49fd-b707-b867d1c36f66.png)]()

 and import it to Postman.

Then use this requests to run automated requests with Postman Runner 

![Screenshot 2024-12-06 152043postman.png](/.attachments/Screenshot%202024-12-06%20152043postman-4bde8aaa-21d5-4003-a937-be78acd6cd77.png).

We can see that we are able to run multiple requests within another tool and as token is expiring late and no rate limiting implemented we can do as much requests as we want ,by copying cookies.
The exact same behavior is reproduceable for CI environment , by copying cookies and running requests withing postman runner.
![Screenshot 2024-12-04 155727runner.png](/.attachments/Screenshot%202024-12-04%20155727runner-0c55e2ed-bfc2-45d5-b677-0a543da78ad6.png).

## **Next Step**
To prevent such situation there are multiple solution ,which should be analyzed more detailed.
- Rate limiting:  Implement server-side rate limiting to restrict the number of requests from a single IP address or user within a specific time frame.
- CAPTCHA: Implement CAPTCHA challenges for suspicious or high-frequency requests.
- User behavior analysis:
    *   Monitor user interactions, click patterns, and request timing to detect automated behavior.
    *   Implement machine learning algorithms to identify and flag suspicious activities.
-   Token-based authentication:
    *   Use short-lived, rotating tokens instead of relying solely on cookies.
    *   Implement JWT (JSON Web Tokens) with short expiration times(this also can copied if automation tool will run on browser ,but it's less possible).
- Signature Validation
    *   Sign each request with a secret known only to the client and server.
    *   Include the signature in the request ,and validate it on the server.
- Also can be implemented some sort of replay protection 

    *   Add a unique identifier to each request. Store a short-lived cache of processed identifiers.
    *   Reject requests with duplicate identifiers.


