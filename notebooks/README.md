Somewhat experimental setup for tracking canonical versions of Learn notebooks in version control.

`partials/python/` contains 'templates' for all the notebooks in the Python track (with `tut_1.ipynb` being the first tutorial notebook, `ex_1.ipynb` being the corresponding exercise notebook, etc.). This is where notebook editing should happen.

These notebooks contain some 'macros' in the source of some cells, such as `#$END_OF_EXERCISE$` or `#$EXERCISE_URL(4)$`. These get replaced via nbconvert magic (see `lesson_preprocessor.py`) when rendering the final notebook. To render some notebooks (writing them to the `rendered/` subdirectory), use `render.sh`. e.g.

    render.sh partials/python/*.ipynb

When you're ready to sync changes to the site, run `prepare_push.py`, passing the name of the track to prepare (e.g. `prepare_push.py python`). This will create a directory structure in a subdirectory `pushables` which is amenable to the Kernels API.

To push a particular notebook, do something like...

    cd pushables/python/ex_4
    kaggle k push -p .

(NB: Should be possible to do in just one step like...

    kaggle k push -p pushables/python/ex_4
    
But API currently has some issues when run on a directory other than pwd.)

The ipynbs in the `pushables` subdir set up by `prepare_push.py` are symlinks to the corresponding files in `rendered/` so you generally shouldn't have to run `prepare_push.py` again unless you add another notebook, or change a notebook's metadata in a way that would affect `kernel-metadata.json` (i.e. changing the title or slug).

Note: currently keeping `rendered/` notebooks under version control. At first this seemed like a bad idea, because in some sense they're "build products", and redundant wrt the template notebooks. However, I think it's really useful to be able to see the diff of a rendered notebook from the previous rendered version before pushing, as an assurance/sanity check.

# TODO

May be problematic that the embeddings track includes some ancilliary kernels which aren't tutorials or exercises but which serve as data sources for tuts and exs. Some code (e.g. in clean.py, lesson_preprocessor.py) assumes that every nb file it sees will be an exercise or a tutorial.
