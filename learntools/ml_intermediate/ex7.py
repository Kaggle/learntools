from learntools.core import *

class DataScienceOfShoelaces(ThoughtExperiment):
    _solution = ("This is tricky, and it depends on details of how data is collected "
                 "(which is common when thinking about leakage). "
                 "Would you at the beginning of the month decide how much leather will "
                 "be used that month? "
                 "If so, this is ok. But if that is determined during the month, you "
                 "would not have access to it when you make the prediction. "
                 "If you have a guess at the beginning of the month, and it is "
                 "subsequently changed during the month, the actual amount used "
                 "during the month cannot be used as a feature (because it causes leakage).")

class RevengeOfShoelaces(ThoughtExperiment):
    _solution = ("This could be fine, but it depends on whether they order shoelaces first "
                 "or leather first. If they order shoelaces first, you won't know how much "
                 "leather they've ordered when you predict their shoelace needs. "
                 "If they order leather first, then you'll have that number available when "
                 "you place your shoelace order, and you should be ok.")

class CryptoWealthJK(ThoughtExperiment):
    _solution = ("There is no source of leakage here. These features should be available "
                 "at the moment you want to make a predition, and they're unlikely to be "
                 "changed in the training data after the prediction target is determined. "
                 "But, the way he describes accuracy could be misleading if you aren't "
                 "careful. If the price moves gradually, today's price will be an accurate "
                 "predictor of tomorrow's price, but it may not tell you whether it's a "
                 "good time to invest. For instance, if it is $100 today, a model predicting "
                 "a price of $100 tomorrow may seem accurate, even if it can't tell you "
                 "whether the price is going up or down from the current price. A better "
                 "prediction target would be the change in price over the next day. "
                 "If you can consistently predict whether the price is about to go up or "
                 "down (and by how much), you may have a winning investment opportunity.")

class PreventingInfections(ThoughtExperiment):
    _solution = ("This poses a risk of both target leakage and train-test contamination (though "
                 "you may be able to avoid both if you are careful).\n\nYou have target leakage if "
                 "a given patient's outcome contributes to the infection rate for his surgeon, "
                 "which is then plugged back into the prediction model for whether that patient "
                 "becomes infected. You can avoid target leakage if you calculate the surgeon's infection "
                 "rate by using only the surgeries before the patient we are predicting for. "
                 "Calculating this for each surgery in your training data may be a little tricky.\n\n"
                 "You also have a train-test contamination problem if you calculate this using all "
                 "surgeries a surgeon performed, including those from the test-set. The result "
                 "would be that your model could look very accurate on the test set, even if it "
                 "wouldn't generalize well to new patients after the model is deployed. This would "
                 "happen because the surgeon-risk feature accounts for data in the test set. "
                 "Test sets exist to estimate how the model will do when seeing new data. So this "
                 "contamination defeats the purpose of the test set.")

class HomeAgainLeakage(CodingProblem):
    _vars = ['potential_leakage_feature']
    _hint = ("Which of these features might be updated in a database after the house is \
    sold? That's the one to worry about.")
    _solution = ("2 is the source of target leakage. Here is an analysis for each feature: "
                 "\n\n1. The size of a house is unlikely to be changed after it is sold (though "
                 "technically it's possible). But typically this will be available when we need "
                 "to make a prediction, and the data won't be modified after the home is sold. So it "
                 "is pretty safe. "
                 "\n\n2. We don't know the rules for when this is updated. If the field is updated "
                 "in the raw data after a home was sold, and the home's sale is used to calculate "
                 "the average, this constitutes a case of target leakage. "
                 "At an extreme, if only one home is sold in the neighborhood, and it is the home "
                 "we are trying to predict, then the average will be exactly equal to the value we are "
                 "trying to predict.  In general, for neighborhoods with few sales, the model will "
                 "perform very well on the training data.  But when you apply the model, "
                 "the home you are predicting won't have been sold yet, so this feature won't work the "
                 "same as it did in the training data. "
                 "\n\n3. These don't change, and will be available at the time we want to make a "
                 "prediction. So there's no risk of target leakage here. "
                 "\n\n4. This also doesn't change, and it is available at the time we want to make "
                 "a prediction. So there's no risk of target leakage here.")

    def check(self, potential_leakage_feature):
        assert type(potential_leakage_feature) == int, \
        "Your answer should be a number (integer), not a {}".format(type(potential_leakage_feature))

        assert potential_leakage_feature == 2, \
        "Try again. It is not feature {}".format(potential_leakage_feature)

qvars = bind_exercises(globals(), [
    DataScienceOfShoelaces,
    RevengeOfShoelaces,
    CryptoWealthJK,
    PreventingInfections,
    HomeAgainLeakage,
    ],
    var_format='q_{n}',
    )
__all__ = list(qvars)
