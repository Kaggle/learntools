# See also examples/example_track/example_meta.py for a longer, commented example
track = dict(
    author_username='dansbecker',
    course_name='Machine Learning Explainability',
    course_url='https://www.kaggle.com/learn/machine-learning-explainability',
    course_forum_url='https://www.kaggle.com/learn-forum/161307'
)

lessons = [ {'topic': topic_name} for topic_name in
                    ['Use Cases for Model Insights',
                    'Permutation Importance',
                    'Partial Plots',
                    'SHAP Values',
                    'Advanced Uses of SHAP Values'
                    ]
            ]

notebooks = [
    dict(
        filename='tut1_intro.ipynb',
        lesson_idx=0,
        type='tutorial',
        ),
    dict(
        filename='tut2_perm_importance.ipynb',
        lesson_idx=1,
        type='tutorial',
        ),
    dict(
        filename='ex2_perm_importance.ipynb',
        lesson_idx=1,
        type='exercise',
        scriptid=1637562
    ),
    dict(
        filename='tut3_partial_plots.ipynb',
        lesson_idx=2,
        type='tutorial'
    ),
    dict(
        filename='ex3_partial_plots.ipynb',
        lesson_idx=2,
        type='exercise',
        scriptid=1637380
    ),
    dict(
        filename='tut4_shap_basic.ipynb',
        lesson_idx=3,
        type='tutorial'
    ),
    dict(
        filename='ex4_shap_basic.ipynb',
        lesson_idx=3,
        type='exercise',
        scriptid=1637226,
        enable_internet=True
    ),
    dict(
        filename='tut5_shap_advanced.ipynb',
        lesson_idx=4,
        type='tutorial'
        ),
    dict(
        filename='ex5_shap_advanced.ipynb',
        lesson_idx=4,
        type='exercise',
        scriptid=1699743
        )
]

for nb in notebooks:
    nb['dataset_sources'] =  [
    "mathan/fifa-2018-match-statistics",
    "dansbecker/hospital-readmissions",
    "dansbecker/new-york-city-taxi-fare-prediction",
  ]

