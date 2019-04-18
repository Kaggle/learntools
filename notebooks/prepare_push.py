#!/usr/bin/env python3
import sys
import os
import json
import nbformat
from nbconvert import NotebookExporter

from traitlets.config import Config
from clean import clean

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

def nb_path_to_track(path):
    dirname = os.path.dirname(path)
    suff = '/raw'
    assert dirname.endswith(suff), dirname
    return dirname[:-len(suff)]

def render_track(track, track_cfg):
    meta = utils.get_track_meta(track, track_cfg)
    cfg = Config()
    cfg.Exporter.preprocessors = ['nb_utils.lesson_preprocessor.LearnLessonPreprocessor']
    exporter = NotebookExporter(config=cfg)
    resources = {'track_meta': meta, 'track_cfg': track_cfg}

    outdir = os.path.join(track, track_cfg['tag'], 'rendered')
    os.makedirs(outdir, exist_ok=True)
    for nb_meta in meta.notebooks:
        in_path = os.path.join(track, 'raw', nb_meta.filename)
        resources['lesson'] = nb_meta.lesson
        resources['nb_meta'] = nb_meta
        clean(in_path)
        nb, _ = exporter.from_filename(in_path, resources)
        out_path = os.path.join(outdir, nb_meta.filename)
        with open(out_path, 'w') as f:
            f.write(nb)

if __name__ == '__main__':
    track = sys.argv[1]
    cfgs = utils.get_track_configs(track)
    for cfg in utils.get_track_configs(track):
        render_track(track, cfg)
        meta = utils.get_track_meta(track, cfg)
        create_metadata_files_for_cfg(track, cfg, meta)
