import enum
from IPython.display import display, Javascript
import json

import learntools

# If set to True, then echo logged events as output.
DEBUG = False

class InteractionType(enum.Enum):
    CHECK = 1
    HINT = 2
    SOLUTION = 3

class OutcomeType(enum.Enum):
    PASS = 1
    FAIL = 2
    EXCEPTION = 3
    UNATTEMPTED = 4

class QuestionType(enum.Enum):
    EQUALITYCHECKPROBLEM = 1
    CODINGPROBLEM = 2
    FUNCTIONPROBLEM = 3
    THOUGHTEXPERIMENT = 4

_EVENT_DEFAULTS = dict(
        learnToolsVersion = str(learntools.__version__),
        valueTowardsCompletion = 0.0,
        failureMessage = '',
        exceptionClass = '',
        trace = '',
)

def track(event):
    # TODO: could be nice to put some validation logic here.
    for k, v in _EVENT_DEFAULTS.items():
        event.setdefault(k, v)

    # Convert enum values to plain ints
    interaction_type = event['interactionType']
    assert interaction_type in InteractionType
    event['interactionType'] = interaction_type.value
    outcome_type = event.get('outcomeType', None)
    if outcome_type:
        assert outcome_type in OutcomeType
        event['outcomeType'] = outcome_type.value
    else:
        assert interaction_type != InteractionType.CHECK, "Check events must have an OutcomeType set: {!r}".format(event)
        # Looks like we need to set some dummy value here (even if this field isn't applicable because this
        # isn't a check event. Setting outcomeType to None/null resulted in 500 errors.)
        event['outcomeType'] = 4

    question_type = event.get('questionType', None)
    if question_type:
        assert question_type in QuestionType
        event['questionType'] = question_type.value

    message = dict(jupyterEvent='custom.exercise_interaction',
            data=event)
    js = 'parent.postMessage({}, "*")'.format(json.dumps(message))
    display(Javascript(js))
    if DEBUG:
        debug_js = 'console.log({})'.format(json.dumps(message))
        display(Javascript(debug_js))
        display(message)

