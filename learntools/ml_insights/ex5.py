from numpy import random
import pandas as pd

def get_data_with_interaction():
    sample_size = 1000
    X1 = random.rand(sample_size)
    X2 = random.rand(sample_size)
    y = (X1 - X2)**2

    return pd.DataFrame({'X1': X1,
                         'X2': X2,
                         'y': y})
