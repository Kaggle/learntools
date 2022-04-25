from learntools.core import *

class ExcessTransFat(FunctionProblem):
    _var = 'excess_trans_fat'
    _test_cases = [
        ((1, 900), True),
        ((.9, 900), False),
        ((.1, 900), False),
        ((1.1, 900), True),
        ((2, 900), True),
    ]
    _hint = ("The calculation here is very similar to the saturated fat example.  You still need to use the fact "
             "that there are 9 calories per 1 gram of fat, and you need to change the percentage from calories "
             "from fat that are allowed from 10% to 1%.")
    _solution = CS(
"""def excess_trans_fat(trans_fat_g, calories_per_serving):
    if trans_fat_g * 9 / calories_per_serving >= .01:
        return True
    else:
        return False
""")

class ExcessSugar(FunctionProblem):
    _var = 'excess_sugar'
    _test_cases = [
        ((1, 40), True),
        ((.9, 40), False),
        ((.1, 40), False),
        ((1.1, 40), True),
        ((2, 40), True),
    ]
    _hint = ("A [Snickers](https://world.openfoodfacts.org/product/9300682052825/snickers) candy bar has: \n"
             "- 25.6 grams of sugar per serving, and\n"
             "- 1030 calories per serving.\n"
             "To calculate the percentage of calories from sugar in a Snickers candy bar, note that:\n"
             "- **For all foods and drinks**, there are approximately 4 calories per 1 gram of sugar.\n" 
             "- So, a Snickers candy bar has 4 * 25.6 = 102.4 calories of sugar per serving.\n"
             "- Thus, the percentage of calories from sugar is 102.4/1030, which is approximately 0.0994, or 9.94%.\n"
             "- This is JUST under 10%, and so your algorithm should judge the Snickers candy bar as NOT having excess sugar.")
    _solution = CS(
"""def excess_sugar(sugars_g, calories_per_serving):
    return (sugars_g * 4 / calories_per_serving >= .1)
""")
    
class ExcessSodium(FunctionProblem):
    _var = 'excess_sodium'
    _test_cases = [
        ((0, 44), False),
        ((0, 45), True),
        ((0, 46), True),
        ((0, 800), True),
        ((1, 1), True),
        ((2, 3), True),
        ((10, 100), True),
        ((100, 10), False),
    ]
    _hint = ("To check if an item is a non-caloric beverage, you need to use the `calories_per_serving` variable.")
    _solution = CS(
"""def excess_sodium(calories_per_serving, sodium_mg):
    if calories_per_serving == 0:
        return (sodium_mg >= 45)
    else:
        return (sodium_mg / calories_per_serving >= 1)
""")
    
class ValueErrorCalories(ThoughtExperiment):
    _hint = ('In order to make sure that the `raise ValueError(...)` code is run, you need to make sure that the value '
             'supplied for `food_type` is something other than `"solid"` or `"liquid"`.')
    _solution = ('The code `raise ValueError()` makes the code error, and it returns the error message shown in the parentheses. '
                 'This is useful in this function, because in order for the function input to make sense, you have to supply a '
                 'value for `"food_type"` that is one of `"solid"` or `"liquid"`. If something other than these two values '
                 'is returned, this line makes the function error, and surfaces a message saying the values '
                 'that are accepted for `"food_type"`, so that the programmer knows how to correct their code.')

class GetLabels(CodingProblem):
    _congrats = "Once you have determined the labels for all of the food items, you're ready to move on to the next lesson!"
    _correct_message = ""
    def check(self):
        pass

qvars = bind_exercises(globals(), [
    ExcessTransFat, 
    ExcessSugar, 
    ExcessSodium, 
    ValueErrorCalories, 
    GetLabels
    ],
    var_format='q{n}',
    )
__all__ = list(qvars)
