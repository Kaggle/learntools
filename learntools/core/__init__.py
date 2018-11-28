"""
learntools.core exports all the content from the core sub-package that is typically
needed by an exercise module. For example, Problem subclasses to inherit from, 
assert functions to call from custom check() methods, the CodeSolution class (by convention,
aliased to CS for brevity) for wrapping _solution attributes, etc.

For most exercise modules, "from learntools.core import *" should include all batteries needed.
"""
# This one isn't used within exercise modules, but we export it here so that exercise
# notebooks can begin with "from learntools.core import binder"
from learntools.core.globals_binder import binder

# All exercise modules conclude with a call to this helper function
from learntools.core.utils import bind_exercises
# Problem and all its subclasses (e.g. EqualityCheckProblem, ThoughtExperiment)
from learntools.core.problem import *
from learntools.core.multiproblem import MultipartProblem
# This is used so frequently, it's worth giving it a short alias.
from learntools.core.richtext import CodeSolution as CS
# Assert helper functions, often used in custom check methods on Problem subclasses
from learntools.core.asserts import *

# In starter code for exercises where the user has to create a variable foo with
# some value, we start them off with `foo = __`. 
from learntools.core.constants import PLACEHOLDER as ____

# A bit hacky, but we want to make sure '____' is imported when exercise modules import *
# from learntools.core, and by default names beginning with an underscore aren't brought
# in by star imports.
__all__ = [name for name in dir() if not name.startswith('_')] + ['____']
