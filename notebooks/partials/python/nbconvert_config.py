c = get_config()

c.NbConvertApp.notebooks = ['*.ipynb']
c.Exporter.preprocessors = ['lesson_preprocessor.LearnLessonPreprocessor']

TODO = 'TODO'
lessons_meta = [
        # TODO: provisional scriptids, slugs etc.
        # TODO: add some development mode where key errors are soft (because we
        # won't know stuff like scriptid and slug until we actually make the kernel,
        # which might not be until after we've done some local development)
        dict(topic='syntax, variable assignment, and numbers',
            exercise=dict(
                scriptid=TODO,
                slug='colinmorris/foo-bar-exercises-1',
                ),
            tutorial=dict(
                slug='colinmorris/foo-bar-tut-1',
                ),
            ),

        dict(topic='functions and getting help',
            exercise=dict(
                scriptid=TODO,
                slug='colinmorris/foo-bar-exercises-2',
                ),
            tutorial=dict(
                slug='colinmorris/foo-bar-tut-2',
                ),
            ),
        
        dict(topic='booleans and conditionals',
            exercise=dict(
                scriptid=TODO,
                slug='colinmorris/foo-bar-exercises-3',
                ),
            tutorial=dict(
                slug='colinmorris/foo-bar-tut-3',
                ),
            ),
        
        dict(topic='lists and tuples',
            exercise=dict(
                scriptid=TODO,
                slug='colinmorris/foo-bar-exercises-4',
                ),
            tutorial=dict(
                slug='colinmorris/foo-bar-tut-4',
                ),
            ),
        
        dict(topic='loops and list comprehensions',
            exercise=dict(
                scriptid=TODO,
                slug='colinmorris/foo-bar-exercises-5',
                ),
            tutorial=dict(
                slug='colinmorris/foo-bar-tut-5',
                ),
            ),
        
        dict(topic='strings and dictionaries',
            exercise=dict(
                scriptid=TODO,
                slug='colinmorris/foo-bar-exercises-6',
                ),
            tutorial=dict(
                slug='colinmorris/foo-bar-tut-6',
                ),
            ),
        
        dict(topic='imports',
            exercise=dict(
                scriptid=TODO,
                slug='colinmorris/foo-bar-exercises-7',
                ),
            tutorial=dict(
                slug='colinmorris/foo-bar-tut-7',
                ),
            ),
]
c.LearnLessonPreprocessor.lessons_metadata = lessons_meta
