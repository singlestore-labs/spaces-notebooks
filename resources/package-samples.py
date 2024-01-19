#!/usr/bin/env python3
"""Package sample notebooks for use in the managed service portal."""
import argparse
import json
import os
import sys
from zipfile import ZipFile

import tomllib


def clear_outputs(path: str) -> str:
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


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='package sample notebooks for use in '
                    'the managed service portal',
    )

    parser.add_argument(
        'notebooks_directory', metavar='notebooks-directory',
        help='root `notebooks` directory',
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

    args = parser.parse_args()

    with open(args.toml, 'rb') as f:
        meta = tomllib.load(f)
        files = []
        for i, name in enumerate(meta['samples']['display']):

            # Verify the notebook file exists
            path = os.path.join(
                args.notebooks_directory,
                name, 'notebook.ipynb',
            )
            if not os.path.isfile(path):
                print(
                    f'error: notebook file does not exist at {path}',
                    file=sys.stderr,
                )
                sys.exit(1)

            # Verify the metadata file exists
            meta_path = os.path.join(
                args.notebooks_directory,
                name, 'meta.toml',
            )
            if not os.path.isfile(meta_path):
                print(
                    f'error: metadata file does not exist at {meta_path}',
                    file=sys.stderr,
                )
                sys.exit(1)

            with open(meta_path, 'rb') as meta_toml:
                nb_meta = tomllib.load(meta_toml)

            try:
                files.append(
                    (
                        path,
                        f'{i + 1:02} - {nb_meta["meta"]["title"]}.ipynb.json',
                    ),
                )
            except Exception:
                print(path, ' =>\n    ', nb_meta)
                raise

    with ZipFile(args.outfile, 'w') as out:
        for path, name in files:
            print(path, ' => ', name)
            out.writestr(name, clear_outputs(path))
