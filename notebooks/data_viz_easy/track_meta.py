# See also examples/example_track/track_meta.py for a longer, commented example
track = dict(
    author_username='alexisbcook',
    course_name="Data Visualization Made Easy",
    course_url="..."
)

lessons = [{'topic': topic_name} for topic_name in
            ['Introduction and Line Plots',
            'Bar Plots and Heatmaps']
            ]

notebooks = [
    dict(
        filename='ex1.ipynb',
        lesson_idx=0,
        type='exercise',
        ),
    dict(
        filename='ex2.ipynb',
        lesson_idx=1,
        type='exercise',
        ),
]


