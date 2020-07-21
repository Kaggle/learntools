import os
from pathlib import Path
import pandas

from learntools.core import *

class AttachData(CodingProblem):
    def check(self):
        assert len(os.listdir('../input')) > 0, \
        "Please attach a dataset and run this code cell again to get credit!"  
        
        # check if CSV file attached to notebook
        has_csv = False
        for dirpath, dirnames, filenames in os.walk('../input'):
            if any([f.endswith(".csv") for f in filenames]):
                has_csv = True
                break
        
        assert has_csv == True, \
        "Please upload a dataset that contains a CSV file."
        
class Filepath(CodingProblem):
    _var = 'my_filepath'
    
    def check(self, my_path):
        assert Path(my_path).is_file(), \
        ("Either you have a typo in `my_filepath`, or you are trying to access a file that has "
         "not yet been uploaded.")
        
        assert my_path.endswith(".csv"), \
        "Please set `my_filepath` to the location of a CSV file."
    
class LoadData(CodingProblem):
    _var = 'my_data'
    
    def check(self, my_data):
        assert type(my_data) == pandas.core.frame.DataFrame, \
        "Please use `pd.read_csv` to read the data file in `my_filepath` into `my_data`."
        
class CreatePlot(CodingProblem):
    _var = 'plt'
    
    def check(self, passed_plt):
        assert len(passed_plt.figure(1).axes) > 0, "Please write code to create a figure."

qvars = bind_exercises(globals(), [
    AttachData,
    Filepath,
    LoadData,
    CreatePlot
    ],
    var_format='step_{n}',
    )
__all__ = list(qvars)
