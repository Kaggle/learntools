# See also examples/example_track/example_meta.py for a longer, commented example
track = dict(
    author_username='dansbecker',
)

lessons = [
        dict(topic='how models work'),
        dict(topic='exploring your data'),
        dict(topic='building your first machine learning model'),
]

notebooks = [
    dict(
        filename='tut1.ipynb',
        lesson_idx=0,
        type='tutorial',
	    dataset_sources= ["dansbecker/melbourne-housing-snapshot"],
	    competition_sources=["home-data-for-ml-course"],
        ),
    dict(
        filename='tut2.ipynb',
        lesson_idx=1,
        type='tutorial',
	    dataset_sources= ["dansbecker/melbourne-housing-snapshot"],
	    competition_sources=["home-data-for-ml-course"],
        ),
    dict(
        filename='ex2.ipynb',
        lesson_idx=1,
        type='exercise',
	    dataset_sources= ["dansbecker/melbourne-housing-snapshot"],
	    competition_sources=["home-data-for-ml-course"],
        scriptid=1258954,
    ),
    dict(
        filename='tut3.ipynb',
        lesson_idx=2,
        type='tutorial',
	    dataset_sources= ["dansbecker/melbourne-housing-snapshot"],
	    competition_sources=["home-data-for-ml-course"],
        ),
    dict(
        filename='ex3.ipynb',
        lesson_idx=2,
        type='exercise',
	    dataset_sources= ["dansbecker/melbourne-housing-snapshot"],
	    competition_sources=["home-data-for-ml-course"],
        scriptid=1,
    ),
]
