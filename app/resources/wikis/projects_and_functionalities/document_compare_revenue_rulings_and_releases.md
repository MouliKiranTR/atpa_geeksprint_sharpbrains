# Document Compare - Revenue Rulings and Releases

## Introduction

The purpose of this document is to give a better insight on how document compare microservice can process "Revenue Rulings and releases" documents. We want to maintain a single point of source, which would be beneficial for the development team with a side effect of improving the performance to query for documents to compare.

This document is related to item #93337.

Currently, document relationships for comparisons of these documents are generated in cp-web-app while the document is loaded, using their citator document (if any) in order to find certain citations within them, such as superseded, modified, etc. If they do exist and belong to the same ODS than the current document, then it is added to the list of possible documents to compare.

Here is some information per document

| **Document**      |**Databases**                      |**ODSes**          |**XPath to identify a doc from XML**| **TTA-REGION**| **Doc Date** |
|-------------------|-----------------------------------|-------------------|------------------------------------|-------------|--------------|
| Revenue Rulings   |rulng54, rulng70, rulings, advrulng|RULREV, PAYRULREV  |//n-docbody/TTA-DOCINFO/TTA-REGION                          | REVRULE_EXP |<FILEDT MDY="value"/>|
| Revenue Procedures|rulng54, rulng70, rulings, advrulng|RULPROC, PAYRULPROC|//n-docbody/TTA-DOCINFO/TTA-REGION                          | REVPROC_EXP |<FILEDT MDY="value"/>|
| Notices           |rulng54, rulng70, rulings, advrulng|RULNOT, PAYRULNOT  |//n-docbody/TTA-DOCINFO/TTA-REGION                        | NOTICE_EXP |<FILEDT MDY="value"/>|
| Citator           |citator                            |                    |//CTD                              |


In order to avoid unnecessary processing while loading a document in real-time, a migration to the new doc-compare microservice is recommended.

## Proposed Implementations

- The first approach is to have a similar behavior than the current functionality in cp-web-app. These would be the steps:
   1. Process all four databases separately: rulng54, rulng70, rulings, advrulng.
   2. Pull its XML file from S3.
   3. When any of the comparable documents (REVRUL, REVPROC, NOTICE) is found, call the metadata service and search for the **relationshipType=12** in the relatedDocuments list.
   4. Generate the S3 file path given the Id from the previous step and retrieve the citation document XML.
   5. Implement the cap-link service from the cap-link-client repository.
**Note**: Ask for Link DB credentials to @<19A56D73-8675-4E18-8787-EC5FD4C2E3FA>.
   6. Call the getInlineOutboundLinkTableLinks from LinkTblClient to retrieve all of the citator inline links, and create a map with its pinpoint destination as a key.
   7. Search in the citation XML for the citations that belong to the same ODS as the current document and that belong to certain citation types: Superseding, Superseded, Modified, Modifying, etc. 
**Note**: See recommendedCiteTypes EnumSet within DocCompareServiceImpl class in cp-web-app for a complete list of comparable citations and LinkCiteType enum in CPLinkData class for mapping "J" value to its corresponding Enum value.
   8. Map the citations obtained in step 7 with the inline links from step 6 by their pinpoint value.
   9. Add the document IDs to the relatedDocumentIds field in the current document entity.
   10. Update document for a two-way-relationship among related ones.
   11. Add placeholder registers for the relatedDocuments as well in case they do not exist.



- The second approach is process Citator (and AdvCitator) only documents which would avoid processing unnecessary databases:
**NOTE**: As per sorting requirement, this approach is no longer recommended.
   1. Process CITATOR database to be consumed by the doc-compare-service. (E.g. iCITATOR:206603.1)
   2. Implement the cap-link service from the cap-link-client repository.
   3. Call the getInlineOutboundLinkTableLinks from LinkTblClient to retrieve all of the citator inline links, and create a map with its pinpoint destination as a key.
   4. Search in the Citation XML for the current document related to the current citator using the CTD tag. Identify the type of it (REVRUL, REVPROC, NOTICE) and get the document Id from the map created in point 3 given the pinpoint destination (E.g. CITATOR:206603.3-1). 
   5. Get the additional information from the metadata service using the DocId.
   6. Parse all the <CTG> tags under <JUDICIAL-HISTORY> to find the comparable citations with same ODS (REVPROC, REVRUL, NOTICE). Consider the "J" value to determine which are comparable.
**Note**: See recommendedCiteTypes EnumSet within DocCompareServiceImpl class in cp-web-app for a complete list of comparable citations and LinkCiteType enum in CPLinkData class for mapping "J" value to its corresponding Enum value.
   7. Map the citations obtained in step 6 with the inline links from step 5 by their pinpoint value.
   8. Add the document IDs to the relatedDdocumentIds field in the current document entity.
   9. Update document for a two-way-relationship among related ones.
   10. Add placeholder registers for the relatedDocuments as well in case they do not exist.

Example of citator document:
```XML
<CTD>
	<!-- Title - First link that redirects to the current document. SRCEID = Pinpoint dest, use Link service to get DocId -->
	<SRCLNK SRCEID="CITATOR:206603.2-1">
		<CTDRULE T="REVR" N="69-651" D="" R="1969-2 CB 135" A=""/>
	</SRCLNK>
        <!-- Use T attribute of CTDRULE tag to determine current Doc Type. E.g. REVR = Revenue Ruling -->
	<CTDRULE T="REVR" N="69-651" D="" R="1969-2 CB 135" A=""/>
	<MARKER MRKDATE="19770415" MRKTIME="00000000" MRKEID="CITATOR:206603.2" MRKTYPE="DU"/>
	
	<!-- Links to related documents -->
	<JUDICIAL-HISTORY>
		<!-- Considers J value to determine which ones to pick -->
		<CTG E="" I="" J="m" CD="19770101" UD="19770101">
			<SRCLNK SRCEID="CITATOR:206603.3-1"> <!-- SRCEID = Pinpoint destination to cite (related document) -->
				<RULE T="REVR" N="71-493" D="" R="1971-2 CB 240" A=""/>
			</SRCLNK>
                        <!-- Use T attribute of RULE tag to determine Doc Type. E.g. REVR = Revenue Ruling, It should be the same as main document -->
			<RULE T="REVR" N="71-493" D="" R="1971-2 CB 240" A=""/>
			<MARKER MRKDATE="19770101" MRKTIME="00000000" MRKEID="CITATOR:206603.3" MRKTYPE="DU"/>
		</CTG>
	</JUDICIAL-HISTORY>

</CTD>
```

These are the values from the document Entity for "Revenue Rulings and Releases":
- **docId**: From LinkTblClient
- **title**: From Kinesis data in first approach or Metadata service from second approach
- **docLink**: from docId above
- **docDate**: From S3 document given XML link in Kinesis data (<TTA-DOCDATE tag="FILEDT" attr="MDY">, <FILEDT MDY="value"/>, or <TTA-CHANGEDATE>) or from Metadata
- **odses**: From metadata.
- **relatedDocIds**: From Citator XML under <JUDICIAL-HISTORY> tag +  LinkTblClient


**Both** approaches would need to remove the current cp-web-app functionality to call this service instead.

::: mermaid
graph TB
   Cit(Load Citator) --> DocDetails(Get Current document details);
   DocDetails --> LoadRelated(Get citations under Judicial History)
   LoadRelated --> isComparable{Is comparable}
   isComparable -->|No| I(Ignore cite)
   isComparable -->|Yes| cite(Get cite docId)
   cite --> add(Add DocId as related)
   add --> save(Save to DB)
   save --> placeholder(Add placeholder for related Docs for two-way comparison)
:::


##Recommended stories:

1. [DCO] Implement cap link service to retrieve link information
2. [DCO] Migration of Revenue Rulings and Releases
3. [DCO] Remove current cp-web-app functionality

###Repositories:
- https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_git/cap-metadata-service
- https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_git/cap-link-client

##References:
- https://lucid.app/lucidchart/5e910629-89c5-4131-a01b-3019b0508fcd/edit?page=0_0&invitationId=inv_3f95e18d-dd6a-49ac-afdd-dbb50d704bda#
- https://lucid.app/folder/invitations/accept/inv_b09fca31-b8db-4c69-a0db-e09e6185bd3e
