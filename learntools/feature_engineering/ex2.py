import pandas as pd

from learntools.core import *


def get_data_splits(dataframe, valid_fraction=0.1):
    """ Splits a dataframe into train, validation, and test sets. First, orders by 
        the column 'click_time'. Set the size of the validation and test sets with
        the valid_fraction keyword argument.
    """

    dataframe = dataframe.sort_values('click_time')
    valid_rows = int(len(dataframe) * valid_fraction)
    train = dataframe[:-valid_rows * 2]
    # valid size == test size, last two sections of the data
    valid = dataframe[-valid_rows * 2:-valid_rows]
    test = dataframe[-valid_rows:]
    
    return train, valid, test

class LeakageQuestion(ThoughtExperiment):
    _solution = ("You should be calculating the encodings from the training set only. "
                 "If you include data from the validation and test sets into this, you'll "                
                 "end up overestimating the model's performance. You should in general be "
                 "vigilant to avoid leakage, that is, including any information from the "
                 "validation and test sets into the model."
                )

class CountEncodings(CodingProblem):
    _vars = ['clicks', 'count_enc', 'train', 'valid']
    _hint = ("CountEncoder works like scikit-learn classes with a `.fit` method to calculate "
    "counts and a `.transform` method to apply the encoding. You can join two dataframes with the same "
    "index using `.join` and add suffixes to columns names with `.add_suffix`")
    _solution = CS("""
    # Create the count encoder
    count_enc = CountEncoder()

    # Learn encoding from the training set
    count_enc.fit(train[cat_features])

    # Apply encoding to the train and validation sets
    train = train.join(count_enc.transform(train[cat_features]).add_suffix('_count'))
    valid = valid.join(count_enc.transform(valid[cat_features]).add_suffix('_count'))
    """) 

    def check(self, clicks, count_enc, train_, valid_):
        cat_features = ['ip', 'app', 'device', 'os', 'channel']
        train, valid, _ = get_data_splits(clicks)

        # Learn encoding from the training set
        count_enc.fit(train[cat_features])

        # Apply encoding to the train and validation sets
        train = train.join(count_enc.transform(train[cat_features]).add_suffix('_count'))
        valid = valid.join(count_enc.transform(valid[cat_features]).add_suffix('_count'))
        
        suffix_count = 0
        for each in train_.columns:
            suffix_count += 1 if each.endswith("_count") else 0
        assert suffix_count == 5, "Be sure to add the _count suffix to the new column names"

        suffix_count = 0
        for each in valid_.columns:
            suffix_count += 1 if each.endswith("_count") else 0
        assert suffix_count == 5, "Be sure to add the _count suffix to the new column names"

        assert train_.equals(train), "Train features don't seem to be right"
        assert valid_.equals(valid), "Validation features don't seem to be right"

class TargetEncodings(CodingProblem):
    _vars = ['clicks', 'target_enc', 'train', 'valid']
    _hint = ("TargetEncoder works like scikit-learn classes with a `.fit` method to learn the "
    "encoding and a `.transform` method to apply the encoding. Also note that you'll need to tell it "
    "which columns are categorical variables.")
    _solution = CS("""
    # Have to tell it which features are categorical when they aren't strings
    target_enc = ce.TargetEncoder(cols=cat_features)

    # Learn encoding from the training set
    target_enc.fit(train[cat_features], train['is_attributed'])

    # Apply encoding to the train and validation sets
    train = train.join(target_enc.transform(train[cat_features]).add_suffix('_target'))
    valid = valid.join(target_enc.transform(valid[cat_features]).add_suffix('_target'))
    """) 

    def check(self, clicks, target_enc, train_, valid_):
        cat_features = ['ip', 'app', 'device', 'os', 'channel']
        train, valid, _ = get_data_splits(clicks)

        # Learn encoding from the training set
        target_enc.fit(train[cat_features], train['is_attributed'])

        # Apply encoding to the train and validation sets
        train = train.join(target_enc.transform(train[cat_features]).add_suffix('_target'))
        valid = valid.join(target_enc.transform(valid[cat_features]).add_suffix('_target'))
        
        suffix_count = 0
        for each in train_.columns:
            suffix_count += 1 if each.endswith("_target") else 0
        assert suffix_count == 5, "Be sure to add the _target suffix to the new column names"

        suffix_count = 0
        for each in valid_.columns:
            suffix_count += 1 if each.endswith("_target") else 0
        assert suffix_count == 5, "Be sure to add the _target suffix to the new column names"

        #print(train_.head())
        #print(train.head())
        assert train_.equals(train), "Train features don't seem to be right"
        assert valid_.equals(valid), "Validation features don't seem to be right"

class RemoveIPEncoding(ThoughtExperiment):
    _solution = """
    (This is my guess) Target encoding attempts to measure the population mean of the target for each 
    level in a categorical feature. This means when there is less data per level, the estimated mean 
    will be further, there will be more variance. There is little data per IP address so it's likely 
    that the estimates are much noisier than for the other features. Going forward, we'll leave out the 
    IP feature when trying different encodings.
    """


class LeaveOneOutEncodings(CodingProblem):
    _vars = ['clicks', 'loo_enc', 'train', 'valid']
    _hint = ("LeaveoneOutEncoder works like scikit-learn classes with a `.fit` method to learn the "
    "encoding and a `.transform` method to apply the encoding. Also note that you'll need to tell it "
    "which columns are categorical variables.")
    _solution = CS("""
    # Have to tell it which features are categorical when they aren't strings
    loo_enc = ce.LeaveOneOutEncoder(cols=cat_features, random_state=7)

    # Learn encoding from the training set
    loo_enc.fit(train[cat_features], train['is_attributed'])

    # Apply encoding to the train and validation sets
    train = train.join(loo_enc.transform(train[cat_features]).add_suffix('_loo'))
    valid = valid.join(loo_enc.transform(valid[cat_features]).add_suffix('_loo'))
    """) 

    def check(self, clicks, loo_enc, train_, valid_):
        cat_features = ['app', 'device', 'os', 'channel']
        train, valid, _ = get_data_splits(clicks)

        loo_enc.fit(train[cat_features], train['is_attributed'])

        train = train.join(loo_enc.transform(train[cat_features]).add_suffix('_loo'))
        valid = valid.join(loo_enc.transform(valid[cat_features]).add_suffix('_loo'))
        
        suffix_count = 0
        for each in train_.columns:
            suffix_count += 1 if each.endswith("_loo") else 0
        assert suffix_count == 4, "Be sure to add the _loo suffix to the new column names"

        suffix_count = 0
        for each in valid_.columns:
            suffix_count += 1 if each.endswith("_loo") else 0
        assert suffix_count == 4, "Be sure to add the _loo suffix to the new column names"

        assert train_.equals(train), "Train features don't seem to be right"
        assert valid_.equals(valid), "Validation features don't seem to be right"

class CatBoostEncodings(CodingProblem):
    _vars = ['clicks', 'ce', 'train', 'valid']
    _hint = ("CatBoostEncoder works like scikit-learn classes with a `.fit` method to learn the "
    "encoding and a `.transform` method to apply the encoding. Also note that you'll need to tell it "
    "which columns are categorical variables.")
    _solution = CS("""
    # Have to tell it which features are categorical when they aren't strings
    loo_enc = ce.CatBoostEncoder(cols=cat_features, random_state=7)

    # Learn encoding from the training set
    loo_enc.fit(train[cat_features], train['is_attributed'])

    # Apply encoding to the train and validation sets
    train = train.join(loo_enc.transform(train[cat_features]).add_suffix('_cb'))
    valid = valid.join(loo_enc.transform(valid[cat_features]).add_suffix('_cb'))
    """) 

    def check(self, clicks, ce, train_, valid_):
        cat_features = ['app', 'device', 'os', 'channel']
        train, valid, _ = get_data_splits(clicks)

        # CatBoostEncoder permutes the data every time you .fit. So have to create
        # a new encoder here to match the new encoder the student makes.
        cb_enc = ce.CatBoostEncoder(cols=cat_features, random_state=7)
        cb_enc.fit(train[cat_features], train['is_attributed'])

        train = train.join(cb_enc.transform(train[cat_features]).add_suffix('_cb'))
        valid = valid.join(cb_enc.transform(valid[cat_features]).add_suffix('_cb'))
        
        suffix_count = 0
        for each in train_.columns:
            suffix_count += 1 if each.endswith("_cb") else 0
        assert suffix_count == 4, "Be sure to add the _cb suffix to the new column names"

        suffix_count = 0
        for each in valid_.columns:
            suffix_count += 1 if each.endswith("_cb") else 0
        assert suffix_count == 4, "Be sure to add the _cb suffix to the new column names"

        assert train_.equals(train), "Train features don't seem to be right"
        assert valid_.equals(valid), "Validation features don't seem to be right"

class LearnSVDEmbeddings(CodingProblem):
    _vars = ['svd', 'svd_components', 'train']
    _hint = ("You can count up co-occurences of categorical values using a groupby operation. This "
             "will create a DataFrame or Series with a multi-index with a level for each categorical variable. "
             "To convert this to a matrix, you can use the `unstack` method. For each matrix, fit the "
             "SVD transformer and save the learned components to the dictionary. ")
    _solution = CS(""" 
    svd = TruncatedSVD(n_components=5)
    # Loop through each pair of categorical features
    for col1, col2 in itertools.permutations(cat_features, 2):
        # For a pair, create a sparse matrix with cooccurence counts
        pair_counts = train.groupby([col1, col2])['is_attributed'].count()
        # Unstack the counts in a matrix
        pair_matrix = pair_counts.unstack(fill_value=0)
        
        # Fit the SVD and store the components
        # Note: these components represent column 2
        svd.fit(pair_matrix)
        svd_components['_'.join([col2, col1])] = pd.DataFrame(svd.components_)""")

    def check(self, svd, svd_components, train):

        assert svd.n_components == 5, "Please set the number of SVD components to 5"

        from itertools import permutations
        
        cat_features = ['app', 'device', 'os', 'channel']
        svd_components_ = {}

        # Loop through each pair of categorical features
        for col1, col2 in permutations(cat_features, 2):
            # For a pair, create a sparse matrix with cooccurence counts
            pair_counts = train.groupby([col1, col2])['is_attributed'].count()
            pair_matrix = pair_counts.unstack(fill_value=0)
            
            # Fit the SVD and store the components
            # Note: these components represent column 2
            svd.fit(pair_matrix)
            svd_components_['_'.join([col2, col1])] = pd.DataFrame(svd.components_)

        assert svd_components.keys() == svd_components_.keys()

        for pair in svd_components:
            assert svd_components[pair].equals(svd_components_[pair]), f"Something wrong with {pair}"


class ApplySVDEncoding(CodingProblem):
    _vars = ['svd_components', 'svd_encodings', 'clicks']
    _hint = ("TODO")
    _solution=CS("""
    svd_encodings = pd.DataFrame(index=clicks.index)
    for feature in svd_components:
        # Get the feature column the SVD components are encoding
        col = feature.split('_')[0]

        ## Use SVD components to encode the categorical features
        # Need to transpose so .reindex works appropriately
        feature_components = svd_components[feature].transpose()
        comp_cols = feature_components.reindex(clicks[col]).set_index(clicks.index)
        
        # Doing this so we know what these features are
        comp_cols = comp_cols.add_prefix(feature + '_svd_')
        
        svd_encodings = svd_encodings.join(comp_cols)
    """)

    def check(self, svd_components, svd_encodings_, clicks):
        svd_encodings = pd.DataFrame(index=clicks.index)
        for feature in svd_components:
            # Get the feature column the SVD components are encoding
            col = feature.split('_')[0]

            ## Use SVD components to encode the categorical features
            # Need to transpose so .reindex works appropriately
            feature_components = svd_components[feature].transpose()
            comp_cols = feature_components.reindex(clicks[col]).set_index(clicks.index)
            
            # Doing this so we know what these features are
            comp_cols = comp_cols.add_prefix(feature + '_svd_')
            
            svd_encodings = svd_encodings.join(comp_cols)


        # Fill null values with the mean
        svd_encodings = svd_encodings.fillna(svd_encodings.mean())

        assert svd_encodings.equals(svd_encodings_)
        

qvars = bind_exercises(globals(), [
    LeakageQuestion,
    CountEncodings,
    TargetEncodings,
    RemoveIPEncoding,
    LeaveOneOutEncodings,
    CatBoostEncodings,
    LearnSVDEmbeddings,
    ApplySVDEncoding
    ],
    tutorial_id=262,
    var_format='q_{n}',
    )
__all__ = list(qvars)