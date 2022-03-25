from learntools.core import *

# problem 1
correct_menu = ['stewed meat with onions', 'risotto with trout and shrimp',
       'fish soup with cream and onion', 'gyro', 'roasted beet salad']

# problem 2
num_customers = [137, 147, 135, 128, 170, 174, 165, 146, 126, 159,
                 141, 148, 132, 147, 168, 153, 170, 161, 148, 152,
                 141, 151, 131, 149, 164, 163, 143, 143, 166, 171]

# problem 3
def get_probs_from_counts_solution(count_list):
    prob_list = [i / sum(count_list) for i in count_list]
    return prob_list

# problem 4
def percentage_growth_solution(num_users, yrs_ago):
    growth = (num_users[0] - num_users[yrs_ago])/num_users[yrs_ago]
    return growth

num_users_test = [2001078, 1930992, 1843064, 1623463, 1593432, 1503323, 1458996, 1204334, 1043553, 920344]
num_users_test2 = [2001232, 1930952, 1841064, 1620963, 1593862, 1503423, 1478996, 1219334, 1009553, 920224]

# problem 5
def percentage_liked_solution(ratings):
    list_liked = [i >= 4 for i in ratings]
    percentage_liked = sum(list_liked)/len(list_liked)
    return percentage_liked


class FoodMenu(CodingProblem):
    _var = 'menu'
    _hint = ("Here is the original line of code that created the menu: "
             "`menu = ['stewed meat with onions', 'bean soup', 'risotto with trout and shrimp', "
             "'fish soup with cream and onion', 'gyro']`.  Use `.append()` to add an item, "
             "and use `.remove()` to remove an item.")
    _solution = CS(
"""# Do not change: Initial menu for your restaurant
menu = ['stewed meat with onions', 'bean soup', 'risotto with trout and shrimp',
       'fish soup with cream and onion', 'gyro']

# Remove 'bean soup', and add 'roasted beet salad' to the end of the menu
menu.remove('bean soup')
menu.append('roasted beet salad')
""")
    def check(self, menu):
        
        # is python list
        assert isinstance(menu, list), \
            '`menu` needs to be a Python list.'
        
        # extra items need to be removed
        assert set(menu) - set(correct_menu) == set(), \
            'These item(s) should be removed from `menu`: {}'.format(list(set(menu) - set(correct_menu)))
        
        for item in correct_menu:
            # contains all needed items
            assert item in menu, '`menu` needs to have this item, but it is missing: `{}`'.format(item)
            # no items duplicated
            assert menu.count(item) == 1, 'Each item should appear in `menu` once, but `{}` appears {} times.'.format(item, menu.count(item))
        

class NumCustomers(EqualityCheckProblem):
    _vars = ['avg_first_seven', 'avg_last_seven', 'max_month', 'min_month']
    _expected = [sum(num_customers[:7])/7, sum(num_customers[-7:])/7, max(num_customers), min(num_customers)]
    _hint = ("To take the average of a list of numbers, you can calculate the sum and then divide by the length. "
             "And, to pull the last `y` entries of a list `my_list`, use `my_list[-y:]`.")
    _solution = CS(
"""# Fill in values for the variables below
avg_first_seven = sum(num_customers[:7])/7 
avg_last_seven = sum(num_customers[-7:])/7
max_month = max(num_customers)
min_month = min(num_customers)
""")

class GetProbsFromCounts(FunctionProblem):
    _var = 'get_probs_from_counts'
    _test_cases = [
        ([1, 3, 5, 11], get_probs_from_counts_solution([1, 3, 5, 11])),
        ([1, 2], get_probs_from_counts_solution([1, 2])),
        ([7, 8, 9, 10, 11], get_probs_from_counts_solution([7, 8, 9, 10, 11]))
    ]
    _hint = ("In the tutorial, you learned how to divide every entry in a list by the maximum entry in the list. "
             "To answer this question, you need to divide every entry in the list by the sum of the entries in the list.")
    _solution = CS(
"""# Write your function
def get_probs_from_counts(count_list):
    prob_list = [i / sum(count_list) for i in count_list]
    return prob_list
""")
    
class WebsiteAnalytics(FunctionProblem):
    _var = 'percentage_growth'
    _test_cases = [
        ((num_users_test, 1), percentage_growth_solution(num_users_test, 1)),
        ((num_users_test2, 2), percentage_growth_solution(num_users_test2, 2)),
        ((num_users_test, 3), percentage_growth_solution(num_users_test, 3)),
        ((num_users_test2, 4), percentage_growth_solution(num_users_test2, 4)),
        ((num_users_test, 5), percentage_growth_solution(num_users_test, 5)),
        ((num_users_test2, 6), percentage_growth_solution(num_users_test2, 6)),
        ((num_users_test, 7), percentage_growth_solution(num_users_test, 7)),
        ((num_users_test2, 8), percentage_growth_solution(num_users_test2, 8)),
        ((num_users_test, 9), percentage_growth_solution(num_users_test, 9)),
    ]
    _hint = ("It's already correct that you need to subtract two numbers from the list, before dividing by an item in the list. "
             "You only need to modify the positions for the items that are pulled from the list.")
    _solution = CS(
"""def percentage_growth(num_users, yrs_ago):
    growth = (num_users[0] - num_users[yrs_ago])/num_users[yrs_ago]
    return growth
""")
    
class PercentageLiked(FunctionProblem):
    _var = 'percentage_liked'
    _test_cases = [
        ([1, 2, 3, 4, 5, 4, 5, 1], percentage_liked_solution([1, 2, 3, 4, 5, 4, 5, 1])),
        ([1, 2, 3, 4], percentage_liked_solution([1, 2, 3, 4])),
        ([1, 2, 3, 4, 5, 4, 5, 1, 2, 2, 2], percentage_liked_solution([1, 2, 3, 4, 5, 4, 5, 1, 2, 2, 2])),
        ([1, 4, 4, 4, 5, 4, 5, 1], percentage_liked_solution([1, 4, 4, 4, 5, 4, 5, 1])),
    ]
    _hint = ('Begin by creating a Python list `list_liked` with `True` if the corresponding entry in `ratings` is '
             'greater than or equal to 4 and is otherwise `False`.  Then take the average value of `list_liked`.')
    _solution = CS(
"""
# Complete the function
def percentage_liked(ratings):
    list_liked = [i >= 4 for i in ratings]
    percentage_liked = sum(list_liked)/len(list_liked)
    return percentage_liked
""")

qvars = bind_exercises(globals(), [
    FoodMenu, 
    NumCustomers, 
    GetProbsFromCounts, 
    WebsiteAnalytics, 
    PercentageLiked
    ],
    var_format='q{n}',
    )
__all__ = list(qvars)
