import sklearn
from sklearn.ensemble import RandomForestClassifier
from learntools.core import *

class CheckClassifierFit(CodingProblem):

    _vars = ['model', 'val_X', 'val_y']
    _hint = 'Create a RandomForestClassifier and fit it to the training data. '
    _solution = CS("""# Define the model. Set random_state to 1
model = RandomForestClassifier(random_state=1)

# fit your model
model.fit(train_X, train_y)""")

    def check(self, model, val_X, val_y):
        assert isinstance(model, RandomForestClassifier), "Not using RandomForestClassifier as the model."
        assert model.random_state == 1, "Didn't set random_state to the right value when initializing the classifier"
        assert model.score(val_X, val_y) > 0.9, "Your model isn't quite as accurate as expected."

class CheckClassifierAccuracy(CodingProblem):

    _vars = ['accuracy']
    _hint = 'Get predictions with model.predict and use metrics.accuracy_score to calculate the accuracy on the validation data'
    _solution = CS("""# Get predictions from the trained model using the validation features
pred_y = model.predict(val_X)

# Calculate the accuracy of the trained model with the validation targets and predicted targets
accuracy = metrics.accuracy_score(val_y, pred_y)
""")
    def check(self, accuracy):
        assert accuracy < 0.99, "Accuracy is too high, did you use the validation data to calculate it?"
        assert accuracy > 0.9, "Accuracy seems too low, did you use the training data for fitting the model?"

class ConfusionMatrixQuestion(ThoughtExperiment):
    _solution = """
    The confusion matrix tells us that we're classifying around 82% of the pulsars correctly. The classifier
    missed 60 pulsars, about 18% of the pulsars in the data, instead classifiying them as noise. However,
    less than 1% of the noise examples were classified as pulsars. Given the small number of pulsars in the dataset,
    our classifier is doing pretty well. With some optimization of the model and data itself, it's likely
    you could improve the true positive rate for the pulsars.
    """

class UnbalancedClassesQuestion(ThoughtExperiment):
    _solution = """
    If your data is 99% noise, then you can easily get 99% accuracy just by classifying everything as noise. If your model
    is actually working, you'd expect to have an accuracy greater than 99%. It's important to look at the confusion matrix
    when you have unbalanced classes like this.
    """

qvars = bind_exercises(globals(), [
    CheckClassifierFit,
    CheckClassifierAccuracy,
    ConfusionMatrixQuestion,
    UnbalancedClassesQuestion
    ],
    var_format='step_{n}',
    )
__all__ = list(qvars)
