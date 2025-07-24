_The document explains different solutions to link to different checkpoint content from the Contract Express tool._

## Document Preview Linking:
Open a Checkpoint Document in preview mode for the requested docId.

### - For migrated content:
- URL Format: {domain}/app/main/docPreviewBySrcEid?ceAction=docPreview&srcEid={srcEid}
  _domain:_ domain for a specific environment [DEV, QA, PreProd, Prod].
  srcEid: source marker id.
- Sample Link:
  Document: Form 10-K Annual Report Pursuant to Section 13 or 15(d) of the Securities Exchange Act of 1934
  Prod URL: https://checkpoint.riag.com/app/main/docPreviewBySrcEid?ceAction=docPreview&srcEid=FRMCLHD:616.385

NOTE: 
- Mapping for SRCEID and DESTEID must be present in CHEKCPOINT."SNAP$_LINK_TBL_SNAP_1". If it isn't there, then the user will be redirected to the home screen.
- CPS pushes the nightly snapshot of valid mapping from CPS DB -> RIA_WEB [Schema] -> LINK_TBL [Table].

![Contract Express - Linking - Detailed.jpeg](/.attachments/Contract%20Express%20-%20Linking%20-%20Detailed-d1697270-4fa3-414f-b477-b965f1085d90.jpeg)

### - To link new content:
- URL Format: {domain}/app/view/previewDocNew?feature=ttools&preview=y&DocID={doc_guid}&&pinpnt={paragraph_markerid}
  _domain:_ domain for a specific environment [DEV, QA, PreProd, Prod].
  _doc_guid:_ Checkpoint document GUID. [Mandatory Parameter]
  _paragraph_markerid:_  MRKEID of a <MRKEID> tag to point to specific content in a document. [Optional Parameter]
- Sample Link:
  Document: A4: The Comprehensive Internal Control Methodology
  Prod URL [Without pinpnt]: https://checkpoint.riag.com/app/view/previewDocNew?feature=ttools&preview=y&DocID=i38eea782504c11deab420a48868caa77
  Prod URL [With pinpnt]: https://checkpoint.riag.com/app/view/previewDocNew?feature=ttools&preview=y&DocID=i38eea782504c11deab420a48868caa77&pinpnt=FRMPIC:1727.14

---

## TOC Preview Linking:
- Open a TOC tree view in preview mode for the requested tocId.
- URL Format: {domain}/app/view/previewTocNew?preview=y&baseTid=_{toc_id}_
  _domain:_ domain for a specific environment [DEV, QA, PreProd, Prod].
  _toc_id:_ TOC node id.
- Sample Link: 
  TOC Node: A4: The Comprehensive Internal Control Methodology
  Prod URL: https://checkpoint.riag.com/app/view/previewTocNew?preview=y&baseTid=T0GAAPCD13%3A3318.1
---

## Contract to Contract Linking:
`<a target="_blank" href="{tool url}"> {Clickable content} </a>`
- **Tool URL format:**  /app/view/ceInterviewPopup?ceAction=createContract&ceTemplateName=_{template_name}_&ceToolType=_{tool_type}_&DocID=_{parent_document_guid}_&pageNumber=_{page_number}_
    - _template_name_:              Template name from contract express portal.
    - _tool_type_:                        document-assembly OR checklist OR decision-tool OR calculator
    - _parent_document_gui_:    Checkpoint document guid that tool belongs to
    - _page_number_:                 To open a linked contract on a specific page [paragraph]

Sample URL: <a target="_blank" href="https://checkpoint.riag.com/app/view/ceInterviewPopup?ceAction=createContract&ceGuid=i6751544a6f4ce54fa168e7eff0f36ddf&ceTemplateName=GAAP_public_annual&ceToolType=ce-checklist&implType=CE">Public Annual Financial Statement Disclosure Checklist</a>

`<a target="_blank" href="https://checkpoint.riag.com/app/view/ceInterviewPopup?ceAction=createContract&ceGuid=i6751544a6f4ce54fa168e7eff0f36ddf&ceTemplateName=GAAP_public_annual&ceToolType=ce-checklist&implType=CE">Public Annual Financial Statement Disclosure Checklist</a>`

---

## Permanent link to the Checkpoint reference document:
- **How to get the permalink of the reference document:**
1. Go to the reference document (Example: [Subsequent Measurement](https://checkpoint.riag.com/app/view/previewDocNew?feature=ttools&preview=y&DocID=iGAAPCD13%3A7653.1&pinpnt=GAAPCD13:7670.43))
2. Get the permalink through the following button in the tools bar:
![==image_0==.png](/.attachments/==image_0==-30eef699-48d0-4d34-a3d0-5b9a9b0427fc.png) 

3. Click on the permalink button that appears at the top of the document and copy the link in a notepad. 
![image.png](/.attachments/image-3d5b3740-e812-4db2-bd14-0594ff2566f4.png)
Permalink sample: https://checkpoint.riag.com/app/find?begParm=y&appVer=25.06&dbName=GAAPCD13&linkType=docloc&locId=gaapcod_350-20-35&ods=GAAPCODCODE&permaId=iGAAPCD13%3A7653.1&permaType=doc&tagName=GAAPSECTION&endParm=y

4. Get the _pinpoint_ of the cited paragraph and added to the permalink.
Sample: &pinpnt=_{pinpoint_id}_
    - _pinpoint_id_:              ID of the cited paragraph

   Permalink sample with pinpoint: https://checkpoint.riag.com/app/find?begParm=y&appVer=25.06&dbName=GAAPCD13&linkType=docloc&locId=gaapcod_350-20-35&ods=GAAPCODCODE&permaId=iGAAPCD13%3A7653.1&permaType=doc&tagName=GAAPSECTION&endParm=y&pinpnt=GAAPCD13:7668.43

5. Add the following identifier: _#ceCitedDoc_
Permalink sample with identifier: https://checkpoint.riag.com/app/find?begParm=y&appVer=25.06&dbName=GAAPCD13&linkType=docloc&locId=gaapcod_350-20-35&ods=GAAPCODCODE&permaId=iGAAPCD13%3A7653.1&permaType=doc&tagName=GAAPSECTION&endParm=y&pinpnt=GAAPCD13:7668.43#ceCitedDoc
