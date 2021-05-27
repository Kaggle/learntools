from learntools.core import *
    
class VarietiesOfFairness(ThoughtExperiment):
    _hint = ""
    _solution = ""
    _congrats = "Solution"
    _correct_message = ("All of the fairness criteria are unfairly biased in favor of Group B. 79.01% of "
                        "applicants are from Group B -- if demographic parity is our fairness criterion, fair "
                        "would mean that 50% of the applicants are from Group B. The model is also slightly "
                        "more accurate for applicants from Group B (with accuracy of 95.02%, vs 94.56% for Group "
                        "A). The true positive rate is very high for Group B (98.03%, vs. 77.23% for Group A). "
                        "In other words, for Group B, almost all people who should be approved are actually approved. "
                        "For Group A, if you should be approved, your chances of actually being approved are much lower.")
    
class BaselineModel(ThoughtExperiment):
    _hint = ""
    _solution = ""
    _congrats = "Solution"
    _correct_message = ("For all applicants with income between 71909.5 and 88440.5, the model's decision depends on "
                        "group membership: the model approves applicants from Group B and denies applicants from Group "
                        "A.  Since we want the model to treat individuals from Group A and Group B fairly, this is "
                        "clearly a bad model.  Although this data is very simple, in practice, with much larger data, "
                        "visualizing the how a model makes decisions can be very useful to more deeply understand what "
                        "might be going wrong with a model.")
    
class VarietiesOfFairnessTwo(ThoughtExperiment):
    _hint = ""
    _solution = ""
    _congrats = "Solution"
    _correct_message = ("When we consider demographic parity, the new model is still biased in favor of Group B, "
                        "but is now a bit more fair than the original model. But now, if you consider either "
                        "equal accuracy or equal opportunity, the model is biased in favor of Group A! It's also "
                        "important to note that the overall accuracy of the model has dropped -- for each group, "
                        "the model is making slightly less accurate decisions.")

class VarietiesOfFairnessThree(ThoughtExperiment):
    _hint = ""
    _solution = ""
    _congrats = "Solution"
    _correct_message = ("This model acheives nearly equal representation in the pool of approved applicants from "
                        "each group -- if demographic parity is what we care about, then this model is "
                        "much more fair than the first two models. Accuracy is roughly the same for each group, "
                        "but there is a substantial drop in overall accuracy for each group. If we examine the model for "
                        "equal opportunity fairness, the model is biased in favor of Group A: all individuals from "
                        "Group A who should be approved are approved, whereas only 63% of individuals from Group B "
                        "who should be approved are approved.  (This is similar to the dynamic in the first model, "
                        "with the favored group switched -- that is, in the first model, nearly all individuals "
                        "from Group B who should be approved were approved by the model.")

qvars = bind_exercises(globals(), [
    VarietiesOfFairness, BaselineModel, VarietiesOfFairnessTwo, VarietiesOfFairnessThree],
    var_format='q_{n}',
    )
__all__ = list(qvars)
