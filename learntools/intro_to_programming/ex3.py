from learntools.core import *

class FloatToInt(ThoughtExperiment):
    _solution = ("Negative floats are always rounded UP to the closest integer (for instance, "
                 "both -1.1 and -1.9 are rounded up to -1). Positive floats are rounded either "
                 "UP or DOWN, depending on whether the preceding or following integer is closer "
                 "(for instance, 1.1 is rounded down to 1, and 1.9 is rounded up to 2).  In the "
                 "case that the float is equidistant from both integers, it is rounded up "
                 "(for instance, 1.5 is rounded up to 2).")
    
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
        ((0, 0), 80000),
        ((0, 1), 90000),
        ((1, 0), 110000),
        ((1, 1), 120000),
        ((1, 2), 130000),
        ((2, 3), 170000),
        ((3, 2), 190000),
        ((3, 3), 200000),
        ((3, 4), 210000),
    ]
    _hint = "HINT: If you're ever stuck on a question, it's a good idea to look at the hint before viewing the solution."
    _solution = ("SOLUTION: If you're still stuck on a question after viewing the hint and re-reading the tutorial, "
                 "you can view the solution.  You can also view the solution after you have successfully submitted "
                 "your own answer, to check if the official solution is any different (there may be more than "
                 "one right answer!).")

class AddingBooleans(EqualityCheckProblem):
    _vars = ['births_per_min', 'births_per_day']
    _expected = [250, births_per_min * mins_per_hour * hours_per_day]
    _hint = ("How can you use the variables to calculate the number of minutes in one day?  Once you have that, you "
             "need only multiply that number by the number of births per minute.")
    _solution = CS(
"""# Set the value of the births_per_min variable
births_per_min = 250

# Set the value of the births_per_day variable
births_per_day = births_per_min * mins_per_hour * hours_per_day
""")
    
class CustomEngravings(EqualityCheckProblem):
    _vars = ['survived_fraction', 'minors_fraction']
    _expected = [survived/total, minors/total]
    _hint = ("To get the fraction of people who survived the titanic, you need to divide the total number of people by the "
             "number of people who surivived.  Remember the variables that you can use to answer this question: `survived`, "
             "`total`, and `minors`.")
    _solution = CS(
"""# Fill in the value of the survived_fraction variable 
survived_fraction = survived/total

# Print the value of the survived_fraction variable
print(survived_fraction)

# Fill in the value of the minors_fraction variable
minors_fraction = minors/total 

# Print the value of the minors_fraction variable
print(minors_fraction)
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
