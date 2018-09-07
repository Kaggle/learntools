"""
lessons_meta: list of lesson dicts

lesson has fields:
    topic: str
    exercise: notebook dict
    tutorial: notebook dict

notebook has fields (* = optional):
    scriptid: kaggle numerical kernel identifier thing
    slug: e.g. 'colinmorris/hello-python'
    title
    filename: the name of the corresponding ipynb file (which should be in current directory)
    *kernel_sources: list of kernel slugs (as in kernel-metadata.json)
    *dataset_sources: list of dataset slugs (as in kernel-metadata.json)

scriptid is used in macro expansion to generate forking links (and so it's okay to use a
a placeholder to get started).

slug, title, and filename are used in generating kernel metadata files for the kernels API
(see prepare_push.py)

TODO: would be nice to encapsulate the code surrounding:
    - represention of a lesson (this abstraction is currently only useful for
      the purposes of macro expansion)
    - represention of a nb
    - validating fields of above objs and filling in default vals
    - making a kernel-metadata.json file for a nb
Currently spread around nbconvert_config.py, lesson_preprocessor.py (cf. Lesson class)
and prepare_push.py, with some redundancy / awkward coupling points.

Crazy idea: have lesson/nb metadata (currently stored in lessons_meta list) live
in ipynb metadata (currently we're storing lesson index and tut/ex type there). I think this
could address some of the awkwardness around the current scheme, namely:
- sys.path hacking in prepare_push.py
- if __name__ == 'builtins' in this module
- filename munging in clean.py
- inexplicable traitlet stuff in LearnLessonPreprocessor (I don't think I understood
  what that code was doing even back when I first wrote it)

What would this new process look like?
1. Have some py file per track responsible just for storing canonical track metadata, per lesson/nb.
2. Have a step that syncs the metadata stored there to the corresponding ipynb files. 
  (join happens based on filename munging, or by explicitly encoding ipynb filename
  in the metadata in 1.) Perhaps along lines of current clean.py.
3. For all other purposes (nbconvert, prepare_push.py) the ipynb metadata is where
    they read the track metadata from (vs. nbconvert_config.lessons_meta now)
"""

PREFIX_TITLES = True

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
                filename='1-embeddings.ipynb',
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
                filename='2-factorization.ipynb',
                ),
            ),
        
        dict(topic='exploring embeddings with gensim',
            exercise=dict(
                scriptid=1,
                ),
            tutorial=dict(
                filename='3-gensim.ipynb',
                ),
            ),
        
        dict(topic='visualizing embeddings with t-SNE',
            exercise=dict(
                scriptid=1,
                ),
            tutorial=dict(
                filename='4-tsne.ipynb',
                ),
            ),
        
]

def slugify(title):
    s = title.replace('(', '').replace(')', '').replace(',', '').replace(':', '').lower()
    tokens = s.split()
    return '-'.join(tokens)

for i, lesson in enumerate(lessons_meta):
    num = i + 1
    lesson['exercise']['filename'] = '{}-exercises.ipynb'.format(num)
    #lesson['tutorial']['filename'] = 'tut_{}.ipynb'.format(num)
    ex = lesson['exercise']
    tut = lesson['tutorial']
    assert 'filename' in tut
    nbs = [ex, tut]
    assert not any('kernel_sources' in nb for nb in nbs)
    for nb in nbs:
        nb['kernel_sources'] = ['colinmorris/0-movielens-preprocessing']
    if 'title' not in tut:
        tut['title'] = lesson['topic'].capitalize()
    if PREFIX_TITLES:
        tut['title'] = '{} {}'.format(num, tut['title'])
    if 'title' not in ex:
        ex['title'] = 'Exercise: {}'.format(tut['title'])
    for thing in nbs:
        thing['slug'] = 'colinmorris/' + slugify(thing['title'])

# Haaaaack.
if __name__ == 'builtins':
    c = get_config()

    c.NbConvertApp.notebooks = ['*.ipynb']
    c.Exporter.preprocessors = ['lesson_preprocessor.LearnLessonPreprocessor']

    c.LearnLessonPreprocessor.lessons_metadata = lessons_meta
