from learntools.core import *
import tensorflow as tf


# Free
class Q1(CodingProblem):
    _solution = ""
    _hint = ""
    def check(self):
        pass


class Q2A(ThoughtExperiment):
    _hint = "Remember that whatever transformation you apply needs at least to keep the classes distinct, but otherwise should more or less keep the appearance of the images the same. If you rotated a picture of a forest, would it still look like a forest?"
    _solution = """It seems to this author that any of the transformations from the first problem might be appropriate, provided the parameter values were reasonable. A picture of a forest that had been rotated or shifted or stretched would still look like a forest, and contrast adjustments could perhaps make up for differences in light and shadow. Rotations especially could be taken through the full range, since there's no real concept of "up or down" for pictures taken straight overhead."""

class Q2B(ThoughtExperiment):
    _hint = "Remember that whatever transformation you apply needs at least to keep the classes distinct, but otherwise should more or less keep the appearance of the images the same. If you rotated a picture of a forest, would it still look like a forest?"
    _solution = "It seems to this author that any of the transformations from the first problem might be appropriate, provided the parameter values were reasonable. A picture of a forest that had been rotated or shifted or stretched would still look like a forest, and contrast adjustments could perhaps make up for differences in light and shadow."

Q2 = MultipartProblem(Q2A, Q2B)


class Q3(CodingProblem):
    pass


qvars = bind_exercises(globals(), [
        Q1, Q2, Q3,
    ],
    var_format='q_{n}',
)
__all__ = list(qvars)
