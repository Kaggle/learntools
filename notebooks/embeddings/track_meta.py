track = dict(
    author_username='colinmorris',
)

lessons = [
        dict(topic='embedding layers',),
        dict(topic='matrix factorization',),
        dict(topic='exploring embeddings with gensim',),
        dict(topic='visualizing embeddings with t-SNE',),
]

_tut_names = ['embeddings', 'factorization', 'gensim', 'tsne']
_tuts = [dict(lesson_idx=i, type='tutorial', 
                filename='{}-{}.ipynb'.format(i+1, name))
        for i, name in enumerate(_tut_names)
        ]

# TODO: scriptids
_exercise_scriptids = [1 for _ in range(len(lessons))]
_exs = [dict(lesson_idx=i, type='exercise', scriptid=sid,
            filename='{}-exercises.ipynb'.format(i+1)) 
        for i, sid in enumerate(_exercise_scriptids)
        ]

notebooks = _tuts + _exs

# Adding data sources
_common_kernel_source_slug = 'colinmorris/0-movielens-preprocessing'
for nb in notebooks:
    nb['kernel_sources'] = [_common_kernel_source_slug]

_exs[1]['kernel_sources'].append('colinmorris/x2-movielens-factorization-r12n')

_nice_model_slug = 'colinmorris/x3-movielens-spiffy-model'
for nb_list, indices in zip( [_tuts, _exs], [ [2, 3], [2] ] ):
    for idx in indices:
        nb_list[idx]['kernel_sources'].append(_nice_model_slug)

# Inter-kernel dependencies
_kernel_to_kernel_deps = [
        (_tuts[1], _tuts[0]),
        (_exs[1], _tuts[1]),
        (_exs[3], _tuts[3]),
]
for nb, src in _kernel_to_kernel_deps:
    # We might not know a notebook's slug at this point, so encode a dependency
    # using the filename, which will be resolved to a slug later (in track_metadata.py)
    nb['kernel_sources'].append(src['filename'])

# Kernels which aren't tutorials or exercises, but serve as data sources for 
# tut/ex kernels, and therefore still need to be synced to kaggle.
_ancillaries = [
        dict(
            title='0 movielens preprocessing',
            filename='0-movie-preprocessing.ipynb',
            dataset_sources=['grouplens/movielens-20m-dataset'],
            ),
        dict(
            title='x2 movielens factorization r12n',
            filename='x2-movielens-factorization-r12n.ipynb',
            kernel_sources = [_common_kernel_source_slug],
        ),
        dict(
            title='x3 movielens spiffy model',
            filename='x3-movielens-spiffy-model.ipynb',
            kernel_sources = [_common_kernel_source_slug],
        )
]

notebooks = _tuts + _exs + _ancillaries
