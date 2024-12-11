

def query_variables(src, key):

    item                    = variables[src][key]

    return item


def query_grids(src, key):

    item                    = grids[src][key]

    return item


def query_static(src, key):

    item                    = static[src][key]

    return item


def available_variables(src, vars):
    
    variables_src           = variables[src]['var_names']

    vars_avail              = []
    vars_src                = []
    
    for v in vars:
        
        if v not in variables_src.keys(): continue

        var_src             = variables_src[v]
        
        vars_avail.append(v)
        vars_src.append(var_src)

    return vars_avail, vars_src


def query_unit_transform(src, variable, option):

    unit_transform_option   = variables[src][f'var_unit_transform_{option}'][variable]

    return unit_transform_option


from my_.resources.units import sec_per_day


grids = {
    'EU3': {
        'path': '/p/scratch/cjibg31/jibg3105/CESMDataRoot/InputData/share/domains/',
        'file': 'domain.lnd.CLM5EU3_v4.nc',
        'var_lat': 'yc',
        'var_lon': 'xc',
    },
}



static = {
            
            'CLM5-EU3-surf': {
                        'grid': 'EU3',
                        'path': '/p/scratch/cjibg31/jibg3105/CESMDataRoot/InputData/lnd/clm2/surfdata_map/',
                        'file': 'surfdata_CLM5EU3_v4_pos.nc',
                        'static_vars': ['PCT_NATVEG', 'PCT_CROP', 'PCT_LAKE', 'PCT_WETLAND', 'PCT_NAT_PFT', 'PCT_CFT'],
                        
                        'abbr_PFT': {
                            0: 'Bare Ground',
                            1: 'NET Temperate',
                            2: 'NET Boreal',
                            3: 'NDT Boreal',
                            4: 'BET Tropical',
                            5: 'BET Temperate',
                            6: 'BDT Tropical',
                            7: 'BDT Temperate',
                            8: 'BDT Boreal',
                            9: 'BES Temperate',
                            10: 'BDS Temperate',
                            11: 'BDS Boreal',
                            12: 'C3 arctic grass',
                            13: 'C3 grass',
                            14: 'C4 grass',
                            15: 'UCrop UIrr',
                            16: 'UCrop Irr',
                        },
                        
                        'names_PFT': {
                            0: 'Bare Ground',
                            1: 'Needleleaf evergreen tree - temperate',
                            2: 'Needleleaf evergreen tree - boreal',
                            3: 'Needleleaf deciduous tree - boreal',
                            4: 'Broadleaf evergreen tree - tropical',
                            5: 'Broadleaf evergreen tree - temperate',
                            6: 'Broadleaf deciduous tree - tropical',
                            7: 'Broadleaf deciduous tree - temperate',
                            8: 'Broadleaf deciduous tree - boreal',
                            9: 'Broadleaf evergreen shrub - temperate',
                            10: 'Broadleaf deciduous shrub - temperate',
                            11: 'Broadleaf deciduous shrub - boreal',
                            12: 'C3 arctic grass',
                            13: 'C3 grass',
                            14: 'C4 grass',
                            15: 'C3 Unmanaged Rainfed Crop',
                            16: 'C3 Unmanaged Irrigated Crop',
                        },
                        
                        'sel_agg_layer_PFT': {
                            'ENF': [1, 2],
                            'DBF': [6, 7, 8],
                            'GRA': [12, 13, 14],
                            'CRO': [15, 16],
                        },

                    },

            'hydroclim-EU3': {
                        'grid': 'EU3',
                        'path': '/p/scratch/cjibg31/jibg3105/data/COSMOREA6/CLIM_CLASS/',
                        'file': 'CLIM_CLASS.nc',
                        'static_vars': ['PRECTmms_COSMOREA6'],
                        'dummy_ax': False,
                    },
}



variables = {
    
            'CLM5-EU3': {
                        'grid': 'EU3',
                        'path': '/p/scratch/cjibg31/jibg3105/data/CLM5EU3/006/join_8d/',
                        'time_step': '8D',
                        'leap_day': False,
                        'freq_files': 'yearly',
                        'name_label': r'$\mathdefault{CLM5_{grid}}$',
                        
                        'var_names': {
                            'GPP': 'GPP',
                            'NEE': 'NEE',
                            'ER': 'ER',
                            'ET': 'QFLX_EVAP_TOT',
                            'ET-corr': 'QFLX_EVAP_TOT',
                            'LAI': 'TLAI',
                        },

                        'var_units': {
                            'GPP': r'$\mathdefault{g\;C\;day^{-1}}$',
                            'NEE': r'$\mathdefault{g\;C\;day^{-1}}$',
                            'ER': r'$\mathdefault{g\;C\;day^{-1}}$',
                            'ET': r'$\mathdefault{mm\;day^{-1}}$',
                            'ET-corr': r'$\mathdefault{mm\;day^{-1}}$',
                            'LAI': r'$\mathdefault{m^{2}\;m^{-2}}$',
                        },
                        
                        'var_unit_transform_methods': {
                            'GPP': 'linear',
                            'NEE': 'linear',
                            'ER': 'linear',
                            'ET': 'linear',
                            'ET-corr': 'linear',
                            'LAI': 'linear',

                        },
                        
                        'var_unit_transform_m': {
                            'GPP': sec_per_day,
                            'NEE': sec_per_day,
                            'ER': sec_per_day,
                            'ET': sec_per_day,
                            'ET-corr': sec_per_day,
                            'LAI': 1.0,

                        },

                        'var_unit_transform_b': {
                            'GPP': 0,
                            'NEE': 0,
                            'ER': 0,
                            'ET': 0,
                            'ET-corr': 0,
                            'LAI': 0.0,
                        },

                    },
            
            
            'CLM5-EU3-pft': {
                        'grid': 'EU3',
                        'path': '/p/scratch/cjibg31/jibg3105/data/CLM5EU3/006/join_8d/pft/unlim_float/',
                        'time_step':'8D',
                        'leap_day': False,
                        'freq_files':'yearly',
                        'name_label': r'$\mathdefault{CLM5_{PFT}}$',
                        
                        'var_names': {
                            'GPP': 'GPP',
                            'ET': 'ET',
                            'ET-corr': 'ET'
                        },

                        'var_layer': {
                            'GPP': 'PFT',
                            'ET': 'PFT',
                            'ET-corr': 'PFT',
                        },

                        'method_layer_agg': {
                            'PFT': 'mean',
                        },

                        'var_units': {
                            'GPP': r'$\mathdefault{g\;C\;day^{-1}}$',
                            'ET': r'$\mathdefault{mm\;day^{-1}}$',
                            'ET-corr': r'$\mathdefault{mm\;day^{-1}}$',
                        },

                        'var_unit_transform_methods': {
                            'GPP': 'linear',
                            'ET': 'linear',
                            'ET-corr': 'linear',
                        },
                        
                        'var_unit_transform_m': {
                            'GPP': 1,
                            'ET': 1,
                            'ET-corr': 1,
                        },

                        'var_unit_transform_b': {
                            'GPP': 0,
                            'ET': 0,
                            'ET-corr': 0,
                        },

                        'sel_agg_layer_PFT': {
                            'ENF': [1, 2],
                            'DBF': [6, 7, 8],
                            'GRA': [12, 13, 14],
                            'CRO': [15, 16],
                        },
                    },
            
            'GLASS-EU3': {
                        'grid': 'EU3',
                        'path': '/p/scratch/cjibg31/jibg3105/data/EDWUE/',
                        'time_step': '8D',
                        'leap_day': True,
                        'freq_files':'yearly',
                        'name_label': r'$\mathdefault{GLASS}$',
                        
                        'var_names': {
                            'GPP': 'GPP_GLASS',
                            'ET': 'ET_GLASS',
                            'LAI': 'LAI_GLASS'
                        },

                        'var_units': {
                            'GPP': r'$\mathdefault{g\;C\;day^{-1}}$',
                            'ET': r'$\mathdefault{mm\;day^{-1}}$',
                            'LAI': r'$\mathdefault{m^{2}\;m^{-2}}$',
                        },

                        'var_unit_transform_methods': {
                            'GPP': 'linear',
                            'ET': 'linear',
                            'LAI': 'linear',
                        },
                        
                        'var_unit_transform_m': {
                            'GPP': 1,
                            'ET': 1,
                            'LAI': 1,
                        },

                        'var_unit_transform_b': {
                            'GPP': 0,
                            'ET': 0,
                            'LAI': 0,
                        },
                    },
            
            'ERA5L-EU3': {
                        'grid': 'EU3',
                        'path': '/p/scratch/cjibg31/jibg3105/data/EDWUE/',
                        'time_step': '8D',
                        'leap_day': True,
                        'freq_files':'yearly',
                        'name_label': r'$\mathdefault{ERA5L}$',
                        
                        'var_names': {
                            'ET': 'ET_ERA5L',
                            'LAI': 'LAI_ERA5L'
                        },

                        'var_units': {
                            'ET': r'$\mathdefault{mm\;day^{-1}}$',
                            'LAI': r'$\mathdefault{m^{2}\;m^{-2}}$',
                        },

                        'var_unit_transform_methods': {
                            'ET': 'linear',
                            'LAI': 'linear',
                        },
                        
                        'var_unit_transform_m': {
                            'ET': 1,
                            'LAI': 1,
                        },

                        'var_unit_transform_b': {
                            'ET': 0,
                            'LAI': 0,
                        },
                    },
            
            'GLEAM-EU3': {
                        'grid': 'EU3',
                        'path': '/p/scratch/cjibg31/jibg3105/data/EDWUE/',
                        'time_step': '8D',
                        'leap_day': True,
                        'freq_files': 'yearly',
                        'name_label': r'$\mathdefault{GLEAM}$',
                        
                        'var_names': {
                            'ET': 'ET_GLEAM',
                        },

                        'var_units': {
                            'ET': r'$\mathdefault{mm\;day^{-1}}$',
                        },

                        'var_unit_transform_methods': {
                            'ET': 'linear',
                        },
                        
                        'var_unit_transform_m': {
                            'ET': 1,
                        },

                        'var_unit_transform_b': {
                            'ET': 0,
                        },
                    },
            
            'COSMOREA6-EU3': {
                        'grid': 'EU3',
                        'path': '/p/scratch/cjibg31/jibg3105/data/COSMOREA6/8daily/',
                        'time_step': '8D',
                        'leap_day': True,
                        'freq_files': 'yearly',
                        'name_label': r'$\mathdefault{COSMOREA6}$',

                        'var_names': {
                            'Temp': 'TBOT',
                            'Precip': 'PRECTmms',
                            'SWdown': 'FSDS',
                            'RH': 'RH',
                        },

                        'var_units': {
                            'Temp': r'$\mathdefault{\degree\;C}$',
                            'Precip': r'$\mathdefault{mm\;day^{-1}}$',
                            'RH': r'$\mathdefault{\%}$',
                            'SWdown': r'$\mathdefault{W\;m^{-2}}$'
                        },

                        'var_unit_transform_methods': {
                            'Temp': 'linear',
                            'Precip': 'linear',
                            'RH': 'linear',
                            'SWdown': 'linear',
                        },
                        
                        'var_unit_transform_m': {
                            'Temp': 1,
                            'Precip': sec_per_day,
                            'RH': 1,
                            'SWdown': 1,
                        },

                        'var_unit_transform_b': {
                            'Temp': -273.15,
                            'Precip': 0,
                            'RH': 0,
                            'SWdown': 0,
                        },
                    },

            'ICOS-WARMWINTER2020': {
                        'processing': 'ONEFLUX',
                        'path': '/p/scratch/cjibg31/jibg3105/data/ICOS/WARMWINTER2020',
                        'leap_day': False,
                        'name_label': r'$\mathdefault{ICOS}$',
                        
                        'date_format': {
                            'H': '%Y%m%d%H%M',
                            'D': '%Y%m%d',
                            'M': '%Y%m',
                        },
                        
                        'var_names': {
                            'GPP': 'GPP_NT_VUT_REF',
                            'NEE': 'NEE_VUT_REF',
                            'ER': 'RECO_NT_VUT_REF',
                            'ET': 'LE_F_MDS',
                            'ET-corr': 'LE_CORR',
                            'Temp': 'TA_F_MDS',
                            'Precip': 'P_F',
                            'RH': 'RH',
                            'SWdown': 'SW_IN_F_MDS',
                        },

                        'var_units': {
                            'GPP': r'$\mathdefault{g\;C\;day^{-1}}$',
                            'NEE': r'$\mathdefault{g\;C\;day^{-1}}$',
                            'ER': r'$\mathdefault{g\;C\;day^{-1}}$',
                            'ET': r'$\mathdefault{mm\;day^{-1}}$',
                            'ET-corr': r'$\mathdefault{mm\;day^{-1}}$',
                            'Temp': r'$\mathdefault{\degree\;C}$',
                            'Precip': r'$\mathdefault{mm\;day^{-1}}$',
                            'RH': r'$\mathdefault{\%}$',
                            'SWdown': r'$\mathdefault{W\;m^{-2}}$'
                        },

                        'var_time_step': {
                            'GPP': 'D',
                            'NEE': 'D',
                            'ER': 'D',
                            'ET': 'D',
                            'ET-corr': 'D',
                            'Temp': 'D',
                            'Precip': 'D',
                            'RH': 'H',
                            'SWdown': 'D',
                        },

                        'csv_open_args': {
                            'na_values': ['-9999'], 'index_col': 0
                            },

                        'var_QC': {
                            'GPP': 'NEE_VUT_REF_QC',
                            'NEE': 'NEE_VUT_REF_QC',
                            'ER': 'NEE_VUT_REF_QC',
                            'ET': 'LE_F_MDS_QC',
                            'ET-corr': 'LE_F_MDS_QC',
                            'Temp': 'TA_F_MDS_QC',
                            'Precip': 'P_F_QC',
                            'RH': 'TA_F_MDS_QC',
                            'SWdown': 'SW_IN_F_MDS_QC',
                        },

                        'var_unit_transform_methods': {
                            'GPP': 'linear',
                            'NEE': 'linear',
                            'ER': 'linear',
                            'ET': 'linear',
                            'ET-corr': 'linear',
                            'Temp': 'linear',
                            'Precip': 'linear',
                            'RH': 'linear',
                            'SWdown': 'linear',
                        },
                        
                        'var_unit_transform_m': {
                            'GPP': 1,
                            'NEE': 1,
                            'ER': 1,
                            'ET': 0.035,
                            'ET-corr': 0.035,
                            'Temp': 1,
                            'Precip': 1,
                            'RH': 1,
                            'SWdown': 1,
                        },

                        'var_unit_transform_b': {
                            'GPP': 0,
                            'NEE': 0,
                            'ER': 0,
                            'ET': 0,
                            'ET-corr': 0,
                            'Temp': 0,
                            'Precip': 0,
                            'RH': 0,
                            'SWdown': 0,
                        },
                    },


            'ICOS-ETC-L2-ARCHIVE': {
                        'processing': 'ARCHIVE',
                        'path': '/p/scratch/cjibg31/jibg3105/data/ICOS/ETC_L2_ARCHIVE',
                        'name_label': r'$\mathdefault{ICOS}$',
                        'date_format': '%Y%m%d',
                        
                        'var_names': {
                            'LAI': 'LAI',
                        },

                        'var_units': {
                            'LAI': r'$\mathdefault{m^{2}\;m^{-2}}$',
                        },

                        'csv_open_args': {
                            'na_values': ['-9999'],
                            },

                        'var_unit_transform_methods': {
                            'LAI': 'linear',
                            },
                        
                        'var_unit_transform_m': {
                            'LAI': 1,
                        },

                        'var_unit_transform_b': {
                            'LAI': 0,
                        },
                    },
}