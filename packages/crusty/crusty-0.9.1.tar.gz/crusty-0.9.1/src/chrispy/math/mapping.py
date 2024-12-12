import pandas as pd
import numpy as np

def linear(values, multiplicant, addend):
    
    new_values = values * multiplicant + addend

    return new_values


def relative_difference(array1, array2, percent: bool = False):

    from my_.math.arithmetic import difference, division

    absolute_difference         = difference(array1, array2)

    relative_difference         = division(absolute_difference, array2)

    if percent == True: return relative_difference * 100

    return relative_difference

