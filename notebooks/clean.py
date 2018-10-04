import sys
import os
import re
import argparse

import nbformat as nbf

BAD_CELL_METADATA_KEYS = { '_uuid', '_cell_guid', }

# TODO: this should probably be set on a per-track basis in track_config.yaml. Or possibly on a per-notebook basis?
# Might also want to consider some middle-ground where we strip only the most obnoxious output (e.g. image/png base64 data, 
# rich (html/table) output beyond a certain size, etc.
CLEAR_OUTPUT = 1

def clean(nb_path):
    nb = nbf.read(nb_path, 4)
    clean_nb(nb)
    nbf.write(nb, nb_path)

def clean_nb(nb):
    """Modify given NotebookNode in place to normalize/strip some extraneous metadata.
    """
    nb['metadata']['language_info']['version'] = '3.6.5'
    for cell in nb.cells:
        if cell['cell_type'] == 'code':
            if CLEAR_OUTPUT:
                cell['outputs'] = []
            cell['execution_count'] = None
        for k in BAD_CELL_METADATA_KEYS:
            cell.get('metadata', {}).pop(k, None)

def main():
    parser = argparse.ArgumentParser(description=("Clean all raw notebooks under "
        "a given track, normalizing or removing extraneous metadata."),
        )
    parser.add_argument('track')
    args = parser.parse_args()
    rawdir = os.path.join(args.track, 'raw')
    nbs = [ os.path.join(rawdir, path)
            for path in os.listdir(rawdir) 
            if path.endswith('.ipynb')
            ]
    for nbpath in nbs:
        nb = nbf.read(nbpath, 4)
        clean_nb(nb)
        nbf.write(nb, nbpath)

if __name__ == '__main__':
    main()
