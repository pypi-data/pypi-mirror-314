
import os
import pandas as pd
from dataclasses import dataclass
from my_.data.sites import from_network, information

WARMWINTER_2020_daily = {
    'name': 'WARMWINTER_2020_daily',
    'version': (1, 0, 6),
    'path': '/p/scratch/cjibg31/jibg3105/data/ICOS/WARMWINTER2020/',
    'type_file': 'csv',
    'time_request': 'D',
    'year_start': 1996,
    'month_start': 1,
    'year_end': 2020,
    'month_end': 12,
    'date_formats': {'H': '%Y%m%d%H%M',
                     'D': '%Y%m%d',
                     'M': '%Y%m',},
    'variables': ['GPP',
                  'NEE',
                  'ER',
                  'LE',
                  'LE-corr',
                  'Temp',
                  'P',
                  'RH',
                  'FSDS',
                  'NetRad',
                  'SoiH',
                  'VPD'],
    'variable_names': {'GPP': 'GPP_NT_VUT_REF',
                       'NEE': 'NEE_VUT_REF',
                       'ER': 'RECO_NT_VUT_REF',
                       'LE': 'LE_F_MDS',
                       'LE-corr': 'LE_CORR',
                       'Temp': 'TA_F_MDS',
                       'Precip': 'P_F',
                       'RH': 'RH',
                       'SWdown': 'SW_IN_F_MDS',
                       'NetRad': 'NETRAD',
                       'SoiH': 'G_F_MDS',
                       'VPD': 'VPD_F_MDS'},
    'variable_QC': {'GPP': 'NEE_VUT_REF_QC',
                    'NEE': 'NEE_VUT_REF_QC',
                    'ER': 'NEE_VUT_REF_QC',
                    'LE': 'LE_F_MDS_QC',
                    'LE-corr': 'LE_F_MDS_QC',
                    'Temp': 'TA_F_MDS_QC',
                    'P': 'P_F_QC',
                    'RH': 'TA_F_MDS_QC',
                    'FSDS': 'SW_IN_F_MDS_QC',
                    'NetRad': 'NETRAD_QC',
                    'SoiH': 'G_F_MDS_QC',
                    'VPD': 'VPD_F_MDS_QC'},
    'variable_dimensions': {'GPP': ['time'],
                            'NEE': ['time'],
                            'ER': ['time'],
                            'LE': ['time'],
                            'LE-corr': ['time'],
                            'Temp': ['time'],
                            'P': ['time'],
                            'RH': ['time'],
                            'FSDS': ['time'],
                            'NetRad': ['time'],
                            'SoiH': ['time'],
                            'VPD': ['time'],},
    'variable_units': {'GPP': {'H': 'umolCO2 m^-2 s^-1',
                               'D': 'g C / (m^2 day)',
                               '7D': 'g C / (m^2 day)',
                               'M': 'g C / (m^2 day)',
                               'Y': 'g C / (m^2 year)'},
                       'NEE': {'H': 'umolCO2 m^-2 s^-1',
                               'D': 'g C / (m^2 day)',
                               '7D': 'g C / (m^2 day)',
                               'M': 'g C / (m^2 day)',
                               'Y': 'g C / (m^2 year)'},
                       'ER': {'H': 'umolCO2 m^-2 s^-1',
                              'D': 'g C / (m^2 day)',
                              'M': 'g C / (m^2 day)',
                              '7D': 'g C / (m^2 day)',
                              'Y': 'g C / (m^2 year)'},
                       'LE': {'H': 'W / m^2',
                              'D': 'W / m^2',
                              '7D': 'W / m^2',
                              'M': 'W / m^2',
                              'Y': 'W / m^2'},
                       'LE-corr': {'H': 'W / m^2',
                                   'D': 'W / m^2',
                                   '7D': 'W / m^2',
                                   'M': 'W / m^2',
                                   'Y': 'W / m^2'},
                       'Temp': {'H': 'degree C',
                                'D': 'degree C',
                                '7D': 'degree C',
                                'M': 'degree C',
                                'Y': 'degree C'},
                       'P': {'H': 'mm',
                             'D': 'mm / day',
                             '7D': 'mm / day',
                             'M': 'mm / day',
                             'Y': 'mm / year'},
                       'RH': {'H': '%'},
                       'FSDS': {'H': 'W / m^2',
                                'D': 'W / m^2',
                                '7D': 'W / m^2',
                                'M': 'W / m^2',
                                'Y': 'W / m^2'},
                       'NetRad': {'H': 'W / m^2',
                                  'D': 'W / m^2',
                                  '7D': 'W / m^2',
                                  'M': 'W / m^2',
                                  'Y': 'W / m^2'},
                       'SoiH': {'H': 'W / m^2',
                                'D': 'W / m^2',
                                '7D': 'W / m^2',
                                'M': 'W / m^2',
                                'Y': 'W / m^2'},
                       'VPD': {'H': 'hPa',
                               'D': 'hPa',
                               '7D': 'hPa',
                               'M': 'hPa',
                               'Y': 'hPa'}},
    'variable_resolutions': {'GPP': ['H', 'D', '7D', 'M', 'Y'],
                             'NEE': ['H', 'D', '7D', 'M', 'Y'],
                             'ER': ['H', 'D', '7D', 'M', 'Y'],
                             'ET': ['H', 'D', '7D', 'M', 'Y'],
                             'ET-corr': ['H', 'D', '7D', 'M', 'Y'],
                             'Temp': ['H', 'D', '7D', 'M', 'Y'],
                             'P': ['H', 'D', '7D', 'M', 'Y'],
                             'RH': ['H'],
                             'FSDS': ['H', 'D', '7D', 'M', 'Y'],
                             'NetRad': ['H', 'D', '7D', 'M', 'Y'],
                             'SoiH': ['H', 'D', '7D', 'M', 'Y'],
                             'VPD': ['H', 'D', '7D', 'M', 'Y'],},
    'mask_value': -9999,
    'leapday': False,}

@dataclass
class ONEFLUX:
    
    name: str
    version: tuple[int, int, int]
    path: os.PathLike
    type_file: str
    year_start: int
    time_request: str
    month_start: int
    year_end: int
    month_end: int
    date_formats: dict
    variables: dict
    variable_names: dict
    variable_QC: dict
    variable_dimensions: dict
    variable_units: dict
    variable_resolutions: dict
    mask_value: list | int | float | str | None
    leapday: bool

    def sites_info(self):

        sites = from_network(network = 'ICOS',
                             verified = False)
        
        names_short = [information(s)['attributes']['general']['shortName']
                      for s in sites]
        
        self.ids = sites
        self.names_short = names_short


    def open_data(self):

        order = ['H', 'D', '7D', 'M', 'Y']

        request_time_available = [k for k, v in self.variable_resolutions.items()
                                  if self.time_request in v]
        
        request_time_missing = [k for k in self.variables
                                if k not in request_time_available]

        
        


        
        #data_ = pd.read_csv()


    def quality_filter(self):
        
        ...


    def le_2_et(self):
        ...

    

if __name__ == '__main__':

    data_ = ONEFLUX(**WARMWINTER_2020_daily)

    data_.open_data()
    
    #print(information(data_.sites[0])['attributes']['general']['shortName'])