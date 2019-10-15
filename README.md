# AlayaCare Automation Skill Test

<details>
<summary>🖱️ Click to show the oringinal text</summary>

Welcome to AlayaCare's automation skill test.
You have shown interest in CI/CD, automation, scripts and cloud technologies ; now it's time to put
your skills to work.
Given a highly simplified setup resembling ours, you will learn to get familiar with Jenkins, Docker
and a typical deployment flow.
Different aspects make up for the test:

- research
- documentation
- setup
- scripting

Each task adds a building block to the setup, you will want to work on them sequentially.
If you face a blocker, you should be able to move on to the next task, although you might not be
able to test your work.
Feel free to work around the instructions in that case, and document what you did.
For example if you cannot load the `database.sql` script through Jenkins, you can always do it
manually and move on.

**N.B.** remember to document everything you do !!

**Bonus:** throughout the test, please feel free to increment all the scripts with better logging,
error handling and other improvements. Each task contains a goal and some guidelines, you're
welcome to adapt them and develop them in your own way.

----------

## Assignment

### How to submit your work ?

**/!\ You need to fork this repository.**

1. Fork this repository
2. Clone your fork locally
3. Work
4. Once you're done, submit a pull request to the remote repository
5. Review your changes and validate

### Delivery

We are expecting the following files:

- `README.md`, all the documentation you wrote
- `Dockerfile`, for the custom Jenkins image
- `init_database.groovy`, Groovy script to import the trunk file
- `init_database.xml`, config file for the eponymous Jenkins job
- `run_migrations.groovy`, Groovy script to run DB migrations
- `run_migrations.xml`, config file for the eponymous Jenkins job
- `deploy.py`, Python script with all the logic
- `migration_summary`, from task 10
- `requirements.txt` if needed
- `docker-compose.yml` in case you have changed the original one

### Overview

- *a database,* contains fake tenant data
- *a Jenkins server,* with some pipelines to run dummy DB migrations
- *a Python CLI tool,* with logic to verify and validate tenant migrations

----------

## Tasks

### I. Up & Running

Let's get our Jenkins server and database up and running on your local.
Everything must be dockerized.

#### task 1

Set up Jenkins & MySQL on your local ; you must use docker containers.
A `docker-compose.yml` has been provided, feel free to use it / increment it.

**N.B.** docker compose already creates a network with all services involved.
That allows us to access mysql under `db` from the `jenkins` container.
If you're running logic outside the docker-compose setup that requires communicating
with one of its containers, you either need to retrieve the container's IP address
or expose its port.

#### task 2

Install `mysql-client` and `python3` on your Jenkins server.
Let's be classy about it : create a new docker image based on `jenkins/jenkins:lts` and install
the packages in your derived image's `Dockerfile`.

#### task 3

Find a clean way to get files to your Jenkins server.
Ideas: `docker cp`, shared mount point, git clone etc.
You will start by sending over `database.sql`, but later on you will be uploading groovy scripts
& python files.

#### task 4

Find a way to export Jenkins job configs.
For each job you set up, a config file is generated on the Jenkins server.
To evaluate your jobs, we need the groovy script + the job config associated.
Out of all the files and directories created by Jenkins for a single job, we are interested in
the one containing the parameter information etc.


### II. Groovy Baby!

Time get our hands dirty with some groovy!
Each groovy script you write is a file, and has a corresponding Jenkins job associated that calls
the file.

#### task 5

Create `init_database.groovy` which will load all of `database.sql` into our DB.
The script must be in Groovy, and will be set up in a Jenkins job called `init_database` (no parameters).
Essentially, the script runs a `mysql` command to source the trunk file, and Groovy is simply
the glue between that command and Jenkins.

**Action:** Run the job to populate the database with initial data.

#### task 6

Create `run_migrations.groovy` which will run a given migration sequentially for specified tenants.
A migration is simply an entry in the table `migrations` with a given name and tenant ID.
The job `run_migrations` takes 2 parameters:

- `TENANT_NAMES`, a CSV of tenant names (e.g. `tenant1` or `tenant1,tenant2`) ; it also accepts
`ALL`, the equivalent of passing all tenant names
- `MIGRATION_NAME`, a blank field accepting a string like `migr6`

The job will run a dummy DB migration for the given tenants, one at a time, by doing something like:

```sql
INSERT INTO migrations(tenant_id, name) VALUES (1, 'migr6');
```

**N.B.** This task can either be done in Groovy (over a `mysql` shell command) or in Python.
If you choose to move the migration logic to Python, you still need a Groovy script to call
the Python logic from a Jenkins job.

**Action:** Run the job a couple times to add more content to the database - worry not, the next
tasks will help us validate each tenant's migration state.


#### task 7

Increment `run_migration` by adding a drop-down column `RUN_TYPE` with 2 choices: `sequential` and
`parallel`.
Instead of running all migrations sequentially, we now wish to run them in parallel - Jenkins
easily supports this.
However, Jenkins' builtin `parallel` tool doesn't allow you to limit the number of sub-processes.
You will therefor need to change `run_migrations.groovy` to run the DB migrations for 5 tenants
at a time when chosing the `parallel` option.


### III. Python

You have full freedom in your choice of Python tools, packages, logging etc.
Ideally, please use `python3`.
All your logic must be accessible in CLI, and should fit in a single file.

#### task 8

Write Python logic that checks DB migrations for all tenants. e.g.

```bash
$ python deploy.py check-migration 'migr2'
tenant1: OK
tenant2: OK
tenant3: missing
...
```

#### task 9

Write Python logic that counts DB migrations for all tenants. e.g.

```bash
$ python deploy.py count-migrations
tenant1: 5
tenant2: 5
tenant3: 4
...
```

#### task 10

Thanks to the Python logic you just wrote, create a little report showing the current state of
tenant migrations.
Point out the tenant with mismatching numbers.
The report can be a markdown document with console outputs of your scripts and / or screenshots.
Jot down your findings, explaining why some tenants have migrations that others don't.

----------

## Resources

- [jenkins docker image](https://github.com/jenkinsci/docker/blob/master/README.md)
- [mysql docker image](https://hub.docker.com/_/mysql)
- [docker compose documentation](https://docs.docker.com/compose/)

</details>


## Tasks and Steps

#### ⚫Before start
Fork the project and clone it to the local disk.
Install docker and docker-compose on your computer. In a terminal, use <code>docker --version</code>
and  <code>docker-compose --version</code>  to make sure **docker** are installed properly. 
Run something like<code>systemctl status docker</code> to make sure docker is active, otherwise run <code>systemctl start docker</code>

On some  platforms, you may have to always use **root** to run the commands mentioned below.

#### ⚫task 1 and ⚫task 2
As the project has been cloned to the local path, enter the project's directory.

We need to build our own jenkins image. Create a new file 'Dockerfile' with the content below:


```bash
FROM jenkins/jenkins:lts
USER root
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install  mysql-client python3 python3-pip -y
RUN apt-get install default-libmysqlclient-dev -y
RUN pip3 install mysqlclient
```
Run <code>docker build -t alaya/test .</code> Don't forget to copy the last dot(**.**).


Edit **docker-compose.yml** file and make it like this:
```
version: '2'
services:
    myjenkins:
        image: alaya/test:latest 
        ports:
            - '127.0.0.1:8080:8080'
    db:
        image: mysql:5.7
        environment:
            MYSQL_ROOT_PASSWORD: 'mHsJ33lF+1FZ'
        ports:
            - '127.0.0.1:3306:3306'
```

Run <code>docker-compose up -d</code> to start the **myjenkins** and **mysql** images.
Run <code>docker ps</code> to check the image you just build and get the name of the new image, such as **devautomationtest_myjenkins_1**  (Names can be different!)

Run something like <code> docker exec -it devautomationtest_myjenkins_1 bash</code> to enter the container's shell(make sure the image name is correct).

In the container's shell, run <code>cat /var/jenkins_home/secrets/initialAdminPassword</code> to get the admin
password for Jenkins. It should be a string.



Use your browser, such as Firefox, to visit http://127.0.0.1:8080 and input the password you just get. Then, click the 
**'Install suggested plugins'**. After the plugins are installed
, you can set the user name and password for your Jenkins. Next, you can set the 
Jenkins URL to http://127.0.0.1:8080/. Click 'Save and Finish' button, you will be redirected to
the dashboard of Jenkins.



#### ⚫task 3

Run <code>docker ps</code> to get the container id, such as *5bec9dd13591*

Run <code>docker cp  ̶/̶h̶o̶m̶e̶/̶h̶a̶n̶k/dev-automation-test/database.sql 5bec9dd13591:/home/</code>, 
make sure you use your own correct **path** and **container id** for this command.


#### ⚫task 4

In any shell, run code <code>wget http://127.0.0.1:8080/jnlpJars/jenkins-cli.jar</code> to download the CLI tool.

**When you have finished the task 5 and task 7**, go back to task 4 and do these steps to get the xml files for these jobs.

Run code <code>java -jar jenkins-cli.jar -s http://127.0.0.1:8080 -auth YOUR_USER:YOUR_PASSWORD get-job run_migrations > run_migrations.xml</code>.

Run code <code>java -jar jenkins-cli.jar -s http://127.0.0.1:8080 -auth YOUR_USER:YOUR_PASSWORD get-job init_database >init_database.xml</code>.

Please use **your own** username and password.



### II. Groovy Baby!
#### ⚫task 5

Document about pipeline: https://jenkins.io/doc/book/pipeline/syntax/
Create **init_database.groovy** which will load all of **database.sql** into the database, with the content below:
```
pipeline {
    agent any
    stages {
        stage('Database init') {
            steps {
                sh 'mysql -h db -u root -p$MYSQL_ROOT_PASSWORD  < /home/database.sql'
            }
    }
    }
}

```
Next, go to Jenkins' dashboard. Create a **Pipeline** job, and name it as  **init_database**. 

Use the init_database.groovy's content  to set the Pipeline script.


Run the job.



#### ⚫task 6 and ⚫task 7

Login jenkins, create a pipeline job  which is similar to the previous one.Name it **run_migrations**.
But for this job you need
to check ☑️**This project is parameterized** because it has two parameters. 
Add two string parameters, one is **TENANT_NAMES**, the other one is **MIGRATION_NAME**. Please choose ☑️**Trim the string** for these two parameters. 

For tast 7, you need to add a **Choice Parameter** as well. Name it **RUN_TYPE**. The two choices are **sequential** and **parallel**.

It should be like this picture below when you run / build this job.
![Pix](data:image/png;base64,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)

For the Pipeline script, please use the **run_migrations.groovy** which is actually a glue code to run the python script **run_migrations.py**

Run <code>docker ps</code> to get the **myjenkins** container id, such as *5bec9dd13591*

Run <code>docker cp /home/hank/dev-automation-test/run_migrations.py 5bec9dd13591:/home/</code> to copy this Python script (run_migrations.py) into the docker image.

Run this job a few times.
### III. Python

#### ⚫task 8 and ⚫task 9

Create deploy.py.

Run <code>docker ps</code> to get the **myjenkins** container id, such as *5bec9dd13591*

Run <code>docker cp /home/hank/dev-automation-test/deploy.py 5bec9dd13591:/home/</code> to copy this Python script(deploy.py) into the docker image.


Run <code>docker exec -it devautomationtest_myjenkins_1 bash </code> to **enter the container's shell**.


Then, **in the container's shell**, you can run something like <code>python3 deploy.py check-migration 'migr2'</code> to check DB migrations for all tenants.

Or run <code>python3 deploy.py count-migrations</code> to count the migrations for all tenants.
#### ⚫task 10

Create migration_summary.md
