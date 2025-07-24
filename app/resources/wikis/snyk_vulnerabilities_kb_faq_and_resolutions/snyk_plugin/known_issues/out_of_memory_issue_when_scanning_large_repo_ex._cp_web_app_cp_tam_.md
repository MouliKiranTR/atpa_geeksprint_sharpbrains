**Suggestions on resolving the out-of-memory issues (Provided by SNYK SUPPORT)**

Ways of getting around the OOM limitation for Snyk Code in the IDE for the large java monorepo:

**- Opening a subdirectory of the monorepo as the project instead of the root directory.** This will reduce the scope of the scanned files to just data flows within that subdirectory. Depending on structure of the project and the level of coupling/cohesion between the subdirectories, there may be an impact to quality of findings.
**- Disabling Code Quality Checks.** This will reduce the ruleset and output set of discovered issues.
**- Disabling Medium and Low severity findings.** This will reduce the noise and output set of discovered issues.

