#!/usr/bin/env python3
import sys
import os
import json

from nb_utils import utils

def create_metadata_files_for_cfg(trackname, cfg, meta):
    tag = cfg['tag']
    push_dir = os.path.join(trackname, tag, 'kernels_api_metadata')
    for nb in meta.notebooks:
        dest_dir = os.path.join(push_dir, nb.stem)
        os.makedirs(dest_dir, exist_ok=True)
        dest_path = os.path.join(dest_dir, 'kernel-metadata.json')
        kernel_meta = nb.kernel_metadata(cfg)
        with open(dest_path, 'w') as f:
            json.dump(kernel_meta, f, indent=2, sort_keys=True)

def main():
    trackname = sys.argv[1]
    for cfg in utils.get_track_configs(trackname):
        meta = utils.get_track_meta(trackname, cfg)
        create_metadata_files_for_cfg(trackname, cfg, meta)

main()
