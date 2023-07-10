# SingleStore Spaces Contributing Guide

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

Example:

```toml
[meta]
title="Atlas & Kai for Mongo Side-by-Side"
description="Compare performance on same code from simple to more complex queries"
tags=["mongodb", "kai"]
```
