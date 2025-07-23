_The document explains the content format and parsing of Contract Express tools. This is useful to display a launch button/clickable URL for a tool._

## **To display the launch button in Checkpoint Document:**

### XML tags/attributes value in the context of CE tool:

| Tag/Attribute | Description |
|--|--|
| _impl-type_ | Helps to identify CE tools and create a launch URL for CE tools. |
| _tool-type_ | Helps identify the type of CE tool. Tool-Type is used to determine the launch button title and also to filter the content in the import answers feature. |
| _<related-app-property name="FILENAME">_ | This is the CE template name. web-app uses this to create a contract. |
| _<related-app-property name="guid">_ | For migrated tools, it is a HotDocs GUID. |
| _<content-lable>_ | Helps to display tools title in the right panel of document view to create a jump to tool URL. |


### Sample XMLs:
- To Display "Launch Document Assembly"
```XML
<related-app-content display="popup" impl-type="CE" tool-type="DOCUMENT-ASSEMBLY">
      <description>Replacement cost method for valuing vehicle parts inventory</description>
      <content-label>Replacement cost method for valuing vehicle parts inventory</content-label>
      <related-app-property name="FILENAME">1110</related-app-property>
      <related-app-property name="guid">i913042ba24c3ec7ef6b5a6244d9785ad</related-app-property>
</related-app-content>
```
- To Display "Launch Checklist"
```XML
<RELATED-APP-CONTENT DISPLAY="popup" IMPL-TYPE="ce" TOOL-TYPE="ppcChecklist">
     <DESCRIPTION>Checklist for COVID-19 Relief and Disclosure Guidance</DESCRIPTION>
     <CONTENT-LABEL>Checklist for COVID-19 Relief and Disclosure Guidance</CONTENT-LABEL>
     <RELATED-APP-PROPERTY NAME="filename">secexp_COVID</RELATED-APP-PROPERTY>
     <RELATED-APP-PROPERTY NAME="guid">ibe25993a6dc260cfa9b685babc257212</RELATED-APP-PROPERTY>
</RELATED-APP-CONTENT>
```

**NOTE:** cp-tools-service parses the same content to support "Tools Search" and provides "Related Tools" to cp-snapshot-service.

---
## **To display a clickable link in [Tools -> Interactive Tools]:**
1. Different interactive tools that supports Contract Express tools,

| Tools | Novus GUID | Sample XML |
|--|--|--|
| Depreciation Calculator | iCALCBROWSE | `<CALCULATOR TYPE="ce-calculator" FILENAME="DepreciationCalculator" GUID="DepreciationCalculator"><TITLE>Depreciation Calculator</TITLE><ODS ID="PPCDEPPCALC"/></CALCULATOR>` |
| Interactive Checklist | iCHECKLISTBROWSE | `<CHECKLIST TYPE="ce-checklist" FILENAME="gaapcis_22" GUID="i6d0dfe31e1b067c3e8fdd0c0384a7939"><marker mrkeid="BROWSEDB:3521.1" guid="c5598f50ee64e38ac2fdbf4e2309ce66" mrktype="du" mrkdate="20230329" mrktime="13282544"/><TITLE>Implementation of New Accounting Standards</TITLE><ODS ID="TRCONFRM10100"/></CHECKLIST>` |
| Financial Management and Controllership | iFINTOOLSBRO | `<TOOL ID="corpgov_frmpic_2" IMPL-TYPE="ce" TOOL-TYPE="ppcChecklist"><MARKER MRKEID="FINTOOLSBRO:13.1" MRKTYPE="ld du" MRKDATE="20230330" MRKTIME="10191748"/><TITLE>Internal Control Overview Checklist</TITLE><ODS ID="FINMAN"/></TOOL>` |

2. XML attributes value in the context of CE tool:

| Attribute | Description |
|--|--|
| _TYPE_ | Helps to identify CE tools and their tool type to create a launch URL. For <CALCULATOR> and <CHECKLIST>. |
| _FILENAME_ | This is the CE template name. web-app uses this to create a contract. For <CALCULATOR> and <CHECKLIST>. |
| _GUID_ | For migrated tools, it is a HotDocs GUID. For new tools created in Contract Express, it will same as FILENAME. For <CALCULATOR> and <CHECKLIST>. |
| _ID_ | This is the CE template name. web-app uses this to create a contract. For FINMAN <TOOL>. |