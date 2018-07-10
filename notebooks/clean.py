import sys
import os
import re

import nbformat as nbf

BAD_CELL_METADATA_KEYS = { '_uuid', '_cell_guid', }

def clean(nb, path):
    fname = os.path.basename(path)
    match = re.fullmatch(r'(tut|ex)_(\d+).ipynb', fname)
    assert match, fname
    ltmeta = dict(
            lesson_index=int(match.group(2))-1,
            type='tutorial' if match.group(1) == 'tut' else 'exercise',
            )
    nb['metadata']['learntools_metadata'] = ltmeta
    nb['metadata']['language_info']['version'] = '3.6.5'
    for cell in nb.cells:
        if cell['cell_type'] == 'code':
            cell['outputs'] = []
            cell['execution_count'] = None
        for k in BAD_CELL_METADATA_KEYS:
            cell.get('metadata', {}).pop(k, None)

def main():
    nbs = sys.argv[1:]
    for nbpath in nbs:
        nb = nbf.read(nbpath, 4)
        clean(nb, nbpath)
        nbf.write(nb, nbpath)

main()
