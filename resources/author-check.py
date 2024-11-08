#!/usr/bin/env python3
import os
import re
import sys
import tomllib


def error(msg):
    print('ERROR:', msg, file=sys.stderr)
    sys.exit(1)


def check_author(author_path):
    print(f'Checking {author_path}...')

    with open(author_path, 'rb') as f:
        meta = tomllib.load(f)

        if 'name' not in meta:
            error(f'No `name` in `meta` section of {author_path}')

        if 'title' not in meta:
            error(f'No `title` in `meta` section of {author_path}')

        if 'external' not in meta:
            error(f'No `external` in `meta` section of {author_path}')

        # Image is optional, but if defined a corresponding image must exist
        # Image can either be a URL or a filename in common/images/author-images
        if 'image' in meta:
            img_reference = meta['image']
            is_url = bool(re.match(r'^https?://', img_reference))

            if (not is_url):
                img_filename = f'{img_reference}.png'
                img_path = os.path.join('common/images/author-images', img_filename)
                if not os.path.isfile(img_path):
                    error(f'Author image does not exist at {img_path} for {author_path}')


if __name__ == '__main__':
    for f in sys.argv[1:]:
        check_author(f)
