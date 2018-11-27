#!/usr/bin/env python3
import sys
import os
import argparse
import logging

from traitlets.config import Config
import nbformat
from nbconvert import NotebookExporter

import utils
from clean import clean

CLEAN = 1

# TODO: would be nice to do some Make-like shortcuts to avoid processing notebooks
# whose rendered mtime > their partial mtime (and > the track meta mtime)

def nb_path_to_track(path):
    dirname = os.path.dirname(path)
    suff = '/raw'
    assert dirname.endswith(suff), dirname
    return dirname[:-len(suff)]

def render_track(track, track_cfg):
    meta = utils.get_track_meta(track, track_cfg)
    cfg = Config()
    cfg.Exporter.preprocessors = ['lesson_preprocessor.LearnLessonPreprocessor']
    exporter = NotebookExporter(config=cfg)
    resources = {'track_meta': meta, 'track_cfg': track_cfg}

    outdir = os.path.join(track, track_cfg['tag'], 'rendered')
    os.makedirs(outdir, exist_ok=True)
    for nb_meta in meta.notebooks:
        in_path = os.path.join(track, 'raw', nb_meta.filename)
        if nb_path_whitelist and in_path not in nb_path_whitelist:
            continue
        resources['lesson'] = nb_meta.lesson
        resources['nb_meta'] = nb_meta
        if CLEAN:
            clean(in_path)
        nb, _ = exporter.from_filename(in_path, resources)
        out_path = os.path.join(outdir, nb_meta.filename)
        with open(out_path, 'w') as f:
            f.write(nb)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=("Preprocess notebooks"))
    # TODO: Maybe default behaviour should be to render under *all* configs?
    parser.add_argument("--config", help="Tag associated with a yaml config file (default: default)", 
            default="default")
    parser.add_argument("track",
            help=("The path to a track. e.g. 'python', or 'examples/example_track'."
                " All notebooks referred to in that track's metadata will be rendered."
                )
            )
    parser.add_argument("-v", "--verbose", action='store_true',)
    args = parser.parse_args()
    
    logging.basicConfig(
            level=(logging.DEBUG if args.verbose else logging.INFO)
            )

    cfg = utils.get_track_config(args.track, args.config)
    render_track(args.track, cfg)
