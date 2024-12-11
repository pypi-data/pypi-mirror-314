import pandas as pd
import numpy as np
import pymannkendall as mk

def mann_kendall(data: np.ndarray | pd.Series,
                 type: str = 'original_test',
                 **kwargs):

    # https://pypi.org/project/pymannkendall/
    
    test = getattr(mk, type)

    results = test(data, **kwargs)

    return results

