# See also examples/example_track/track_meta.py for a longer, commented example
track = dict(
    author_username='alexisbcook',
    course_name='Data Visualization Made Easy',
    course_url='...'
)

lessons = [{'topic': topic_name} for topic_name in
            ['Introduction and Line Plots',
            'Bar Plots and Heatmaps',
            'Scatter Plots',
            'Distributions',
            'Choosing Plot Types and Customizing Style',
            'Final Project',]
            ]

notebooks = [
    dict(
        filename='tut1.ipynb',
        lesson_idx=0,
        type='tutorial',
        ),
    dict(
        filename='ex1.ipynb',
        lesson_idx=0,
        type='exercise',
        ),
    dict(
        filename='tut2.ipynb',
        lesson_idx=1,
        type='tutorial',
        ),
    dict(
        filename='ex2.ipynb',
        lesson_idx=1,
        type='exercise',
        ),
    dict(
        filename='tut3.ipynb',
        lesson_idx=2,
        type='tutorial',
        ),
    dict(
        filename='ex3.ipynb',
        lesson_idx=2,
        type='exercise',
        ),
    dict(
        filename='tut4.ipynb',
        lesson_idx=3,
        type='tutorial',
        ),
    dict(
        filename='ex4.ipynb',
        lesson_idx=3,
        type='exercise',
        ),
    dict(
        filename='tut5.ipynb',
        lesson_idx=4,
        type='tutorial',
        ),
    dict(
        filename='ex5.ipynb',
        lesson_idx=4,
        type='exercise',
        ),
    dict(
        filename='tut6.ipynb',
        lesson_idx=5,
        type='tutorial',
        ),
    dict(
        filename='ex6.ipynb',
        lesson_idx=5,
        type='exercise',
        ),
]



