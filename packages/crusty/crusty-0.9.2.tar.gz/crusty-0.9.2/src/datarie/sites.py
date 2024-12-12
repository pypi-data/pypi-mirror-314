
import deims
import pandas as pd
from datarie.handy import create_dirs, check_file_exists, save_df
from datarie.csv import open_csv


def from_network(network: str = 'eLTER',
                 verified: bool = True) -> list:
    
    network_codes = {'eLTER': '4742ffca-65ac-4aae-815f-83738500a1fc',
                     'DLTER': 'e904354a-f3a0-40ce-a9b5-61741f66c824',
                     'ICOS': '80633d38-4c85-4ee0-a4ce-7bbbd99c888c'}
    

    sites = deims.getListOfSites(network = network_codes[network], 
                                           verified_only = verified)

    return sites


def information(id: str):

    information     = deims.getSiteById(id)

    return information


def coordinates(id: str):

    coordinates = information(id)['attributes']['geographic']['coordinates']

    latitude = float(coordinates.replace('(', '').replace(')', '').split(' ')[2])
    longitude = float(coordinates.replace('(', '').replace(')', '').split(' ')[1])

    return latitude, longitude


def ecosystem_type(id: str):

    ecosystem_type  = information(id)['attributes']['environmentalCharacteristics']['eunisHabitat']
    
    if ecosystem_type is None: return 'None'

    return ecosystem_type[0]['label']


def name(id: str):

    name            = information(id)['title']

    return name


def sites_df(network: str = 'eLTER',
             verified: bool = True,
             out_dir: str = 'deims',
             out_file: str = 'sites.csv'):

    out = f'{out_dir}/{out_file}'

    if check_file_exists(out): 
        
        print(f'\n{out} file already exists!\n')
        
        return open_csv(out, index_col = 0)
    
    print(f'\nSaving site file {out}.\n')

    create_dirs(out_dir)

    ids = from_network(network,
                       verified)

    names = [name(s) for s in ids]

    coords = [coordinates(s) for s in ids]
    latitudes = [c[0] for c in coords]
    longitudes = [c[1] for c in coords] 
    ecosystem_types = [ecosystem_type(s) for s in ids]

    df = pd.DataFrame({'name': names,
                       'latitude': latitudes,
                       'longitude': longitudes,
                       'ecosystem_type': ecosystem_types},
                       index = ids)

    save_df(df, out)

    return df




    