# SingleStore Spaces Contributing Guide

First, please fork this repo and commit your changes to forked repo. From there make a Pull Request with your notebook submission keeping the following in mind:


## File structure

To add a new space you should create a new folder inside `/notebooks`.

Here are some requirements for the file structure

1. Folder name must be `kebab-case`
2. Folder must contain a Jupyter Notebook called `notebook.ipynb`
3. Folder must contain a `meta.toml` file which holds information about your SingleStore Space. See below for the structure of this file.

### `meta.toml` file

Your `meta.toml` file should have a `[meta]` section with the following keys:

- title: string
- description: string (optional)
- tags: string[] (optional)
- icon: string. See full list of icon names on: https://github.com/singlestore-labs/spaces-notebooks/tree/master/common/images/header-icons

Example:

```toml
[meta]
title="Atlas & Kai for Mongo Side-by-Side"
description="Compare performance on same code from simple to more complex queries"
tags=["mongodb", "kai"]
```


## Pre-commit checks on the clone of this repo

The CI pipeline in this repo runs a bunch of validation checks and code reformatting with pre-commit checks. If you don't install those checks in your clone of the repo, the code will likely never pass. To install the pre-commit tool in your clone run the following from your clone directory. This will force the checks before you can push.

```bash
pip3 install pre-commit
pre-commit install
```

The checks run automatically when you attempt to commit, but you can run them manually as well with the following:
```bash
pre-commit run --all-files
```
