#!/usr/bin/env python3
import os
import sys
import tomllib


def check_lesson(lesson_path):
    print('Checking ' + lesson_path)

    with open(lesson_path, 'rb') as f:
        meta = tomllib.load(f)

        notebooks = meta['meta']['notebooks']

        for notebook in notebooks:
            notebook_path = os.path.join(
                'notebooks',
                notebook,
                'notebook.ipynb',
            )

            if not os.path.isfile(notebook_path):
                print(
                    f'error: notebook file does not exist at {notebook_path}',
                    file=sys.stderr,
                )
                sys.exit(1)


if __name__ == '__main__':
    for f in sys.argv[1:]:
        check_lesson(f)
