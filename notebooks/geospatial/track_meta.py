# See also examples/example_track/example_meta.py for a longer, commented example
track = dict(
    author_username='alexisbcook',
    course_name='Geospatial Analysis',
    course_url='https://www.kaggle.com/learn/geospatial-analysis',
    course_forum_url='https://www.kaggle.com/learn-forum/161464'
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
        scriptid=5832167#5822773#
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
        scriptid=5832146#5822782#
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
        scriptid=5832145#5822780#
        ),
    dict(
        filename='tut4.ipynb',
        lesson_idx=3,
        type='tutorial',
        dataset_sources = ["alexisbcook/geospatial-learn-course-data", "alexisbcook/data-for-datavis"],
        enable_internet=True
        ),
    dict(
        filename='ex4.ipynb',
        lesson_idx=3,
        type='exercise',
        dataset_sources = ["alexisbcook/geospatial-learn-course-data", "alexisbcook/data-for-datavis"],
        scriptid=5832170#5822779#
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
        scriptid=5832147#5822783#
        ),
]
