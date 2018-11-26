track = dict(
    # Create shadow (private) notebooks under my username for now for testing
    #author_username='colinmorris',
    author_username='residentmario',
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
renaming-and-combining-workbook
method-chaining-reference
method-chaining-workbook""".split()

import os; import json
def _make_notebook(slug, type_, lesson_idx):
    # XXX
    # I guess this is most likely to be run from the notebooks directory, so
    # make path relative to that.
    path = os.path.join('pandas', 'old_metadata', slug, 'kernel-metadata.json')
    with open(path) as f:
        ex = json.load(f)
    
    datasets = ex.get('dataset_sources', [])
    adpan = 'residentmario/advanced-pandas-exercises'
    # The "advanced pandas exercises" dataset is no longer used, but we'll keep
    # using it in all exercise workbooks as a hack to make sure they all have 
    # at least 2 datasets, for consistency of input file paths.
    if type_ == 'exercise' and adpan not in datasets:
        datasets.append(adpan)
        assert len(datasets) >= 2

    return dict(
            filename=slug+'.ipynb',
            type=type_,
            lesson_idx=lesson_idx,
            dataset_sources=ex.get('dataset_sources', []),
            keywords=ex.get('keywords', []),
            title=ex['title'],
            scriptid=ex.get('id_no', -1),
            )

type_order = ['tutorial', 'exercise']
for i in range(0, len(SLUGS), 2):
    slugs = SLUGS[i:i+2]
    slug = slugs[0]
    suff = '-reference'
    if slug.endswith(suff):
        slug = slug[:-len(suff)]
    topic = slug.replace('-', ' ')
    lesson = dict(topic=topic)
    lessons.append(lesson)
    lesson_idx = len(lessons) - 1
    for slug, type_ in zip(slugs, type_order):
        nb = _make_notebook(slug, type_, lesson_idx)
        notebooks.append(nb)

