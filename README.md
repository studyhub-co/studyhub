# StudyHub

## Installation (to run locally) 

### Backend

Requires [Python 3.8.*](https://www.python.org/downloads/), git ([Windows](https://git-scm.com/download/win), [macOS](https://git-scm.com/download/mac)).
If you are using Windows and WSL, python requires inside WSL instance (see below) and Win OS (Requires by node-gyp in vscode-textmate application) both.
Install Visual C++ Build Environment: [Visual Studio Build Tools](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=BuildTools) (using "Visual C++ build tools" workload).    

#### Interpreter environment

Instead of the console, you can use your favorite IDE to cover the next steps. All commands run from the project's root directory.

**Windows**

Python py-mini-racer application do not support Windows. So recommended running in a [WSL](https://docs.microsoft.com/en-us/windows/wsl/) (Windows Subsystem for Linux). Steps to install [here](https://docs.microsoft.com/en-us/windows/wsl/install-win10). Recommended [Ubuntu 18.04 LTS](https://aka.ms/wsl-ubuntu-1804) image to [install](https://docs.microsoft.com/en-us/windows/wsl/install-manual). Once you have distribution installed don't forget to run it from Start menu for the first time to complete your newly installed Linux distribution is to create an account, including a User Name and Password.
Also, add "c:\Program Files\Git\usr\bin\" to PATH environment variable (needs for some npm packages).  

**macOS**

Recommended to run in a [virtual environment](https://docs.python.org/3.8/library/venv.html)

```
python -m venv venv
```

#### Get source code

```commandline
git clone https://github.com/studyhub-co/studyhub.git
cd studyhub
```

#### Install requirements

**Windows**

```commandline
wsl sudo apt -y update
wsl sudo apt -y upgrade
wsl sudo apt -y install python3-pip python3.8 python3.8-dev libmysqlclient-dev
wsl python3.8 -m pip install --upgrade pip
wsl python3.8 -m pip install -r requirements.dev.txt
```

**macOS**

```commandline
pip install -r requirements.dev.txt
```

#### Database

##### Requires [PostgreSQL](https://www.postgresql.org/) (>= 10.15)

1. Install PostgreSQL:

**Windows**

- Download installer from: https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
- Install (You can install PgAdmin to manage database with this installer).
- Add "c:\Program Files\PostgreSQL\{version}\bin\" to PATH environment variable ({version} = your version of PostrgreSQL installed)

**macOS**

Install postgresql and pgadmin4 (optional). 

```
brew install postgresql
brew install --cask pgadmin4
```

2. Create a database (you can use PgAdmin instead command line below):

```
createuser -U postgres studyhub
createdb -U postgres -O studyhub studyhub
```

3. Connect to `studyhub` database with `postgres` user and create an EXTENSION:

```
psql -U postgres studyhub 
studyhub# CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
studyhub# \q
```

4. Activate your virtual environment variables

**Windows**

```
copy scripts\set_env_vars.cmd scripts\set_env_vars.local.cmd
notepad scripts\set_env_vars.local.cmd
```

**macOS**

TODO

5. create database schema

**Windows**

```commandline
scripts\wsl_manage_py.cmd migrate
```

**macOS**

```commandline
./manage.py migrate
```

6. Import initial problems types source code data.

TODO 

##### Requires [Mysql](https://dev.mysql.com/downloads/installer/) (>= 5.7)

Mysql problem type requires Mysql database instance. 

1) Download and choose Developer type due installation process.
Select "Use Legacy Authentication Method". 
2) Create Mysql problem type database:

```commandline
mysqlsh
MySQL JS> \c root@localhost
MySQL JS> \sql
MySQL SQL> CREATE DATABASE studyhub;
MySQL SQL> CREATE USER 'studyhub'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
MySQL SQL> GRANT ALL PRIVILEGES ON studyhub.* TO 'studyhub'@'localhost';
MySQL SQL> \q
```

3) Edit Mysql settings environment variables 

**Windows**

```commandline
notepad scripts\set_env_vars.local.cmd
```

**macOS**

...

***

### Front-end

1. Install [Node.js](https://nodejs.org/en/download/) + npm v6 (included)

2. Install yarn.

```commandline
npm install -g yarn
````

3. Unpack VSCode editor extensions:

**Windows**

```commandline
"C:\Program Files\Git\usr\bin\unzip" courses\static\courses\js\codesandbox-apps\vscode-extensions\out\extensions.zip -d courses\static\courses\js\codesandbox-apps\vscode-extensions\out\
```

**macOS**

```commandline
unzip courses/static/courses/js/codesandbox-apps/vscode-extensions/out/extensions.zip  -d courses/static/courses/js/codesandbox-apps/vscode-extensions/out/
```

* install lerna

```commandline
npm install -g lerna
```

* get npm packages in every yarn workspace, remove duplicated react typescript types.

```commandline
lerna bootstrap --npm-client=yarn && yarn clear_types
```

* build all workspace modules

```commandline
lerna run build
lerna run dist
```

* start compile bundles and watch for source code changes (SPA)

```commandline
yarn watch
```

* start compile bundles and watch for source code changes (JS application that run sandboxes)
Run the new terminal.

```commandline
cd ./courses/sandbox-eval-project/
yarn install
yarn watch
```

### Run development server

* Create an admin account 

**Windows**

```commandline
scripts\wsl_manage_py.cmd createsuperuser
```

**macOS**

```commandline
/manage.py createsuperuser
```

* Run:

**Windows**

```commandline
scripts\wsl_manage_py.cmd runserver
```

**macOS**

```commandline
./manage.py runserver
```

* You should find the site running on http://localhost:8000
* Login and go to http://localhost:8000/studio/ to create a unit, module, lesson, and materials.
* Navigate to http://localhost:8000/ to see what you created!

## Structure
Django apps:
* `settings` app contains the project settings. 
* `curricula` is the main app that produces the page at /curriculum/. The files apis.py and urls_api.py utilize the Django REST Framework to make an API for the models

### Models
The model hierarchy is:
* Course
* Unit 
* Module
* Lesson
* Material

## Deployment (Amazon web services example)

You can use any hosting services that support python: VPS, orchestration service, etc. But we have some built-in applications that rely on AWS.  
So, for now, Amazon EBS + RDS + S3 is the best choice to host the project. 

* install [AWS CLI](http://docs.aws.amazon.com/cli/latest/userguide/installing.html):
```
brew install awscli
```
* install [AWS EB CLI](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install.html):
```
brew install awsebcli
```
* run `aws configure`

* Create Amazon EBS environments (using [web console](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features.managing.html) or [AWS CLI](https://docs.aws.amazon.com/cli/latest/reference/elasticbeanstalk/create-environment.html)), e.g.:  
"pib-dev-v2" for dev branch deploying  
"pib-prod-v2" for production branch deploying (you can clone it from 'pib-dev-v2')

* Create two Amazon RDS databases instances with engines: 
1) PostgreSQL. Connect to PostgreSQL DBMS instance and create two roles/databases, e.g.:  
 pib_dev_db with pib_dev_user owner  
 pib_prod_db with pib_prod_user owner
2) MySQL Community

* Create four Amazon S3 public buckets:

'assets' for storing STATIC files (production EBS instance) 
'media' for storing MEDIA files (production EBS instance)

'assets-dev' for storing STATIC files (development EBS instance)  
'media-dev' for storing MEDIA files (development EBS instance)

* Add [Environment variables](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/environments-cfg-softwaresettings.html?icmpid=docs_elasticbeanstalk_console):

Add and setup common (for production and development version) environment variables in Configuration EBS instance section from
```commandline
./scripts/set_env_vars.cmd
```

Add production related environment variables:
```commandline
AWS_ACCESS_KEY
AWS_SECRET_ACCESS_KEY
AWS_HEALTH_LOCAL_ALLOWED_HOST
# MEDIA files bucket:
AWS_S3_BUCKET_NAME
AWS_S3_PUBLIC_URL
# STATIC files bucket:
AWS_S3_BUCKET_NAME_STATIC
AWS_S3_PUBLIC_URL_STATIC
RAVEN_DSN
```

* run `eb init` (you'll need the access id/key)
* on git `develop` branch run `eb use pib-dev-v2`
* on git `master` branch run `eb use pib-prod-v2`

* prepare eval project bundle # TODO replace with dynamic paths 
```commandline
cd ./courses/sandbox-eval-project
yarn build:sandbox
```

* prepare SPA bundle
```
yarn prod
```

* `eb deploy` (it will deploy to the proper environment depending on what branch you are on).

## Development

* We respect the rules set out by pep8 with the exception of a 100 character line limit.
* We use the flake8 python script for linting.
* For frontend code we use eslint for linting. See .eslintrc.json and .prettierrc files for details.

### Development tools

#### embedded 

* [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/)

#### external

* [React Developer Tools](https://chrome.google.com/webstore/detail/react-developer-tools/fmkadmapgofadopljbjfkapdkoienihi?hl=en)
* [Redux DevTools Extension](https://github.com/zalmoxisus/redux-devtools-extension)



