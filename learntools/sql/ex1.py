from learntools.core import *


class CountTables(EqualityCheckProblem):
    _var = 'num_tables'
    _expected = 1
    _hint = \
"""Run `chicago_crime.list_tables()` in the top cell. Interpret the output to fill in `num_tables`"""

    _solution = CS(
"""
chicago_crime.list_tables()
num_tables = 1   # also could have done num_tables = len(chicago_crime.list_tables())
"""
)

class CountTimestampFields(EqualityCheckProblem):
    _var = 'num_timestamp_fields'
    _expected = 2
    _hint = \
"""Run `chicago_crime.table_schema('crime')` and count the number of fields with TIMESTAMP type"""

    _solution = CS(
"""
chicago_crime.table_schema('crime')
num_timestamp_fields = 2
"""
)

class IdentifyFieldsForPlotting(CodingProblem):
    _var = 'fields_for_plotting'
    _hint = "There are a couple options, but two of the fields are things commonly used to plot on maps. " + \
            "Both are FLOAT types. Use quotes around the field names in your answer"
    _solution = CS("fields_for_plotting = ['latitude', 'longitude']")
    def check(self, fields_for_plotting):
        assert (type(fields_for_plotting) is list), "fields_for_plotting should be a list"
        assert (len(fields_for_plotting) == 2), "fields for plotting should have exactly two strings. Your answer had {}".format(len(fields_for_plotting))
        assert (type(fields_for_plotting[0] == str), "The first item in fields_for_plotting should be a string")
        assert (type(fields_for_plotting[1] == str), "The second item in fields_for_plotting should be a string")
        lower_case_fields = [i.lower() for i in fields_for_plotting]
        if ('x_coordinate' in lower_case_fields) and ('y_coordinate' in lower_case_fields):
            print("latitude and longitude would be better and more standard than the x_coordinate and y_coordinate, but this might work.")
        else:
            assert (('latitude' in lower_case_fields) and ('longitude' in lower_case_fields)), \
                   ('There are two fields or variables that are commonly used to plot things on maps. {} is not exactly right'.format(fields_for_plotting))


qvars = bind_exercises(globals(), [
    CountTables,
    CountTimestampFields,
    IdentifyFieldsForPlotting,
    ],
    tutorial_id=169,
    var_format='q_{n}',
    )

__all__ = list(qvars)
