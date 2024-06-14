#!/usr/bin/env python3
import os
import sys
import tomllib

def error(msg):
    print('ERROR:', msg, file=sys.stderr)
    sys.exit(1)

def check_author(author_path):
    print(f"Checking {author_path}...")

    with open(author_path, 'rb') as f:
        meta = tomllib.load(f)

        if 'name' not in meta:
            error(f'No `name` in `meta` section of {author_path}')

        if 'description' not in meta:
            error(f'No `description` in `meta` section of {author_path}')

        # Logo is optional, but if defined a corresponding image must exist
        if 'logo' in meta:
            logo_filename = f"{meta['logo']}.png"
            logo_path = os.path.join("common/images/author-images", logo_filename)
            if not os.path.isfile(logo_path):
                error(f'Logo image does not exist at {logo_path} for {author_path}')

if __name__ == '__main__':
    for f in sys.argv[1:]:
        check_author(f)
