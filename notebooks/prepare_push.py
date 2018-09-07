#!/usr/bin/env python3
import sys
import os
import json

# Whether to overwrite existing metadata files.
FORCE = True

def make_meta(thing):
    return dict(
            id=thing['slug'],
            language='python',
            is_private='true',
            code_file="script.ipynb",
            enable_gpu="false",
            enable_internet="false",
            kernel_type='notebook',
            title=thing['title'],
            dataset_sources=thing.get('dataset_sources', []),
            kernel_sources=thing.get('kernel_sources', []),
            competition_sources=[],
            )

def prepare_push(lesson, track, force):
    for thing in [lesson['exercise'], lesson['tutorial'],]:
        name = thing['filename'].split('.')[0]
        dest_dir = os.path.join('pushables', track, name)
        os.makedirs(dest_dir, exist_ok=True)
        meta_fname = os.path.join(dest_dir, 'kernel-metadata.json')
        if not os.path.exists(meta_fname) or force:
            meta = make_meta(thing)
            with open(meta_fname, 'w') as f:
                json.dump(meta, f, indent=2, sort_keys=True)

        sympath = os.path.join(dest_dir, 'script.ipynb')
        # symlink the canonical rendered version with the pushable directory
        if not os.path.exists(sympath):
            canon = os.path.join('rendered', track, thing['filename'])
            # Since we're checking these symlinks in to version control, make 
            # them point to relative paths so they'll play nicely with any filesystem
            rel_canon = os.path.relpath(canon, dest_dir)
            os.symlink(rel_canon, sympath)

def main():
    trackname = sys.argv[1]
    trackdir = 'partials/{}'.format(trackname)
    # Yuck
    sys.path.append(trackdir)
    from nbconvert_config import lessons_meta
    for lesson in lessons_meta:
        prepare_push(lesson, trackname, FORCE)

main()
