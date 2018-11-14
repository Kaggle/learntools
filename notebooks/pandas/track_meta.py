track = dict(
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

def _make_notebook(slug, type_, lesson_idx):
    # XXX
    path = os.path.join('old_metadata', slug, 'kernel_metadata.json')
    with open(path) as f:
        ex = json.load(f)

    return dict(
            filename=slug+'.ipynb',
            type=type_,
            lesson_idx=lesson_idx,
            # TODO: Exclude advanced pandas
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

lessons = [
        dict(
            topic='example',
            ),
]

notebooks = [
    dict(
        filename='tut1.ipynb',
        lesson_idx=0,
        type='tutorial',
        scriptid=1,
        ),
    dict(
        filename='ex1.ipynb',
        lesson_idx=0,
        type='exercise',
        scriptid=1,
        ),
]


