# See also examples/example_track/example_meta.py for a longer, commented example
track = dict(
    author_username='alexisbcook',
    course_name='Geospatial',
    course_url='https://www.kaggle.com/learn/geospatial'
)

lessons = [ {'topic': topic_name} for topic_name in
                    ['Your First Map',
                     'Coordinate Reference Systems',
                     'Interactive Maps',
                     'Manipulating Geospatial Data', 
                     'Proximity Analysis'
                     ]
            ]

notebooks = [
    dict(
        filename='tut1.ipynb',
        lesson_idx=0,
        type='tutorial',
        dataset_sources = ["alexisbcook/geospatial-learn-course-data", "alexisbcook/data-for-datavis"],
        ),
    dict(
        filename='ex1.ipynb',
        lesson_idx=0,
        type='exercise',
        dataset_sources = ["alexisbcook/geospatial-learn-course-data", "alexisbcook/data-for-datavis"],
        scriptid=5822773#5832167
        ),
    dict(
        filename='tut2.ipynb',
        lesson_idx=1,
        type='tutorial',
        dataset_sources = ["alexisbcook/geospatial-learn-course-data", "alexisbcook/data-for-datavis"],
        ),
    dict(
        filename='ex2.ipynb',
        lesson_idx=1,
        type='exercise',
        dataset_sources = ["alexisbcook/geospatial-learn-course-data", "alexisbcook/data-for-datavis"],
        scriptid=5822782#5832146
        ),
    dict(
        filename='tut3.ipynb',
        lesson_idx=2,
        type='tutorial',
        dataset_sources = ["alexisbcook/geospatial-learn-course-data", "alexisbcook/data-for-datavis"],
        ),
    dict(
        filename='ex3.ipynb',
        lesson_idx=2,
        type='exercise',
        dataset_sources = ["alexisbcook/geospatial-learn-course-data", "alexisbcook/data-for-datavis"],
        scriptid=5822780#5832145
        ),
    dict(
        filename='tut4.ipynb',
        lesson_idx=3,
        type='tutorial',
        dataset_sources = ["alexisbcook/geospatial-learn-course-data", "alexisbcook/data-for-datavis"],
        ),
    dict(
        filename='ex4.ipynb',
        lesson_idx=3,
        type='exercise',
        dataset_sources = ["alexisbcook/geospatial-learn-course-data", "alexisbcook/data-for-datavis"],
        scriptid=5822779#5832170
        ),
    dict(
        filename='tut5.ipynb',
        lesson_idx=4,
        type='tutorial',
        dataset_sources = ["alexisbcook/geospatial-learn-course-data", "alexisbcook/data-for-datavis"],
        ),
    dict(
        filename='ex5.ipynb',
        lesson_idx=4,
        type='exercise',
        dataset_sources = ["alexisbcook/geospatial-learn-course-data", "alexisbcook/data-for-datavis"],
        scriptid=5822783#5832141
        ),
]
