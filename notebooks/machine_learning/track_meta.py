# See also examples/example_track/example_meta.py for a longer, commented example
track = dict(
    author_username='dansbecker',
)

lessons = [
        dict(topic='How Models Work'),
        dict(topic='Explore Your Data')
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
        scriptid=1258954        
    )
]
