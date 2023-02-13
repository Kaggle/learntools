from learntools.core import *

import pandas as pd
import numpy as np
import charset_normalizer
import os
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
    _solution = CS(
"""police_killings = pd.read_csv("../input/fatal-police-shootings-in-the-us/PoliceKillingsUS.csv", encoding='Windows-1252')
""")
    
class SaveCSV(CodingProblem):
    _hint = "Use `.to_csv().`"
    _solution = CS(
"""
police_killings.to_csv("my_file.csv")
""")
    def check(self):
        # Test 1: does the file exist?
        csv_working = [i for i in os.listdir("../working") if i.endswith('csv')]
        assert len(csv_working) > 0, \
        "Please save a CSV file and run this code cell again to get credit!"  
        
        # Test 2: correct encoding?
        for i in csv_working:
            filepath = '../working/' + i
            try: 
                df = pd.read_csv(filepath)
            except:
                assert True==False, "It looks like you used the wrong encoding when saving your CSV file."

qvars = bind_exercises(globals(), [
    EncodingsIntro,
    ReadIn,
    SaveCSV
    ],
    var_format='q{n}',
    )
__all__ = list(qvars)
