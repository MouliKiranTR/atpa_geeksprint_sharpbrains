# Summary
Users are having their user details page access time out. This was cause by the slow performance to the Get Orders for Users query. This query was very performant in Oracle but it performs very poorly in Postgres. 

**Owner:** @<1EEF89FE-A95B-429D-8940-CDDFCF32AD59> 
**Contributors:** @<0ED19A06-8ED7-6233-8278-DD84CD11EBEE>, @<2B24B1EC-0C3E-6D78-8168-4BBC94754190>, Venkat Dangeti (CSS), Pavan Medarametla(West DBAs)
**Reported By:** Aldric Rowe
**Incident:** [INC6669020](https://thomsonreuters.service-now.com/nav_to.do?uri=%2Fincident.do%3Fsys_id%3D038e2ffd1bd4d694b66ea7d8b04bcb32)

## Root Cause
The root cause is a very slowly performing DB query for getting the orders related to a user. This in turn caused DB session backups as queries were queued and waiting for these queries to complete. This caused slow response times to the user and resulted in a number of timeouts.

## Investigation 
1. DD traces showed that the app servers were running fine but did have a high level of latency
1. The Postgres DB was having slow response times.
1. All of the slowly responding queries were exactly the same. A query we call "Get Orders for a User"
1. Since it is slow running this caused a backup of DB Sessions waiting for their turn to run.
1. Over a matter of about 30 minutes the backed up DB sessions cleared up.
1. The User details page the started to return but it is still very slow.

## Next Steps: 
This is a DB query performance issue. 
1. This is a know performance issue.
1. The performance fix is QA/DEMO for testing.
1. It will be promoted to QED on Sept 3rd, 2024.
1. It will deploy with the September release on Sept 6th, 2024.

Aldric Rowe or Brian Walpert in tech support put a message up to inform our customers of the performance issue and a timeline of when it will be resolved.