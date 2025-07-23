When configuring Checkpoint DB for the first time.

1. We need to have access to the DB to get our credentials; In case you do not have them you can raise a request to the DevOps team requesting the access and they will provide you your credentials.
2. Download Oracle SQL Server: https://www.oracle.com/tools/downloads/sqldev-v192-downloads.html
3. We need to modify the following configuration file according to our credentials: [CPDBConnection (1).json](/.attachments/CPDBConnection%20(1)-6eb8db16-0d3b-429b-9193-be2cf9bef71b.json)
4. Search for all the "user" coincidences and replace them with your DB username. <IMG  src="https://kb.epam.com/download/thumbnails/1094356665/image2020-7-14_11-17-57.png?version=1&amp;modificationDate=1594743493272&amp;api=v2"/> there are 4 places where you are gonna need to change.
5. Save the file.
6. Open SQL Server and select "Import Connections".
<IMG  src="https://kb.epam.com/download/attachments/1094356665/image2020-7-14_11-23-10.png?version=1&amp;modificationDate=1594743806124&amp;api=v2"/>
7. Browse the configuration file that you previously edited and select the file.
<IMG  src="https://kb.epam.com/download/attachments/1094356665/image2020-7-14_11-25-22.png?version=1&amp;modificationDate=1594743938484&amp;api=v2"/>
8. Select all the connections and click on finish.
<IMG  src="https://kb.epam.com/download/attachments/1094356665/image2020-7-14_11-26-11.png?version=1&amp;modificationDate=1594743987417&amp;api=v2"/>
9. After this, it will load the databases. Once you try to expand each of them you are gonna required to introduce your password that you got with your credentials. **NOTE:** If your password _has expired_ you can reset it, clicking in the database, and selecting "reset password...".
<IMG  src="https://kb.epam.com/download/attachments/1094356665/image2020-7-14_11-27-44.png?version=1&amp;modificationDate=1594744080416&amp;api=v2"/>
10. That's all... Under "Oher Users" and CHECKPOINT you are gonna be able to see the databases and apply each query if needed.
<IMG  src="https://kb.epam.com/download/attachments/1094356665/image2020-7-14_11-29-18.png?version=1&amp;modificationDate=1594744174088&amp;api=v2"/>