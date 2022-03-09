from learntools.core import *
import math

def get_expected_cost(beds, baths):
    value = 80000 + 30000 * beds + 10000 * baths
    return value

def get_cost(sqft_walls, sqft_ceiling, sqft_per_gallon, cost_per_gallon):
    total_sqft = sqft_walls + sqft_ceiling
    gallons_needed = total_sqft / sqft_per_gallon
    cost = cost_per_gallon * gallons_needed
    return cost

class GetExpectedCost(FunctionProblem):
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
    _hint = ("The value should be the base cost (`80000`), plus the total cost of the bedrooms (`30000 * beds`), "
             "plus the total cost of the bathrooms (`10000 * baths`).")
    _solution = CS(
"""
def get_expected_cost(beds, baths):
    value = 80000 + 30000 * beds + 10000 * baths
    return value
""")
    
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
    
class GetCostPaint(FunctionProblem):
    _var = 'get_cost'
    _test_cases = [
        ((432, 144, 400, 15), 21.599999999999998),
        ((400, 400, 400, 10), 20.0),
        ((400, 500, 300, 16), 48.0),
    ]
    _hint = ("Begin by calculating the total number of square feet that need to be painted. "
    "Then, based on that, figure out how many gallons you need.  Then, once you know how many "
    "gallons you need, you can calculate the total cost of the project.")
    _solution = CS(
"""
def get_cost(sqft_walls, sqft_ceiling, sqft_per_gallon, cost_per_gallon):
    total_sqft = sqft_walls + sqft_ceiling
    gallons_needed = total_sqft / sqft_per_gallon
    cost = cost_per_gallon * gallons_needed
    return cost
""") 

class GetCostPaintExample(EqualityCheckProblem):
    _var = 'project_cost'
    _expected = get_cost(432, 144, 400, 15)
    _hint = ("If we needed to instead calculate the cost of applying one coat of paint to a room with "
             "800 square feet of walls and 160 square feet of ceiling, and one gallon of paint covered "
             "300 square feet and cost $10, we would set `project_cost = get_cost(800, 160, 300, 10)`.")
    _solution = CS(
"""# Set the project_cost variable to the cost of the project
project_cost = get_cost(432, 144, 400, 15) 
""")
    
class NoMoreFractions(FunctionProblem):
    _var = 'get_actual_cost'
    _test_cases = [
        ((432, 144, 400, 15), 30),
        ((400, 500, 400, 10), 30),
        ((400, 900, 300, 16), 80),
    ]
    _hint = ("Begin with the `get_cost()` function as a starting point.  The only change you need to "
             "make is to add `math.ceil()` to round up the number of gallons that need to be purchased. "
             "Can you figure out where to add it to the function?")
    _solution = CS(
"""def get_actual_cost(sqft_walls, sqft_ceiling, sqft_per_gallon, cost_per_gallon):
    total_sqft = sqft_walls + sqft_ceiling
    gallons_needed = total_sqft / sqft_per_gallon
    gallons_to_buy = math.ceil(gallons_needed)
    cost = cost_per_gallon * gallons_to_buy
    return cost
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
