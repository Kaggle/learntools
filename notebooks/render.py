import sys
import os

from traitlets.config import Config
import nbformat
from nbconvert import NotebookExporter

import utils
from clean import clean

CLEAN = 1

# TODO: would be nice to do some Make-like shortcuts to avoid processing notebooks
# whose rendered mtime > their partial mtime (and > the track meta mtime)
def main():
    # TODO: Call clean before preprocessing stuff.
    track = sys.argv[1]
    meta = utils.get_track_meta(track)
    track_cfg = utils.get_track_config(track)
    cfg = Config()
    cfg.Exporter.preprocessors = ['lesson_preprocessor.LearnLessonPreprocessor']
    exporter = NotebookExporter(config=cfg)
    resources = {'track_meta': meta}

    for nb_meta in meta.notebooks:
        resources['lesson'] = nb_meta.lesson
        in_path = os.path.join(track, 'partials', nb_meta.filename)
        if CLEAN:
            clean(in_path)
        nb, _ = exporter.from_filename(in_path, resources)
        out_path = os.path.join(track, 'rendered', nb_meta.filename)
        with open(out_path, 'w') as f:
            f.write(nb)
        break

if __name__ == '__main__':
    main()
