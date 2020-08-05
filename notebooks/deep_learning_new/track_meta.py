# See also examples/example_track/track_meta.py for a longer, commented example
track = dict(
    author_username='ryanholbrook',
    course_name="Introduction to Deep Learning",
    course_url='https://www.kaggle.com/learn/introduction-to-deep-learning',
    course_forum_url='https://www.kaggle.com/learn-forum',
)

topics = ["Linear Regression as a Neural Network", # 1
          "Making Models Deep",                    # 2
          "Practical SGD",                         # 3
          "Overfitting and Underfitting",          # 4
          "Improving Optimization",                # 5
          # "Deep Classifiers",                      # 6
          ]

lessons = [{'topic': topic_name} for topic_name in topics]

notebooks = []
for i, _ in enumerate(topics):
    notebooks += [
        dict(
            filename="tut{}.ipynb".format(i+1),
            lesson_idx=i,
            type='tutorial',
        ),
    ]

