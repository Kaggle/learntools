from learntools.core import *

inputs = 50

# Data Preparation
class Q1(CodingProblem):
    _hint = ""
    _solution = ""
    def check(self):
        pass

class Q2(CodingProblem):
    _var = "input_shape"
    _hints = [
        "Think about whether you should look at the processed data `X_train` or the original data `fuel`.",
        "You should look at the processed data `X_train`, since that is the data actually going into the network. Since the target was already removed, you can just look at the second entry in `X_train.shape` (the columns) to find the number of features."
    ]
    _solution = CS("""
input_shape = [{inputs}]
# or,
input_shape = [X_train.shape[1]]
""".format(inputs=inputs))

    def check(self, input_shape):
        assert (type(input_shape) in [list, tuple]), \
            ("""The input shape should be a list (or tuple) with a single integer, like `[__]`.""")
        assert (input_shape[0] not in [13, 14]), \
            ("Look at the columns of `X_train` for the number of input features, since `X_train` (the processed data) is what is actually being used as input.")
        assert (len(input_shape) == 1), \
            ("""You should use a list of length 1 here. Each entry in the `input_shape` list says how many input values you have in that dimension. The inputs here are numbers (one dimensional) and so your answer should look something like:
```python
input_shape = [____]
```
""")
        assert (input_shape[0] == inputs), \
            ("The number of inputs should be {good_inputs}, but you gave {bad_inputs}".format(good_inputs=inputs, bad_inputs=input_shape[0]))


# Compile
class Q1(CodingProblem):
    _hint = """Your code should look something like:
```python
model.compile(
____,
____,
)
```
"""
    _solution = CS("""
model.compile(
    optimizer='adam',
    loss='mae'
)
""")
    _var = "model"
    def check(self, model):
        try:
            optimizer = model.optimizer.__class__.__name__
        except:
            optimizer = None
        try:
            loss = model.compiled_loss._losses
        except:
            loss = None
        assert (optimizer is not None), \
        ("You are missing the optimizer.")
        assert (loss is not None), \
        ("You are missing the loss.")
        assert (loss.lower() == 'mae'), \
            ("The loss should be `'mae'`. You gave `{}`".format(loss))
        assert (optimizer.lower() == 'adam'), \
            ("The optimizer should be `'adam'`. You gave `{}`".format(optimizer))

# Train the model
class Q2(CodingProblem):
    _hint = """
Your solution should look something like:
```python
history = model.fit(
    ____, # training data
    ____, # validation data
    ____, # batch size
    ____, # epochs
)
```

"""
    _solution = CS("""
history = model.fit(
    X_train, y_train,
    validation_data=(X_valid, y_valid),
    batch_size=128,
    epochs=100,
)
""")
    _var = "history"
    def check(self, history):
        # Epochs
        epochs = history.params['epochs']
        true_epochs = 200
        assert (epochs == true_epochs), \
            ("You have the incorrect number of epochs. You gave {}, but there should be {}.".format(epochs, true_epochs))

# Evaluate training
class Q3(ThoughtExperiment):
    _solution = "This depends on how the loss has evolved during training: if the learning curves have levelled off, there won't usually be any advantage to training for additional epochs.  Conversely, if the loss appears to still be decreasing, then training for longer could be advantageous."

# Learning rate and batch size
class Q4(ThoughtExperiment):
    _solution = """
You probably saw that smaller batch sizes gave noisier weight updates and loss curves. This is because each batch is a small *sample* of data and smaller samples tend to give noisier estimates. Smaller batches can have an "averaging" effect though which can be beneficial.

Smaller learning rates make the updates smaller and the training takes longer to converge. Large learning rates can speed up training, but don't "settle in" to a minimum as well. When the learning rate is too large, the training can fail completely. (Try setting the learning rate to a large value like 0.99 to see this.)
"""


qvars = bind_exercises(globals(), [
        Q1, Q2, Q3, Q4,
    ],
    var_format='q_{n}',
)
__all__ = list(qvars)
