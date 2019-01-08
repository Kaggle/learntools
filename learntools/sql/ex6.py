from learntools.core import *


class ListTables(EqualityCheckProblem):
    _var = 'list_of_tables'
    _expected = 
    _solution = CS('list_of_tables = stackoverflow.list_tables()')


qvars = bind_exercises(globals(), [

    ],
    tutorial_id=82,
    var_format='q_{n}',
    )

__all__ = list(qvars)
