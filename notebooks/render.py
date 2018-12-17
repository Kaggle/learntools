#!/usr/bin/env python3
import sys
import os
import argparse
import logging

from traitlets.config import Config
import nbformat
from nbconvert import NotebookExporter

from nb_utils import utils
from clean import clean

CLEAN = 1

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
        if CLEAN:
            clean(in_path)
        nb, _ = exporter.from_filename(in_path, resources)
        out_path = os.path.join(outdir, nb_meta.filename)
        with open(out_path, 'w') as f:
            f.write(nb)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=("Preprocess notebooks"))
    parser.add_argument("-c", "--config", help="Tag associated with a yaml config file (default: all configs)",
            default=None)
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

    if args.config:
        cfgs = [utils.get_track_config(args.track, args.config)]
    else:
        cfgs = utils.get_track_configs(args.track)
    for cfg in cfgs:
        render_track(args.track, cfg)
