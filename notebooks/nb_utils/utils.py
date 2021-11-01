import importlib
import os

import yaml
from nb_utils import track_metadata

def get_track_meta(track_dir, cfg):
    parts = track_dir.split(os.path.sep)
    pkg = '.'.join(filter(None, parts))
    module_name = pkg + '.track_meta'
    meta_module = importlib.import_module(module_name)
    return track_metadata.TrackMeta.from_module(meta_module, cfg)

def get_track_config(track_dir, tag):
    fname = tag
    if not tag.endswith('.yaml'):
        fname += '.yaml'
    cfg_path = os.path.join(track_dir, fname)
    with open(cfg_path) as f:
        # TODO: Some wrapper that knows about valid keys and default values. And
        # maybe with dotted access to keys.
        return yaml.load(f, Loader=yaml.FullLoader)

def get_track_configs(track_dir):
    for fname in os.listdir(track_dir):
        if not fname.endswith('.yaml'):
            continue
        path = os.path.join(track_dir, fname)
        with open(path) as f:
            yield yaml.load(f, Loader=yaml.FullLoader)
