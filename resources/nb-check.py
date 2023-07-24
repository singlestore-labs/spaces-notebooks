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

    # Clear out execution metadata and cell output
    for cell in nb.get('cells', []):
        if 'metadata' in cell:
            cell['metadata'] = {}
        if 'outputs' in cell:
            cell['outputs'] = []
        if 'execution_count' in cell:
            cell['execution_count'] = None

    with open(f, 'w') as outfile:
        outfile.write(json.dumps(nb, indent=2))
        outfile.write('\n')
