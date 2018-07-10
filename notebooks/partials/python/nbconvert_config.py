TODO = 'TODO'
lessons_meta = [
        # TODO: provisional scriptids, slugs etc.
        # TODO: add some development mode where key errors are soft (because we
        # won't know stuff like scriptid and slug until we actually make the kernel,
        # which might not be until after we've done some local development)
        dict(topic='syntax, variable assignment, and numbers',
            exercise=dict(
                title='Exercises (Syntax, Variables, and Numbers)',
                scriptid=TODO,
                slug='colinmorris/foo-bar-exercises-1',
                ),
            tutorial=dict(
                title='Hello, Python',
                slug='colinmorris/foo-bar-tut-1',
                ),
            ),

        dict(topic='functions and getting help',
            exercise=dict(
                scriptid=TODO,
                slug='colinmorris/foo-bar-exercises-2',
                ),
            tutorial=dict(
                title='Functions and Getting Help',
                slug='colinmorris/foo-bar-tut-2',
                ),
            ),
        
        dict(topic='booleans and conditionals',
            exercise=dict(
                scriptid=TODO,
                slug='colinmorris/foo-bar-exercises-3',
                ),
            tutorial=dict(
                title='Booleans and Conditionals',
                slug='colinmorris/foo-bar-tut-3',
                ),
            ),
        
        dict(topic='lists and tuples',
            exercise=dict(
                scriptid=TODO,
                slug='colinmorris/foo-bar-exercises-4',
                ),
            tutorial=dict(
                title='Lists',
                slug='colinmorris/foo-bar-tut-4',
                ),
            ),
        
        dict(topic='loops and list comprehensions',
            exercise=dict(
                scriptid=TODO,
                slug='colinmorris/foo-bar-exercises-5',
                ),
            tutorial=dict(
                title='Loops and List Comprehensions',
                slug='colinmorris/foo-bar-tut-5',
                ),
            ),
        
        dict(topic='strings and dictionaries',
            exercise=dict(
                scriptid=TODO,
                slug='colinmorris/foo-bar-exercises-6',
                ),
            tutorial=dict(
                title='Strings and Dictionaries',
                slug='colinmorris/foo-bar-tut-6',
                ),
            ),
        
        dict(topic='imports',
            exercise=dict(
                scriptid=TODO,
                slug='colinmorris/foo-bar-exercises-7',
                ),
            tutorial=dict(
                title='Working with External Libraries',
                slug='colinmorris/foo-bar-tut-7',
                ),
            ),
]

def slugify(title):
    s = title.replace('(', '').replace(')', '').lower()
    tokens = s.split()
    return '-'.join(tokens)

for i, lesson in enumerate(lessons_metadata):
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
