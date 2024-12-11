<!-- markdownlint-disable MD033 MD024 -->
# 🐙 CPG Flow

<img src="/assets/DNA_CURIOUS_FLOYD_CROPPED.png" height="300" alt="CPG Flow logo" align="right"/>

![Python](https://img.shields.io/badge/-Python-black?style=for-the-badge&logoColor=white&logo=python&color=2F73BF)

TODO: Badges
Will look something like this

[![⚙️ Build Workflow](https://github.com/antoinezanardi/werewolves-assistant-api-next/actions/workflows/build.yml/badge.svg)](https://github.com/antoinezanardi/werewolves-assistant-api-next/actions/workflows/build.yml)
[![🚀 Deploy To Production Workflow](https://github.com/antoinezanardi/werewolves-assistant-api-next/actions/workflows/deploy-to-production.yml/badge.svg)](https://github.com/antoinezanardi/werewolves-assistant-api-next/actions/workflows/deploy-to-production.yml)

[![GitHub release](https://img.shields.io/github/release/antoinezanardi/werewolves-assistant-api-next.svg)](https://GitHub.com/antoinezanardi/werewolves-assistant-api-next/releases/)
[![semantic-release: conventional commits](https://img.shields.io/badge/semantic--release-conventional%20commits-Æ1A7DBD?logo=semantic-release&color=1E7FBF)](https://github.com/semantic-release/semantic-release)
[![GitHub license](https://img.shields.io/github/license/antoinezanardi/werewolves-assistant-api-next.svg)](https://github.com/antoinezanardi/https://img.shields.io/github/license/werewolves-assistant-api-next.svg/blob/main/LICENSE)
![Dependencies](https://img.shields.io/badge/-dependencies-black?style=flat-square&logoColor=white&logo=pnpm&color=B76507)[![Known Vulnerabilities](https://snyk.io/test/github/antoinezanardi/werewolves-assistant-api-next/badge.svg?targetFile=package.json&style=flat-square)](https://snyk.io/test/github/antoinezanardi/werewolves-assistant-api-next?targetFile=package.json)

[![Tests count](https://byob.yarr.is/antoinezanardi/werewolves-assistant-api-next/tests-count)](https://byob.yarr.is/antoinezanardi/werewolves-assistant-api-next/tests-count)
[![Scenarios](https://byob.yarr.is/antoinezanardi/werewolves-assistant-api-next/scenarios)](https://byob.yarr.is/antoinezanardi/werewolves-assistant-api-next/scenarios)

[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=antoinezanardi_werewolves-assistant-api-next&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=antoinezanardi_werewolves-assistant-api-next)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=antoinezanardi_werewolves-assistant-api-next&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=antoinezanardi_werewolves-assistant-api-next)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=antoinezanardi_werewolves-assistant-api-next&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=antoinezanardi_werewolves-assistant-api-next)

<br />

## 📋 Table of Contents

1. 🐙 [What is this API ?](#what-is-this-api)
2. ✨ [Production and development links](#production-and-development-links)
3. 🔨 [Installation](#installation)
4. 🚀 [Build](#build)
5. 🐳 [Docker](#docker)
6. 💯 [Tests](#tests)
7. 🌿 [Env variables](#env-variables)
8. ☑️ [Code analysis and consistency](#code-analysis-and-consistency)
9. 📈 [Releases & Changelog](#versions)
10. 🎬 [GitHub Actions](#github-actions)
11. ✨ [Misc commands](#misc-commands)
12. ©️ [License](#license)
13. ❤️ [Contributors](#contributors)

## <a name="what-is-this-api">🐙 What is this API ?</a>

Welcome to CPG Flow!

This API provides a set of tools and workflows for managing population genomics data pipelines, designed to streamline the processing, analysis, and storage of large-scale genomic datasets. It facilitates automated pipeline execution, enabling reproducible research while integrating with cloud-based resources for scalable computation.

CPG Flow supports various stages of genomic data processing, from raw data ingestion to final analysis outputs, making it easier for researchers to manage and scale their population genomics workflows.

## <a name="production-and-development-links">✨ Production and development links</a>

### 🌐 Production

The production version of this API is available at **[api.werewolves-assistant.com](https://api.werewolves-assistant.com/docs)**.

This API is used by the **[Werewolves Assistant Web App](https://werewolves-assistant.com)**.

The production server is updated automatically with the latest version of the API when a new release is created. (When a new tag is pushed on the `main` branch)

### 🛠️ Development

The development version of this API is available at **[preprod.api.werewolves-assistant.com](https://preprod.api.werewolves-assistant.com/docs)**.

This API is used by the **[Werewolves Assistant Web App](https://preprod.werewolves-assistant.com)**.

The development server is updated automatically when a commit is pushed on the `develop` branch.

## <a name="installation">🔨 Installation</a>

To install this project, you will need to have on your machine :

![Node](https://img.shields.io/badge/-nodejs-black?style=for-the-badge&logoColor=white&logo=node.js&color=366A31)
![PNPM](https://img.shields.io/badge/-pnpm-black?style=for-the-badge&logoColor=white&logo=pnpm&color=B76507)
![Docker](https://img.shields.io/badge/-Docker-black?style=for-the-badge&logoColor=white&logo=docker&color=004EA2)

We recommend to use the node version specified in the `.nvmrc` file.

**If you don't have `pnpm` installed, you can still use `npm` for all commands below, but we recommend to use `pnpm` for faster and more reliable installs.**

Then, run the following commands :

```bash
# Install dependencies and Husky hooks
pnpm install

# Run the app in dev mode
pnpm run start:dev
```

The above command will start the app in development mode and watch for changes on local.

You can also run the app in development mode with Docker, more information in the **[Docker section](#docker)**.

## <a name="build">🚀 Build</a>

TODO

## <a name="docker">🐳 Docker</a>

TODO

### 🔨 Development mode

To develop on this project first clone the repository. Then use the make init to setup for development. This will install the pre-commit hooks and requirements.

```bash
git clone https://github.com/populationgenomics/cpg-flow.git
make init
```

### 🚀 Production mode

TODO

### 🧪 Test mode

TODO

## <a name="tests">💯 Tests</a>

### 🧪 Unit and E2E tests

TODO: Test results and badges here (in more detail). Will look something like this.

![Jest](https://img.shields.io/badge/-Jest-black?style=for-the-badge&logoColor=white&logo=jest&color=BF3B14)

[![Tests count](https://byob.yarr.is/antoinezanardi/werewolves-assistant-api-next/tests-count)](https://byob.yarr.is/antoinezanardi/werewolves-assistant-api-next/tests-count)

[![Covered Statements](https://byob.yarr.is/antoinezanardi/werewolves-assistant-api-next/covered-statements)](https://byob.yarr.is/antoinezanardi/werewolves-assistant-api-next/covered-statements)

[![Covered Branches](https://byob.yarr.is/antoinezanardi/werewolves-assistant-api-next/covered-branches)](https://byob.yarr.is/antoinezanardi/werewolves-assistant-api-next/covered-branches)

[![Covered Functions](https://byob.yarr.is/antoinezanardi/werewolves-assistant-api-next/covered-functions)](https://byob.yarr.is/antoinezanardi/werewolves-assistant-api-next/covered-functions)

[![Covered Lines](https://byob.yarr.is/antoinezanardi/werewolves-assistant-api-next/covered-lines)](https://byob.yarr.is/antoinezanardi/werewolves-assistant-api-next/covered-lines)

### 🥒 Acceptance tests

![Cucumber](https://img.shields.io/badge/-Cucumber-black?style=for-the-badge&logoColor=white&logo=cucumber&color=169652)

[![Scenarios](https://byob.yarr.is/antoinezanardi/werewolves-assistant-api-next/scenarios)](https://byob.yarr.is/antoinezanardi/werewolves-assistant-api-next/scenarios)

Click on the badge below 👇 to see the **[reports](https://reports.cucumber.io/report-collections/9a53c3ab-ff98-43ce-977d-4b6ba9f9ae18)**.

[![ScenariosReports](https://messages.cucumber.io/api/report-collections/9a53c3ab-ff98-43ce-977d-4b6ba9f9ae18/badge)](https://reports.cucumber.io/report-collections/9a53c3ab-ff98-43ce-977d-4b6ba9f9ae18)

### 👽 Mutant testing

![Stryker](https://img.shields.io/badge/-Stryker-black?style=for-the-badge&logoColor=white&logo=stryker&color=7F1B10)

[![Mutation testing badge](https://img.shields.io/endpoint?style=flat&url=https%3A%2F%2Fbadge-api.stryker-mutator.io%2Fgithub.com%2Fantoinezanardi%2Fwerewolves-assistant-api-next%2Fmain)](https://dashboard.stryker-mutator.io/reports/github.com/antoinezanardi/werewolves-assistant-api-next/main)

You can also check the **[mutation testing report](https://dashboard.stryker-mutator.io/reports/github.com/antoinezanardi/werewolves-assistant-api-next/main#mutant)**.

### ▶️ Commands

Before testing, you must follow the **[installation steps](#installation)**.

TODO

## <a name="env-variables">🌿 Env variables</a>

TODO

<!--
Environment variables are :

|        Name         |               Description               | Required | Default value |                   Limitations                    |
| :-----------------: | :-------------------------------------: | :------: | :-----------: | :----------------------------------------------: |
|       `HOST`        | Host on which the API will be available |    ❌     |  `127.0.0.1`  |          If set, can't be empty string           |
|       `PORT`        | Port on which the API will be available |    ❌     |    `8080`     | If set, must be a number between `0` and `65535` |
|   `ENVIRONNEMENT`   |  Environment in which the API will run  |    ✅     |       ❌       |  Must be `development`, `production` or `test`   |
|   `DATABASE_HOST`   |        MongoDB database host URL        |    ✅     |       ❌       |              Can't be empty string               |
|   `DATABASE_PORT`   |          MongoDB database port          |    ❌     |  `undefined`  | If set, must be a number between `0` and `65535` |
|   `DATABASE_NAME`   |          MongoDB database name          |    ✅     |       ❌       |              Can't be empty string               |
| `DATABASE_USERNAME` |          MongoDB database user          |    ✅     |       ❌       |              Can't be empty string               |
| `DATABASE_PASSWORD` |        MongoDB database password        |    ✅     |       ❌       |              Can't be empty string               |
|    `CORS_ORIGIN`    |           CORS allowed origin           |    ❌     |      `*`      |          If set, can't be empty string           |
-->


## <a name="code-analysis-and-consistency">☑️ Code analysis and consistency</a>

### 🔍 Code linting & formatting

![Precommit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)

In order to keep the code clean, consistent and free of bad TS practices, more than **300 ESLint rules are activated** !

Complete list of all enabled rules is available in the **[.eslintrc.js file](https://github.com/antoinezanardi/werewolves-assistant-api-next/blob/master/.eslintrc.js)**.

### ▶️ Commands

Before linting, you must follow the [installation steps](#installation).

Then, run the following command

```bash
# Lint
pre-commit run --all-files
```

When setting up local linting for development you can also run the following once:

```bash
# Install the pre-commit hook
pre-commit install
```

### 🥇 Project quality scanner

Multiple tools are set up to maintain the best code quality and to prevent vulnerabilities:

TODO:
<!--
![CodeQL](https://img.shields.io/badge/-CodeQL-black?style=for-the-badge&logoColor=white&logo=github&color=2781FE)

You can check the **[CodeQL analysis report here](https://github.com/antoinezanardi/werewolves-assistant-api-next/security/code-scanning)**.

![SonarCloud](https://img.shields.io/badge/-SonarCloud-black?style=for-the-badge&logoColor=white&logo=sonarcloud&color=F37A3A)

SonarCloud summary is available **[here](https://sonarcloud.io/summary/new_code?id=antoinezanardi_werewolves-assistant-api-next)**.

[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=antoinezanardi_werewolves-assistant-api-next&metric=coverage)](https://sonarcloud.io/summary/new_code?id=antoinezanardi_werewolves-assistant-api-next)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=antoinezanardi_werewolves-assistant-api-next&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=antoinezanardi_werewolves-assistant-api-next)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=antoinezanardi_werewolves-assistant-api-next&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=antoinezanardi_werewolves-assistant-api-next)

[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=antoinezanardi_werewolves-assistant-api-next&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=antoinezanardi_werewolves-assistant-api-next)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=antoinezanardi_werewolves-assistant-api-next&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=antoinezanardi_werewolves-assistant-api-next)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=antoinezanardi_werewolves-assistant-api-next&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=antoinezanardi_werewolves-assistant-api-next)

[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=antoinezanardi_werewolves-assistant-api-next&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=antoinezanardi_werewolves-assistant-api-next)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=antoinezanardi_werewolves-assistant-api-next&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=antoinezanardi_werewolves-assistant-api-next)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=antoinezanardi_werewolves-assistant-api-next&metric=bugs)](https://sonarcloud.io/summary/new_code?id=antoinezanardi_werewolves-assistant-api-next)
-->

## <a name="versions">📈 Releases & Changelog</a>

TODO:

<!--
Releases on **main** branch are generated and published automatically by :

![Semantic Release](https://img.shields.io/badge/-Semantic%20Release-black?style=for-the-badge&logoColor=white&logo=semantic-release&color=000000)

It uses the **[conventional commit](https://www.conventionalcommits.org/en/v1.0.0/)** strategy.

Each change when a new release comes up is listed in the **<a href="https://github.com/antoinezanardi/werewolves-assistant-api-next/blob/master/CHANGELOG.md" target="_blank">CHANGELOG.md file</a>**.

Also, you can keep up with changes by watching releases via the **Watch GitHub button** at the top of this page.

#### 🏷️ <a href="https://github.com/antoinezanardi/werewolves-assistant-api-next/releases" target="_blank">All releases for this project are available here</a>.

-->

## <a name="github-actions">🎬 GitHub Actions</a>

This project uses **GitHub Actions** to automate some boring tasks.

You can find all the workflows in the **[.github/workflows directory](https://github.com/populationgenomics/cpg-flow/tree/main/.github/workflows).**

### 🎢 Workflows

TODO
<!--
|                                                                            Name                                                                             |                                                                                                                                                                         Description & Status                                                                                                                                                                          |                      Triggered on                      |
| :---------------------------------------------------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :----------------------------------------------------: |
|                         **[⚙️ Build](https://github.com/antoinezanardi/werewolves-assistant-api-next/actions/workflows/build.yml)**                          |                                   Various checks for app health, code quality and tests coverage<br/><br/>[![⚙️ Build Workflow](https://github.com/antoinezanardi/werewolves-assistant-api-next/actions/workflows/build.yml/badge.svg)](https://github.com/antoinezanardi/werewolves-assistant-api-next/actions/workflows/build.yml)                                   | `push` on `develop` and all pull requests to `develop` |
| **[🔃 Lint PR Name Into Develop Workflow](https://github.com/antoinezanardi/werewolves-assistant-api-next/actions/workflows/lint-pr-name-into-develop.yml)** |   Checks if pull request name respects `conventionnal-commit` rules<br/><br/>[![🔃 Lint PR Name Into Develop Workflow](https://github.com/antoinezanardi/werewolves-assistant-api-next/actions/workflows/lint-pr-name-into-develop.yml/badge.svg)](https://github.com/antoinezanardi/werewolves-assistant-api-next/actions/workflows/lint-pr-name-into-develop.yml)    |         `pull-request` `created` or `updated`          |
|       **[⛵️ Push On Develop Branch Workflow](https://github.com/antoinezanardi/werewolves-assistant-api-next/actions/workflows/push-on-develop.yml)**        |                      Uploads app with `develop` version to `Docker Hub`<br/><br/>[![⛵️ Push On Develop Branch Workflow](https://github.com/antoinezanardi/werewolves-assistant-api-next/actions/workflows/push-on-develop.yml/badge.svg)](https://github.com/antoinezanardi/werewolves-assistant-api-next/actions/workflows/push-on-develop.yml)                       |                  `push` on `develop`                   |
|         **[🔃️ Upsert PR Release Workflow](https://github.com/antoinezanardi/werewolves-assistant-api-next/actions/workflows/upsert-pr-release.yml)**         | Creates or updates pull request to `main` depending on commits on `develop` since last release<br/><br/>[![🔃️ Upsert PR Release Workflow](https://github.com/antoinezanardi/werewolves-assistant-api-next/actions/workflows/upsert-pr-release.yml/badge.svg)](https://github.com/antoinezanardi/werewolves-assistant-api-next/actions/workflows/upsert-pr-release.yml) |                  `push` on `develop`                   |
|          **[🏷️ Release Creation Workflow](https://github.com/antoinezanardi/werewolves-assistant-api-next/actions/workflows/release-creation.yml)**          |           Creates a new release using `semantic-release` with tag and updated changelog<br/><br/>[![🏷️ Release Creation Workflow](https://github.com/antoinezanardi/werewolves-assistant-api-next/actions/workflows/release-creation.yml/badge.svg)](https://github.com/antoinezanardi/werewolves-assistant-api-next/actions/workflows/release-creation.yml)           |                    `push` on `main`                    |
|      **[🚀 Deploy To Production Workflow](https://github.com/antoinezanardi/werewolves-assistant-api-next/actions/workflows/deploy-to-production.yml)**      |              Deploys app with last tag version to `Docker Hub` and `GCP`<br/><br/>[![🚀 Deploy To Production Workflow](https://github.com/antoinezanardi/werewolves-assistant-api-next/actions/workflows/deploy-to-production.yml/badge.svg)](https://github.com/antoinezanardi/werewolves-assistant-api-next/actions/workflows/deploy-to-production.yml)              |                     `tag-creation`                     |

-->

## <a name="misc-commands">✨ Misc commands</a>

TODO

<!--
### 🌳 Animated tree visualisation of the project's evolution with **[Gource](https://gource.io/)**
```shell
# Please ensure that `gource` is installed on your system.
pnpm run gource
```

### 🔀 Create git branch with a conventional name
```shell
pnpm run script:create-branch
```

### ⤴️ Create pull request against the `develop` branch from current branch
```shell
pnpm run script:create-pull-request
```

### 📣 To all IntelliJ IDEs users (IntelliJ, Webstorm, PHPStorm, etc.)

All the above commands are available in the **.run directory** at the root of the project.

You can add them as **run configurations** in your IDE.

-->

## <a name="license">©️ License</a>

This project is licensed under the [MIT License](http://opensource.org/licenses/MIT).

## <a name="contributors">❤️ Contributors</a>

There is no contributor yet. Want to be the first ?

If you want to contribute to this project, please read the [**contribution guide**](https://github.com/populationgenomics/cpg-flow/blob/master/CONTRIBUTING.md).
