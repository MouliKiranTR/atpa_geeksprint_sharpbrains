To test out lambda locally ,we have to install **Docker Desktop** for building lambda image.
It can be downloaded from here 
[Docker Desktop](
https://www.docker.com/products/docker-desktop).
Also please refer to this Atrium link as **TR employees requires subscription** for docker desktop
[Docker-Desktop-Atrium](https://trten.sharepoint.com/sites/intr-docker?xsdata=MDV8MDJ8fDIwOTJiNTYyNTQ5NDQ1NmJhNWVjMDhkYzljNGJhODI3fDYyY2NiODY0NmExYTRiNWQ4ZTFjMzk3ZGVjMWE4MjU4fDB8MHw2Mzg1NTcwOTU5Mzc0MTg3MzJ8VW5rbm93bnxWR1ZoYlhOVFpXTjFjbWwwZVZObGNuWnBZMlY4ZXlKV0lqb2lNQzR3TGpBd01EQWlMQ0pRSWpvaVYybHVNeklpTENKQlRpSTZJazkwYUdWeUlpd2lWMVFpT2pFeGZRPT18MXxMMk5vWVhSekx6RTVPakV5T0dGa1lUa3lMV0l6TVRRdE5ERmlOeTFpWlRWaUxXSTVNR0pqTTJKbE1qZzBOMTgxTXpkalkyWXpPQzAxWW1JNUxUUXlOMkl0WWpNNVlpMDNaRE5sT1dFM1pqUTRZVEJBZFc1eExtZGliQzV6Y0dGalpYTXZiV1Z6YzJGblpYTXZNVGN5TURFeE1qYzVNalV5TUE9PXxjODFhY2RlZWQ2Y2Q0MDQ3YTVlYzA4ZGM5YzRiYTgyN3w3MGJhMTA5YTI4Nzc0ZTA2YTczMzk3OWRmODMyYmE4Mg%3D%3D&sdata=TnRrTzdGdzBBQVRPYkJRWXllQytaUXI3MWJNQmVEM0tlTjAyZ2M4dklzZz0%3D&ovuser=62ccb864-6a1a-4b5d-8e1c-397dec1a8258%2CMostafijur.Rahman%40thomsonreuters.com&OR=Teams-HL&CT=1721208047497&clickparams=eyJBcHBOYW1lIjoiVGVhbXMtRGVza3RvcCIsIkFwcFZlcnNpb24iOiI0OS8yNDA2MTMxODQwOCIsIkhhc0ZlZGVyYXRlZFVzZXIiOnRydWV9).
We will also need to install SAM CLI(if don't have already)
[SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
After successfully installing your docker desktop and SAM CLI no additional configuration is needed(for docker or CLI) just **keep docker desktop running** when running lambda.
Then you have to configure your lambda base on parameters needed for specific lambda.
First open _IntelijIdea run/debug_ configuration and select AWS Lambda.
Then configure it by adding your Handler class ,**example** **TocHandler**(should be located under  root/handler).
![Screenshot 2024-08-20 112254handler2.png](/.attachments/Screenshot%202024-08-20%20112254handler2-1e5634ad-a09a-4755-b5e8-1d62235b39d0.png)
Select your runtime based on your java version.
Add environment variables and input.
![Screenshot 2024-08-20 112513handler2.png](/.attachments/Screenshot%202024-08-20%20112513handler2-2b382a09-6ffc-400a-a6b1-46958d0b404d.png)
Input may vary from microservice ,so please find your trigger and input needed variables.
![Screenshot 2024-08-20 115557handler4.png](/.attachments/Screenshot%202024-08-20%20115557handler4-082b521e-2edc-4d37-a26d-608f81ea355b.png)
For example for toc-publisher ,it's S3 ,so we will have s3 input ,with this parameters, please fill only needed ones

```
`{
  "Records": [
    {
      "eventVersion": "2.0",
      "eventSource": "aws:s3",
      "awsRegion": "us-east-1",
      "eventTime": "1970-01-01T00:00:00Z",
      "eventName": "ObjectCreated:Put",
      "userIdentity": {
        "principalId": "EXAMPLE"
      },
      "requestParameters": {
        "sourceIPAddress": "127.0.0.1"
      },
      "responseElements": {
        "x-amz-request-id": "EXAMPLE123456789",
        "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH"
      },
      "s3": {
        "s3SchemaVersion": "1.0",
        "configurationId": "testConfigRule",
        "bucket": {
          "name": "a205159-cp-toc-service-dev",
          "ownerIdentity": {
            "principalId": "EXAMPLE"
          },
          "arn": "arn:aws:s3:::`a205159-cp-toc-service-dev`"
        },
        "object": {
          "key": "root-toc/x.xml",
          "size": 1024,
          "eTag": "7b02f40483b7435e491b4c59013e4bdd",
          "sequencer": "0A1B2C3D4E5F678901"
        }
      }
    }
  ]
}`
```

