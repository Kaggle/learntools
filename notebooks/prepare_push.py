#!/usr/bin/env python3
import sys
import os
import json

import utils

def main():
    trackname = sys.argv[1]
    meta = utils.get_track_meta(trackname)
    cfg = utils.get_track_config(trackname)
    push_dir = os.path.join(trackname, 'kernels_api_metadata')
    for nb in meta.notebooks:
        dest_dir = os.path.join(push_dir, nb.stem)
        os.makedirs(dest_dir, exist_ok=True)
        dest_path = os.path.join(dest_dir, 'kernel-metadata.json')
        kernel_meta = nb.kernel_metadata(cfg)
        with open(dest_path, 'w') as f:
            json.dump(kernel_meta, f, indent=2, sort_keys=True)

main()
