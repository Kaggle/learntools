import os

import pandas as pd

def assert_has_columns(df, cols, name=None, strict=False):
    df_desc = "dataframe"
    if name:
        df_desc += ' `{}`'.format(name)
    for col in cols:
        assert col in df.columns, "Expected {} to have column `{}`".format(
                df_desc, col
                )
    if strict:
        for col in df.columns:
            msg = "Unexpected column in {}: `{}`".format(df_desc, col)
            assert col in cols, msg

def assert_isinstance(cls, **named_things):
    # TODO: Kind of a bad idea to use kwargs here, because names might not be
    # valid Python identifiers in some cases.
    for name, val in named_things.items():
        assert isinstance(val, cls), "Expected {} to have type `{!r}` but had type `{!r}`".format(name, cls, type(val))

def assert_len(thing, exp_len, name):
    actual = len(thing)
    assert actual == exp_len, "Expected {} to have length {}, but was {}".format(
            name, exp_len, actual,
            )

def assert_file_exists(path):
    if '/' in path:
        pp = 'at path'
    else:
        pp = 'with name'
    msg = "Expected file to exist {} `{}`".format(pp, path)
    assert os.path.exists(path), msg
    assert os.path.isfile(path), "Expected `{}` to be a file".format(path)

def assert_df_equals(actual, exp, name=None):
    actual_name = name or "dataframe"
    assert_isinstance(pd.DataFrame, **{actual_name: actual, "_expected_value": exp})
    actual_name = '`{}`'.format(name) if name else "dataframe"
    assert len(actual) == len(exp), "Expected {} to have length {} but was actually {}".format(
        actual_name, len(exp), len(actual))
    # Only verify that the first n records match - I guess this could be slow if 
    # our dataframes have hundreds of thousands of rows. This *could* bite us, though
    # it seems unlikely to cause a false negative.
    lim = 100
    actual_sub = actual.head(lim)
    exp_sub = exp.head(lim)
    eq = actual_sub.equals(exp_sub)
    if eq:
        return
    # Okay, so they weren't equal. Let's try to come up with a helpful message about
    # how they disagree. (TODO: I wonder if someone has written code for this already
    # somewhere. Seems like it would be useful for unit testing, for example.)
    assert_has_columns(actual, exp.columns, name, strict=True)
    # TODO: Check index equality? Check equality of values column by column? 
    # Check dtype match per column. (This is something that df.equals cares about,
    # though in some cases that might be stricter than what we want. e.g. we might 
    # not care if a column has values [1, 2, 3] in expected and [1., 2., 3.] in actual)
    assert False, "Incorrect value for dataframe{}".format(' `{}`'.format(name) if name else '')

def assert_series_equals(actual, exp, name=None):
    # TODO: Would be nice to standardize on variable names being wrapped in backticks 
    # at the top of the call stack, so that e.g. we can call assert_isinstance with
    # a default name like "series" and not have it wrapped in backticks.
    # TODO: Actually, maybe name should be mandatory for these functions?
    actual_name = name or 'series'
    assert_isinstance(pd.Series, **{actual_name: actual, "_expected_value": exp})
    actual_name = '`{}`'.format(name) if name else "series"
    assert len(actual) == len(exp), "Expected {} to have length {} but was actually {}".format(
        actual_name, len(exp), len(actual))
    lim = 100
    actual_sub = actual.head(lim)
    exp_sub = exp.head(lim)
    eq = actual_sub.equals(exp_sub)
    if eq:
        return
    # We now they're unequal, now just need to explain why
    assert actual.name == exp.name, "Expected {} to have name=`{}` not `{}`".format(
            actual_name, exp.name, actual.name)
    # TODO: More checks
    assert False, "Incorrect value for {}".format(actual_name)

# For star import purposes, export only names that begin with assert (i.e. our helper fns)
__all__ = [name for name in dir() if name.startswith('assert')]
