<P  class=MsoNormal><B><U>COMMON RULES</U></B></P>

<UL style="margin-top:0in"  type=disc>
 <LI  class=MsoListParagraph style="margin-left:0in"><B>During the vulnerability investigation, we should
     schedule a call with Tauhid, Kavya, and Ishaan as soon as possible to gain
     a better understanding and determine the next steps.</B></LI>
 <LI  class=MsoListParagraph style="margin-left:0in"><B>If you encounter a blocker, bring it to the team's
     attention as soon as possible so it can be addressed and the next steps
     can be identified.</B></LI>
 <LI  class=MsoListParagraph style="margin-left:0in"><B>Link your PRs to user story by adding GitHub PR
     links to the US for better tracking. </B></LI>


<P  class=MsoListParagraph>[ISSUE] Only few repos are presented in ADO to link.
Need to investigate</P>

<P  class=MsoListParagraph>Add you PR to <A 
href="https://teams.microsoft.com/l/entity/0d820ecd-def2-4297-adad-78056cde7c78/_djb2_msteams_prefix_1006742186?context=%7B%22chatId%22%3A%2219%3A7cbbe52d65294f34924d798bc7532637%40thread.v2%22%2C%22contextType%22%3A%22chat%22%7D&amp;tenantId=62ccb864-6a1a-4b5d-8e1c-397dec1a8258" 
title="https://teams.microsoft.com/l/entity/0d820ecd-def2-4297-adad-78056cde7c78/_djb2_msteams_prefix_1006742186?context=%7B%22chatId%22%3A%2219%3A7cbbe52d65294f34924d798bc7532637%40thread.v2%22%2C%22contextType%22%3A%22chat%22%7D&amp;tenantId=62ccb864-6a1a-4b5d-8e1">PR
Review</A> and make a post in <B>House Mormont Chat</B></P>

<P  class=MsoListParagraph><B><SPAN style="color:red">Important! </SPAN></B>Please
delete your request from <A 
href="https://teams.microsoft.com/l/entity/0d820ecd-def2-4297-adad-78056cde7c78/_djb2_msteams_prefix_1006742186?context=%7B%22chatId%22%3A%2219%3A7cbbe52d65294f34924d798bc7532637%40thread.v2%22%2C%22contextType%22%3A%22chat%22%7D&amp;tenantId=62ccb864-6a1a-4b5d-8e1c-397dec1a8258" 
title="https://teams.microsoft.com/l/entity/0d820ecd-def2-4297-adad-78056cde7c78/_djb2_msteams_prefix_1006742186?context=%7B%22chatId%22%3A%2219%3A7cbbe52d65294f34924d798bc7532637%40thread.v2%22%2C%22contextType%22%3A%22chat%22%7D&amp;tenantId=62ccb864-6a1a-4b5d-8e1">PR
Review</A> when it’s addressed.</P>

</UL>

<UL style="margin-top:0in"  type=disc>
 <LI  class=MsoListParagraph style="margin-left:0in"><B>Everyone should review PR and add comment it. </B></LI>


<P  class=MsoListParagraph>Final review will be done by<SPAN>  </SPAN>Tauhid, Kavya, Ishaan</P>

</UL>
<UL style="margin-top:0in"  type=disc>
 <LI  class=MsoListParagraph style="margin-left:0in"><B>Record KT session with Transcript and use Copilot
     to create HOW TO documentation and post it in Wiki</B></LI>
</UL>

<hr>

<P  class=MsoNormal><B><U>CHECKLIST FOR DEVELOPERS:</U></B></P>

<OL style="margin-top:0in"  start=1  type=1>
 <LI  class=MsoNormal><B>Requirement
     Analysis &amp; Planning</B></LI>


<UL style="margin-top:0in"  type=disc>
 <LI  class=MsoListParagraph>Review the user story
     </LI>
 <LI  class=MsoListParagraph>Make initial investigation
     on vulnerabilities in scope to determine its complexity and, if necessary, break it down into subtasks</LI>
 <LI  class=MsoListParagraph>[CP_WEB_APP only] Find
     how to call functionality in Checkpoint or its Admin Portal (<A 
     href="https://checkpoint.ci.thomsonreuters.com/admin"  rel="noopener noreferrer"  target="_blank" 
     title="https://checkpoint.ci.thomsonreuters.com/admin">https://checkpoint.ci.thomsonreuters.com/admin</A>).
     <BR/>
     → Use a list of Developers and their main areas of expertise to help identify
     the right person to consult for specific tasks <A 
     href="https://trten.sharepoint.com/:x:/r/sites/TRTAKSCheckpointAnswers/Shared%20Documents/General/07%20Team%20Resources/Team%20Expertise%20Roster.xlsx?d=w8d3f36b2e1d54a65bd35bf70d342493c&amp;csf=1&amp;web=1&amp;e=N8fbtm"><SPAN 
     class=MsoSmartlink>Team Expertise Roster.xlsx</SPAN></A>. <SPAN> </SPAN>As a result, <SPAN> </SPAN>you will capture a list of UI
     capabilities to be tested and communicate this with senior developers to
     ensure thorough testing.</LI>


<P  class=MsoListParagraph">→if you can’t find how to
call API in Checkpoint by yourself or help of other Developers, you discuss it with
QAs. <BR/>
<B><SPAN style="color:red">Important! </SPAN></B>Raise it as a Blocker to the
Team if you haven’t received any answer.</P>
</UL>
<P  class=MsoListParagraph style="margin-left:1.0in">&nbsp;</P>

<UL style="margin-top:0in"  type=disc>
 <LI  class=MsoListParagraph>Set up a call with
     your Buddy (Araks, Kavya, Ishaan), Tech Lead or Delivery Manager to discuss
     architecture (if needed) and logic of changes. <BR/>
     It helps you to get a better understanding and next steps as soon as
     possible.<BR/>
     <BR/>
     </LI>
 <LI  class=MsoListParagraph>Make high level
     estimation on how long it takes to remediate vulnerabilities<BR/>
     <B><SPAN style="color:red">Important!</SPAN></B><SPAN style="color:red"> </SPAN>Let
     know you Delivery Manager/Scrum Master if it’s better to split user story
     and provide your suggestions. It helps to enhance your focus and speed up
     the remediation process</LI>
</UL>

</OL>


<OL style="margin-top:0in"  start=2  type=1>
 <LI  class=MsoNormal><B>Set
     up and Run repo locally</B></LI>
 <UL style="margin-top:0in"  type=disc>
  <LI  class=MsoNormal>Use documentation on GitHub
      (Readme) or Wiki.</LI>
  <LI  class=MsoNormal>Reach out to <A 
      href="https://teams.microsoft.com/l/team/19%3A0896bdeb125e4f778e5cdfcf296bb75c%40thread.skype/conversations?groupId=3ca8ef20-54e8-45d7-b797-236a56294505&amp;tenantId=62ccb864-6a1a-4b5d-8e1c-397dec1a8258">DevOps
      team</A><SPAN>  </SPAN>if no documentation is available
      on how to set up or run repo</LI>



<P  class=MsoNormal style="margin-left:.0in"><B><SPAN style="color:red">Important!
</SPAN></B>Document your findings in Readme on GitHub for this repo</P>

 </UL>
</OL>

<OL style="margin-top:0in"  start=3  type=1>
 <LI  class=MsoNormal><B>Development</B></LI>
 <UL style="margin-top:0in"  type=disc>
  <LI  class=MsoNormal>Write clean, readable,
      and optimized code following coding standards - <A 
      href="https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/472/Best-Practices-and-Coding-Standards">Best
      Practices and Coding Standards - Overview</A></LI>

<P  class=MsoNormal style="margin-left:.0in"><B><SPAN style="color:red">Important!
</SPAN></B>When working with upgrading libraries please follow recommended versions on Wiki: <A 
      href="https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/1045/Libraries-versions-used-for-Snyk-vulnerabilities-remediation">Libraries versions used for Snyk vulnerabilities remediation - Overview</A>

<u>Please make sure you are using the latest versions of libraries when addressing vulnerabilities.</u>

</P>
  <LI  class=MsoNormal>Make changes to repo’s
      lambda accordingly (if applicable)</LI>
  <LI  class=MsoNormal>Ignore false-positive
      cases + Document it on Wiki</LI>
  <LI  class=MsoNormal>When updating service dependencies, avoid overriding a dependency version from the parent pom unless the parent version causes issues or doesn't work for the child pom. Avoid duplicating dependency from parent pom to child pom.</LI>
 </UL>


<P  class=MsoNormal style="margin-left:.in"><B><SPAN style="color:red">Important!
</SPAN></B>Please approve/decline ignored by team members cases on <A 
href="https://ps360.int.thomsonreuters.com/snyk/findings-ignore-review/">PS360
Portal</A><B> </B>if you are Snyk Custodian (Kavya, Ishaan, Araks, Tauhid) <SPAN> </SPAN></P>
</OL>
<OL style="margin-top:0in"  start=4  type=1>
 <LI  class=MsoNormal><B>Unit
     Testing</B></LI>
 <UL style="margin-top:0in"  type=disc>
  <LI  class=MsoNormal>Cover critical parts of
      the code with automated tests.</LI>
 </UL>
 <LI  class=MsoNormal><B>SonarQube
     Analysis</B></LI>
 <UL style="margin-top:0in"  type=disc>
  <LI  class=MsoNormal>Perform static code
      analysis to identify bugs, vulnerabilities, and code smells.</LI>
  <LI  class=MsoNormal>Remove deprecated methods
      and add actual one</LI>
 </UL>
</OL>

<P  class=MsoNormal style="margin-left:.75in"><B><SPAN style="color:red">Important!</SPAN></B><SPAN style="color:red"> </SPAN>Please use SonarLint instruction to configure your
IDEA</P>

<OL style="margin-top:0in"  start=6  type=1>
 <LI  class=MsoNormal><B>Self-Testing</B></LI>
 <UL style="margin-top:0in"  type=disc>
  <LI  class=MsoNormal>Perform basic functional
      checks before handing over to QA.</LI>
  <LI  class=MsoNormal>Perform lambda testing (if
      applicable)</LI>
  <LI  class=MsoNormal>Check logs (if there are
      any new errors) </LI>
 </UL>
</OL>

<P  class=MsoNormal style="margin-left:1.0in">&nbsp;</P>

<OL style="margin-top:0in"  start=7  type=1>
 <LI  class=MsoNormal><B>Documentation</B>
     </LI>
 <UL style="margin-top:0in"  type=disc>
  <LI  class=MsoNormal>Create/update
      documentation (for example, Readme in GitHub on How to set up repo, etc), comments in the code, and
      API references (if applicable).</LI>
  <LI  class=MsoNormal>Create documentation for
      QA where you have to add next information:<BR/>
      → List of UI capabilities to be tested + specify changed files and it’s classes
      in brackets;
      <BR/>
      → Outline areas that may be affected + specify changed files and it’s classes
      in brackets. 
      <BR/>
      → Specify if there are any changes in the base classes (e.g. using of StringEscapeUtils methods). 
      <BR/><BR/>
      All this will help identify what has been modified and where to focus their testing and identify additional areas to check
      <BR/></LI>


<B><SPAN style="color:red">Important! </SPAN></B>Add this information to User story in Discussion section.

 </UL>
</OL>

<P  class=MsoNormal style="margin-left:.5in">&nbsp;</P>

<OL style="margin-top:0in"  start=8  type=1>
 <LI  class=MsoNormal><B>PR
     preparation and Code Review<BR/>
     <SPAN style="color:red">Important! </SPAN></B>On the <B>25th-26th of each
     month</B>, we have a <B>code freeze</B>. Do not merge code unless you are
     sure that its testing will be completed before the freeze.<BR/>
     <BR/>
     </LI>
 <UL style="margin-top:0in"  type=disc>
  <LI  class=MsoNormal>Prepare PR<SPAN>  </SPAN>using instruction: <A 
      href="https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/473/PR-Review-Checklist-Java-Applications">PR
      Review Checklist - Java Applications - Overview</A> </LI>
 </UL>
</OL>

<P  class=MsoNormal style="margin-left:1.0in"><B><SPAN style="color:red">Important!</SPAN></B><SPAN style="color:red"> </SPAN>Add 3 reviewers to PR. 2 of them should be newcomers
and 1 final approve should be done by Ishaan, Kavya, Araks or Tauhid.</P>

<OL style="margin-top:0in"  start=8  type=1>
 <UL style="margin-top:0in"  type=disc>
  <LI  class=MsoNormal>Link your GitHub PR to user
      story for better tracking.</LI>
 </UL>
</OL>

<P  class=MsoNormal style="margin-left:1.0in"><U>[issue] Only few repos are
presented in ADO to link. Need to investigate</U></P>

<OL style="margin-top:0in"  start=8  type=1>
 <UL style="margin-top:0in"  type=disc>
  <LI  class=MsoNormal>Submit code for peer
      review and address feedback.</LI>
  <LI  class=MsoNormal>Inform your team members that
      you need PR review: </LI>
 </UL>
</OL>

<P  class=MsoNormal style="margin-left:1.0in">→ Make a post in House Mormont
Chat and tag reviewers using <B>@</B></P>

<P  class=MsoNormal style="margin-left:1.0in">→ Add information on your PR to <A 
href="https://teams.microsoft.com/l/entity/0d820ecd-def2-4297-adad-78056cde7c78/_djb2_msteams_prefix_1006742186?context=%7B%22chatId%22%3A%2219%3A7cbbe52d65294f34924d798bc7532637%40thread.v2%22%2C%22contextType%22%3A%22chat%22%7D&amp;tenantId=62ccb864-6a1a-4b5d-8e1c-397dec1a8258" 
title="https://teams.microsoft.com/l/entity/0d820ecd-def2-4297-adad-78056cde7c78/_djb2_msteams_prefix_1006742186?context=%7B%22chatId%22%3A%2219%3A7cbbe52d65294f34924d798bc7532637%40thread.v2%22%2C%22contextType%22%3A%22chat%22%7D&amp;tenantId=62ccb864-6a1a-4b5d-8e1">PR
Review</A> tab</P>

<P  class=MsoNormal style="margin-left:.5in">&nbsp;</P>

<OL style="margin-top:0in"  start=9  type=1>
 <LI  class=MsoNormal><B>Build
     &amp; Deployment</B></LI>
 <UL style="margin-top:0in"  type=disc>
  <LI  class=MsoNormal>Ensure successful build
      creation and deployment.</LI>
 </UL>
</OL>

<P  class=MsoNormal style="margin-left:1.0in"><B><SPAN style="color:red">Important!</SPAN></B><SPAN style="color:red"> </SPAN>Reach out to <A 
href="https://teams.microsoft.com/l/team/19%3A0896bdeb125e4f778e5cdfcf296bb75c%40thread.skype/conversations?groupId=3ca8ef20-54e8-45d7-b797-236a56294505&amp;tenantId=62ccb864-6a1a-4b5d-8e1c-397dec1a8258">DevOps
team</A> if you need assistance with pipeline configuration</P>

<OL style="margin-top:0in"  start=10  type=1>
 <LI  class=MsoNormal><B>Other</B></LI>
 <UL style="margin-top:0in"  type=disc>
  <LI  class=MsoNormal><B>Bug Fixing</B> –
      Address defects reported by QA and analyze root causes.</LI>
  <LI  class=MsoNormal><B>Retrospective</B> –
      Reflect on completed work and identify process improvements.</LI>
 </UL>
</OL>

<P  class=MsoNormal><B>&nbsp;</B></P>





<hr>
<P  class=MsoNormal><B><U>FOR QA ENGINEERS:</U></B></P>

<OL style="margin-top:0in"  start=1  type=1>
 <LI  class=MsoNormal><B>Requirement
     Analysis</B></LI>
 <UL style="margin-top:0in"  type=disc>
  <LI  class=MsoNormal>Review user story
      acceptance criteria, documentation on how to test functionality and define
      test cases.</LI>
 </UL>
 <LI  class=MsoNormal><B>Test
     Data Preparation</B></LI>
 <UL style="margin-top:0in"  type=disc>
  <LI  class=MsoNormal>Set up necessary test
      accounts and scenarios (if applicable).</LI>
 </UL>
 <LI  class=MsoNormal><B>Check
     if all vulnerabilities and remediated in</B> <A  href="https://app.snyk.io/">https://app.snyk.io/</A></LI>
 <LI  class=MsoNormal><B>Run
     Automate Regression Testing in CI</B></LI>
 <UL style="margin-top:0in"  type=disc>
  <LI  class=MsoNormal>Check regression report to
      ensure that changes do not break existing functionality.</LI>
  <LI  class=MsoNormal>Create and maintain
      automated test scripts for new functionality (if applicable).</LI>
  <LI  class=MsoNormal>Update test cases (if
      applicable)</LI>
 </UL>
 <LI  class=MsoNormal><B>Manual
     functional Testing</B></LI>
 <UL style="margin-top:0in"  type=disc>
  <LI  class=MsoNormal>Make manual verification
      that functionality meets requirements</LI>
  <LI  class=MsoNormal>Check all login
      scenarios using <A href="(https://trten.sharepoint.com.mcas.ms/:w:/r/sites/TRTAKSCheckpointAnswers/_layouts/15/doc2.aspx?sourcedoc=%7B46C007C1-0361-4C01-B132-A1B3990722D2%7D&file=Login%20Scenarios.docx&action=default&mobileredirect=true&cid=546731d9-c694-457c-b7cf-a7184ef48fa3&wdOrigin=TEAMS-WEB.p2p_ns.rwc&wdExp=TEAMS-TREATMENT&wdhostclicktime=1742464910555&web=1)">Login Scenarios.docx </A></LI>
  <LI  class=MsoNormal>Check CIAM Force User
      Migration functionality</LI>
  <LI  class=MsoNormal>Perform lambda testing (if
      applicable)</LI>
  <LI  class=MsoNormal>Check logs (if there are
      any new errors) </LI>
 </UL>
 <LI  class=MsoNormal><B>Cross-Browser
     &amp; Cross-Platform Testing</B></LI>
 <UL style="margin-top:0in"  type=disc>
  <LI  class=MsoNormal>Test across different
      devices and browsers.</LI>
 </UL>
 <LI  class=MsoNormal><B>API
     Testing (if applicable)</B></LI>
 <UL style="margin-top:0in"  type=disc>
  <LI  class=MsoNormal>Validate server
      responses, errors, and performance.</LI>
 </UL>
 
<LI  class=MsoNormal><B>Add
     Test report to the User Story </B></LI>
 <UL style="margin-top:0in"  type=disc>
  <LI  class=MsoNormal>Inform your team members
      by adding comment that everything working correctly to the user story</LI>
   <LI  class=MsoNormal>
    Move User story to <B>Resolved</B> state
   </LI> 
</UL>


<P  class=MsoNormal style="margin-left:0.15in"><B><SPAN style="color:red">Important!</SPAN></B><SPAN style="color:red"> </SPAN> 
Add tag to the user story that it is candidate for nearest Release (for example: 25.04, 25.05…)
</P>
</OL>
<OL style="margin-top:0in"  start=9  type=1>
 <LI  class=MsoNormal><B>Other</B></LI>
 <UL style="margin-top:0in"  type=disc>
  <LI  class=MsoNormal><B>Bug Reporting</B> –
      Document found defects with clear reproduction steps.</LI>
  <LI  class=MsoNormal><B>Bug Verification</B> –
      Re-test fixed issues to ensure proper resolution.</LI>
  <LI  class=MsoNormal><B>Retrospective
      Participation</B> – Discuss issues and suggest process improvements.</LI>
 <LI  class=MsoNormal><B>QA Wiki in ADO</B> – <A  href="https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_wiki/wikis/Checkpoint.wiki/1054/Checkpoint-QA">[Checkpoint QA - Overview]</A></LI>
     
 </UL>
</OL>