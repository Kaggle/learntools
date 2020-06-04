# See also examples/example_track/track_meta.py for a longer, commented example
track = dict(
    author_username='ryanholbrook',
    course_name='Computer Vision',
    course_url='https://www.kaggle.com/ryanholbrook/computer-vision'
)

lessons = [
    {'topic': topic_name} for topic_name in
    [
        'The Convolutional Classifier',
        'Convnet Architecture',
        'Filter, Detect, Condense',
        # 'Convolution and Pooling',
        # 'Exploring Convnets',
        # 'Transfer Learning',
        # 'Data Augmentation',
     ]
]

notebooks = [
    dict(
        filename='tut1.ipynb',
        lesson_idx=0,
        type='tutorial',
    ),
    dict(
        filename='tut2.ipynb',
        lesson_idx=1,
        type='tutorial',
    ),
    dict(
        filename='tut3.ipynb',
        lesson_idx=2,
        type='tutorial',
    ),
]

for nb in notebooks:
    nb['dataset_sources'] = [
        "ryanholbrook/stanford-cars-for-learn",
        "ryanholbrook/saved-models",
    ]
