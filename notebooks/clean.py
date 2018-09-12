import sys
import os
import re

import nbformat as nbf

BAD_CELL_METADATA_KEYS = { '_uuid', '_cell_guid', }

CLEAR_OUTPUT = 0

def clean(nb, path):
    fname = os.path.basename(path)
    # TODO: This is silly. Should be doable based on metadata defined in 
    # the track's nbconvert_config.py, rather than by munging filenames.
    # This is the format used in python track
    match = re.fullmatch(r'(tut|ex)_(\d+).ipynb', fname)
    # Hacks on hacks
    if not match:
        # Format used for emb track
        try:
            lesson_index = int(fname[0]) - 1
        except ValueError:
            # In case of ancilliary nbs
            lesson_index = -2
        ltmeta = dict(
                lesson_index = lesson_index,
                type='exercise' if 'exercise' in fname else 'tutorial',
                )
    else:
        ltmeta = dict(
                lesson_index=int(match.group(2))-1,
                type='tutorial' if match.group(1) == 'tut' else 'exercise',
                )
    # This is set so it can be read by lesson_preprocessor.py, basically so it can
    # know how to look up the notebook it's currently looking at in the list of nb
    # metadata set in nbconvert_config.py.
    nb['metadata']['learntools_metadata'] = ltmeta
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
