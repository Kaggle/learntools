track = dict(
    author_username='residentmario',
    course_name='Pandas',
    course_url='https://www.kaggle.com/learn/pandas'
)

lessons = [ {'topic': topic_name} for topic_name in
                    ['Creating, Reading and Writing',
                     'Indexing, Selecting & Assigning',
                     'Summary Functions and Maps',
                     'Grouping and Sorting',
                     'Data Types and Missing Data',
                     'Renaming and Combining']]
notebooks = [
    dict(
        filename='creating-reading-and-writing.ipynb',
        lesson_idx=0,
        type='exercise',
        scriptid=587970,
        title="Creating, Reading and Writing",
        ),
    dict(
        filename='creating-reading-and-writing-reference.ipynb',
        lesson_idx=0,
        type='tutorial',
        title="Creating, Reading, and Writing reference",
        ),
    dict(
        filename='indexing-selecting-assigning.ipynb',
        lesson_idx=1,
        type='exercise',
        scriptid=587910,
        title='Indexing, Selecting & Assigning',
        ),
    dict(
        filename='indexing-selecting-assigning-reference.ipynb',
        lesson_idx=1,
        type='tutorial',
        title='Indexing, selecting, assigning reference',
        ),
    dict(
        filename='summary-functions-and-maps.ipynb',
        lesson_idx=2,
        type='exercise',
        scriptid=595524,
        title='Summary Functions and Maps',
        ),
    dict(
        filename='summary-functions-and-maps-reference.ipynb',
        lesson_idx=2,
        type='tutorial',
        title="Summary functions and maps reference",
        ),
    dict(
        filename='grouping-and-sorting.ipynb',
        lesson_idx=3,
        type='exercise',
        scriptid=598715,
        title='Grouping and Sorting',
        ),
    dict(
        filename='grouping-and-sorting-reference.ipynb',
        lesson_idx=3,
        type='tutorial',
        title="Grouping and sorting reference",
        ),
    dict(
        filename='data-types-and-missing-data.ipynb',
        lesson_idx=4,
        type='exercise',
        scriptid=598826,
        title='Data Types and Missing Data',
        ),
    dict(
        filename='data-types-and-missing-data-reference.ipynb',
        lesson_idx=4,
        type='tutorial',
        title='Data types and missing data reference'
        ),
    dict(
        filename='renaming-and-combining.ipynb',
        lesson_idx=5,
        type='exercise',
        scriptid=638064,
        title='Renaming and Combining',
        ),
    dict(
        filename='renaming-and-combining-reference.ipynb',
        lesson_idx=5,
        type='tutorial',
        title='Renaming and Combining Reference'
        )
]

for nb in notebooks:
    nb['dataset_sources'] = ['open-powerlifting/powerlifting-database',
                             'residentmario/things-on-reddit',
                             'zynicide/wine-reviews',
                             'jpmiller/publicassistance',
                             'datasnaek/youtube-new'
                             ]
