Fork and clone https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_git/cp-doc-conversionws
•	Set a Tomcat global library in the left panel Platform Settings → Global Libraries. Use the lib folder from your apache tomcat installation.
![Picture1.png](/.attachments/Picture1-f71384aa-2797-49d7-8e55-15c5d5c136f4.png)

* Indicate Sources and Test and Resource folders from sources list.
•	Select "src" folder and click on "Sources"
•	Select "test" folder and click on "Tests"
•	(Optional) Select "web/WEB-INF/lib" folder and select "Resources"
•	(Optional) Select "test/lib" folder and select "Tests Resources"
![Picture2.png](/.attachments/Picture2-c13fe370-e122-4bfe-a69f-b35bcf541046.png)

Add project java dependency libraries. You will be asked if the newly created library should be added to a module. Select cp-doc-conversionws module and click "OK". You can rename the library later.
1.	App libraries from: cp-doc-conversionws\web\WEB-INF\lib
![Picture3.png](/.attachments/Picture3-b1cbe30f-23dd-49d1-9d3e-83df04615804.png)

2. JUnit libraries from: cp-doc-conversionws\test\lib
![Picture4.png](/.attachments/Picture4-4af3afb9-46b6-4e45-a375-7ae978169667.png)
3. Ensure that the Tomcat, App and JUnit libraries are added to the module Dependencies
![Picture5.png](/.attachments/Picture5-02364fc6-58fa-40ff-b962-c8ca82031894.png)
![Picture6.png](/.attachments/Picture6-e8a939ed-7bb2-4022-b056-bb0becd508ee.png)
![Picture7.png](/.attachments/Picture7-1b392089-dc75-428c-b1ca-e403a72a0262.png)
4. Set compile output paths for both app and test:
•	\out\production\cp-doc-conversionws
•	\out\test\cp-doc-conversionws
![Picture8.png](/.attachments/Picture8-e0a170b1-11a8-4ddc-92d9-81953f0c5979.png)
5. Add Web Facet. Facets → + → Web. Note: You'll be asked if the Web Facet should be added to any module. Select cp-doc-conversionws module and click OK. The Facet would be added to the Module. 
![Picture9.png](/.attachments/Picture9-b739df50-48de-4d9b-b72a-6d42c0d70ca9.png)
6. Edit the Deployment Descriptor (web.xml) and the Web Resource Directory paths to use the project paths
![Picture10.png](/.attachments/Picture10-488944a5-abea-4ba2-8e19-1bf6f2f2d0d2.png)
7. Add Application Artifact. Go to Artifacts → + → Web Application: Exploded → From Modules..., Select cp-doc-conversionws and click OK. 
![Picture11.png](/.attachments/Picture11-2b433b02-679e-46c1-8a57-64a2e55091f5.png)
![Picture12.png](/.attachments/Picture12-2859bbc8-378e-4667-94d1-73370155b989.png)
8. The Artifact should automatically add WEB-INF folder with all dependency libraries. Click OK to close Project Structure window.
![Picture13.png](/.attachments/Picture13-f0b5e078-5d12-45c9-ba3c-d51298896779.png)
9. Double click on "cp-doc-conversionws" in Available Elements section to add the compiled classes to the Artifact.
![Picture14.png](/.attachments/Picture14-fbed14c7-78ce-4e48-b734-61928d833a00.png)
![Picture15.png](/.attachments/Picture15-edf8fc53-fc10-4654-8b47-00cccee50fdb.png)
10. Configure Tomcat Application Server. Go to "Run"→ "Edit Configurations". Click on "+" → "Tomcat Server" → "Local". Configure as in the image. Note: Ensure you have the "C:\tmp\cplog" folder created in your system.
![Picture16.png](/.attachments/Picture16-a3eaafa1-aed6-405b-a9d2-e280f5d428b0.png)

VM Options:
-Xmn128m
-Xms1500m
-Xmx1500m
-Xss2m
-Dapp.log.dir=c:\tmp\cplog
-Dapp.http.port=9080
-Dapp.environment=Dev
-DappProperties=app.properties
-Dfile.encoding=UTF-8
-Djavax.xml.stream.XMLOutputFactory=com.sun.xml.internal.stream.XMLOutputFactoryImpl
-XX:+CMSParallelRemarkEnabled
-XX:+CMSClassUnloadingEnabled

11. In Deployment tab, Add the Doc Conversion artifact. Go to "+" → "Artifact...". It will add the "cp-doc-conversionws:war exploded" artifact automatically. Change the Application Context to "/" and click OK.
![Picture17.png](/.attachments/Picture17-12f4bf85-9ff5-4c32-8fe7-8e1a7ba0447e.png)

•  (Optional) If required, set VM Option "-DappProperties" to "appLocal.properties" file. And paste the following file into web\WEB-INF\properties folder. File: appLocal.properties


•  Edit "soap:address" in DocConversion.wsdl to use the address: 
"http://localhost:9080/services/DocConversion"
•  Build the project (Build → Build project) and run the server. Test with http://localhost:9080/services/DocConversion?wsdl.
You should see something like:
![Picture18.png](/.attachments/Picture18-f1cffa5c-e7c5-44f0-ac79-bca2beb88270.png)

•  or with http://localhost:9080 and see the message: "Place your content here".
•  To call DocConversion service from cp-web-app add the following line in "appLocal.properties":
prismDocConv.url=http://localhost:9080/services/DocConversion?wsdl


**Troubleshoot steps:**
1.Ensure that source roots are checked under facets section
![Picture19.png](/.attachments/Picture19-d7d28347-b2d0-476b-a2ec-49555c1f441a.png)
2.Under tomcat run configurations, check for application context path to be “/”  (IDE sets default address which might cause issue in running the application)
![Picture20.png](/.attachments/Picture20-2113e4c7-c1d8-4b20-8950-ad7b9c45ed2c.png)
3.	Make sure the soap address in DocConversion.wsdl file to be as shown below
- port number to be same as its present in the tomcat run configuration
<soap:address location="http://localhost:9080/services/DocConversion"/>