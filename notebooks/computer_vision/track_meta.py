track = dict(
    author_username='ryanholbrook',
    course_name='Computer Vision',
    course_url='https://www.kaggle.com/ryanholbrook/computer-vision',
)

TOPICS = [
    'The Convolutional Classifier',
    'Convolution and ReLU',
    'Convolution and Moving Windows',
    'Maximum Pooling',
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
        ),
        # dict(
        #     filename="ex{}.ipynb".format(i+1),
        #     lesson_idx=i,
        #     type='exercise',
        #     scriptid=____,
        # ),
    ]

for nb in notebooks:
    nb['dataset_sources'] = [
        'ryanholbrook/stanford-cars-for-learn',
        'ryanholbrook/computer-vision-resources',
        'ryanholbrook/cv-course-models',
    ]
    nb['kernel_sources'] =[
        'ryanholbrook/visiontools',
    ]
