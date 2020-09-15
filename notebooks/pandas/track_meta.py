track = dict(
    author_username='residentmario',
    course_name='Pandas',
    course_url='https://www.kaggle.com/learn/pandas',
    course_forum_url='https://www.kaggle.com/learn-forum/161299'
)

lessons = []
notebooks = []
lessons = [ {'topic': topic_name} for topic_name in
                    ["Creating, Reading and Writing",
                    "Indexing, Selecting & Assigning",
                    "Summary Functions and Maps",
                    "Grouping And Sorting",
                    "Data Types And Missing Values",
                    "Renaming and Combining",
                    ]
        ]

notebooks = [
    dict(
        filename='tut_0.ipynb',
        lesson_idx=0,
        type='tutorial',
        scriptid=550418
        ),
    dict(
        filename='ex_0.ipynb',
        lesson_idx=0,
        type='exercise',
        scriptid=587970
    ),
    dict(
        filename='tut_1.ipynb',
        lesson_idx=1,
        type='tutorial',
        scriptid=582111
    ),
    dict(
        filename='ex_1.ipynb',
        lesson_idx=1,
        type='exercise',
        scriptid=587910
    ),
    dict(
        filename='tut_2.ipynb',
        lesson_idx=2,
        type='tutorial',
        scriptid=595033
    ),
    dict(
        filename='ex_2.ipynb',
        lesson_idx=2,
        type='exercise',
        scriptid=595524
    ),
    dict(
        filename='tut_3.ipynb',
        lesson_idx=3,
        type='tutorial',
        scriptid=598164
        ),
    dict(
        filename='ex_3.ipynb',
        lesson_idx=3,
        type='exercise',
        scriptid=598715
        ),
    dict(
        filename='tut_4.ipynb',
        lesson_idx=4,
        type='tutorial',
        scriptid=598827
        ),
    dict(
        filename='ex_4.ipynb',
        lesson_idx=4,
        type='exercise',
        scriptid=598826
        ),
    dict(
        filename='tut_5.ipynb',
        lesson_idx=5,
        type='tutorial',
        scriptid=636767
        ),
    dict(
        filename='ex_5.ipynb',
        lesson_idx=5,
        type='exercise',
        scriptid=638064
        ),
]

for nb in notebooks:
    nb['dataset_sources'] = \
                ['zynicide/wine-reviews',
                'nolanbconaway/pitchfork-data',
                'dansbecker/powerlifting-database',
                'residentmario/things-on-reddit',
                'jpmiller/publicassistance',
                'rtatman/188-million-us-wildfires',
                'residentmario/ramen-ratings',
                'datasnaek/chess',
                'nasa/kepler-exoplanet-search-results',
                'datasnaek/youtube-new',
                ]
