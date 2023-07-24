#!/usr/bin/env python3
import json
import sys


for f in sys.argv[1:]:

    with open(f, 'r') as infile:
        nb = json.loads(infile.read())

    # Clear out SingleStore metadata
    metadata = nb.get('metadata', {})

    for k in list(metadata.keys()):
        if k.startswith('singlestore'):
            del metadata[k]

    cells = nb.get('cells', [])

    # Clear out execution metadata and cell output
    for cell in cells:
        if 'metadata' in cell:
            cell['metadata'] = {}
        if 'outputs' in cell:
            cell['outputs'] = []
        if 'execution_count' in cell:
            cell['execution_count'] = None

    # Remove empty cells at the end of the notebook
    end = len(cells) - 1
    while end > 0 and 'source' in cells[end] and not cells[end]['source']:
        cells.pop(end)
        end -= 1

    with open(f, 'w') as outfile:
        outfile.write(json.dumps(nb, indent=2))
        outfile.write('\n')
