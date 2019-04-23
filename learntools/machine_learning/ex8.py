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

qvars = bind_exercises(globals(), [
    CheckClassifierFit,
    CheckClassifierAccuracy
    ],
    tutorial_id=122,
    var_format='step_{n}',
    )
__all__ = list(qvars)