track = dict(
    author_username='colinmorris',
    # Keys below are all optional
    course_name='Examples',
    course_url='https://www.kaggle.com/learn/example',
    enable_gpu=True, # Default false
)

# This track consists of two lessons (1 having a tutorial and an exercise,
# and the other having just a tutorial)
lessons = [
        dict(
            # By convention, this should be a lowercase noun-phrase. Macros will
            # use this in constructions like...
            # > Click here to move on to the next lesson on ${lesson.topic}.
            topic='example things',
            ),
        dict(
            topic='advanced examples',
        ),
]

# Metadata for any notebooks in this track that are to be preprocessed and 
# synced to Kaggle. 
# partials/ may contain other notebooks (e.g. tut2-scratch.ipynb in the case of 
# example_track). They'll just be ignored by render.py, prepare_push.py, etc.
notebooks = [
    dict(
        filename='tut1-hello.ipynb',
        type='tutorial',
        # This tutorial corresponds to our first lesson (on the topic of 'example things')
        lesson_idx=0,
        # In addition to setting this at the track level, we can override it
        # on a per-notebook basis.
        enable_gpu=False,
        ),
    dict(
        filename='ex1-hello.ipynb',
        type='exercise',
        lesson_idx=0,
        # If not specified, scriptid takes on a dummy default value of 1, which
        # means auto-generated forking links will not work.
        scriptid=123,
    ),
    dict(
        filename='tut2.ipynb',
        type='tutorial',
        lesson_idx=1,
        # This kernel uses the tutorial 1 kernel as a data source. If we knew tutorial
        # 1's slug ahead of time, we could have also specified the dependency using that
        # slug, e.g 'colinmorris/example-things'. 
        kernel_sources=['tut1-hello.ipynb'],
    ),
    dict(
        filename='appendix.ipynb',
        # Neither a tutorial nor exercise. Maybe this is a notebook with some extra 
        # examples or explanation to supplement a tutorial. It may also exist to do
        # some preprocessing or model training to generate files which are used as
        # a data source by a tutorial or exercise.
        type='extra',
        # The title field is optional for tutorials and exercises. If not explicitly
        # provided, tutorial titles are the corresponding lesson topic in title case.
        # Exercises are the same, but with an "Exercise: " prefix.
        # For 'extra' notebooks, title is mandatory.
        title='Appendix I',
    ),
]


