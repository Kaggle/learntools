# See also examples/example_track/track_meta.py for a longer, commented example
track = dict(
    author_username='dansbecker',
    course_name='Microchallenges',
    course_url='https://www.kaggle.com/learn/microchallenges'
)

lessons = [ {'topic': topic_name} for topic_name in
                    ['Blackjack Microchallenge',
                    'Airline Price Optimization Microchallenge',
                    ]

notebooks = [
    dict(
        filename='ex1.ipynb',
        lesson_idx=0,
        type='exercise',
        scriptid=1,
        ),
    dict(
        filename='ex2.ipynb',
        lesson_idx=1,
        type='exercise',
        scriptid=1,
        ),
]


