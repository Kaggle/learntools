# This file defines ____ which we use in courses as a sentinel indicating a user hasn't
# attempted an exercise.

class PlaceholderValue(object):

    def __eq__(self, other):
        return isinstance(other, PlaceholderValue)

    def _repr_markdown_(self):
        """This returns the empty string. Some questions' starter code cell will look like:
            foo = ____
            q1.check()
            foo
        i.e. we want to echo the value of the variable at the end to make sure the user
        understands what kind of object they've created. While the variable still has 
        its placeholder value, we shouldn't echo anything.
        """
        return ''

PLACEHOLDER = PlaceholderValue()
