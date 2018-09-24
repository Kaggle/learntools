import importlib
import os

import track_metadata

def get_track_meta(track_dir):
    parts = track_dir.split(os.path.sep)
    pkg = '.'.join(filter(None, parts))
    module_name = pkg + '.track_meta'
    meta_module = importlib.import_module(module_name)
    return track_metadata.TrackMeta.from_module(meta_module)
