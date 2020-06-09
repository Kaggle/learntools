# See also examples/example_track/track_meta.py for a longer, commented example
track = dict(
    author_username='ryanholbrook',
    course_name='Computer Vision',
    course_url='https://www.kaggle.com/ryanholbrook/computer-vision',
)

TOPICS = [
    ('The Convolutional Classifier', 1),
    ('Convnet Architecture', 2),
    ('Filter, Detect, Condense', 3),
    ('Convolution and Pooling', 4),
    # ('Exploring Convnets', 5),
    ('Transfer Learning', 6),
    ('Data Augmentation', 7),
]


lessons = [{'topic': topic_name} for topic_name, _ in TOPICS]


notebooks = []

for _, i in TOPICS:
    notebooks.append(
        dict(
            filename="tut{}.ipynb".format(i),
            lesson_idx=i-1,
            type='tutorial',
        )
    )

for nb in notebooks:
    nb['dataset_sources'] = [
        "ryanholbrook/stanford-cars-for-learn",
        "ryanholbrook/computer-vision-resources",
    ]
