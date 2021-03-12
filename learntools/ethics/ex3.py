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
                        "erroneously associate some identities as toxic.  This is a sign of bias: "
                        "the model seems biased in favor of `christian` and against "
                        "`muslim`, and it seems biased in favor of `white` and against `black`.")

class TestUnderstanding(ThoughtExperiment):
    _hint = ""
    _solution = ""
    _congrats = "Solution"
    _correct_message = ("Comments that refer to Islam are more likely to be classified as toxic, because of a flawed state of the online community where the data was collected.  This can introduce **historical bias**.")
    
class TestUnderstandingTwo(ThoughtExperiment):
    _hint = ""
    _solution = ""
    _congrats = "Solution"
    _correct_message = ("By translating comments to English, we introduce additional error when classifying non-English comments.  This can introduce **measurement bias**, since non-English comments will often not be translated perfectly.  It could also introduce **aggregation bias**: the model would likely perform better for comments expressed in all languages, if the comments from different languages were treated differently.")
    
class TestUnderstandingThree(ThoughtExperiment):
    _hint = ""
    _solution = ""
    _congrats = "Solution"
    _correct_message = ("If the model is evaluated based on comments from users in the United Kingdom and deployed to users in Australia, this will lead to **evaluation bias** and **deployment bias**.  The model will also have **representation bias**, because it was built to serve users in Australia, but was trained with data from users based in the United Kingdom.")

qvars = bind_exercises(globals(), [
    TryOut, MostToxic, CloserInvestigation, IdentifyBias, TestUnderstanding, TestUnderstandingTwo, TestUnderstandingThree
    ],
    var_format='q_{n}',
    )
__all__ = list(qvars)
