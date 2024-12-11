
def count_valid(array):

    import numpy as np

    valid_values                = ~np.isnan(array)

    count_valid                 = np.count_nonzero(valid_values)

    return count_valid


def count_value_occ(array, value):

    import numpy as np

    valid_values                = np.where(array == value, True, False)

    count_valid                 = np.count_nonzero(valid_values)

    return count_valid