import enum
from IPython.display import display, Javascript
import json

import learntools

class InteractionType(enum.Enum):
    CHECK = 1
    HINT = 2
    SOLUTION = 3

class OutcomeType(enum.Enum):
    PASS = 1
    FAIL = 2
    EXCEPTION = 3
    UNATTEMPTED = 4

_EVENT_DEFAULTS = dict(
        learnToolsVersion = str(learntools.__version__),
        valueTowardsCompletion = 0.0, # technically optional
        failureMessage = '',
        exceptionClass = '',
        trace = '',
)

def track(event):
    # TODO: could be nice to put some validation logic here.
    for k, v in _EVENT_DEFAULTS.items():
        event.setdefault(k, v)

    # Convert enum values to plain ints
    intxn_type = event['interactionType']
    assert intxn_type in InteractionType
    event['interactionType'] = intxn_type.value
    outcome_type = event.get('outcomeType', None)
    if outcome_type:
        assert outcome_type in OutcomeType
        event['outcomeType'] = outcome_type.value

    message = dict(jupyterEvent='custom.exercise_interaction',
            data=event)
    js = 'parent.postMessage({}, "*")'.format(json.dumps(message))
    display(Javascript(js))

