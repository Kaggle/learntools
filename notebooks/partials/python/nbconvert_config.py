lessons_meta = [
        # NB: Kind of an ugly ouroboros bootstrapping process here where we need some version of this
        # metadata (with placeholder scriptids/slugs) in order to push initial kernel versions, which
        # then lets us update this with the actual scriptids/slugs.
        dict(topic='syntax, variable assignment, and numbers',
            exercise=dict(
                title='Exercise (Syntax, Variables, and Numbers)',
                scriptid=1275163,
                ),
            tutorial=dict(
                title='Hello, Python',
                ),
            # Keys later added to each of exercise and tutorial:
            #   - filename (e.g. ex_1.ipynb)
            #   - slug (e.g. colinmorris/hello-python)
            #   - title (exercise only. set to "Exercise ({tutorial_title})")
            ),

        dict(topic='functions and getting help',
            exercise=dict(
                scriptid=1275158,
                ),
            tutorial=dict(
                title='Functions and Getting Help',
                ),
            ),
        
        dict(topic='booleans and conditionals',
            exercise=dict(
                scriptid=1275165,
                ),
            tutorial=dict(
                title='Booleans and Conditionals',
                ),
            ),
        
        dict(topic='lists and tuples',
            exercise=dict(
                scriptid=1275173,
                ),
            tutorial=dict(
                title='Lists',
                ),
            ),
        
        dict(topic='loops and list comprehensions',
            exercise=dict(
                scriptid=1275177,
                ),
            tutorial=dict(
                title='Loops and List Comprehensions',
                ),
            ),
        
        dict(topic='strings and dictionaries',
            exercise=dict(
                scriptid=1275185,
                ),
            tutorial=dict(
                title='Strings and Dictionaries',
                ),
            ),
        
        dict(topic='imports',
            exercise=dict(
                scriptid=1275190,
                ),
            tutorial=dict(
                title='Working with External Libraries',
                ),
            ),
]

def slugify(title):
    s = title.replace('(', '').replace(')', '').replace(',', '').lower()
    tokens = s.split()
    return '-'.join(tokens)

for i, lesson in enumerate(lessons_meta):
    num = i + 1
    lesson['exercise']['filename'] = 'ex_{}.ipynb'.format(num)
    lesson['tutorial']['filename'] = 'tut_{}.ipynb'.format(num)
    ex = lesson['exercise']
    tut = lesson['tutorial']
    if 'title' not in ex:
        ex['title'] = 'Exercise ({})'.format(tut['title'])
    for thing in [ex, tut]:
        thing['slug'] = 'colinmorris/' + slugify(thing['title'])

# Haaaaack.
if __name__ == 'builtins':
    c = get_config()

    c.NbConvertApp.notebooks = ['*.ipynb']
    c.Exporter.preprocessors = ['lesson_preprocessor.LearnLessonPreprocessor']

    c.LearnLessonPreprocessor.lessons_metadata = lessons_meta
