import itertools

import pandas as pd
from sklearn import preprocessing

from learntools.core import *


class InteractionFeatures(CodingProblem):
    _vars = ['clicks', 'interactions']
    _hint = ("The easiest way to loop through the pairs is with itertools.combinations. "
             "Once you have that working, for each pair of columns convert them to strings "
             "then you can join them with the `+` operator. It's usually good to join with "
             "a symbol like _ inbetween to ensure unique values. Now you should have a column "
             "of new categorical values, you can label encoder those and add them to the "
             "DataFrame")
    _solution = CS("""
    cat_features = ['ip', 'app', 'device', 'os', 'channel']
    interactions = pd.DataFrame(index=clicks.index)
    for col1, col2 in itertools.combinations(cat_features, 2):
        new_col_name = '_'.join([col1, col2])

        # Convert to strings and combine
        new_values = clicks[col1].map(str) + "_" + clicks[col2].map(str)

        encoder = preprocessing.LabelEncoder()
        interactions[new_col_name] = encoder.fit_transform(new_values)
    """)

    def check(self, clicks, interactions_):
        # interactions_ is the student's version
        #%%RM_IF(PROD)%%
        cat_features = ['ip', 'app', 'device', 'os', 'channel']
        interactions = pd.DataFrame(index=clicks.index)
        for col1, col2 in itertools.combinations(cat_features, 2):
            new_col_name = '_'.join([col1, col2])
            # Convert to strings and combine
            new_values = clicks[col1].map(str) + "_" + clicks[col2].map(str)

            encoder = preprocessing.LabelEncoder()
            interactions[new_col_name] = encoder.fit_transform(new_values)

        assert interactions.equals(interactions_)

class PastEventsFeature(CodingProblem):
    _vars = ['count_past_events', 'clicks']
    _hint = ("You can get a rolling time window using .rolling(), but first you "
             "need to convert the index to a time series. The current row is "
             "included in the window, but we want to count all the events before "
             "the current row, so be sure to adjust the count.")
    _solution = CS("""
    def count_past_events(series):
        series = pd.Series(series.index, index=series)
        # Subtract 1 so the current event isn't counted
        past_events = series.rolling('6h').count() - 1
        return past_events
    """)

    def check(self, student_func, clicks):

        def count_past_events(series, time_window='6H'):
            series = pd.Series(series.index, index=series)
            # Subtract 1 so the current event isn't counted
            past_events = series.rolling(time_window).count() - 1
            return past_events

        sample = clicks[:100000]['click_time']

        soln_result = count_past_events(sample)
        student_result = student_func(sample)
        assert student_result is not ____, "Please implement the `count_past_events` function."

        message = ("Not quite right. Make sure to subtract one from the counts to "
                   "exclude the current row.")
        assert soln_result.equals(student_result), message

class FutureInformationQuestion(ThoughtExperiment):
    _solution = ("In general, you shouldn't use information from the future. When you're "
                "using models like this in a real-world scenario you won't have data from "
                "the future. Your model's score will likely be higher when training and "
                "testing on historical data, but it will overestimate the performance on real"
                " data. I should note that using future data will improve the score on Kaggle "
                "competition test data, but avoid it when building machine learning products.")

class LastEventFeature(CodingProblem):

    _vars = ["time_diff", "clicks"]
    _hint = "Try using the .diff() method on a time series."
    _solution = CS("""
    def time_diff(series):
            return series.diff().dt.total_seconds()
    """)

    def check(self, student_func, clicks):

        def time_diff(series):
            return series.diff().dt.total_seconds()

        sample = clicks[:100000]['click_time']

        soln_result = time_diff(sample)
        student_result = student_func(sample)
        assert student_result is not ____, "Please implement the `time_diff` function."

        assert soln_result.equals(student_result)


class PreviousAttributionsFeature(CodingProblem):

    _vars = ["previous_attributions", "clicks"]
    _hint = ("Here you want a window that always starts at the first row but "
             "expands as you get further in the data. You can use the `.expanding` "
             "methods for this. Also, the current row is included in the window, "
             "so you'll need to subtract that off as well")
    _solution = CS("""
    def previous_attributions(series):
        # Subtracting raw values so I don't count the current event
        sums = series.expanding(min_periods=2).sum() - series
        return sums
    """)

    def check(self, student_func, clicks):

        def previous_attributions(series):
            # Subtracting raw values so I don't count the current event
            sums = series.expanding(min_periods=2).sum() - series
            return sums

        sample = clicks[:1000000]['is_attributed']

        soln_result = previous_attributions(sample)
        student_result = student_func(sample)
        assert student_result is not ____, "Please implement the `previous_attributes` function"

        assert soln_result.equals(student_result)

class TreeVsDLModels(ThoughtExperiment):
    _solution = ("The features themselves will work for either model. However, "
                "numerical inputs to neural networks need to be standardized first. "
                "That is, the features need to be scaled such that they have 0 mean "
                "and a standard deviation of 1. This can be done using "
                "sklearn.preprocessing.StandardScaler.")

qvars = bind_exercises(globals(), [
    InteractionFeatures,
    PastEventsFeature,
    FutureInformationQuestion,
    LastEventFeature,
    PreviousAttributionsFeature,
    TreeVsDLModels
    ],
    var_format='q_{n}',
    )
__all__ = list(qvars)
