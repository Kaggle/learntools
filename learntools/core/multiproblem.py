class MultipartProblem:
    """A container for multiple related Problems grouped together in one 
    question. If q1 is a MPP, its subquestions are accessed as q1.a, q1.b, etc.
    """
    
    def __init__(self, *probs):
        self.problems = probs
        # Mapping from string identifier (e.g. 'a', 'b'...) to ProblemView
        self._prob_map = {}

    def _repr_markdown_(self):
        return repr(self)

    def __repr__(self):
        varname = self._varname
        part_names = ['`{}.{}`'.format(varname, letter) for letter in self._prob_map]
        return """This question is in {} parts. Those parts can be accessed as {}.
For example, to get a hint about part a, you would type `{}.a.hint()`.""".format(
            len(self._prob_map), ', '.join(part_names), varname
        )

