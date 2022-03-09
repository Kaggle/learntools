from learntools.core import *
import math

def get_expected_cost(beds, baths):
    value = 80000 + 30000 * beds + 10000 * baths
    return value

######### TODO
class GetExpectedCost(CodingProblem):
    _congrats = ("If you see `Hello, world!` above, You have successfully printed a message, "
                 "and you're ready to move on to the next question.")
    _correct_message = ""
    def check(self):
        pass 
    
class RunGetExpectedCost(EqualityCheckProblem):
    _vars = ['option_one', 'option_two', 'option_three', 'option_four']
    _expected = [get_expected_cost(2, 3), get_expected_cost(3, 2), get_expected_cost(3, 3), get_expected_cost(3, 4)]
    _hint = ("If `option_five` needed to have the expected cost of a house with five "
             "bedrooms and three bathrooms, we would write `option_five = get_expected_cost(5, 3)`.")
    _solution = CS(
"""# Use the get_expected_cost function to fill in each value
option_one = get_expected_cost(2, 3)
option_two = get_expected_cost(3, 2)
option_three = get_expected_cost(3, 3)
option_four = get_expected_cost(3, 4)
""")
    
class GetCostPaint(CodingProblem):
    _hint = "HINT: If you're ever stuck on a question, it's a good idea to look at the hint before viewing the solution."
    _solution = ("SOLUTION: If you're still stuck on a question after viewing the hint and re-reading the tutorial, "
                 "you can view the solution.  You can also view the solution after you have successfully submitted "
                 "your own answer, to check if the official solution is any different (there may be more than "
                 "one right answer!).")
    _congrats = "Once you have ran `q3.hint()` and `q3.solution()`, you're ready to move on to the next question."
    _correct_message = ""
    def check(self):
        pass 

class GetCostPaintExample(EqualityCheckProblem):
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
    
class NoMoreFractions(EqualityCheckProblem):
    _vars = ['survived_fraction', 'minors_fraction']
    _expected = [survived/total, minors/total]
    _hint = ("To get the fraction of people who survived the titanic, you need to divide the total number of people by the "
             "number of people who surivived.  Remember the variables that you can use to answer this question: `survived`, "
             "`total`, and `minors`.")
    _solution = CS(
"""# TODO: Fill in the value of the variable here
survived_fraction = survived/total

# Print the value of the variable
print(survived_fraction)

# TODO: Fill in the value of the variable here
minors_fraction = minors/total 

# Print the value of the variable
print(minors_fraction)
""")


qvars = bind_exercises(globals(), [
    GetExpectedCost,
    RunGetExpectedCost,
    GetCostPaint,
    GetCostPaintExample,
    NoMoreFractions
    ],
    var_format='q{n}',
    )
__all__ = list(qvars)
