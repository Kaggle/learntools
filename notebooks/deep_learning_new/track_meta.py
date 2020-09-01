# See also examples/example_track/track_meta.py for a longer, commented example
track = dict(
    author_username='ryanholbrook',
    course_name="Introduction to Deep Learning",
    course_url='https://www.kaggle.com/learn/introduction-to-deep-learning',
    course_forum_url='https://www.kaggle.com/learn-forum',
)

topics = ["A Single Neuron",              # 1
          "Making Networks Deep",         # 2
          "Practical SGD",                # 3
          "Underfitting and Overfitting", # 4
          "Special Layers",               # 5
          "Deep Classifiers",             # 6
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

for nb in notebooks:
    nb['dataset_sources'] = [
        'ryanholbrook/dl-course-data',
    ]

