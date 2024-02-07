# SingleStore Spaces Contributing Guide

First, please fork this repo and commit your changes to the forked repo. From there make a Pull Request with your notebook submission keeping the following in mind:


## Key Requirements

First, you should check whether this notebook can be run using a Free Shared Tier instance. This is ideal for scenarios requiring few tables (<10), pipelines (<10) and less than 1GB of compressed storage. See the [limitations](https://docs.singlestore.com/cloud/shared-edition/) to determine if your notebook can be run on a Free Shared Tier database.

If your database can be run using the Free Shared Tier (Starter Workspace), you must:
1. Mention this using a Markdown cell at the top of the notebook. See [example](https://www.singlestore.com/spaces/mongo-atlas-single-store-kai/). You should explicitly state that this notebook can run on both the Starter and Standard Workspaces.
2. Add "starter" to the tags in the meta.toml file below.
3. Use the following syntax when creating OR dropping your database. NOTE: When you create a Starter Workspace, a database is automatically created for it. Starter Workspaces are limited to one database. The only way you can drop the auto-created database linked to the Starter Workspace is by terminating the Workspace altogether.

```python
shared_tier_check = %sql show variables like 'is_shared_tier'
if not shared_tier_check or shared_tier_check[0][1] == 'OFF':
    %sql DROP DATABASE IF EXISTS your_database_name;
    %sql CREATE DATABASE your_database_name
```

4. At the end of the notebook, you should do the same check when cleaning up any databases created.

```python
shared_tier_check = %sql show variables like 'is_shared_tier'
if not shared_tier_check or shared_tier_check[0][1] == 'OFF':
    %sql DROP DATABASE IF EXISTS your_database_name;
```


If your database can only be run using Standard workspaces, you must:
1. Mention this using a Markdown cell at the top of the notebook. See [example](https://www.singlestore.com/spaces/ingest-data-from-confluent-cloud-kafka/). You should explicitly state that this notebook can run only on Standard Workspaces.
2. Add "advanced" to the tags in the meta.toml file below.



## File structure

To add a new space you should create a new folder inside `/notebooks`.

Here are some requirements for the file structure:

1. Folder name must use `kebab-case`
2. Folder must contain a Jupyter Notebook called `notebook.ipynb`
3. Folder must contain a `meta.toml` file which holds information about your SingleStore Space. See below for the structure of this file.

### `meta.toml` file

Your `meta.toml` file should have a `[meta]` section with the following keys:

- title: string
- description: string (optional)
- tags: string[] (optional)
- icon: string. You don't need to reference the extension. See full list of icon names [here](https://github.com/singlestore-labs/spaces-notebooks/tree/master/common/images/header-icons)

Example:

```toml
[meta]
title="Atlas & Kai for Mongo Side-by-Side"
description="Compare performance on same code from simple to more complex queries"
tags=["mongodb", "kai"]
icon="database"
```


## Pre-commit checks on the clone of this repo

The CI pipeline in this repo runs a bunch of validation checks and code reformatting with pre-commit checks. If you don't install those checks in your clone of the repo, the code will likely never pass. To install the pre-commit tool in your clone run the following from your clone directory. This will force the checks before you can push.

You will need to develop your notebooks using Python 3.11 or higher. By default, Notebooks developed on SingleStore will be using this version of Python. This is required for the pre-commit checks to run:

```bash
pip3 install pre-commit
pre-commit install
```

The checks run automatically when you attempt to commit, but you can run them manually as well with the following:
```bash
pre-commit run --all-files
```
