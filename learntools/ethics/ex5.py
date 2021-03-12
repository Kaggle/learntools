from learntools.core import *
    
class TryOut(ThoughtExperiment):
    _hint = ""
    _solution = ""
    _congrats = "Solution"
    _correct_message = ("Your model card should be written for the groups that are most likely to read "
                        "it. Such groups probably include wildfire management professionals, image "
                        "recognition analysts, researchers, policymakers and developers of similar AI "
                        "systems. The model card may therefore assume some knowledge of wildfire management and of AI systems.")
    
class MostToxic(ThoughtExperiment):
    _hint = ""
    _solution = ""
    _congrats = "Solution"
    _correct_message = "The answer is **Quantitative Analyses**."
    
class SpeechToText(ThoughtExperiment):
    _hint = ""
    _solution = ""
    _congrats = "Solution"
    _correct_message = "The answer is **Intended Use**."
    
qvars = bind_exercises(globals(), [
    TryOut, MostToxic, SpeechToText
    ],
    var_format='q_{n}',
    )
__all__ = list(qvars)
