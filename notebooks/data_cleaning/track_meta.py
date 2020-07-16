track = dict(
    author_username='rtatman',
    course_name='Data Cleaning',
    course_url='https://www.kaggle.com/learn/data-cleaning',
    course_forum_url='https://www.kaggle.com/learn-forum'
)

lessons = [ {'topic': topic_name} for topic_name in
                    ['Handling missing values',    #1
                     'Scaling and normalization',  #2
                     'Parsing dates',              #3
                     'Character encodings',        #4
                     'Inconsistent data entry']    #5
            ]

notebooks = [
    dict(
        filename='tut1.ipynb',
        lesson_idx=0,
        type='tutorial',
        dataset_sources=['maxhorowitz/nflplaybyplay2009to2016', 'aparnashastry/building-permit-applications-data']
        ),
    dict(
        filename='ex1.ipynb',
        lesson_idx=0,
        type='exercise',
        scriptid=-1
    ),
    dict(
        filename='tut2.ipynb',
        lesson_idx=1,
        type='tutorial',
        dataset_sources=['aaronschlegel/seattle-pet-licenses', 'kemical/kickstarter-projects']
        ),
    dict(
        filename='ex2.ipynb',
        lesson_idx=1,
        type='exercise',
        scriptid=-1
    ),
    dict(
        filename='tut3.ipynb',
        lesson_idx=2,
        type='tutorial',
        dataset_sources=['nasa/landslide-events', 'usgs/earthquake-database', 'smithsonian/volcanic-eruptions']
    ),
    dict(
        filename='ex3.ipynb',
        lesson_idx=2,
        type='exercise',
        scriptid=-1
    ),
    dict(
        filename='tut4.ipynb',
        lesson_idx=3,
        type='tutorial',
        dataset_sources=['kemical/kickstarter-projects', 'kwullum/fatal-police-shootings-in-the-us']
    ),
    dict(
        filename='ex4.ipynb',
        lesson_idx=3,
        type='exercise',
        scriptid=-1
    ),
    dict(
        filename='tut5.ipynb',
        lesson_idx=4,
        type='tutorial',
        dataset_sources=['zusmani/pakistansuicideattacks']
        ),
    dict(
        filename='ex5.ipynb',
        lesson_idx=4,
        type='exercise',
        scriptid=-1
        ),
]