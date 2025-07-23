We had a new ask to delete Internal Revenue Code from the under used More... section of Find by Citation.
To achive this we have to 

- Clean up the JSP files. 
- Clean up the configuration.

JSP files are located in web-app ,under CPWar/web/v10/jsp/Templates.
We have to find the one we need and delete it.
But to remove it from list on templates there is a need to clean up configuration as well.
It should be done on database level.
We need to remove the template configuration from the CM master tables which should then remove them from the checkpoint tables.
__PLEASE NOTE_: Deletion from CM master tables should be done by ?
Here is the list of templates where changes should be done

1. **ods** table - find ods by id or name ,and UPDATE the value of **f_temp_id** to **null**
1. **ods_tmpllistref_xref** - find by ods_id and DELETE all the records(please check if you have to 
1. **final_template** - find by f_temp_id and **DELETE** record
1. **final_template_jsp** - find by jsp_id and **DELETE** record
1. **final_template_xref** - find by f_temp_id and **DELETE** record.

![Screenshot 2024-12-23 134606db.png](/.attachments/Screenshot%202024-12-23%20134606db-c3beabb1-cda9-4b8d-9fd3-4fccd6ac4b33.png)

After this changes CPS build picks up changes once a day and it will bring changes to checkpoint.
To test this out we first have to check if changes is visible on CI database after build process is done.
If this step is done correctly , we have to check also practods files, as application is not looking directly to database but to practods. This file is generated from the tables we have updated .
We can do this by checking this file directly from NOVUS, we can check this via Easel by querying by guid.
![Screenshot 2024-12-23 140359code.png](/.attachments/Screenshot%202024-12-23%20140359code-f747f8ee-06c2-4052-a00a-fe944bd8d9e7.png)


