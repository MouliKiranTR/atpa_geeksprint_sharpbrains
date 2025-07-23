**Note:** _This doc is written with an example of a205159-cp-dev-toc-publisher for dev env, but this can be acceptable for other lambdas as well._
To test lambda we should first check what is the trigger for it. 
To do it we should go to [our specific lambda functions](https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/functions/a205159-cp-dev-toc-publisher) page and select **Configuration->Triggers**
![Screenshot 2024-10-24 125100lambdatrig.png](/.attachments/Screenshot%202024-10-24%20125100lambdatrig-46d46ca3-3efb-4036-b86e-258d676cddb2.png)
Here for this specific lambda(_it may vary depending on your lambda, so please check the configuration as shown in this example_)  we can see that it is triggered when new object is created inside S3  _a205159-cp-toc-service-dev_ bucket's  _/root-toc_ folder. Link to [S3 bucket](https://us-east-1.console.aws.amazon.com/s3/buckets/a205159-cp-toc-service-dev?region=us-east-1&bucketType=general&prefix=root-toc/).
To create a file inside s3 bucket for testing purpose(dev env?) ,we can download one of the file
![Screenshot 2024-10-24 123550srdowload.png](/.attachments/Screenshot%202024-10-24%20123550srdowload-31e3d41e-32f6-43ae-86fd-2654c4284763.png)
 and upload it back to our folder 
![Screenshot 2024-10-24 114507s3addfiles.png](/.attachments/Screenshot%202024-10-24%20114507s3addfiles-b72b3644-aa91-4367-a8e9-10ab5148a8fc.png)
![Screenshot 2024-10-24 114247bucket.png](/.attachments/Screenshot%202024-10-24%20114247bucket-83b41ea1-72fc-4b8b-b372-402a99e2fe7a.png).
After this lambda should be triggered, and to check this we have to go back to lambdas page select **Monitor** and check the invocations(_please note that here can be 1-2 minutes delay until it's shown_) ,to see that it was successful
![Screenshot 2024-10-24 123724lambdasuccess.png](/.attachments/Screenshot%202024-10-24%20123724lambdasuccess-37701c76-57e1-438a-b5b9-3a083fd45d3c.png).
We can check also logs from CloudWatch(**Monitor->View CloudWatch** logs and select the last log by your event time(when your lambda was triggered) to read the last logs and see if it's has done the work and called the service needed. For this specific case please see this [CloudWatch log](https://us-east-1.console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups/log-group/$252Faws$252Flambda$252Fa205159-cp-dev-toc-publisher/log-events/2024$252F10$252F24$252F$255B$2524LATEST$255D8400abb770b3456f8b4db69e2bc567de) ,we can go down on logs and see (**Note: There can be some Warnings ,for example for toc-publisher there is some Warning related to The AWS SDK for Java 1.x ,but we can ignore it**)
![Screenshot 2024-10-24 132144logs.png](/.attachments/Screenshot%202024-10-24%20132144logs-a824fc59-0edf-4199-9389-647fba1b4e39.png)
