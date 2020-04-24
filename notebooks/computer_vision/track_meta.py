# See also examples/example_track/track_meta.py for a longer, commented example
track = dict(
    author_username='ryanholbrook',
    course_name='computer_vision',
    course_url='https://www.kaggle.com/ryanholbrook/computer-vision'
)

lessons = [
        dict(
            # By convention, this should be a lowercase noun-phrase.
            topic='First Notebook',
            ),
]

notebooks = [
    dict(
        filename='computer_vision.ipynb',
        lesson_idx=0,
        type='tutorial',
        scriptid=1,
        ),
]

for nb in notebooks:
    nb['dataset_sources'] = ["ryanholbrook/stanford-cars-for-learn"]


