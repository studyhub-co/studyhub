# StudyHub

## Installation (to run locally) 

### Backend

Requires [Python 3.8.*](https://www.python.org/downloads/), git ([Windows](https://git-scm.com/download/win), [macOS](https://git-scm.com/download/mac)). 

#### Interpreter environment

**macOS**

Recommended to run in a [virtual environment](https://docs.python.org/3.8/library/venv.html)

```
python -m venv venv
```

**Windows**

Python py-mini-racer application do not support Windows. So recommended to run in a [WSL](https://docs.microsoft.com/en-us/windows/wsl/) (Windows Subsystem for Linux). Recommended [Ubuntu 18.04 LTS](https://aka.ms/wsl-ubuntu-1804) image to [install](https://docs.microsoft.com/en-us/windows/wsl/install-manual).

#### Install requirements

Instead of the console you can use your favorite IDE to cover the next steps.  

```commandline
git clone https://github.com/studyhub-co/studyhub.git
cd studyhub
```

**Windows**

**macOS**

```commandline
pip install -r requirements.txt
```

### Database

Requires [PostgreSQL](https://www.postgresql.org/) (>= 10.5)

* install PostgreSQL:

**Windows**

Download installer from: https://www.enterprisedb.com/downloads/postgres-postgresql-downloads

**macOS**

```
brew install postgresql
```

* create a db:

**Windows**

Download and install pgadmin https://www.pgadmin.org/download/pgadmin-4-windows/

or


**macOS**

Download and install pgadmin https://www.pgadmin.org/download/pgadmin-4-macos/

or

```
createdb studyhub
```

* connect to `studyhub` database with `postgres` user and create EXTENSION

```
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

* install yarn:
```
brew install npm
brew install yarn
```

* get packages (from root directory):
```
yarn install
yarn clear_types # remove duplicated react types
cd ./courses/static/courses/js/codesandbox-apps/codesandbox-browserfs/
npm install
npm run build
npm run dist
cd ./courses/static/courses/js/codesandbox-apps/common/
yarn install
cd ./courses/static/courses/js/codesandbox-apps/codesandbox-api/
yarn build
cd ./courses/static/courses/js/codesandbox-apps/vscode-textmate/
npm run install install-dependencies
npm run compile
cd ./courses/static/courses/js/containers/StudioViews/EditorsViews/containers/LessonWorkSpace/Codesandbox/node-services
yarn install
yarn build
cd ./courses/sandbox-eval-project/
yarn install
yarn build:sandbox_pib_dev
```

* Build the front-end
development watch mode
```
yarn run dev
```
or (prepare production bundle)
```
yarn run prod
```

* Activate your virtual environment

* Setup the db:
```
./manage.py migrate
```

* Create an admin account by running `/manage.py createsuperuser`

* Run:
```
./manage.py runserver
```
* You should find the site running on `http://localhost:8000`
* To login to the admin account go to `http://localhost:8000/admin`
* pib will look for a default curriculum named `Default Curriculum`, so in the admin create a curriculum titled `Default Curriculum`
* Then create a unit, module, lesson, and question, then navigate to /curriculum/ to see what you created!

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

## Deployment (Server side installation)

You can use any hosting services that support python: VPS, orchestration service, etc. But we have some built-in applications that rely on AWS.  
So, for now, Amazon EBS + RDS + S3 is the best choice to host the project. 

To Setup:

* install AWS CLI (http://docs.aws.amazon.com/cli/latest/userguide/installing.html):
```
brew install awscli
```
* install AWS EB CLI (http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install.html):
```
brew install awsebcli
```
* run `aws configure` 
* run `eb init` (you'll need the access id/key
* on git `develop` branch run `eb use pib-dev`
* on git `master` branch run `eb use pib-prod`

To Deploy:

* `eb deploy`
It will deploy to the proper environment depending on what branch you are on.

## Launching the Dev Environment

To save money, the dev environment will not always be up. To launch the dev environment, from the `develop` branch, run the following command:

```
eb create --branch_default --cfg pib-dev --timeout 40
```

Follow the directions, and use "pib-dev" instead of the default "physicsisbeautiful-dev".

This will take several minutes to run. If the command fails, you can try to run, `eb deploy` from the `develop` branch. Otherwise you may need to go on the aws console (Elastic Beanstalk) and rebuild the environment. The only other piece is that if you change the dns from `pib-dev.us-east-1.elasticbeanstalk.com` then you will need to go to the Google Domains and modify the DNS for `dev.physicsisbeautiful.com` to point at the new URL of the new dev environment.

Run `eb deploy` once the environment is up to get the latest version of dev running in the environment.


## Development

* We respect the rules set out by pep8 with the exception of a 100 character line limit.
* We use the flake8 python script for linting.
* For frontend code we use eslint for linting. See .eslintrc.json and .prettierrc files for details.
