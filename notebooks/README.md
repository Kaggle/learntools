The 'notebook pipeline' in this directory is a pseudo templating system with kaggle kernels API integration.

## Directory structure

To start a new track (i.e. a themed sequence of notebooks such as are found on the Kaggle Learn homepage, or in Kaggle Learn Challenges) called "spam", run `new_track.sh spam`. This will create a `spam/` subdirectory, with the following contents:

```
raw/
__init__.py
track_meta.py
default.yaml
```

`raw/` is where the notebooks you author should go. These will be straightforward ipynb notebooks which (perhaps with some setup such as downloading necessary datasets, installing libraries, and careful path manipulation) may be runnable locally. However, they're *also* recipes for generating ipynb notebooks.

`track_meta.py` defines some metadata, mostly about the notebooks you'll be syncing. A notebook in the `raw/` subdirectory will only be rendered (and have a `kernel-metadata.json` file generated) if it has an entry in `track_meta.py`. (This means you're welcome to put as many throwaway testing notebooks as you like in `raw` without worrying about them breaking anything.)
See `examples/example_track/track_meta.py` for an exhaustively commented example.

`default.yaml` is a config file specifying one way to build our raw notebooks into kernels. Whereas `track_meta.py` deals wit the "what", this config file deals more with the "how". A single track may have many config files, each of which may generate a distinct set of kernels.

Once you've created some raw notebooks and run the pipeline (more on that below), your directory structure will look like:

```
raw/
default/
    rendered/
    kernels_api_metadata/
__init__.py
track_meta.py
default.yaml
```

`rendered/` is where the notebooks generated from the `raw/` recipes go. These are what get synced to Kaggle Kernels. You should not edit these directly (treat them as build products).

`kernels_api_metadata/` contains `kernel-metadata.json` files for syncing notebooks to Kaggle Kernels via the API.

If you create further config files (e.g. `testing.yaml`), they will generate their own analogous subdirectories (e.g. `testing/rendered/`, `testing/kernels_api_metadata/`).

# Pipeline steps

## Step 1: Prepare Push

`prepare_push.py` translates notebooks in `raw/` to publishable notebooks in `rendered/`.
The logic for this step mostly lives in `lesson_preprocessor.py`. Most of its work is in expanding macros which look like `#$HIDE_OUTPUT$`, or `#$EXERCISE_URL(2)$`. See MACROS.txt for a listing of available macros.

The Kaggle Kernels API requires a `kernel-metadata.json` file for any kernel being pushed to the site. `prepare_push.py` also generates these in the `kernels_api_metadata` subdirectory. 

## Step 2: Pushing

Use ./pushall.sh as
    ./pushall deep_learning/prod

Changes to the functionality of this pipeline happen by modifying the nb_utils folder.
