## Previous Contract Express Version: 8.10.33994
## Current Contract Express Version: 9.5.36515

---

_All these configuration changes need to be performed on Contract Express App and DB instances._

### Update: ProductsConfig.json
**Change:** Replace the "TemplateLicenceId" attribute for the Checkpoint client with the appropriate Licence value of Checkpoint. [Current LicenceId = 1]
   - To allow template access to checkpoint users, update the TemplateLicenceId.

**Change:** Set ShareHomeFolder property value to "true".
   - To allow users to share the contract with other users within the same licence space. It gives owner of the contract full permission to access the ACL endpoints.

---

### Update: appSettings.json
**Change:** Add checkpoint domain to [Content-Security-Policy -> frame-ancestor] header.
- This change allows rendering of contract express content within checkpoint popup.
- CE Test Env. CSP value:
`content-security-policy: default-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com/; object-src 'none'; script-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self' https://fonts.gstatic.com/; frame-ancestors 'self'; frame-src *; connect-src 'self' https://ce.contractexpress.com:4431/ https://ce.contractexpress.com:4432/; sandbox allow-popups allow-forms allow-same-origin allow-scripts; base-uri 'self';`
- CE Prod Env. CSP value:
`content-security-policy: default-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com/ https://use.fontawesome.com/; object-src 'none'; script-src 'self' https://www.webspellchecker.net/ https://cdn.pendo.io/agent/static/ https://data.pendo.io/data/ https://pendo-io-static.storage.googleapis.com/ https://app.pendo.io/ 'unsafe-inline'; img-src 'self' https://*.highq.com data: https://stats.g.doubleclick.net https://data.pendo.io/data/; connect-src 'self' https://stats.g.doubleclick.net https://data.pendo.io/data/; font-src 'self' data: https://fonts.gstatic.com/ https://use.fontawesome.com/; frame-ancestors 'self' https://preprod.checkpoint.thomsonreuters.com https://checkpoint.riag.com https://riacheckpoint.com; frame-src * blob: ; child-src * blob: ; base-uri 'self';`

---

### Create an API client

![image.png](/.attachments/image-00b3ba4b-cc40-42bc-8d52-78ac62c27aec.png)

- Use the generated Client_ID in the checkpoint web-app and below DB scripts.

---

### Database changes
_NOTE: First verify the tables. If it doesn't match the below description then run the script._

**Tables:** Client, Client_Secret, Client_Scope, ClientCustomeGrantTypes, Licence

Migrate Checkpoint API client authentication to the new flow. Default value = 0.
- _Table: Client_
- `Query: SELECT * FROM CLIENT WHERE FLOW <> 5 AND CLIENT_ID = {checkpoint_api_client_id};`
If flow value != 0 then  `UPDATE CLIENT SET flow = 5 WHERE client_id = {client_id};`

Should have 3 rows for a client_id. One for each scope value.
- _Table: Client_Scope_
- One row with each scope value: (CEAPI, offline_access, openid)

Add record with grant_type=checkpoint for a client_id to enable SSO.
- _Table: ClientCustomeGrantTypes_
- `QUERY: INSERT INTO ClientCustomeGrantTypes(GrantType, Client_Id) VALUES('checkpoint', 13);`

Add record with id=-1 to enable multi-tent trial sign up.

	Table: Licence [CE Checkpoint auth DB]

	QUERY:
	SET IDENTITY_INSERT dbo.LICENCE ON
	declare @LICENCE XML

	SET @LICENCE = '<Licence>
	  <Name>10 year long</Name>
	  <Expiry>2024-01-01T00:00:00.0000000</Expiry>
	  <Users>1</Users>
	  <IsTrial>false</IsTrial>
	  <AllowGuests>false</AllowGuests>
	  <VaryTerms>false</VaryTerms>
	  <Signature xmlns="http://www.w3.org/2000/09/xmldsig#">
		<SignedInfo>
		  <CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315" />
		  <SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1" />
		  <Reference URI="">
			<Transforms>
			  <Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature" />
			</Transforms>
			<DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1" />
			<DigestValue>akadC1OFeQDfZxManUH0hm57Kek=</DigestValue>
		  </Reference>
		</SignedInfo>
		<SignatureValue>EkMF60k4ref6qrX23rOyoVgx0mbW6xtTEAxC84Wwyb7NlwHnfezR5Cguj31h0JLCk7ClCEGxY0fKzP+ei6eIC5Z31E+1+ZPZy5D2Dp5m8zDs0wwblYQhfWoiaezOM+q03twZdVj2WGqKblWQQFlu9S/IbzVvnPCti9U9CQi/hPg=</SignatureValue>
	  </Signature>
	</Licence>'

	select @LICENCE

	INSERT into dbo.LICENCE (LICENCE_ID, NAME, LICENCE, VALID_TO, USER_LIMIT, DATA_STORE, READ_ONLY, VARY_TERMS, ALLOW_GUESTS,
	ISSUER_URL, ISSUER_NAME, REALM, ALLOW_REPO_ACCESS, REPO_ID, REPO_SECRET, LICENCE_KEY, LICENCE_TYPE, TIER1_LIMIT, TIER2_LIMIT, ALLOW_PUBLIC_FLOWCHARTS, RESTRICTED)
	values
	(-1,'Trial Licence Permit',@LICENCE,NULL,100,'ContractExpressEntities',0,0,1,'','','',0,NULL,NULL,NULL,0,1,0,0,0);

	SET IDENTITY_INSERT dbo.LICENCE OFF;
	

Fix Access to CheckpointUser Home Folder:
	
	/* 
	 * To provide full permission on user's home folder for newly created users. 
	 * NOTE: Could be done by setting ShareHomeFolder=true in ProductsConfig.json file.
	 */
	{
		select * from LICENCE_SPACE 
		where DEFAULT_PROFILE = N'Checkpoint' 
		and TEMPLATE_LICENCE_ID <> LICENCE_ID 
		and SHARE_HOME_FOLDER <> 1;
	
		
		UPDATE LICENCE_SPACE 
		SET SHARE_HOME_FOLDER = 1
		where DEFAULT_PROFILE = N'Checkpoint' and TEMPLATE_LICENCE_ID <> LICENCE_ID and SHARE_HOME_FOLDER = 0;
	}


	/* Check for users who don't have full permission on their home folder */
	{
		/* Select user with insufficient permission */
		select F.* 
		from FOLDER F inner join USER_SETTINGS U on U.HOME_FOLDER_ID = F.FOLDER_ID inner join LICENCE_SPACE L on F.LICENCE_ID = L.LICENCE_ID
		where L.DEFAULT_PROFILE = N'Checkpoint' and L.TEMPLATE_LICENCE_ID <> L.LICENCE_ID 

		/* 
		 * NOTE: Only execute below update if above select query returns at least 1 row.
		 * Update the user(s) access to thier home folder with Full permission.
		 */
		update F
		set F.ACL = N'<Claims><Rule Seq="1" Claim="userid" Value="'+U.USER_ID+'" Right="3" /></Claims>'
		from FOLDER F inner join USER_SETTINGS U on U.HOME_FOLDER_ID = F.FOLDER_ID inner join LICENCE_SPACE L on F.LICENCE_ID = L.LICENCE_ID
		where L.DEFAULT_PROFILE = N'Checkpoint' and L.TEMPLATE_LICENCE_ID <> L.LICENCE_ID; 
	}

	--select * from LICENCE_SPACE
	--select DISTINCT THEME from LICENCE_SPACE
	--select DISTINCT DEFAULT_PROFILE from LICENCE_SPACE
	--select * from LICENCE_SPACE where DEFAULT_PROFILE = N'Checkpoint' and TEMPLATE_LICENCE_ID <> LICENCE_ID