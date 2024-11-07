#!/usr/bin/env python3
"""Package sample notebooks for use in the managed service portal."""
import argparse
import json
import os
import sys
from zipfile import ZipFile

import tomllib


NOTEBOOK_FILE_NAME = 'notebook.ipynb'

REQUIRED_FILES = [NOTEBOOK_FILE_NAME, 'meta.toml']


def strip_outputs(path: str) -> str:
    """Remove outputs from notebook at path."""

    with open(path, 'r') as infile:
        nb = json.loads(infile.read())

        for cell in nb['cells']:
            if 'metadata' in cell:
                cell['metadata']['execution'] = {}
            if 'outputs' in cell:
                cell['outputs'] = []
            if 'metadata' in nb:
                if 'singlestore_connection' in nb['metadata']:
                    nb['metadata']['singlestore_connection'] = {}

        return json.dumps(nb, indent=2)


def get_valid_notebooks(notebooks: str, notebooks_directory: str) -> list[str]:
    """Return a list of valid notebooks"""

    notebook_names = []

    if notebooks == 'sample':
        with open(args.toml, 'rb') as f:
            meta = tomllib.load(f)
            notebook_names = meta['samples']['display']
    elif notebooks == 'all':
        # get all
        notebook_names = os.listdir(notebooks_directory)
    else:
        # comma-separated list
        notebook_names = list(map(str.strip, notebooks.split(',')))

    valid_notebooks = []

    for notebook_name in notebook_names:

        for required_file in REQUIRED_FILES:
            path = os.path.join(
                args.notebooks_directory,
                notebook_name,
                required_file,
            )

            if not os.path.isfile(path):
                print(
                    f'error: Required file does not exist: {path}',
                    file=sys.stderr,
                )
                sys.exit(1)

        valid_notebooks.append(notebook_name)

    return valid_notebooks


def convert_to_destination_path(path: str) -> str:
    """Remove 'notebooks' from path"""
    parts = path.split('/')
    filtered_parts = list(filter(lambda x: x != 'notebooks', parts))

    return '/'.join(filtered_parts)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='package sample notebooks for use in '
                    'the managed service portal',
    )

    parser.add_argument(
        'notebooks_directory',
        metavar='notebooks-directory',
        help='root `notebooks` directory',
    )
    parser.add_argument(
        '--notebooks',
        help='which notebooks to package',
        default='all',
        required=True,
    )
    parser.add_argument(
        '-t', '--toml',
        help='toml file containing configuration',
        default='meta.toml',
    )
    parser.add_argument(
        '-o', '--outfile',
        help='name of the output file',
        default='sample-notebooks.zip',
    )
    parser.add_argument(
        '-s', '--strip-outputs',
        help='strip the output cells from the notebooks',
        default=False,
        action=argparse.BooleanOptionalAction,
    )

    args = parser.parse_args()

    valid_notebooks = get_valid_notebooks(
        notebooks=args.notebooks,
        notebooks_directory=args.notebooks_directory,
    )

    with ZipFile(args.outfile, 'w') as out:
        for notebook_name in valid_notebooks:
            print(notebook_name)

            notebook_directory_path = os.path.join(
                args.notebooks_directory,
                notebook_name,
            )

            notebook_path = os.path.join(
                notebook_directory_path,
                NOTEBOOK_FILE_NAME,
            )

            # write the whole notebook directory
            for dirpath, dirs, files in os.walk(notebook_directory_path):
                for file in files:
                    source = os.path.join(dirpath, file)
                    destination = convert_to_destination_path(source)

                    if source == notebook_path and args.strip_outputs:
                        # write notebook with stripped output
                        stripped_nodebook = strip_outputs(notebook_path)
                        out.writestr(destination, stripped_nodebook)
                    else:
                        # write file normally
                        out.write(source, arcname=destination)
