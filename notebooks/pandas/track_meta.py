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
        ),
    dict(
        filename='creating-reading-and-writing-reference.ipynb',
        lesson_idx=0,
        type='tutorial',
        title="Creating, reading, and writing reference",
        ),
    dict(
        filename='indexing-selecting-assigning.ipynb',
        lesson_idx=1,
        type='exercise',
        scriptid=587910,
        ),
    dict(
        filename='indexing-selecting-assigning-reference.ipynb',
        lesson_idx=1,
        type='tutorial',
        title='Indexing, selecting, assigning reference'
        ),
    dict(
        filename='summary-functions-and-maps.ipynb',
        lesson_idx=2,
        type='exercise',
        scriptid=595524,
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
        ),
    dict(
        filename='renaming-and-combining-reference.ipynb',
        lesson_idx=5,
        type='tutorial',
        title='Renaming and combining reference'
        )
]

for nb in notebooks:
    nb['dataset_sources'] = ['nolanbconaway/pitchfork-data',
                             'open-powerlifting/powerlifting-database',
                             'residentmario/things-on-reddit',
                             'residentmario/advanced-pandas-exercises',
                             'zynicide/wine-reviews',
                             'jpmiller/publicassistance',
                             'datasnaek/youtube-new'
                             ],
