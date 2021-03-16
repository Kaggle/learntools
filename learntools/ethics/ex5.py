from learntools.core import *
    
class ScenarioA(ThoughtExperiment):
    _hint = ""
    _solution = ""
    _congrats = "Solution"
    _correct_message = ("Model cards should be written for the groups that are most "
                        "likely to read it. For *Simple Zoom*, such groups probably "
                        "include people using the tool to record videos, organizations "
                        "seeking to adopt the tool, IT and audio-visual teams and agencies, "
                        "computer vision researchers, policymakers and developers of similar "
                        "AI systems. Given how broad this group is, your team can only "
                        "assume a basic knowledge of video recording terms throughout the model card.")
    
class ScenarioB(ThoughtExperiment):
    _hint = "There is a risk that the large props could partially or fully hide the presenter."
    _solution = ""
    _congrats = "Solution"
    _correct_message = ("Since *Simple Zoom* is not suitable for presentations in which the presenter "
                        "is partially or fully hidden at any time, it might not work well in a "
                        "presentation in which the presenter uses a large object, because the object "
                        "could partially or fully hide the presenter. There are many potential ways to "
                        "address this issue. For example, your team could reach out to the *Simple Zoom* "
                        "team to assess the potential risks and harms of using *Simple Zoom* with props. "
                        "As another example, your team could eventually add a message in the Presenter "
                        "Pro user interface explaining that the *Simple Zoom* feature should not be used "
                        "in presentations that use props.")
    
class ScenarioB2(ThoughtExperiment):
    _hint = ""
    _solution = ""
    _congrats = "Solution"
    _correct_message = ("There are many possible answers to this question. For example, you may want to "
                        "check that the model’s equal performance across demographic groups (gender, skin "
                        "tone and age) remains equal across different camera angles, distances from camera, "
                        "camera types and lighting conditions. As another example, you may want to know how "
                        "well the model performs from the specific camera angles that _Production Pro_ "
                        "customers most commonly use.")
    
qvars = bind_exercises(globals(), [
    ScenarioA, ScenarioB, ScenarioB2
    ],
    var_format='q_{n}',
    )
__all__ = list(qvars)
