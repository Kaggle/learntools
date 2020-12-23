from learntools.core import *
    
class TryOut(ThoughtExperiment):
    _hint = ""
    _solution = ""
    _congrats = ""
    _correct_message = ""
    
class MostToxic(ThoughtExperiment):
    _hint = ""
    _solution = ""
    _congrats = "Solution"
    _correct_message = "None of the words are surprising.  They are all clearly toxic."
    
class CloserInvestigation(ThoughtExperiment):
    _hint = ""
    _solution = ""
    _congrats = ""
    _correct_message = ""

class IdentifyBias(ThoughtExperiment):
    _hint = ""
    _solution = ""
    _congrats = "Solution"
    _correct_message = ("The comment `I have a muslim friend` was marked as toxic, whereas "
                        "`I have a christian friend` was not.  Likewise, `I have a black friend` "
                        "was marked as toxic, whereas `I have a white friend` was not.  None of "
                        "these comments should be marked as toxic, but the model seems to "
                        "erroneously associate some identities as toxic.  This is a sign of bias "
                        "in the model: the model seems biased in favor of `christian` and against "
                        "`muslim`, and it seems biased in favor of `white` and against `black`.")

class TestUnderstanding(ThoughtExperiment):
    _hint = ""
    _solution = ""
    _congrats = "Solution"
    _correct_message = ("Each question is addressed in a separate bullet point:\n"
                        "- The first case, where comments that refer to Islam are likely to be toxic, is due to a flawed state of the world (and specifically, of this specific online community).  This can introduce **historical bias** to the model.\n"
                        "- The second case, where comments are translated to English, will likely introduce additional error when classifying non-English comments.  This can introduce **measurement bias** (since non-English comments will often not be translated perfectly) and **aggregation bias** (if comments are separated by language, the model is likely to be more accurate) to the model.\n"
                       "- The third case, where the model is evaluated based on comments from users in the United Kingdom, yet deployed to users in Australia will lead to a model that suffers from **evaluation bias** and **deployment bias**.  The model will also have **representation bias**, because it was built to serve users in Australia, but was trained with data from users based in the United Kingdom.")

qvars = bind_exercises(globals(), [
    TryOut, MostToxic, CloserInvestigation, IdentifyBias, TestUnderstanding
    ],
    var_format='q_{n}',
    )
__all__ = list(qvars)
