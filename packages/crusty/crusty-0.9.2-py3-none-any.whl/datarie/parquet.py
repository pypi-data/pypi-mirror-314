

def open_parquet(file_str, args = {}):

    import pandas as pd
    from glob import glob

    file                        = glob(file_str)[0]

    df                          = pd.read_parquet(file, **args)

    return df