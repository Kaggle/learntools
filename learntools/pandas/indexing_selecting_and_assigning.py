import pandas as pd

from learntools.core import *

reviews = pd.read_csv("../input/wine-reviews/winemag-data-130k-v2.csv", index_col=0)

# 1
class SelectDescCol(EqualityCheckProblem):
    _var = 'desc'
    _expected = (
            reviews.description
    )
    #_solution = CS("desc = reviews.description")
    # This behaviour really should have been opt-in, rather than opt-out :/
    show_solution_on_correct = False
    _hint = "As an example, say we would like to select the column `column` from a DataFrame `table`.  Then we have two options: we can call either `table.column` or `table[\"column\"]`."
    _solution = """
```python
desc = reviews.description
```
or 
```python
desc = reviews["description"]
```
`desc` is a pandas `Series` object, with an index matching the `reviews` DataFrame. 
In general, when we select a single column from a DataFrame, we'll get a Series.
"""

# 2
class FirstDesc(EqualityCheckProblem):
    _var = 'first_description'
    _expected = (
            reviews.description.iloc[0]
    )
    _hint = "To obtain a specific entry (corresponding to column `column` and row `i`) in a DataFrame `table`, we can call `table.column.iloc[i]`.  Remember that Python indexing starts at 0!"
    _solution = """
```python
first_description = reviews.description.iloc[0]
```
Note that while this is the preferred way to obtain the entry in the DataFrame, many other options will return a valid result, such as `reviews.description.loc[0]`, `reviews.description[0]`, and more!  
"""

# 3
class FirstRow(EqualityCheckProblem):
    _var = 'first_row'
    _expected = (
            reviews.iloc[0]
    )
    _hint = "To obtain a specific row of a DataFrame, we can use the `iloc` operator.  For more information, see the section on **Index-based selection** in the [reference component](https://www.kaggle.com/residentmario/indexing-selecting-assigning-reference)."
    _solution = CS("first_row = reviews.iloc[0]")

# 4
class FirstDescs(EqualityCheckProblem):
    _var = 'first_descriptions'
    _expected = (
            reviews.description.iloc[:10]
    )
    _hint = "We can use either the `loc` or `iloc` operator to solve this problem.  For more information, see the sections on **Index-based selection** and **Label-based selection** in the [reference component](https://www.kaggle.com/residentmario/indexing-selecting-assigning-reference)."
    _solution = """
```python
first_descriptions = reviews.description.iloc[:10]
```
Note that many other options will return a valid result, such as `desc.head(10)` and `reviews.loc[:9, "description"]`.    
"""

# 5
class SampleReviews(EqualityCheckProblem):
    _var = 'sample_reviews'
    indices = [1, 2, 3, 5, 8]
    _expected = (
            reviews.loc[indices],
    )
    _hint = "Use either the `loc` or `iloc` operator to select rows of a DataFrame."
    _solution = CS("""\
indices = [1, 2, 3, 5, 8]
sample_reviews = reviews.loc[indices]""")

# 6
class RowColSelect(EqualityCheckProblem):
    _var = 'df'
    cols = ['country', 'province', 'region_1', 'region_2']
    indices = [0, 1, 10, 100]
    _expected = (
            reviews.loc[indices, cols],
    )
    _hint = "Use the `loc` operator.  (Note that it is also *possible* to solve this problem using the `iloc` operator, but this would require extra effort to convert each column name to a corresponding integer-valued index.)"
    _solution = CS("""\
cols = ['country', 'province', 'region_1', 'region_2']
indices = [0, 1, 10, 100]
df = reviews.loc[indices, cols]""")

# 7
class RowColSelect2(EqualityCheckProblem):
    _var = 'df'
    cols = ['country', 'variety']
    _expected = (
            reviews.head(100).loc[:,cols],
    )
    _hint = "It is most straightforward to solve this problem with the `loc` operator.  (However, if you decide to use `iloc`, remember to first convert each column into a corresponding integer-valued index.)"
    _solution = """
```python
cols = ['country', 'variety']
df = reviews.loc[:99, cols]
```
or 
```python
cols_idx = [0, 11]
df = reviews.iloc[:100, cols_idx]
```
"""

# 8
class ItalianWines(EqualityCheckProblem):
    _var = 'italian_wines'
    _expected = (
            reviews[reviews.country == 'Italy'],
    )
    _hint = "For more information, see the section on **Conditional selection** in the [reference component](https://www.kaggle.com/residentmario/indexing-selecting-assigning-reference)."
    _solution = CS("italian_wines = reviews[reviews.country == 'Italy']")

# 9
class TopOceanicWines(EqualityCheckProblem):
    _var = 'top_oceania_wines'
    cols = ['country', 'variety']
    _expected = reviews[
                (reviews.country.isin(['Australia', 'New Zealand']))
                & (reviews.points >= 95)
    ]
    _hint = "For more information, see the section on **Conditional selection** in the [reference component](https://www.kaggle.com/residentmario/indexing-selecting-assigning-reference)."
    _solution = CS("""\
top_oceania_wines = reviews.loc[
    (reviews.country.isin(['Australia', 'New Zealand']))
    & (reviews.points >= 95)
]""")

qvars = bind_exercises(globals(), [
    SelectDescCol,
    FirstDesc,
    FirstRow,
    FirstDescs,
    SampleReviews,
    RowColSelect,
    RowColSelect2,
    ItalianWines,
    TopOceanicWines,
    ],
    )
__all__ = list(qvars)
