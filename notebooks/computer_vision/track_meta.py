track = dict(
    author_username='ryanholbrook',
    course_name='Computer Vision',
    course_url='https://www.kaggle.com/learn/computer-vision',
    course_forum_url='https://www.kaggle.com/learn-forum/196537',
)

TOPICS = [
    'The Convolutional Classifier',
    'Convolution and ReLU',
    'Maximum Pooling',
    'The Sliding Window',
    'Custom Convnets',
    'Data Augmentation',
]


lessons = [{'topic': topic_name} for topic_name in TOPICS]


notebooks = [
    dict(
        filename="tut1.ipynb",
        lesson_idx=0,
        type='tutorial',
        enable_gpu=True,
    ),
    dict(
        filename="ex1.ipynb",
        lesson_idx=0,
        type='exercise',
        enable_gpu=True,
        scriptid=10781907
    ),
    dict(
        filename="tut2.ipynb",
        lesson_idx=1,
        type='tutorial',
    ),
    dict(
        filename="ex2.ipynb",
        lesson_idx=1,
        type='exercise',
        scriptid=11989557
    ),
    dict(
        filename="tut3.ipynb",
        lesson_idx=2,
        type='tutorial',
    ),
    dict(
        filename="ex3.ipynb",
        lesson_idx=2,
        type='exercise',
        scriptid=11989559
    ),
    dict(
        filename="tut4.ipynb",
        lesson_idx=3,
        type='tutorial',
    ),
    dict(
        filename="ex4.ipynb",
        lesson_idx=3,
        type='exercise',
        scriptid=12400209
    ),
    dict(
        filename="tut5.ipynb",
        lesson_idx=4,
        type='tutorial',
        enable_gpu=True,
    ),
    dict(
        filename="ex5.ipynb",
        lesson_idx=4,
        type='exercise',
        enable_gpu=True,
        scriptid=11989565
    ),
    dict(
        filename="tut6.ipynb",
        lesson_idx=5,
        type='tutorial',
        enable_gpu=True,
    ), 
    dict(
        filename="ex6.ipynb",
        lesson_idx=5,
        type='exercise',
        enable_gpu=True,
        scriptid=11991328
    ),  
]

for nb in notebooks:
    nb['dataset_sources'] = [
        'ryanholbrook/car-or-truck',
        'ryanholbrook/computer-vision-resources',
        'ryanholbrook/cv-course-models',
        ]

    # Add extra datasets to Exercise 6
    if '6' in nb['filename']:
        nb['dataset_sources'] += [
            'ryanholbrook/tensorflow-flowers', 
            'ryanholbrook/eurosat',
            ]
