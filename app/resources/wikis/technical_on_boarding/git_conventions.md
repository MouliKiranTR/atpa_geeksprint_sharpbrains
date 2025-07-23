[[_TOC_]]

---
# Git configurations
Please, update your git user information! Use your real name in git commits. You can do the following to do it globally:
```
$ git config --global user.name "FirstName LastName"

$ git config --global user.email firstName.lastName@thomsonreuters.com
```
Optionally, you can configure your default editor. If not configured, Git uses your system’s default editor.

- For Emacs in Mac:
`$ git config --global core.editor emacs`

- For Notepad++ in Windows:
`$ git config --global core.editor "'C:/Program Files/<notepad++_path>/notepad++.exe' -multiInst -notabbar -nosession -noPlugin"`

---

# Branching Naming Convention
1. Stick to lowercase for the branch name.
2. Use separators: slash (/) to separate ADO Item ID and description, and hyphens (-) to separate words in descriptions.
<!---
3. Start with a category from the following options (the list can be expanded based on needs):
   - **feature**: Add/remove/modify an application feature
   - **bugfix**: Fixing bugs
   - **poc**: Used for experimentation, may no have a related ADO item
   - **hotfix**: temporary fixes to be deployed ASAP
   - **docs**: Documentation branches
-->
3. Use the ADO item ID (`no-ref` if no ADO item was created).
<!---5. Include the Author name?: firstName.lastName - Can the branch name start with the author?-->
4. Add a concise and expressive description using hyphens as a separator. Use present tense and keep it between 5 to 7 words maximum.
5. And mostly be consistent

**Examples:**
- `12345/new-search-button`
- `67890/fix-calendar-ui`
- `no-ref/enable-logs-temporarily`
- `origin/12345/new-doc-link` (Remote branch)


**Avoid:**
1. Using non-descriptive names
2. Using too long name branch descriptions
3. Punctuation or any non alphanumeric character unless specified in the above conventions
5. Continuous hyphens (--) and leading/trailing hyphens


**References:**
- https://medium.com/@abhay.pixolo/naming-conventions-for-git-branches-a-cheatsheet-8549feca2534
- https://tilburgsciencehub.com/building-blocks/collaborate-and-share-your-work/use-github/naming-git-branches/
- https://www.alibabacloud.com/blog/git-branching-naming-convention---best-practices_597423
- https://learn.openwaterfoundation.org/owf-learn-git/workflow/branch-naming/
---

# Commit conventions
 

1. The first line of your commit is treated as the subject and the rest of the text as the body. A blank line between subject and body is critical. Do not forget that blank line. This point might seem unimportant but it makes git history much more pleasant to work with.
2. Use imperative statements in the subject line, e.g. "Fix broken search results link". Think on the subject line as if you would say the following:
. If applied, this commit will your subject line here.
3. Begin the subject line sentence with a capitalized verb, e.g. "Add, Prune, Fix, Introduce, Avoid, etc."
4. Do not end the subject line with a period. Space is precious.
5. Keep the subject line concise to 50 characters or less if possible.
6. Wrap lines in the body at 72 characters or less.
   - Numbered lists and bullet points are great to explain your changes better.
7. In the body of the commit message, explain how things worked before this commit, what has changed, and how things work now with this change. Avoid lazy commit messages and ask yourself these questions:
   - Why is this change necessary?
   - How does it address the issue?
   - What side effects does this change have?
8. Mention related ADO item(s) at the end of the commit message separated by a blank line and prefixed with either "#" for items or "!" for another PR. E.g. #123456.
9. Preferably use git commit without [-m "<msg>" / --message="<msg>"] option, especially on the first commit. The first commit will be taken as a reference on the PR creation.
10. In the House Mormont team(HM), we handle SNYK fixes by implementing a consistent naming convention for our commits and PR titles: <br>
- **PR Title:** HM-168130 [Snyk] [cp_privacydata-service] [SCA] Fix Critical and High Snyk Vulnerabilities  
Format: <Team name>-<US number> Title of the User Story <br>
- **Commit:** HM-168130 updated dep versions  
Format: <Team name>-<US number> commit message <br>
This standardized naming convention allows us to easily associate PRs/commits with their corresponding User Stories and identify the team responsible for the changes.
 

Additionally, you can override the default commit template to remember these rules at the time of commit:
`$ git config --global commit.template ~/.gitmessage.txt`

 

### Commit example
```
Summarize changes in around 50 characters or less

# A blank line after the subject to separate from the body


More detailed explanatory text, if necessary. Wrap it to about 72
characters or so.

 

Explain the problem that this commit is solving. Here in the body

is the place to explain them. Further paragraphs come after blank

lines. Markdown syntax is used.

 

1. Numbered lists are useful.
   - [Number + dot + space] is used for numbered lists.

2. Bullet points are okay, too.

   - Typically a hyphen or asterisk is used for the bullet,

     preceded by a single space, with blank lines in between.

 

Put references to ADO items at the bottom, like this:

Related work items: #12345, #56789
See also PR: !456789
```
---

# Pull Request conventions

1. The PR title should follow the same conventions as a regular commit. See the commit conventions above.
2. Whenever you complete your pull request that contains multiple commits, select to squash all your commits so a single commit for all of your changes is created.

### Pull Request Example
Here is an [example pull request](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_git/cp-web-app/pullrequest/10448) that was created following the conventions properly.

```
Here is the regular body as described in the commit conventions above

Before:
# Include images/gifs or details about the previous user interface or behavior.

After
# Include images/gifs or details about the new user interface or behavior.

PR Compliant with:
-[ ] Unit Tests
# --- Java projects ---
-[ ] Checkstyle
-[ ] Code Coverage
-[ ] Sonar quality gates

Tested in:
-[ ] Chrome
-[ ] Edge
-[ ] Firefox
-[ ] Internet Explorer

Is 508 Accessibility compliant?
-[ ] Yes
-[ ] No
```

# Additional references:
- https://chris.beams.io/posts/git-commit/
- https://github.com/spring-projects/spring-framework/blob/30bce7/CONTRIBUTING.md#format-commit-messages
- https://gist.github.com/lisawolderiksen/a7b99d94c92c6671181611be1641c733
- https://thoughtbot.com/blog/5-useful-tips-for-a-better-commit-message
- http://who-t.blogspot.com/2009/12/on-commit-messages.html