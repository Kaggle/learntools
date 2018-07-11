import sys
import os
import json

FORCE = True

def make_meta(thing):
    return dict(
            resources=[{'path': 'script.ipynb'}],
            slug=thing['slug'],
            language='python',
            kernel_type='notebook',
            new_title=thing['title'],
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
                json.dump(meta, f, indent=2)

        script_loc = os.path.join(dest_dir, 'script.ipynb')
        # symlink the canonical rendered version with the pushable directory
        if not os.path.exists(script_loc):
            canon = os.path.join('rendered', track, thing['filename'])
            canon = os.path.abspath(canon)
            os.symlink(canon, script_loc)

def main():
    trackname = sys.argv[1]
    trackdir = 'partials/{}'.format(trackname)
    sys.path.append(trackdir)
    from nbconvert_config import lessons_meta
    for lesson in lessons_meta:
        prepare_push(lesson, trackname, FORCE)

main()
