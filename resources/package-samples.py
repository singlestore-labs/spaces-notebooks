#!/usr/bin/env python3
"""Package sample notebooks for use in the managed service portal."""
import argparse
import os
import sys
import tomllib
from zipfile import ZipFile


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
            path = os.path.join(
                args.notebooks_directory,
                name, name + '.ipynb',
            )
            if not os.path.isfile(path):
                print(
                    f'error: `.ipynb` file does not exist at {path}',
                    file=sys.stderr,
                )
                sys.exit(1)
            files.append((path, f'{i + 1:02} - {os.path.basename(path)}.json'))

    with ZipFile(args.outfile, 'w') as out:
        for path, name in files:
            print(path, ' => ', name)
            out.write(path, arcname=name)
