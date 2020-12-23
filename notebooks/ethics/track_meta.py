# See also examples/example_track/track_meta.py for a longer, commented example
track = dict(
    author_username='alexisbcook',
    course_name='AI Ethics',
    course_url='https://www.kaggle.com/learn/ai-ethics',
    course_forum_url='https://www.kaggle.com/learn-forum',
)

lessons = [ {'topic': topic_name} for topic_name in
                    ["Introduction to AI Ethics",
                     "Human-Centered Design",
                     "Identifying Bias",
                     "Fairness",
                     "Model Cards"
                     ]
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
        scriptid=-1
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
        scriptid=-1
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
        scriptid=-1,
        competition_sources='jigsaw-unintended-bias-in-toxicity-classification'
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
        scriptid=-1
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
        scriptid=-1
        ),
]
