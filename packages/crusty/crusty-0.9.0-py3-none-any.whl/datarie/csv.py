
import pandas as pd

def open_csv(file_str: str,
             **args) -> pd.DataFrame:

    import pandas as pd
    from glob import glob

    file                       = glob(file_str)[0]

    df                          = pd.read_csv(file, **args)

    return df
