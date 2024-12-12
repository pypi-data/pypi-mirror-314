
import os
import pandas as pd
from glob import glob

def open_multiple_csv(files: os.PathLike, 
                      args: dict = {}, 
                      names = []):

    dfs                         = {}

    #if isinstance(files)
        
    for i_f in range(len(files)):

        name                    = names[i_f]
        file_name               = files[i_f]
        file                    = glob(file_name)[0]
        df                      = pd.read_csv(file, **args)

        dfs.update({name: df})

    return dfs


def open_csv(file_str: os.PathLike, 
             **args) -> pd.DataFrame:

    import pandas as pd
    from glob import glob

    file                       = glob(file_str)[0]

    df                          = pd.read_csv(file, **args)

    return df
