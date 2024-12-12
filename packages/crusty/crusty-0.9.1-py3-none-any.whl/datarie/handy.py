import pandas as pd

def check_file_exists(str_file):

    from glob import glob

    if len(glob(str_file)) > 0:
        
        print(f'\nOutput file(s) {str_file} exists. Return.\n')
        
        return True
    
    else:
        
        print(f'\nOutput file(s) {str_file} does not exist.')
        print('It will be created now...\n')
        
        return False


def yearly_files(path, y0: int = 1995, y1: int = 2018):

    files = [f"{path}/{str(y)}.nc" for y in range(y0, y1+1)]

    return files


def monthly_files(path, y0: int = 1995, y1: int = 2018):

    files = [f"{path}/{str(y)}-{str(m).zfill(2)}.nc" for y in range(y0, y1+1) for m in range(1,13)]

    return files


def yearly_or_monthly_files(freq_files, path, y0, y1):

    if freq_files == 'monthly':

        files = monthly_files(path, y0, y1)

    elif freq_files == 'yearly':

        files = yearly_files(path, y0, y1)

    return files


def save_df(df: pd.DataFrame, 
            name: str, 
            format: str = 'csv', 
            mode: str = 'w'):

    if format == 'csv':
            
        df.to_csv(name)
        
    elif format == 'parquet':
           
        df.to_parquet(name)


def open_csv_or_parquet(file: str, 
                        csv_args = {'index_col': 0}, 
                        parquet_args = {}):

    from datarie.csv import open_csv
    from datarie.parquet import open_parquet

    ending = file.split('.')[-1]
    
    open_method = open_csv if ending == 'csv' else open_parquet

    args = csv_args if ending == 'csv' else parquet_args

    df = open_method(file, **args)

    return df

    
def create_dirs(dirs: str):

    from pathlib import Path

    if isinstance(dirs, str): 
        
        dirs_= [dirs]

    else: 

        dirs_ = dirs
        
    for dir in dirs_:

        Path(dir).mkdir(parents = True, exist_ok = True)


