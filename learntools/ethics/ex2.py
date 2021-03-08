from learntools.core import *
    
class ReduceWaste(ThoughtExperiment):
    _hint = ""
    _solution = ""
    _congrats = "Solution"
    _correct_message = "These are all good ways to start!"
    
class DetectCancer(ThoughtExperiment):
    _hint = ""
    _solution = ""
    _congrats = "Solution"
    _correct_message = ("Yes, it would. People would generally agree that the goal is desirable, especially "
                        "since the AI system will be working with pathologists rather than in their place. AI "
                        "can help people with repetitive tasks and AI systems have proven effective in similar "
                        "medical image recognition use cases. That said, it is important to follow current "
                        "industry best practices and to be thorough in the rest of the design process, including "
                        "in analyzing harms and in considering how medical practitioners will actually interact "
                        "with the product in a medical setting.")
    
class FlagActivity(ThoughtExperiment):
    _hint = ""
    _solution = ""
    _congrats = "Solution"
    _correct_message = ("One potential harm is that the AI system could be biased against certain groups, flagging, "
                        "delaying or denying their legitimate transactions at higher rates than those of other groups. "
                        "The bank can reduce these harms by selecting data carefully, identifying and mitigating potential "
                        "bias (see Lessons 3 and 4), not operationalizing the system until potential bias is addressed "
                        "and ensuring appropriate and continuous human oversight of the system once it is operational.")

class PrototypeChatbot(ThoughtExperiment):
    _hint = ""
    _solution = ""
    _congrats = "Solution"
    _correct_message = ("The correct answer is: Build a non-AI prototype quickly and start testing it with a "
                        "diverse group of potential users. Iterating on a non-AI prototype is easier, faster "
                        "and less expensive than iterating on an AI prototype. Iterating on a non-AI prototype "
                        "also provides early information on user expectations, interactions and needs. This "
                        "information should inform the eventual design of AI prototypes.")

    
class DetectMisinformation(ThoughtExperiment):
    _hint = ""
    _solution = ""
    _congrats = "Solution"
    _correct_message = ("The social media company should ask customers how they would want to challenge a "
                        "determination. It could be by easily accessing a challenge form on which a user can describe "
                        "why their message does not contain misinformation, requesting further review by a human reviewer, "
                        "requesting an explanation of why the content was flagged or a combination of these and other means.")

class ImproveVehicles(ThoughtExperiment):
    _hint = ""
    _solution = ""
    _congrats = "Solution"
    _correct_message = "All of these are great ways to improve safety."

qvars = bind_exercises(globals(), [
    ReduceWaste, DetectCancer, FlagActivity, PrototypeChatbot, DetectMisinformation, ImproveVehicles
    ],
    var_format='q_{n}',
    )
__all__ = list(qvars)
