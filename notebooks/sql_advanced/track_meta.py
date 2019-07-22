# See also examples/example_track/example_meta.py for a longer, commented example
track = dict(
    author_username='dansbecker',
    course_name='SQL',
    course_url='https://www.kaggle.com/learn/advanced-sql'
)

lessons = [ {'topic': topic_name} for topic_name in
                    ['Analytic Functions',
                     'JOINs and UNIONs',
                     ]
            ]

notebooks = [
    dict(
        filename='tut1.ipynb',
        lesson_idx=0,
        type='tutorial',
        dataset_sources = ["datasf/san-francisco"],
        ),
    dict(
        filename='ex1.ipynb',
        lesson_idx=0,
        type='exercise',
        dataset_sources = ["chicago/chicago-taxi-trips-bq"],
        scriptid=-1
        ),
    dict(
        filename='tut2.ipynb',
        lesson_idx=1,
        type='tutorial',
        dataset_sources = ["hacker-news/hacker-news"],
        ),
    dict(
        filename='ex2.ipynb',
        lesson_idx=1,
        type='exercise',
        dataset_sources = ["stackoverflow/stackoverflow"],
        scriptid=-1
        ),
]
