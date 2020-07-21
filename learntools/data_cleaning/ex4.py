from learntools.core import *

import pandas as pd
import numpy as np
import chardet
np.random.seed(0)

sample_entry = b'\xa7A\xa6n'
before = sample_entry.decode("big5-tw")
new_entry = before.encode()

police_killings = pd.read_csv("../input/fatal-police-shootings-in-the-us/PoliceKillingsUS.csv", encoding='Windows-1252')
 
class EncodingsIntro(EqualityCheckProblem):
    _var = 'new_entry'
    _expected = new_entry
    _hint = "Try using `.decode()` to get the string, then `.encode()` to get the bytes representation, encoded in UTF-8."
    _solution = CS(
"""before = sample_entry.decode("big5-tw")
new_entry = before.encode()
""")
    
class ReadIn(EqualityCheckProblem):
    _var = 'police_killings'
    _expected = police_killings
    _hint = "If you try to guess the encoding with the first 10,000 bytes of the file, it might give you the wrong answer.  Try using 100,000 or more lines of the file."
    _solution = "police_killings = pd.read_csv(\"../input/fatal-police-shootings-in-the-us/PoliceKillingsUS.csv\", encoding='Windows-1252')"
    
class SaveCSV(CodingProblem):
    def check(self):
        assert len(os.listdir('../working')) > 0, \
        "Please attach save a CSV file and run this code cell again to get credit!"  
        
        # check if CSV file attached to notebook
        has_csv = False
        for dirpath, dirnames, filenames in os.walk('../working'):
            if any([f.endswith(".csv") for f in filenames]):
                has_csv = True
                break
        
        assert has_csv == True, \
        "Please save the DataFrame to a CSV file."

qvars = bind_exercises(globals(), [
    EncodingsIntro,
    ReadIn,
    SaveCSV
    ],
    var_format='q{n}',
    )
__all__ = list(qvars)
