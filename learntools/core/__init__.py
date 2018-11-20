from learntools.core.globals_binder import binder
from learntools.core.utils import bind_exercises
from learntools.core import problem
from learntools.core.problem import *
from learntools.core.multiproblem import MultipartProblem
from learntools.core.richtext import CodeSolution
# In starter code for exercises where the user has to create a variable foo with
# some value, we start them off with `foo = __`. 
from learntools.core.constants import PLACEHOLDER as ____

# A bit hacky, but we want to make sure '____' is imported when exercise modules import *
# from learntools.core, and by default names beginning with an underscore aren't brought
# in by star imports.
__all__ = problem.__all__ + ['binder', 'bind_exercises', 'MultipartProblem', 'CodeSolution', '____']
