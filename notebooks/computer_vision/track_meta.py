track = dict(
    author_username='ryanholbrook',
    course_name='Computer Vision',
    course_url='https://www.kaggle.com/ryanholbrook/computer-vision',
    course_forum_url='https://www.kaggle.com/learn-forum',
)

TOPICS = [
    'The Convolutional Classifier',
    'Convolution and ReLU',
    'Maximum Pooling',
    'The Moving Window',
    'Custom Convnets',
    'Data Augmentation',
]


lessons = [{'topic': topic_name} for topic_name in TOPICS]


notebooks = []

for i, _ in enumerate(TOPICS):
    notebooks += [
        dict(
            filename="tut{}.ipynb".format(i+1),
            lesson_idx=i,
            type='tutorial',
            enable_gpu=True,
        ),
    ]

notebooks += [
    dict(
        filename="ex1.ipynb",
        lesson_idx=0,
        type='exercise',
        enable_gpu=True,
    ),
    dict(
        filename="ex2.ipynb",
        lesson_idx=1,
        type='exercise',
    ),
    dict(
        filename="ex3.ipynb",
        lesson_idx=2,
        type='exercise',
    ),
    dict(
        filename="ex4.ipynb",
        lesson_idx=3,
        type='exercise',
    ),
    dict(
        filename="ex5.ipynb",
        lesson_idx=4,
        type='exercise',
        enable_gpu=True,
    ),
    dict(
        filename="ex6.ipynb",
        lesson_idx=5,
        type='exercise',
        enable_gpu=True,
    ),    
]

for nb in notebooks:
    nb['dataset_sources'] = [
        'ryanholbrook/stanford-cars-for-learn',
        'ryanholbrook/computer-vision-resources',
        'ryanholbrook/cv-course-models',
    ]
    nb['kernel_sources'] = [
        'ryanholbrook/visiontools',
        'ryanholbrook/cv-prelude',
    ]

# Add extra datasets to Exercise 6
notebooks[-1]['dataset_sources'] += [
    'ryanholbrook/tensorflow-flowers',    
    'ryanholbrook/eurosat',
]
