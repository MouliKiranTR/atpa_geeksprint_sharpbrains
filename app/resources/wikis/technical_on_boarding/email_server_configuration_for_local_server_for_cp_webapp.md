In local server set up on a developers machine, the email server property needs to updated to send emails from local server in appDevServer.properties file. The following property needs to have this new value-

`email.server = relay-internal.int.thomsonreuters.com`

This will allow the local server to send emails. Without updating this value, local servers will receive timeout while trying setup the smtp server like this-


```
Error ID: CPEmailUserTask$EmailTransport.setupData.msgEx
Text: Messaging Exception 
Exception (depth 1):
Stack Trace: com.sun.mail.util.MailConnectException: Couldn't connect to host, port: relay.corp.services, 25; timeout -1;
  nested exception is:
                java.net.ConnectException: Connection timed out: connect
                at com.sun.mail.smtp.SMTPTransport.openServer(SMTPTransport.java:2118)
                at com.sun.mail.smtp.SMTPTransport.protocolConnect(SMTPTransport.java:712)
                at javax.mail.Service.connect(Service.java:366)
                at javax.mail.Service.connect(Service.java:246)
                at javax.mail.Service.connect(Service.java:195)
                at com.tta.checkpoint.utils.CPSmtpTransport.connect(CPSmtpTransport.java:138)
                at com.tta.checkpoint.taskProc.newsStdSeqTask.CPEmailUserTask$EmailTransport.setUp(CPEmailUserTask.java:333)

```

For more information, please follow this [migration guide](https://trten.sharepoint.com/sites/SMTPRelay/SitePages/Migration-Guide.aspx).


