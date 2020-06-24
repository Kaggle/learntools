track = dict(
    author_username='colinmorris',
    course_name='Python',
    course_url='https://www.kaggle.com/learn/python',
    course_forum_url='https://www.kaggle.com/learn-forum/161283'
)

lessons = [
        dict(topic='syntax, variable assignment, and numbers',),
        dict(topic='functions and getting help',),
        dict(topic='booleans and conditionals',),
        dict(topic='lists and tuples',),
        dict(topic='loops and list comprehensions',),
        dict(topic='strings and dictionaries',),
        dict(topic='imports',),
]

_tuts = [dict(lesson_idx=i, type='tutorial', filename='tut_{}.ipynb'.format(i+1))
        for i in range(len(lessons))
        ]
_tuts[0]['title'] = 'Hello, Python'
_tuts[3]['title'] = 'Lists'
_tuts[6]['title'] = 'Working with External Libraries'

_exercise_scriptids = [1275163, 1275158, 1275165, 1275173,
        1275177, 1275185, 1275190]

_exs = [dict(lesson_idx=i, scriptid=sid, type='exercise', filename='ex_{}.ipynb'.format(i+1)) 
        for i, sid in enumerate(_exercise_scriptids)
        ]

_exs[0]['title'] = 'Exercise: Syntax, Variables, and Numbers'
_exs[3]['title'] = 'Exercise: Lists'
_exs[6]['title'] = 'Exercise: Working with External Libraries'


notebooks = _tuts + _exs
