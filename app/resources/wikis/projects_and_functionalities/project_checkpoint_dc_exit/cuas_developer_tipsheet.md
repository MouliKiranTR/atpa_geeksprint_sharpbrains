This document contains tips for the CUAS Developers working on bug fixes for the DC Exit project.

# Contacts
- **PM:** @<2B24B1EC-0C3E-6D78-8168-4BBC94754190> 
- **DM**: @<F34AE528-328C-6FF1-B8A8-7502D9B6C231> (Very limited knowledge of CUAS)
- **Architects**: @<34F78585-59F3-6EB2-991D-65625C11D736> and @<0ED19A06-8ED7-6233-8278-DD84CD11EBEE> 
- **Platform CM**: <font color="blue">**Upadrasta, Dinakar (Extranet)**</font> and <font color="blue">**Pusukuri, Pavankumar (Extranet)**</font>, @<0543612D-CDD7-6D3A-93D9-009AEA1EA850> (US PM Hours)
- **DBA**: @<8FB0F476-2B36-6D18-BEFE-CF9A7C7FF76F>
- **DB Devs**:
   - <font color="blue">**Yauheni Dzenisenka (Extranet)**</font>
   - <font color="blue">**Iurrii Golubnichenko (Extranet)**</font>
   - <font color="blue">**Adilkhan Kaikenov (Extranet)**</font>
   - <font color="blue">**Dzianis Haladushka (Extranet)**</font>
- **Checkpoint Dev Lead**: @<19A56D73-8675-4E18-8787-EC5FD4C2E3FA> 
- **CUAS Dev Lead**: @<1EEF89FE-A95B-429D-8940-CDDFCF32AD59> 
- **CUAS Devs**:
   - @<E2E52886-51B6-6B20-AFC8-343E9828F5A6> 
   - @<E371540B-30C9-60AC-93CA-5595F784C81F> 
   - @<E412A25B-11F9-47B3-970A-62F6B65EC5E2> 

# Need to Know
- The Cloud CUAS-API is not being built and deployed into CI automatically. The CI deployment for cloud must be requested from Platform CM. Use the [CUAS channel](https://teams.microsoft.com/l/channel/19%3A5eb66f5cd34b41b7a696fb86f286532b%40thread.tacv2/CUAS?groupId=f1eb32ec-6aff-4ee7-bc44-15b0bb0a3886&tenantId=) in the [Checkpoint and CUAS DC Exit Project](https://teams.microsoft.com/l/team/19%3ATv1j58W5TJHfMdRc9MJ5_z-dQHTgHcWaaga1igagHmc1%40thread.tacv2/conversations?groupId=f1eb32ec-6aff-4ee7-bc44-15b0bb0a3886&tenantId=62ccb864-6a1a-4b5d-8e1c-397dec1a8258) in MS Teams
- Pull latest code and perform Check-ins using the [TFVC repo](https://dev.azure.com/tr-tax-default/CheckpointUserAdministration/_versionControl). 

# Check-in Requirements (in addition to normal)
- All Changes must be tested on PostgreSQL and Oracle
- Notify the CUAS team with any changes that may impact them.
- If a DB change to the DDL are needed make sure to work with the DBA.
   - We need to make sure that things still work on both so a DDL change in Postgres should not break the application for Oracle.
- **Only 1** code review is necessary for DC Exit changes. This is to help speed up getting fixes into an environment for it to be tested since we don't have a lot of time.
- Check-ins should be made into the TFVC repo.

# Developer Tips
Developers should add any tips they have that will help others to get their job done more accurately and more quickly. Reducing our time to issues will help us build confidence more quickly.

## Simultaneously Run Against Oracle and PostgreSQL
Inside Intellij you can run two instances of the CUAS-API. One can be pointed at Oracle and the other can be pointed at PostgreSQL. This will speed up your development testing so that you don't have to start the API against Postgres, test, shutdown, start the API against Oracle, test, shutdown. Instead, you can bring up both at once.

@<1EEF89FE-A95B-429D-8940-CDDFCF32AD59> has pushed some Intellij run configurations.
1. Get latest CUAS-API code from TFVC
2. Make sure that cuas-api.properties has `cuas.database.type=oracle`
3. Create a copy of cuas-api.properties
   1. Rename the copy to cuas-api-postgres.properties
   2. Change the cuas-api-postgres.properties file so that `cuas.database.type=postgres`
   3. Save cuas-api-postgres.properties into the same directory as cuas-api.properties.
4. You can now utilize the following run configurations:
   1. **CUAS-API : Run App - Oracle**: Starts the API with Oracle as the DB
   2. **CUAS-API : Run App - Postgres**: Starts the API with Postgres as the DB
   3. **CUAS-API : Run App - Both DBs**: Starts 2 instances of the API. One connected to Oracle and the other connected to Postgres. This is very helpful when you want to test changes in both environments.
5. Test your changes against both DBs.
6. Do not checking you cuas-api-postgres.properties file. This is for local development only.

Note: To run that API at the same time both APIs must have a unique port.
- localhost:8080 - Oracle
- localhost:8081 - Postgres

## More Tips - User the H2 heading for each  tip.

# Solutions to Common Errors
This section should be used for posting bugs which may end up having multiple instances and what was done to fix it. An example of this could be a DB type error. You may find and fix one instance of this error but as testing goes on other instances may be found. If so, devs can come here first and see if there is already a solution posted for their issue.

## Insert Fails
A number of inserts have failed because the sequence in Postgres is behind the table ID column and it is attempting to insert a record with an ID value that already exists.
- You should receive a SQLException indicating that the item cannot be inserted due to the sequence. If not, then this is not your issue and it will need more investigation.
- Run the following command to see what the current value of the sequence is.
   ```SQL
   SELECT currval('checkpoint.a_order_seq');
   ```
- Select the last ID in the table via a select on the table that the sequence applies to.
   ``` SQL
   SELECT * FROM checkpoint.a_order
   ORDER BY order_id DESC
   LIMIT 1;
   ```
- Run the follow SQL to advance the sequence to the appropriate id. The number in this example is the ID identified in the pervious query.
   ```SQL
   SELECT setval('checkpoint.a_order_seq', nextval('checkpoint.a_order_seq') + 1777504);
   ```
- Connect with DBA to notify them that this will need to be fixed in all environments. They should have this added to the DB migration process. We do not want this to happen in the Prod DB.
   - Note: I have been seeing the sequences get reset when a data refresh is done. This is an ongoing issue that we need to resolve with the DBA.

It is likely that inserts into that table will now function properly.

## SQL Syntax Errors
The following list are syntax issues where Postgres does work but it does work in Oracle.

The majority of these syntax errors need to be handled by:
1. Adding the Oracle syntax in `oracle.properties` and the Postgres syntax in `postgreSQL.properties`. 
   - Name your new SQL properties with the `[CLASS_NAME].[METHOD_NAME]`
   - Example Property Name: `CiamUserDataMigrationService.checkAccountReadiness`
   
2. In the groovy code you will need to use the `DatabaseResolver.instance.getSql([SQL_PROP_NAME_STRING])`.

### SYSDATE - Example:
- @<E412A25B-11F9-47B3-970A-62F6B65EC5E2> could you enter an example for this?
### TRUNK
- @<E412A25B-11F9-47B3-970A-62F6B65EC5E2> could you enter an example for this?
### ROWNUM - Example:
   - In `CiamUserDataMigrationService.groovy` there is a query inside the `checkAccountReadiness` which used the following syntax:
       ```SQL
       ) WHERE ROWNUM <= :limit
       ```
   - This was replace with the following:
      ```Java
      ) WHERE /$ + DatabaseResolver.instance.getSql("CiamUserDataMigrationService.checkAccountReadiness") + $/ <= :limit
      ```
   - This change also requires changes to:
      - oracle.properties
         ```
         CiamUserDataMigrationService.checkAccountReadiness=ROWNUM
         ```
      - postgreSQL.properties
         ```
         CiamUserDataMigrationService.checkAccountReadiness=ROW_NUMBER() OVER()
         ```
   - The syntax error is now resolved and works with both Oracle and Postgres.