#!/usr/bin/env python3
import os
import sys
import tomllib


def check_lesson(lesson):
    print('Checking ' + lesson)
    lesson_toml_path = os.path.join(
        'lessons',
        lesson,
    )

    with open(lesson_toml_path, 'rb') as f:
        meta = tomllib.load(f)

        notebooks = meta['meta']['notebooks']

        for notebook in notebooks:
            notebook_path = os.path.join(
                'notebooks',
                notebook,
                'notebook.ipynb'
            )

            if not os.path.isfile(notebook_path):
                print(
                    f'error: notebook file does not exist at {notebook_path}',
                    file=sys.stderr,
                )
                sys.exit(1)

def check_all_lessons():
    lessons = os.listdir('lessons')

    for lesson in lessons:
        check_lesson(lesson)

    print('Passed')


if __name__ == '__main__':
    check_all_lessons()
