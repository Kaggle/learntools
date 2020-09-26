# See also examples/example_track/track_meta.py for a longer, commented example
track = dict(
    author_username='alexisbcook',
    course_name='Microchallenges',
    course_url='https://www.kaggle.com/learn/microchallenges',
    course_forum_url='https://www.kaggle.com/learn-forum'
)

lessons = [ {'topic': topic_name} for topic_name in
                    ['Blackjack Microchallenge',
                    'Airline Price Optimization Microchallenge',
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
]


