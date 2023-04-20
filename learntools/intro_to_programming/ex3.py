from learntools.core import *

def get_expected_cost(beds, baths, has_basement):
    value = 80000 + 30000 * beds + 10000 * baths + 40000 * has_basement
    return value

class FloatToInt(ThoughtExperiment):
    _solution = ("Negative floats are always rounded UP to the closest integer (for instance, "
                 "both -1.1 and -1.9 are rounded up to -1). Positive floats are always rounded "
                 "DOWN to the closest integer (for instance, 2.1 and 2.9 are rounded down to 2).")
    
class MultiplyBooleans(ThoughtExperiment):
    _solution = ("When you multiple an integer or float by a boolean with value `True`, it just returns "
                 "that same integer or float (and is equivalent to multiplying by 1).  If you "
                 "multiply an integer or float by a boolean with value `False`, it always returns 0.  This "
                 "is true for both positive and negative numbers.  If you multiply a string by a boolean with "
                 "value `True`, it just returns that same string.  And if you multiply a string by a boolean "
                 "with value `False`, it returns an empty string (or a string with length zero).")
    
class EstimateHouseValueBool(FunctionProblem):
    _var = 'get_expected_cost'
    _test_cases = [
        ((1, 1, False), 120000),
        ((2, 1, True), 190000),
        ((3, 2, True), 230000),
        ((4, 5, False), 250000),
    ]
    _hint = ("The variable `has_basement` is either `True` or `False`.  What happens when you "
             "multiply it by 40000 (the value of a basement)?  Refer to the previous question "
             "if you are unsure.")
    _solution = CS(
"""def get_expected_cost(beds, baths, has_basement):
    value = 80000 + 30000 * beds + 10000 * baths + 40000 * has_basement
    return value
""")

class AddingBooleans(ThoughtExperiment):
    _solution = "When you add booleans, adding `False` is equivalent to adding 0, and adding `True` is equivalent to adding 1."
    
class CustomEngravings(FunctionProblem):
    _var = 'cost_of_project'
    _test_cases = [
        (("Charlie+Denver", True), 240),
        (("08/10/2000", False), 120),
        (("Adrian", True), 160),
        (("Ana", False), 71),
    ]
    _hint = ("There are two options - either the project uses solid gold or does not.  With this in mind, you can structure your solution like this: `cost = solid_gold * ____ + (not solid_gold) * ____`.  You need to figure out how to fill in the blanks. Also, remember that:\n"
             "- If `solid_gold = True`, then `(not solid_gold) = False`, and if `solid_gold = False`, then `(not solid_gold) = True`.\n"
             "- Multiplying an integer by `True` is equivalent to multiplying it by 1, and multiplying an integer by `False` is equivalent to multiplying it by 0.")
    _solution = CS(
"""def cost_of_project(engraving, solid_gold):
    cost = solid_gold * (100 + 10 * len(engraving)) + (not solid_gold) * (50 + 7 * len(engraving))
    return cost
""")


qvars = bind_exercises(globals(), [
    FloatToInt,
    MultiplyBooleans,
    EstimateHouseValueBool,
    AddingBooleans,
    CustomEngravings
    ],
    var_format='q{n}',
    )
__all__ = list(qvars)
