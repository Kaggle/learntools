"""
lessons_meta: list of lesson dicts

lesson has fields:
    topic: str
    exercise: notebook dict
    tutorial: notebook dict

notebook has fields:
    scriptid: kaggle numerical kernel identifier thing
    slug: e.g. 'colinmorris/hello-python'
    title
    filename: the name of the corresponding ipynb file (which should be in current directory) 

scriptid is used in macro expansion to generate forking links (and so it's okay to use a
a placeholder to get started).

slug, title, and filename are used in generating kernel metadata files for the kernels API
(see prepare_push.py)
"""

# (Cribbed from ../python. With some updates and documentation above.)
lessons_meta = [
        # NB: Kind of an ugly ouroboros bootstrapping process here where we need some version of this
        # metadata (with placeholder scriptids/slugs) in order to push initial kernel versions, which
        # then lets us update this with the actual scriptids/slugs.
        dict(topic='embedding layers',
            exercise=dict(
                scriptid=1,
                ),
            tutorial=dict(
                ),
            # Keys later added to each of exercise and tutorial:
            #   - filename (e.g. ex_1.ipynb)
            #   - slug (e.g. colinmorris/hello-python)
            #   - title (exercise set to "Exercise ({tutorial_title})". tut set to capitalized topic)
            ),

        dict(topic='matrix factorization',
            exercise=dict(
                scriptid=1,
                ),
            tutorial=dict(
                ),
            ),
        
        dict(topic='exploring embeddings with gensim',
            exercise=dict(
                scriptid=1,
                ),
            tutorial=dict(
                ),
            ),
        
        dict(topic='visualizing embeddings with t-SNE',
            exercise=dict(
                scriptid=1,
                ),
            tutorial=dict(
                ),
            ),
        
]

def slugify(title):
    s = title.replace('(', '').replace(')', '').replace(',', '').replace(':', '').lower()
    tokens = s.split()
    return '-'.join(tokens)

for i, lesson in enumerate(lessons_meta):
    num = i + 1
    lesson['exercise']['filename'] = 'ex_{}.ipynb'.format(num)
    lesson['tutorial']['filename'] = 'tut_{}.ipynb'.format(num)
    ex = lesson['exercise']
    tut = lesson['tutorial']
    if 'title' not in tut:
        tut['title'] = lesson['topic'].capitalize()
    if 'title' not in ex:
        ex['title'] = 'Exercise: {}'.format(tut['title'])
    for thing in [ex, tut]:
        thing['slug'] = 'colinmorris/' + slugify(thing['title'])

# Haaaaack.
if __name__ == 'builtins':
    c = get_config()

    c.NbConvertApp.notebooks = ['*.ipynb']
    c.Exporter.preprocessors = ['lesson_preprocessor.LearnLessonPreprocessor']

    c.LearnLessonPreprocessor.lessons_metadata = lessons_meta
