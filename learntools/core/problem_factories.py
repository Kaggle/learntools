from learntools.core.problem import *

class ProblemSeed:
    
    def __init__(self, name, solution, hint, parent=Problem):
        self.name = name
        self.solution = solution
        self.hint = hint
        self.parent = parent

    def with_expected(self, **kwargs):
       varnames, expected_vals = zip(*kwargs.items())
       namespace = dict(
               _vars = varnames,
               _expected = expected_vals,
               _hint = self.hint,
               _solution = self.solution,
               )
       return type(self.name, (self.parent,), namespace)

def simple_problem(name, solution, hint=None):
    assert name.isidentifier()
    return ProblemSeed(name, solution, hint, parent=EqualityCheckProblem)
