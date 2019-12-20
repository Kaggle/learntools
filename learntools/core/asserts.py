"""
Some assertion helpers used in Problem.check implementations.

These are most heavily used in EqualityCheckProblems. They have nice error messages, and thus could be
used in how we code check methods in CodingProblems, though that wasn't a widespread practice when
this comment was written in Dec 2019.
"""

import os
import numbers
import math
import functools
import logging

import pandas as pd
import numpy as np

def name_or_var(assert_fn):
    """
    Assert helpers marked with this decorator take a "name" argument, which is a
    markdown string describing the actual value being checked. It may be a generic
    name like "dataframe", or a prose description like "the result of calling `circle_area`",
    or a variable name wrapped in backticks.

    The latter case is extremely common, so this decorator adds an optional "var" keyword-arg
    to the function. Passing var="foo" is a convenient shorthand for name="`foo`". (If you
    pass a value for "var", you should not also pass a value for "name".)

    Example:

    @name_or_var
    def assert_negative(actual, name):
        assert actual < 0, "{} should have been negative, but was actually {}".format(name, actual)

    # The following are all valid calls
    assert_negative(x, "Bank balance")
    assert_negative(x, name="`Bank.balance` attribute")
    assert_negative(x, var="bank_balance") # Equivalent to assert_negative(x, "`bank_balance`")
    """
    @functools.wraps(assert_fn)
    def wrapped(*args, **kwargs):
        var = kwargs.pop('var', None)
        if var:
            if 'name' in kwargs:
                logging.warn("Function {} received values for keyword args name *and* var. Overwriting original name kwarg.".format(
                    assert_fn.__name__))
            kwargs['name'] = '`{}`'.format(var)
        return assert_fn(*args, **kwargs)
    return wrapped

@name_or_var
def assert_equal(actual, expected, name, failure_factory=None):
    """Assert a protean notion of equality specific to the use case of learntools
    checking. Subclasses of EqualityCheckProblem ultimately use this function
    in their check method.

    Includes special cases for several types of expected values, including Pandas
    objects, ndarrays, and floats.
    """
    # We default to == comparison, but have special cases for certain data types.
    if isinstance(expected, float):
        assert isinstance(actual, numbers.Number), \
            "Expected {} to be a number, but had value `{!r}` (type = `{}`)".format(
                name, actual, type(actual).__name__)
        check = math.isclose(actual, expected, rel_tol=1e-06)
    elif isinstance(expected, pd.DataFrame):
        assert_df_equals(actual, expected, name)
        return
    elif isinstance(expected, pd.Series):
        assert_series_equals(actual, expected, name)
        return
    elif isinstance(actual, np.ndarray) or isinstance(expected, np.ndarray):
        check = np.array_equal(actual, expected)
    else:
        check = actual == expected
    if failure_factory:
        # This optional kwarg lets the caller pass a function to generate a custom
        # failure message. Currently only used in the Python ex1 favourite color question.
        _failure_message = failure_factory(name, actual, expected)
    else:
        _failure_message = "Incorrect value for {}: `{}`".format(
                name, repr(actual))
    assert check, _failure_message

@name_or_var
def assert_has_columns(df, cols, name="dataframe", strict=False):
    """Assert that the given dataframe contains columns with the given names.
    If strict is True, then assert it has *only* those columns.
    """
    for col in cols:
        assert col in df.columns, "Expected {} to have column `{}`".format(
                name, col
                )
    if strict:
        for col in df.columns:
            msg = "Unexpected column in {}: `{}`".format(name, col)
            assert col in cols, msg

@name_or_var
def assert_isinstance(cls, actual, name):
    assert isinstance(actual, cls), "Expected {} to have type `{!r}` but had type `{!r}`".format(name, cls, type(actual))

@name_or_var
def assert_is_one_of(actual, options, name):
    msg = "Incorrect value for {}: `{!r}`".format(name, actual)
    assert actual in options, msg

@name_or_var
def assert_len(thing, exp_len, name):
    """Assert that the given thing has the given length.

    PRECONDITION: the thing implements __len__
    """
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

@name_or_var
def assert_df_equals(actual, exp, name="dataframe"):
    assert_isinstance(pd.DataFrame, actual, name)
    assert len(actual) == len(exp), "Expected {} to have length {} but was actually {}".format(
        name, len(exp), len(actual))
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
    assert False, "Incorrect value for {}".format(name)

@name_or_var
def assert_series_equals(actual, exp, name="series"):
    assert_isinstance(pd.Series, actual, name=name)
    assert len(actual) == len(exp), "Expected {} to have length {} but was actually {}".format(
        name, len(exp), len(actual))
    lim = 100
    actual_sub = actual.head(lim)
    exp_sub = exp.head(lim)
    eq = actual_sub.equals(exp_sub)
    if eq:
        return
    # TODO: More checks
    assert False, "Incorrect value for {}".format(name)

# For star import purposes, export only names that begin with assert (i.e. our helper fns)
__all__ = [name for name in dir() if name.startswith('assert')]
