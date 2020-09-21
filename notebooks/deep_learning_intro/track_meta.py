# See also examples/example_track/track_meta.py for a longer, commented example
track = dict(
    author_username='ryanholbrook',
    course_name="Introduction to Deep Learning",
    course_url='https://www.kaggle.com/learn/introduction-to-deep-learning',
    course_forum_url='https://www.kaggle.com/learn-forum',
)

TOPICS = ["A Single Neuron",                 # 1
          "Deep Neural Networks",            # 2
          "Stochastic Gradient Descent",     # 3
          "Underfitting and Overfitting",    # 4
          "Dropout and Batch Normalization", # 5
          "Binary Classification",           # 6
          ]
lessons = [{'topic': topic_name} for topic_name in TOPICS]

notebooks = []
GPU_TUTORIAL = []
for i, _ in enumerate(TOPICS):
    notebooks += [
        dict(
            filename="tut{}.ipynb".format(i+1),
            lesson_idx=i,
            type='tutorial',
            enable_gpu=(i+1 in GPU_TUTORIAL),
        ),
    ]

GPU_EXERCISE = [3, 4, 5, 6]
for i, _ in enumerate(TOPICS):
    notebooks += [
        dict(
            filename="ex{}.ipynb".format(i+1),
            lesson_idx=i,
            type='exercise',
            enable_gpu=(i+1 in GPU_EXERCISE),
        ),
    ]

for nb in notebooks:
    nb['dataset_sources'] = [
        'ryanholbrook/dl-course-data',
    ]

