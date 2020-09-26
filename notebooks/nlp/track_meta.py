# See also examples/example_track/example_meta.py for a longer, commented example
track = dict(
    author_username='matleonard',
    course_name='Natural Language Processing',
    course_url='https://www.kaggle.com/learn/natural-language-processing',
    course_forum_url='https://www.kaggle.com/learn-forum/161466'
)

lessons = [ {'topic': topic_name} for topic_name in
                    ['Intro to NLP',
                    'Text Classification',
                    'Word Vectors']
            ]

notebooks = [
    dict(
        filename='tut1.ipynb',
        lesson_idx=0,
        type='tutorial',
        ),
    dict(
        filename='ex1.ipynb',
        lesson_idx=0,
        type='exercise',
        scriptid=6061023
    ),
    dict(
        filename='tut2.ipynb',
        lesson_idx=1,
        type='tutorial',
        ),
    dict(
        filename='ex2.ipynb',
        lesson_idx=1,
        type='exercise',
        scriptid=6061027
    ),
    dict(
        filename='tut3.ipynb',
        lesson_idx=2,
        type='tutorial'
    ),
    dict(
        filename='ex3.ipynb',
        lesson_idx=2,
        type='exercise',
        scriptid=6061026
    ),
]

for nb in notebooks:
    nb['dataset_sources'] = ["matleonard/nlp-course", 
                             "alexisbcook/geospatial-learn-course-data"]
