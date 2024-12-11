

def stat(array, method):

    import numpy as np

    import my_math.stats as stats

    func                = getattr(stats, method)

    array_mean          = func(array, axis = (-1, -2))

    return array_mean


def mask(array, mask, true_value):

    import numpy as np

    array_masked        = np.where(mask == true_value, array, np.nan)

    return array_masked
