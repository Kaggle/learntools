from learntools.core import *

num_years = 4
days_per_year = 365 
hours_per_day = 24
mins_per_hour = 60
secs_per_min = 60
births_per_min = 250

survived = 342
minors = 113
total = 891

class RunHelloWorld(CodingProblem):
    _congrats = ("If you see 'Hello, world!' above, You have successfully printed a message, "
                 "and you're ready to move on to the next question.")
    _correct_message = ""
    def check(self):
        pass 
    
class PrintAnotherMsg(CodingProblem):
    _congrats = "Once you have printed your own message, you're ready to move on to the next question."
    _correct_message = ""
    def check(self):
        pass 
    
class LearnCheckingCode(CodingProblem):
    _hint = "If you're ever stuck on a question, it's a good idea to look at the hint before viewing the solution."
    _solution = ("If you're still stuck on a question after viewing the hint and re-reading the tutorial, "
                 "you can view the solution.  You can also view the solution after you have successfully submitted "
                 "your own answer, to check if the official solution is any different (there may be more than "
                 "one right answer!).")
    _congrats = "Once you have printed the hint and the solution, you're ready to move on to the next question."
    _correct_message = ""
    def check(self):
        pass 

class BirthsPerYear(EqualityCheckProblem):
    _vars = ['births_per_min', 'births_per_day']
    _expected = [250, births_per_min * mins_per_hour * hours_per_day]
    _hint = ("How can you use the variables to calculate the number of minutes in one day?  Once you have that, you "
             "need only multiply that number by the number of births per minute.")
    _solution = CS(
"""# Set the value of the births_per_min variable
births_per_min = 250

# Set the value of the births_per_day variable
births_per_day = births_per_min * mins_per_hour * hours_per_day
""")
    
class BonusTitanic(EqualityCheckProblem):
    _vars = ['survived_fraction', 'minors_fraction']
    _expected = [survived/total, minors/total]
    _hint = ("To get the fraction of people who survived the titanic, you need to divide the number of survivors by the "
             "total number of people.  Remember the variables that you can use to answer this question: `survived`, "
             "`total`, and `minors`.")
    _solution = CS(
"""# Fill in the value of the survived_fraction variable 
survived_fraction = survived/total

# Print the value of the survived_fraction variable
print(survived_fraction)

# Fill in the value of the minors_fraction variable
minors_fraction = minors/total 

# Print the value of the minors_fraction variable
print(minors_fraction)
""")


qvars = bind_exercises(globals(), [
    RunHelloWorld,
    PrintAnotherMsg,
    LearnCheckingCode,
    BirthsPerYear,
    BonusTitanic
    ],
    var_format='q{n}',
    )
__all__ = list(qvars)
