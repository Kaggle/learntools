# See also examples/example_track/example_meta.py for a longer, commented example
track = dict(
    author_username='alexisbcook',
    course_name='Intro to Game AI and Reinforcement Learning',
    course_url='https://www.kaggle.com/learn/intro-to-game-ai-and-reinforcement-learning'
)

lessons = [ {'topic': topic_name} for topic_name in
                    ["Play the Game",
                     "One-Step Lookahead",
                     "N-Step Lookahead",
                     "Deep Reinforcement Learning"
                     ]
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
        scriptid=7677818
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
        scriptid=8139646
        ),
    dict(
        filename='tut3.ipynb',
        lesson_idx=2,
        type='tutorial',
        ),
    dict(
        filename='ex3.ipynb',
        lesson_idx=2,
        type='exercise',
        scriptid=8139647
        ),
    dict(
        filename='tut4.ipynb',
        lesson_idx=3,
        type='tutorial',
        ),
    dict(
        filename='ex4.ipynb',
        lesson_idx=3,
        type='exercise',
        scriptid=8222487
        ),
]

for nb in notebooks:
    nb['competition_sources'] = ["connectx"]