import pandas as pd
import numpy as np

def gauss_kde_pdf(data: pd.DataFrame | pd.Series | np.ndarray , 
                    n: int = 1000, 
                    return_dict: bool = False):
    
    import pandas as pd
    import numpy as np
    from scipy.stats import gaussian_kde

    if isinstance(data, pd.DataFrame): data = data.values
    if isinstance(data, pd.Series): data = data.values

    data_clean = data[~np.isnan(data)]

    mins = np.min(data_clean)

    maxs = np.max(data_clean)

    xs = np.linspace(mins, maxs, n)

    kde_sp = gaussian_kde(data_clean)

    ys = kde_sp.pdf(xs)

    if return_dict:     
        return pd.DataFrame({'xs': xs, 'ys': ys})
    else:
        return xs, ys


def gauss_kde_cdf(data, n = 1000):

    import pandas as pd
    import numpy as np
    from scipy.stats import gaussian_kde
    from scipy.special import ndtr

    if isinstance(data, pd.DataFrame): data = data.values
    if isinstance(data, pd.Series): data = data.values


    data_clean = data[~np.isnan(data)]

    mins = np.min(data_clean)

    maxs = np.max(data_clean)

    xs = np.linspace(mins, maxs, n)

    kde_sp = gaussian_kde(data_clean)

    ys = np.array([ndtr(np.ravel(x - kde_sp.dataset) / kde_sp.factor).mean() for x in xs])

    return xs, ys


def distribution_pdf(distribution: str = 'norm', parameter: int | list = [0, 1], n = 100000):

    import scipy.stats as stats
    import numpy as np

    func_dist = getattr(stats, distribution)

    mins = func_dist.ppf(1/n, *parameter)

    maxs = func_dist.ppf(1 - 1/n, *parameter)

    xs = np.linspace(mins, maxs, n)

    ys = func_dist.pdf(xs, *parameter)

    return xs, ys


def distribution_cdf(distribution: str = 'norm', 
                     parameter: int | list = [0, 1], 
                     n = 100000):

    import scipy.stats as stats
    import numpy as np

    func_dist = getattr(stats, distribution)


    mins = func_dist.ppf(1/n, *parameter)

    maxs = func_dist.ppf(1 - 1/n, *parameter)

    xs = np.linspace(mins, maxs, n)

    ys = func_dist.cdf(xs, *parameter)

    return xs, ys

def distribution_fit(array, distribution: str = 'gamma'):

    import scipy.stats as stats

    if distribution == 'gaussian_kde': return array

    func_dist                       = getattr(stats, distribution)

    parameters                      = func_dist.fit(array)

    return parameters


def distribution_data(distribution: str = 'norm', 
                      parameter: dict | tuple = {}, 
                      n = 100000):

    #Baustelle

    import scipy.stats as stats
    import numpy as np

    func_dist = getattr(stats, distribution)

    data = func_dist.rvs(0, 1, n)    