from learntools.core import *
from google.cloud import bigquery

# Setup (0.65s on Kaggle)
client = bigquery.Client()
dataset_ref = client.dataset("chicago_crime", project="bigquery-public-data")
dataset = client.get_dataset(dataset_ref)

# (1) CountTables
num_tables_answer = len(list(client.list_tables(dataset)))

# (2) CountTimestampFields
table_ref = dataset_ref.table("crime")
table = client.get_table(table_ref)
num_timestamp_fields_answer = [schema.field_type for schema in table.schema].count('TIMESTAMP')

class CountTables(EqualityCheckProblem):
    _var = 'num_tables'
    _expected = num_tables_answer
    _hint = \
"""Use the `list_tables()` method to get a list of the tables in the dataset."""

    _solution = CS(
"""
# List all the tables in the "chicago_crime" dataset
tables = list(client.list_tables(dataset))

# Print number of tables in the dataset
print(len(tables))

num_tables = 1
"""
)

class CountTimestampFields(EqualityCheckProblem):
    _var = 'num_timestamp_fields'
    _expected = num_timestamp_fields_answer
    _hint = ("Begin by fetching the `crime` table. Then take a look at the table schema, and "
             "check the field type of each column.  How many times does `'TIMESTAMP'` appear?")
    _solution = CS(
"""
# Construct a reference to the "crime" table
table_ref = dataset_ref.table("crime")

# API request - fetch the table
table = client.get_table(table_ref)

# Print information on all the columns in the "crime" table in the "chicago_crime" dataset
print(table.schema)

num_timestamp_fields = 2
"""
)

class IdentifyFieldsForPlotting(CodingProblem):
    _var = 'fields_for_plotting'
    _hint = ("Look at the table schema.  There are a couple options, but two of the fields are "
             "things commonly used to plot on maps. "
             "Both are `'FLOAT'` types. Use quotes around the field names in your answer.")
    _solution = CS("fields_for_plotting = ['latitude', 'longitude']")
    def check(self, fields_for_plotting):
        assert (type(fields_for_plotting) is list), "`fields_for_plotting` should be a list."
        assert (len(fields_for_plotting) == 2), "`fields_for_plotting` should have exactly **two** strings. Your answer had {}.".format(len(fields_for_plotting))
        assert (type(fields_for_plotting[0] == str), "The first item in `fields_for_plotting` should be a string.")
        assert (type(fields_for_plotting[1] == str), "The second item in `fields_for_plotting` should be a string.")
        lower_case_fields = [i.lower() for i in fields_for_plotting]
        if ('x_coordinate' in lower_case_fields) and ('y_coordinate' in lower_case_fields):
            print("`'latitude'` and `'longitude'` would be better and more standard than `'x_coordinate'` and `'y_coordinate'`, but this might work.")
        else:
            assert (('latitude' in lower_case_fields) and ('longitude' in lower_case_fields)), \
                   ('There are two fields or variables that are commonly used to plot things on maps. {} is not exactly right'.format(fields_for_plotting))


qvars = bind_exercises(globals(), [
    CountTables,
    CountTimestampFields,
    IdentifyFieldsForPlotting,
    ],
    var_format='q_{n}',
    )

__all__ = list(qvars)
