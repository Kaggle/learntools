import sys
import os
import re

import nbformat as nbf

BAD_CELL_METADATA_KEYS = { '_uuid', '_cell_guid', }

CLEAR_OUTPUT = 0

def clean(nb, path):
    fname = os.path.basename(path)
    nb['metadata']['language_info']['version'] = '3.6.5'
    for cell in nb.cells:
        if cell['cell_type'] == 'code':
            if CLEAR_OUTPUT:
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
