#!/usr/bin/env python3
"""Program for validating notebook content."""
import html
import json
import os
import sys
import tomllib
import uuid
from typing import Any


NOTEBOOK_HEADER = [
    '<div id="singlestore-header" style="display: flex; background-color: {background_color}; padding: 5px;">\n',
    '    <div id="icon-image" style="width: 90px; height: 90px;">\n',
    '        <img width="100%" height="100%" src="https://raw.githubusercontent.com/singlestore-labs/spaces-notebooks/master/common/images/header-icons/{icon_name}.png" />\n',
    '    </div>\n',
    '    <div id="text" style="padding: 5px; margin-left: 10px;">\n',
    '        <div id="badge" style="display: inline-block; background-color: rgba(0, 0, 0, 0.15); border-radius: 4px; padding: 4px 8px; align-items: center; margin-top: 6px; margin-bottom: -2px; font-size: 80%">SingleStore Notebooks</div>\n',
    '        <h1 style="font-weight: 500; margin: 8px 0 0 4px;">{title}</h1>\n',
    '    </div>\n',
    '</div>',
]

NOTEBOOK_FOOTER = [
    '<div id="singlestore-footer" style="background-color: rgba(194, 193, 199, 0.25); height:2px; margin-bottom:10px"></div>\n',
    '<div><img src="https://raw.githubusercontent.com/singlestore-labs/spaces-notebooks/master/common/images/singlestore-logo-grey.png" style="padding: 0px; margin: 0px; height: 24px"/></div>',
]

ICON_COLORS = {
    'arrow-up-right-dots': 'rgba(255, 167, 103, 0.25)',
    'arrows-spin': 'rgba(124, 195, 235, 0.25)',
    'binary': 'rgba(210, 255, 153, 0.25)',
    'block-question': 'rgba(255, 224, 129, 0.25)',
    'bolt': 'rgba(235, 249, 245, 0.25)',
    'book-open-cover': 'rgba(124, 195, 235, 0.25)',
    'browser': 'rgba(235, 249, 245, 0.25)',
    'calendar-check': 'rgba(235, 249, 245, 0.25)',
    'camera-movie': 'rgba(255, 182, 176, 0.25)',
    'chart-network': 'rgba(210, 255, 153, 0.25)',
    'chart-scatter': 'rgba(124, 195, 235, 0.25)',
    'clouds': 'rgba(124, 195, 235, 0.25)',
    'confluent-logo': 'rgba(124, 195, 235, 0.25)',
    'crystal-ball': 'rgba(255, 167, 103, 0.25)',
    'database': 'rgba(235, 249, 245, 0.25)',
    'dollar-circle': 'rgba(255, 167, 103, 0.25)',
    'face-viewfinder': 'rgba(209, 153, 255, 0.25)',
    'file-export': 'rgba(255, 182, 176, 0.25)',
    'files': 'rgba(255, 224, 129, 0.25)',
    'filter': 'rgba(255, 167, 103, 0.25)',
    'gears': 'rgba(235, 249, 245, 0.25)',
    'globe': 'rgba(209, 153, 255, 0.25)',
    'handshake': 'rgba(255, 224, 129, 0.25)',
    'id-card': 'rgba(255, 182, 176, 0.25)',
    'image': 'rgba(255, 224, 129, 0.25)',
    'laptop': 'rgba(209, 153, 255, 0.25)',
    'lightbulb-on': 'rgba(255, 167, 103, 0.25)',
    'link': 'rgba(124, 195, 235, 0.25)',
    'location-dots': 'rgba(210, 255, 153, 0.25)',
    'lock': 'rgba(235, 249, 245, 0.25)',
    'map': 'rgba(255, 224, 129, 0.25)',
    'megaphone': 'rgba(124, 195, 235, 0.25)',
    'memo-circle-check': 'rgba(210, 255, 153, 0.25)',
    'message-dots': 'rgba(210, 255, 153, 0.25)',
    'nodes-circle': 'rgba(255, 224, 129, 0.25)',
    'notes': 'rgba(209, 153, 255, 0.25)',
    'pipeline': 'rgba(255, 167, 103, 0.25)',
    'radar': 'rgba(255, 182, 176, 0.25)',
    'rocket': 'rgba(210, 255, 153, 0.25)',
    'screwdriver-wrench': 'rgba(255, 182, 176, 0.25)',
    'server': 'rgba(255, 182, 176, 0.25)',
    'shield': 'rgba(124, 195, 235, 0.25)',
    'shop': 'rgba(235, 249, 245, 0.25)',
    'shopping-bag': 'rgba(255, 224, 129, 0.25)',
    'shopping-cart': 'rgba(255, 167, 103, 0.25)',
    'star': 'rgba(255, 182, 176, 0.25)',
    'user-plus': 'rgba(209, 153, 255, 0.25)',
    'users': 'rgba(210, 255, 153, 0.25)',
    'vector-circle': 'rgba(209, 153, 255, 0.25)',
    'waveform': 'rgba(209, 153, 255, 0.25)',
}


def error(msg: str) -> None:
    """Print an error message and end the program."""
    print('ERROR:', msg, file=sys.stderr)
    sys.exit(1)


def new_markdown_cell(cell_id: str, content: list[str]) -> dict[str, Any]:
    """
    Construct a markdown cell for a notebook.

    Parameters
    ----------
    cell_id : str
        The UUID to use for the cell ID
    content : list[str]
        The list of strings that make up the cell contents

    Returns
    -------
    dict[str, Any]

    """
    return dict(
        cell_type='markdown',
        id=cell_id,
        metadata={},
        source=content,
    )


for f in sys.argv[1:]:

    try:
        toml_path = os.path.join(os.path.dirname(f), 'meta.toml')
        with open(toml_path, 'rb') as toml_f:
            toml_info = tomllib.load(toml_f)
    except Exception:
        error(f'could not load `meta.toml` file: {toml_path}')

    with open(f, 'r') as infile:
        nb = json.loads(infile.read())

    if os.path.basename(f) != 'notebook.ipynb':
        error(f'notebook must be named `notebook.ipynb`: {f}')

    # Clear out SingleStore metadata
    metadata = nb.get('metadata', {})

    for k in list(metadata.keys()):
        if k.startswith('singlestore'):
            del metadata[k]

    cells = nb.get('cells', [])

    # Remove metadata and outputs
    for i, cell in enumerate(cells):
        if 'metadata' in cell:
            cell['metadata'] = {}
        if 'outputs' in cell:
            cell['outputs'] = []

    # Remove empty cells at the end of the notebook
    end = len(cells) - 1
    while end > 0 and 'source' in cells[end] and not cells[end]['source']:
        cells.pop(end)
        end -= 1

    header_id = str(uuid.uuid4())
    footer_id = str(uuid.uuid4())

    # Remove header cell, it will be regenerated later
    if cells:
        source = cells[0].get('source', [])
        if not isinstance(source, str):
            source = ''.join(source)
        if 'id="singlestore-header"' in source:
            header_cell = cells.pop(0)
            header_id = header_cell.get('id', header_id)

    # Remove footer cell, it will be regenerated later
    if cells:
        source = cells[-1].get('source', [])
        if not isinstance(source, str):
            source = ''.join(source)
        if 'id="singlestore-footer"' in source:
            footer_cell = cells.pop(-1)
            footer_id = footer_cell.get('id', footer_id)

    for cell in cells:

        # Convert source lists to a string
        source = cell.get('source', [])
        if isinstance(source, list):
            source = ''.join(source)
        source = [x.rstrip() + '\n' for x in source.rstrip().split('\n')]
        source[-1] = source[-1].rstrip()
        if source == ['']:
            source = []
        cell['source'] = source

        # Remove "attachments": null (not sure how they get in there)
        if 'attachments' in cell and cell['attachments'] is None:
            cell['attachments'] = {}

    # Prepare parameter substitutions for header
    try:
        icon_name = toml_info['meta']['icon']
        background_color = ICON_COLORS[icon_name]
    except KeyError as exc:
        print(str(exc))
        error(f'missing or incorrect icon in {toml_path}')

    try:
        title = html.escape(toml_info['meta']['title'])
    except KeyError as exc:
        error(f'missing title in {toml_path}')

    # Add header cell
    header = [
        x.format(
            background_color=background_color,
            icon_name=icon_name,
            title=title,
        ) for x in NOTEBOOK_HEADER
    ]
    cells.insert(0, new_markdown_cell(header_id, header))

    # Add footer cell
    cells.append(new_markdown_cell(footer_id, NOTEBOOK_FOOTER))

    # Ensure sequential execution counts
    code_idx = 1
    for cell in cells:
        if cell.get('cell_type', '') == 'code':
            cell['execution_count'] = code_idx
            code_idx += 1

    with open(f, 'w') as outfile:
        outfile.write(json.dumps(nb, indent=2))
        outfile.write('\n')
