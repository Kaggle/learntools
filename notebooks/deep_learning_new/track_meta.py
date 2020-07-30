# See also examples/example_track/track_meta.py for a longer, commented example
track = dict(
    author_username='ryanholbrook',
    course_name="Introduction to Deep Learning",
    course_url='https://www.kaggle.com/learn/introduction-to-deep-learning',
    course_forum_url='https://www.kaggle.com/learn-forum',
)

lessons = [ {'topic': topic_name} for topic_name in
            ["Linear Regression as a Neural Network", # 1
             # "Making Models Deep",                    # 2
             # "Practical SGD",                         # 3
             # "Overfitting and Underfitting",          # 4
             # "Improving Optimization",                # 5
             # "Deep Classifiers",                      # 6
            ]
]

notebooks = [
    dict(
        filename='tut1.ipynb',
        lesson_idx=0,
        type='tutorial',
        ),
    # dict(
    #     filename='ex1.ipynb',
    #     lesson_idx=0,
    #     type='exercise',
    #     scriptid=1,
    #     ),
]


