# See also examples/example_track/track_meta.py for a longer, commented example
track = dict(
    author_username='alexisbcook',
    course_name='AI Ethics',
    course_url='https://www.kaggle.com/learn/ai-ethics',
    course_forum_url='https://www.kaggle.com/learn-forum',
)

TOPICS = [
    'Bias',
]

lessons = [{'topic': topic_name} for topic_name in TOPICS]

notebooks = [
    dict(
        filename='tut.ipynb',
        lesson_idx=0,
        type='tutorial',
        ),
    dict(
        filename='ex.ipynb',
        lesson_idx=0,
        type='exercise',
        scriptid=1,
        competition_sources='jigsaw-unintended-bias-in-toxicity-classification'
        ),
]
