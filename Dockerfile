# syntax=docker/dockerfile:1
FROM python:3.8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt-get -y update
# Upgrade already installed packages:
RUN apt-get -y upgrade
# Install a packages to build SPA:
RUN apt-get -y install nodejs npm
WORKDIR /code
COPY requirements.txt /code/
COPY requirements.dev.txt /code/
RUN pip install -r requirements.txt
RUN pip install -r requirements.dev.txt
COPY . /code/
# BUILD SPA
# RUN unzip -o courses/static/courses/js/codesandbox-apps/vscode-extensions/out/extensions.zip  -d courses/static/courses/js/codesandbox-apps/vscode-extensions/out/
RUN npm install -g yarn
RUN npm install -g lerna
RUN lerna bootstrap --npm-client=yarn && yarn clear_types
# build all workspace modules
# to remake with dependency
RUN yarn --cwd courses/static/courses/js/codesandbox-apps/codesandbox-api run build
RUN yarn workspace @codesandbox/common run build
RUN lerna run build
RUN lerna run dist
# compile bundles
RUN yarn build_dev
RUN yarn --cwd courses/sandbox-eval-project install
RUN yarn --cwd courses/sandbox-eval-project build:sandbox
# clean up node_modules TODO remove in courses/sandbox-eval-project/ also
RUN rimraf node_modules