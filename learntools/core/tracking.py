import enum
from IPython.display import display, Javascript
import json
import learntools
import os

# If set to True, then echo logged events as output.
DEBUG = False

USE_KAGGLESDK = os.environ.get('LEARN_USE_KAGGLE_SDK') == 'True'
if USE_KAGGLESDK:
    from kagglesdk import KaggleClient
    from kagglesdk.education.types.education_api_service import ApiTrackExerciseInteractionRequest
    from kagglesdk.education.types.education_service import LearnExerciseInteractionType, LearnExerciseOutcomeType, LearnExerciseQuestionType

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

def interaction_type_to_kagglesdk(event):
  switch = {
      InteractionType.CHECK: LearnExerciseInteractionType.CHECK,
      InteractionType.HINT: LearnExerciseInteractionType.HINT,
      InteractionType.SOLUTION: LearnExerciseInteractionType.SOLUTION,
  }
  value = event['interactionType']
  assert value in switch
  return switch.get(value)

def outcome_type_to_kagglesdk(interaction_type, event):
    switch = {
        OutcomeType.PASS: LearnExerciseOutcomeType.PASS,
        OutcomeType.FAIL: LearnExerciseOutcomeType.FAIL,
        OutcomeType.EXCEPTION: LearnExerciseOutcomeType.EXCEPTION,
        OutcomeType.UNATTEMPTED: LearnExerciseOutcomeType.UNATTEMPTED,
    }

    value = event.get('outcomeType', None)
    if value:
        assert value in switch
        return switch.get(value)
    else:
        assert interaction_type != LearnExerciseInteractionType.CHECK, "Check events must have an OutcomeType set: {!r}".format(event)
        return LearnExerciseOutcomeType.LEARN_EXERCISE_OUTCOME_TYPE_UNSPECIFIED

def question_type_to_kagglesdk(event):
    switch = {
        QuestionType.EQUALITYCHECKPROBLEM: LearnExerciseQuestionType.EQUALITY_CHECK_PROBLEM,
        QuestionType.CODINGPROBLEM: LearnExerciseQuestionType.CODING_PROBLEM,
        QuestionType.FUNCTIONPROBLEM: LearnExerciseQuestionType.FUNCTION_PROBLEM,
        QuestionType.THOUGHTEXPERIMENT: LearnExerciseQuestionType.THOUGHT_EXPERIMENT,
    }

    question_type = event.get('questionType', None)
    if question_type:
        assert question_type in switch
        return switch.get(question_type)
    return None

def track_using_kagglesdk(event):
    request = ApiTrackExerciseInteractionRequest()
    request.learn_tools_version = str(learntools.__version__)
    request.value_towards_completion = event.get('valueTowardsCompletion', 0.0)
    request.interaction_type = interaction_type_to_kagglesdk(event)
    request.outcome_type = outcome_type_to_kagglesdk(request.interaction_type, event)
    request.fork_parent_kernel_session_id = os.environ.get('KAGGLE_LEARN_SESSION_ID')

    question_type = question_type_to_kagglesdk(event)
    if question_type:
        request.question_type = question_type

    client = KaggleClient()
    result = client.education.education_api_client.track_exercise_interaction(request)

    # Post the result back to the outer frame. When running in Kaggle
    # Notebooks, the outer frame is listening for this message and may show a
    # nudge.
    message = dict(
        jupyterEvent='custom.exercise_interaction_result',
        data=result.to_json())
    js = 'parent.postMessage({}, "*")'.format(json.dumps(message))
    display(Javascript(js))


def track_using_iframe(event):
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

def track(event):
    if USE_KAGGLESDK:
        track_using_kagglesdk(event)
    else:
        track_using_iframe(event)
    