track = dict(
    author_username='residentmario',
    course_name='Pandas',
    course_url='https://www.kaggle.com/learn/pandas'
)

lessons = []
notebooks = []

SLUGS = """creating-reading-and-writing-reference
creating-reading-and-writing-workbook
indexing-selecting-assigning-reference
indexing-selecting-assigning
summary-functions-and-maps-reference
summary-functions-and-maps-workbook
grouping-and-sorting-reference
grouping-and-sorting
data-types-and-missing-data-reference
data-types-and-missing-data-workbook
renaming-and-combining-reference
renaming-and-combining-workbook""".split()

datasets = ['zynicide/wine-reviews',
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

import os; import json
def _make_notebook(slug, type_, lesson_idx):
    path = os.path.join('pandas', 'old_metadata', slug, 'kernel-metadata.json')
    with open(path) as f:
        ex = json.load(f)
    return dict(
            filename=slug+'.ipynb',
            type=type_,
            lesson_idx=lesson_idx,
            dataset_sources=datasets,
            title=ex['title'],
            scriptid=ex.get('id_no', -1),
            )

type_order = ['tutorial', 'exercise']
for i in range(0, len(SLUGS), 2):
    slugs = SLUGS[i:i+2]
    tut_slug = slugs[0]
    suff = '-reference'
    if tut_slug.endswith(suff):
        tut_slug = slug[:-len(suff)]
    topic = tut_slug.replace('-', ' ')
    lesson = dict(topic=topic)
    lessons.append(lesson)
    lesson_idx = len(lessons) - 1
    for slug, type_ in zip(slugs, type_order):
        nb = _make_notebook(slug, type_, lesson_idx)
        notebooks.append(nb)
