from learntools.core import *

def get_grade(score):
    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    elif score >= 60:
        grade = "D"
    else:
        grade = "F"
    return grade

def get_water_bill(num_gallons):
    if num_gallons <= 8000:
        bill = 5 * num_gallons / 1000
    elif num_gallons <= 22000:
        bill = 6 * num_gallons / 1000
    elif num_gallons <= 30000:
        bill = 7 * num_gallons / 1000
    else:
        bill = 10 * num_gallons / 1000
    return bill

def get_phone_bill(gb):
    # everyone pays $100/month
    bill = 100
    # number of GB over the 15GB plan (negative if under)
    gb_over = gb - 15
    # if gb_over is positive, there is an additional fee
    if gb_over > 0:
        # calculate cost of additional GB
        overage_fee = 100 * gb_over
        # add additional cost to bill
        bill = bill + overage_fee
    return bill

class GetGrade(FunctionProblem):
    _var = 'get_grade'
    _test_cases = [(i, get_grade(i)) for i in range(0,101)]
    _hint = ('`"A"` should only be returned if `score >= 90`.  Otherwise, if the score is between 80 and 89 (inclusive), or '
             '70 and 79 (inclusive), 60 and 69 (inclusive), or less than 60, a different score should be returned.  Make '
             'sure that your function always returns one of: `"A"`, `"B"`, `"C"`, `"D"`, or `"F"`.')
    _solution = CS(
"""def get_grade(score):
    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    elif score >= 60:
        grade = "D"
    else:
        grade = "F"
    return grade
""")

class CostProjectPartDeux(FunctionProblem):
    _var = 'cost_of_project'
    _test_cases = [
        (("Charlie+Denver", True), 240),
        (("08/10/2000", False), 120),
        (("Adrian", True), 160),
        (("Ana", False), 71),
    ]
    _hint = ("If `solid_gold = True`, then the cost of the ring is \\$100 (base cost), plus \\$10 times the length of the "
             "engraving.  You can get the length of the engraving with `len(engraving)`.  Otherwise, if "
             "`solid_gold = False`, then the cost of the ring is \\$50 (base cost), plus \\$7 times the length of the engraving.")
    _solution = CS(
"""# option 1
def cost_of_project(engraving, solid_gold):
    num_units = len(engraving)
    if solid_gold == True:
        cost = 100 + 10 * num_units
    else:
        cost = 50 + 7 * num_units
    return cost
    
# option 2 
def cost_of_project(engraving, solid_gold):
    if solid_gold == True:
        cost = 100 + 10 * len(engraving)
    else:
        cost = 50 + 7 * len(engraving)
    return cost
""")
    
class GetWaterBill(FunctionProblem):
    _var = 'get_water_bill'
    _test_cases = [(1000*i, get_water_bill(1000*i)) for i in range (0, 41)]
    _hint = """
Your solution should look something like:
```python
def get_water_bill(num_gallons):
    if num_gallons <= 8000:
        bill = ____ 
    elif num_gallons <= 22000:
        bill = ____ 
    elif num_gallons <= 30000:
        bill = ____
    else:
        bill = ____ 
    return bill
```
"""
    _solution = CS(
"""def get_water_bill(num_gallons):
    if num_gallons <= 8000:
        bill = 5 * num_gallons / 1000
    elif num_gallons <= 22000:
        bill = 6 * num_gallons / 1000
    elif num_gallons <= 30000:
        bill = 7 * num_gallons / 1000
    else:
        bill = 10 * num_gallons / 1000
    return bill
""")
    
class GetPhoneBill(FunctionProblem):
    _var = 'get_phone_bill'
    _test_cases = [(5 + .5*i, get_phone_bill(5 + .5*i)) for i in range (0, 35)]
    _hint = """
Your solution should look something like:
```python
def get_phone_bill(gb):
    if gb <= 15:
        bill = ____
    else:
        bill = 100 + ____
    return bill
```
"""
    _solution = CS(
"""def get_phone_bill(gb):
    if gb <= 15:
        bill = 100
    else:
        bill = 100 + (gb - 15) * 100
    return bill
""")

class GetLabels(CodingProblem):
    _congrats = "Once you have determined the labels for all of the food items, you're ready to move on to the next lesson!"
    _correct_message = ""
    def check(self):
        pass

qvars = bind_exercises(globals(), [
    GetGrade, 
    CostProjectPartDeux, 
    GetWaterBill, 
    GetPhoneBill, 
    GetLabels
    ],
    var_format='q{n}',
    )
__all__ = list(qvars)
