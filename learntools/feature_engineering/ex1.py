from sklearn import preprocessing

from learntools.core import *

class TimestampFeatures(CodingProblem):
    _vars = ['clicks', 'click_data']
    _hint = ("With a timestamp column in a dataframe, you can get access to "
             "datetime attibutes and functions with the `.dt` attribute. For "
             "example `tscolumn.dt.day` will convert a timestamp column to days")
    _solution = CS(
    """
    clicks = click_data.assign(day=click_times.dt.day.astype('uint8'),
                               hour=click_times.dt.hour.astype('uint8'), 
                               minute=click_times.dt.minute.astype('uint8'),
                               second=click_times.dt.second.astype('uint8'))
    """)
    
    def check(self, clicks, click_data):
        click_times = click_data['click_time']
        solution = click_data.assign(day=click_times.dt.day.astype('uint8'),
                                     hour=click_times.dt.hour.astype('uint8'), 
                                     minute=click_times.dt.minute.astype('uint8'),
                                     second=click_times.dt.second.astype('uint8'))

        

        assert (solution.drop('attributed_time', axis=1) == 
                clicks.drop('attributed_time', axis=1)).all().all()

class LabelEncoding(CodingProblem):
    _var = 'clicks'
    _hint = ("Try looping through each of the categorical features and using the "
             " using LabelEncoder's .fit_transform method")
    _solution = CS(
    """
    label_encoder = preprocessing.LabelEncoder()
    for feature in cat_features:
        encoded = label_encoder.fit_transform(clicks[feature])
        clicks[feature + '_labels'] = encoded
    """
    )

    def check(self, clicks):
        cat_features = ['ip', 'app', 'device', 'os', 'channel']
        label_encoder = preprocessing.LabelEncoder()
        

        for feature in cat_features:
            encoded = label_encoder.fit_transform(clicks[feature])
            message = f"The {feature} column isn't encoded properly."
            assert (clicks[feature + '_labels'] == encoded).all(), message

class OnehotEncoding(ThoughtExperiment):
    _solution = """
    The `ip_labels` column has 58,000 values, which means it will create
    an extremely sparse matrix with 58,000 columns. Generally a bad idea. 
    Luckily, LightGBM works well with label encoded features.
    """

class TrainTestSplits(ThoughtExperiment):
    _solution = """
    Since our model is meant to predict events in the future, we must also validate the
    model on events in the future. If the data is mixed up between the training and test 
    sets, then future data will leak in to the model and our validation results will 
    overestimate the performance on new data.
    """

class CreateSplits(CodingProblem):
    _vars = ['clicks', 'train', 'valid', 'test']
    _hint = ("You can sort dataframes with the `.sort_values` method. Then find how many rows "
             "are 10% of the data (as an integer) and use that to slice the dataframe "
             "appropriately. You can index starting from the end of the dataframe using negative "
             "values, for example `df[-1000:]` will return the last 1000 rows.")

    _solution = CS("""
    valid_fraction = 0.1
    clicks_srt = clicks.sort_values('click_time')
    valid_rows = int(len(clicks_srt) * valid_fraction)
    train = clicks_srt[:-valid_rows * 2]
    # valid size == test size, last two sections of the data
    valid = clicks_srt[-valid_rows * 2:-valid_rows]
    test = clicks_srt[-valid_rows:]
    """)

    def check(self, clicks_, train_, valid_, test_):
        valid_fraction = 0.1
        clicks_srt = clicks_.sort_values('click_time')
        valid_rows = int(len(clicks_srt) * valid_fraction)
        train = clicks_srt[:-valid_rows * 2]
        # valid size == test size, last two sections of the data
        valid = clicks_srt[-valid_rows * 2:-valid_rows]
        test = clicks_srt[-valid_rows:]

        assert train_.shape == train.shape, "The train set isn't 80% of the data"
        assert valid_.shape == valid.shape, "The validation set isn't 10% of the data"
        assert test_.shape == test.shape, "The test set isn't 10% of the data"

        assert (train_['click_time'].values == train['click_time'].values).all(), (""
            "The click times aren't properly sorted in the train set")
        assert (valid_['click_time'].values == valid['click_time'].values).all(), (""
            "The click times aren't properly sorted in the validation set")
        assert (test_['click_time'].values == test['click_time'].values).all(), (""
            "The click times aren't properly sorted in the test set")

class EvaluateModel(EqualityCheckProblem):
    _var = "score"
    _expected = 0.9726727334566094
    _hint = ("Use the boosting model to make predictions bst.predict using the test data. "
    "Then, you can use roc_auc_score from the metrics module to calculate the AUC score. "
    "Also, be sure to calculate the score using the test dataset. ")
    _solution = CS("""
    ypred = bst.predict(valid[feature_cols])
    score = metrics.roc_auc_score(valid['is_attributed'], ypred)""")

qvars = bind_exercises(globals(), [
    TimestampFeatures,
    LabelEncoding,
    OnehotEncoding,
    TrainTestSplits,
    CreateSplits,
    EvaluateModel
    ],
    tutorial_id=262,
    var_format='q_{n}',
    )
__all__ = list(qvars)