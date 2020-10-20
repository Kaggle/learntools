track = dict(
    author_username='ryanholbrook',
    course_name="Intro to Deep Learning",
    course_url='https://www.kaggle.com/learn/intro-to-deep-learning',
    course_forum_url='https://www.kaggle.com/learn-forum/191966',
)

TOPICS = ["A Single Neuron",                      # 1
          "Deep Neural Networks",                 # 2
          "Stochastic Gradient Descent",          # 3
          "Overfitting and Underfitting",         # 4
          "Dropout and Batch Normalization",      # 5
          "Binary Classification",                # 6
          "Detecting the Higgs Boson with TPUs",  # 7
          ]
lessons = [{'topic': topic_name} for topic_name in TOPICS]

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
        scriptid=11887334
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
        scriptid=11887344
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
        scriptid=11887330,
        enable_gpu=True
    ),
    dict(
        filename='tut4.ipynb',
        lesson_idx=3,
        type='tutorial'
    ),
    dict(
        filename='ex4.ipynb',
        lesson_idx=3,
        type='exercise',
        scriptid=11906770,
        enable_gpu=True
    ),
    dict(
        filename='tut5.ipynb',
        lesson_idx=4,
        type='tutorial'
        ),
    dict(
        filename='ex5.ipynb',
        lesson_idx=4,
        type='exercise',
        scriptid=11887342,
        enable_gpu=True
        ),
    dict(
        filename='tut6.ipynb',
        lesson_idx=5,
        type='tutorial'
        ),
    dict(
        filename='ex6.ipynb',
        lesson_idx=5,
        type='exercise',
        scriptid=11887335,
        enable_gpu=True
        ),
    dict(
        filename='tut_tpus.ipynb',
        lesson_idx=6,
        type='tutorial'
        ),
]

for nb in notebooks:
    if nb['filename'] != "tut_tpus.ipynb":
        nb['dataset_sources'] = ['ryanholbrook/dl-course-data']
    else:
        nb['dataset_sources'] = ['ryanholbrook/higgs-boson']
    
