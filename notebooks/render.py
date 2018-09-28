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

def render_notebooks(nbpaths):
    tracks = list(map(nb_path_to_track, nbpaths))
    track = tracks[0]
    assert all(t == track for t in tracks), "All notebooks to be rendered must be in same track."
    render_track(track, nbpaths)

def render_track(track, nb_path_whitelist=None):
    meta = utils.get_track_meta(track)
    track_cfg = utils.get_track_config(track)
    cfg = Config()
    cfg.Exporter.preprocessors = ['lesson_preprocessor.LearnLessonPreprocessor']
    exporter = NotebookExporter(config=cfg)
    resources = {'track_meta': meta, 'track_cfg': track_cfg}

    for nb_meta in meta.notebooks:
        in_path = os.path.join(track, 'raw', nb_meta.filename)
        if nb_path_whitelist and in_path not in nb_path_whitelist:
            continue
        resources['lesson'] = nb_meta.lesson
        resources['nb_meta'] = nb_meta
        if CLEAN:
            clean(in_path)
        nb, _ = exporter.from_filename(in_path, resources)
        out_path = os.path.join(track, 'rendered', nb_meta.filename)
        with open(out_path, 'w') as f:
            f.write(nb)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=("Preprocess notebooks, "
        "writing publication-ready ipynbs to <track>/rendered/"),
        usage="%(prog)s (track | {0} [{0} ...])".format('partial'),
        )
    # These arguments are a convenient fiction
    parser.add_argument("track",
            help=("The path to a track. e.g. 'python', or 'examples/example_track'."
                " All notebooks referred to in that track's metadata will be rendered."
                )
            )
    parser.add_argument("raw", nargs="*",
            help=("An explicit list of notebook files to be rendered. Mutually"
                " exclusive with track argument."
                )
            )
    parser.add_argument("-v", "--verbose", action='store_true',)
    args = parser.parse_args()
    
    logging.basicConfig(
            level=(logging.DEBUG if args.verbose else logging.INFO)
            )

    if args.raw or args.track.endswith('.ipynb'):
        raw = [args.track] + args.raw
        render_notebooks(raw)
    else:
        render_track(args.track)
