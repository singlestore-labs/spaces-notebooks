#!/usr/bin/env python3
import re
import sys
import tomllib


def error(msg):
    print('ERROR:', msg, file=sys.stderr)
    sys.exit(1)


for f in sys.argv[1:]:

    with open(f, 'r') as infile:
        info = tomllib.loads(infile.read())

    if 'meta' not in info:
        error(f'No `meta` section in `{f}`')

    # The meta section requires, title, description, and icon
    meta = info['meta']

    if 'title' not in meta:
        error(f'No `title` in `meta` section of {f}')

    if 'description' not in meta:
        error(f'No `description` in `meta` section of {f}')

    if 'icon' not in meta:
        error(f'No `icon` in `meta` section of {f}')

    # Tags must be all lower-case, ascii letters
    tags = meta.get('tags', [])

    if [x.lower() for x in tags] != tags:
        error(f'Tags must be in all lower-case ({tags}) in {f}')

    if [re.sub(r'[^a-z0-9]', r'', x) for x in tags] != tags:
        error(f'Tags can only contain letters and numbers ({tags}) in {f}')

    # Currently only "spaces" is allowed in destinations
    destinations = meta.get('destinations', [])

    if destinations and [x for x in destinations if x != 'spaces']:
        error(f'Only "spaces" is allowed in `destinations` in {f}')
