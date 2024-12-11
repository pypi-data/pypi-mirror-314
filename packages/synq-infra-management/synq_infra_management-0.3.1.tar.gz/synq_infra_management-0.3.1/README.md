# Synq Infra Management

## Overview

This project automates the management of SQL tests using Synq's gRPC API. It allows you to deploy, update, and delete SQL tests based on configurations stored in YAML files (e.g., tests_def.yaml and *_data.yaml). The project compares local test definitions with those already deployed in Synq and applies any necessary updates or deletions.

# Initial setup

## 1. Installing Dependencies for Local Testing

``` bash
python -m venv .env
source .env/bin/activate

pip install -r requirements.txt
pip install synq_infra_management
pip install pre-commit

pre-commit install

export SNOWFLAKE_ACCOUNT=ACCOUNT.eu-west-1
export SYNQ_LONG_LIVED_TOKEN=synq_token_api
```

## 2. Configuring a New Repository

### File Structure
To set up the SQL tests, create a directory for your SQL test files and copy the tests_def.yaml file into it. You can create as many *_data.yaml files as needed. (See examples in the example directory).

After copying the YAML files, also copy requirements.txt and main.py. In main.py, update the sql_tests_dir variable to point to the directory you just created.

### Example repo to use: [Templates SQL Tests](https://github.com/IAG-Loyalty/synq-sql-tests-templates)


The directory structure should look like this:

``` css
.
├── main.py
├── README.md
├── requirements.txt
└── synq_sql_tests
    ├── BRONZE_data.yaml
    ├── GOLD_data.yaml
    └── tests_def.yaml
```

### Usage example

To test the changes and deployment process:

``` bash
# Execute the --plan option to preview the changes that will be applied in Synq
python main.py --plan

# Execute the --apply option to apply changes to Synq (only for testing purposes).
# The --apply command should be used in the GitHub Actions pipeline, not locally.
python main.py --apply
```
### Plan output explanation:

![Alt text](examples/documentation/plan_example.png)
---

### GitHub Actions Pipeline Structure

The standard workflow is split into two parts: a Pull Request (PR) workflow and a post-merge workflow. Teams can modify this setup based on their own responsibilities and requirements.

The example directory contains sample workflow files. To use these, create a .github/workflows directory in the root of your repository.

### PR Plan Workflow

This workflow triggers when a PR is opened or updated. Every update triggers a new workflow run in GitHub Actions. The Run Plan step will display the potential changes to the environment.

To set this up, you'll need two variables:

- <b>SYNQ_LONG_LIVED_TOKEN</b> (secret)
- <b>SNOWFLAKE_ACCOUNT</b> (variable)
- <b>ORGANISATION</b> (variable)


Go to your repository’s GitHub page and navigate to <b>Settings > Environments > New Environment</b> or just click in the already created environment to configure these.

#### Secrets:
![Alt text](examples/documentation/secret_example.png)

#### Variables:
![Alt text](examples/documentation/variable_example.png)

> Note: If deploying SQL tests to multiple Snowflake accounts, add additional accounts as environment variables in the Run Plan workflow step.

``` yml
    - name: Run Plan
      env:
        SYNQ_LONG_LIVED_TOKEN: ${{ secrets.SYNQ_LONG_LIVED_TOKEN }}
        SNOWFLAKE_ACCOUNT: ${{ vars.SNOWFLAKE_ACCOUNT }}
        SNOWFLAKE_ACCOUNT_2: ${{ vars.SNOWFLAKE_ACCOUNT_2 }}
        ORGANISATION: ${{ vars.ORGANISATION }}
      run: python main.py --plan
```
---

### Post Merge Workflow

The post-merge workflow operates similarly to the PR workflow. If multiple Snowflake accounts are involved, ensure all are included in the plan job.

``` yml
jobs:
  plan:

...

    - name: Run Plan for Verification
      env:
        SYNQ_LONG_LIVED_TOKEN: ${{ secrets.SYNQ_LONG_LIVED_TOKEN }}
        SNOWFLAKE_ACCOUNT: ${{ vars.SNOWFLAKE_ACCOUNT }}
        SNOWFLAKE_ACCOUNT_2: ${{ vars.SNOWFLAKE_ACCOUNT_2 }}
        ORGANISATION: ${{ vars.ORGANISATION }}
      run: python main.py --plan
```

For the apply job, you will need to set up a new environment in GitHub:

1. Go to <b>Settings > Environments</b> and create a new environment called ``production``.
2. Enable <b>Required reviewers</b> and Prevent self-review</b>.
3. Add as many reviewers as needed, including teams if necessary.
4. In the <b>Environment secrets</b> section, add ``SYNQ_LONG_LIVED_TOKEN``.
5. In <b>Environment variables</b>, add your ``SNOWFLAKE_ACCOUNT`` and your ``ORGANISATION``.

<b>Apply Step Example:</b>

``` yml
  apply:
    runs-on: ubuntu-latest
    needs: plan
    environment:
      name: production

...

    - name: Approve and Apply
      env:
        SYNQ_LONG_LIVED_TOKEN: ${{ secrets.SYNQ_LONG_LIVED_TOKEN }}
        SNOWFLAKE_ACCOUNT: ${{ vars.SNOWFLAKE_ACCOUNT }}
        SNOWFLAKE_ACCOUNT_2: ${{ vars.SNOWFLAKE_ACCOUNT_2 }}
        ORGANISATION: ${{ vars.ORGANISATION }}
      run: python main.py --apply

```

### Final Notes
- The ``--apply`` command should be reserved for approved GitHub Actions workflows, not local execution.
- The process supports multiple Snowflake accounts. Just add them as environment variables as shown above.

# Project Documentation

## Project Structure

`main.py`: The entry point of the project, which handles argument parsing and controls the execution of the deployment or planning of SQL tests.

`create_sql_tests.py`: Contains the logic to parse YAML files, generate SQL tests, and manage the deployment and deletion of tests.

`grpc_client/client.py`: Handles the gRPC channel setup to connect with the Synq API.

`proto_parsers/sqltest_parser.py`: Contains the sqlTestParser class to parse and manage SQL tests.

## Dependencies

`gRPC`: Used for communication with Synq's API.

`YAML`: For loading and parsing YAML configuration files.

## Setup

<b>1. Environment Variables</b>

You need to set up two environment variables in your GitHub Actions production environment:

- `SYNQ_LONG_LIVED_TOKEN`: API Token from Synq.

- `SNOWFLAKE_ACCOUNT`: List of Snowflake Account IDs (comma-separated if more than one)

- `ORGANISATION`: Name of your organisation. E.g: iag_loyalty, ba_holidays

<b>2. YAML Files</b>

`tests_def.yaml`: Contains the test definitions, including SQL templates and tags.

`*_data.yaml`: Contains the actual tests with tables, columns, and specific tag information.

## Usage

The project can be run in two modes:

1. `Plan Mode`: This mode compares the local YAML files with the deployed tests in Synq and shows the differences without making any changes. Use the --plan argument for this mode.

2. `Apply Mode`: This mode deploys new tests, updates existing ones, and deletes outdated tests based on the differences found between the local YAML files and the deployed tests. Use the --apply argument for this mode.

## Example commands

- <b>Plan Mode</b>:
``` bash
python main.py --plan
```
- <b>Apply Mode</b>:

``` bash
python main.py --apply
```

## Example SQL Test Setup

Here is an example of how to set up an SQL test:

`tests_def.yaml`:

```yaml
- name: [Test Name]
  id: [Test ID]
  tags:
    type: [Test Type]
  sql: [SQL Query]

################################

- name: values between two columns
  id: test_1_id
  tags:
    type: values_between
  sql: |
    select {.Column} from {.Table} where {.Column} <= {.WhereA} or {.Column} >= {.WhereB};

```

`*_data.yaml`:

```yaml
- table: [your_table]
  database: [your_database]
  schema: [your_schema]
  account: [your_snowflake_account]
  tags:
    owner: [team_name]
    product: [product_name]
    environment: [prd]
  schedule: [ daily ] # could be hourly, daily or Specific times like '2pm', '9am', etc
  columns:
    - name: [column_name]
      where_a: [condition] # Optional
      where_b: [condition] # Optional
      tests:
        - [test_id]

    - name: [column_name]
      tests:
        - [test_id]
            values: [condition] # Optional     
```

In this example:

1. <b>Test Definition</b>: In `tests_def.yaml`, `test_1` is defined with a SQL template that will count rows where a specific condition is met.

2. <b>Data</b>: In `*_data.yaml`, the test is applied to a specific table and column, with the condition value provided as `expected_value`. Each file that matches with `*_data.yaml`` inside of synq_tests directory will be read by the program

## GitHub Actions Pipeline

The project can be integrated into a CI/CD pipeline using GitHub Actions. The pipeline should consist of two stages:

1. <b>Plan Stage</b>: This stage runs when a pull request is opened. It executes `main.py --plan` and prints the possible changes without applying them.

2. <b>Apply Stage</b>: This stage requires approval before execution. After the pull request is merged, the pipeline runs `main.py --apply` to deploy the changes.

Example GitHub Actions Workflow:

<b>Plan:</b>
```yaml
name: PR Plan

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  plan:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'

    - name: Install dependencies
      run: pip install -r requirements.txt

    - name: Run Plan
      env:
        SYNQ_LONG_LIVED_TOKEN: ${{ secrets.SYNQ_LONG_LIVED_TOKEN }}
        SNOWFLAKE_ACCOUNT: ${{ vars.SNOWFLAKE_ACCOUNT }}
        ORGANISATION: ${{ vars.ORGANISATION }}
      run: python main.py --plan
```

<b>Apply:</b>
```yaml
name: Apply

on:
  push:
    branches:
      - main

jobs:
  plan:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.8'

    - name: Install dependencies
      run: pip install -r requirements.txt

    - name: Run Plan for Verification
      env:
        SYNQ_LONG_LIVED_TOKEN: ${{ secrets.SYNQ_LONG_LIVED_TOKEN }}
        SNOWFLAKE_ACCOUNT: ${{ vars.SNOWFLAKE_ACCOUNT }}
        ORGANISATION: ${{ vars.ORGANISATION }}
      run: python main.py --plan

  apply:
    runs-on: ubuntu-latest
    needs: plan
    environment:
      name: production

    steps:
    - name: Checkout repository
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.8'

    - name: Install dependencies
      run: pip install -r requirements.txt

    - name: Approve and Apply
      env:
        SYNQ_LONG_LIVED_TOKEN: ${{ secrets.SYNQ_LONG_LIVED_TOKEN }}
        SNOWFLAKE_ACCOUNT: ${{ vars.SNOWFLAKE_ACCOUNT }}
        ORGANISATION: ${{ vars.ORGANISATION }}
      run: python main.py --apply

```

