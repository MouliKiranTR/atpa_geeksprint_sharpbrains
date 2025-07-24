To avoid merge conflicts, you should always update the master branch of your repository, to do that, we recommend the next steps:

1. Add the URL of the source repository to you remote list:
   `git remote add upstream <source-repository-url>`

1. Get new changes from that repository:
   `git fetch upstream`

1. Merge the changes with your master branch:
   `git merge upstream/master`

> If you don't like to execute two commands to sync your local repository with upstream you can use the following command:
> `git pull upstream master`

