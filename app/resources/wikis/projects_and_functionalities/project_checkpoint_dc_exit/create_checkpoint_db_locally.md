
# Creating the DB in a local environment

To create the Checkpoint database in your local environment, follow the steps below:

1. Install and start docker to be able to use the docker-compose.
2. Clone the `cp_web-app-dbchange` repository and check out the `scripts-baseline` branch.

   ```shell
   $ git clone https://github.com/tr/cp_web-app-dbchange/
   $ cd cp_web-app-dbchange
   $ git fetch origin scripts-baseline
   $ git switch scripts-baseline
   ```
3. Copy the scripts from ./sqlscripts/* into ./shell/sqlscripts/migrations/.

   ```shell
   $ mkdir -p ./shell/sqlscripts/migrations
   $ cp ./sqlscripts/* ./shell/sqlscripts/migrations/.
   ```
4. Run the run-local-setup.sh script in Git Bash command line:

   ```shell
   $ cd shell
   $ ./run-local-setup.sh --db-prepare
   ```
   **Note:** Below you can find other options to use with the script. Read the script file to understand what each option do.
      - `./run-local-setup.sh --db-prepare`
      - `./run-local-setup.sh --db-update`
      - `./run-local-setup.sh --db-delete`
      - `./run-local-setup.sh --db-reset`
5. Wait until the Docker finishes and the DB is ready. 
6. Connect to the DB using localhost in port 5433