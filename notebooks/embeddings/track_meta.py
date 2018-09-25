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

