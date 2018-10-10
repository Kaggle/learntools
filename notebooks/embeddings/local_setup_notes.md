# Local setup instructions

(A bit sketchy on some details, these are more intended as a reminder.)

- Make an `input` directory at pwd (`../` with respect to notebooks in `raw/`)
- Download movielens-20m dataset to `input`
- Run `0-movie-preprocessing.ipynb` to generate contents at `../input/movielens_preprocessed`
- Generally kernel output files (which are read by downstream kernels - e.g. serialized models) are written directly to `raw/`, but in kernels, need to be accessed via some `../input/<kernel_name>/___` path.
