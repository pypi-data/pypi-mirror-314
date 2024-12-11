

# Notes
# None and none and nones and default values correspond with here?
# Spinup functionality

from dataclasses import dataclass, field

@dataclass
class case:

    """
    I hope to be a generic class for most CLM5 user cases.

    Infos:
    https://www2.cesm.ucar.edu/models/ccsm4.0/clm/models/lnd/clm/doc/UsersGuide/x1327.html
    https://docs.cesm.ucar.edu/models/cesm2/settings/current/drv_input_cesm.html
    https://docs.cesm.ucar.edu/models/cesm2/settings/current/clm5_0_nml.html
    https://docs.cesm.ucar.edu/models/cesm2/settings/current/datm_input.html

    Maybe in future: different datm interpolation methods?
    https://escomp.github.io/ctsm-docs/versions/release-clm5.0/html/users_guide/setting-up-and-running-a-case/customizing-the-datm-namelist.html

    To do:
    - Custom forcings switch: consider the stated stream files in the user datm namelist

    """

    dir_script: str 
    name: str
    compset: str
    n_cpu: int
    year_start: int
    year_end: int
    year_start_forcing: int
    year_end_forcing: int
    dir_domain_lnd: str
    file_domain_lnd: str
    dir_surf: str
    file_surf: str
    months_per_wallclock: int
    time_resolution_forcing_hours: int

    ncpl: int                   = 24
    wallclock: str              = '24:00:00'
    
    mode_datm: str              = 'CLMCRUNCEPv7'
    hist_vars_grid: list        = field(default_factory = list)
    hist_vars_pft: list         = field(default_factory = list)
    hist_frq_grid: int          = -24
    hist_flt_grid: int          = 365
    hist_frq_pft: int           = -24
    hist_flt_pft: int           = 365

    month_start: int            = 1
    month_end: int              = 12

    month_start_forcing: int    = 1
    month_end_forcing: int      = 12

    custom_forcings: bool       = True


    dir_domain_atm: None | str  = None
    file_domain_atm: None | str = None

    dir_init: str | None        = None
    file_init: str | None       = None

    dir_forcing: str | None     = None

    mode_co2: None | str        = None 

    type_co2: str               = 'constant' 
    ppmv_co2: float             = 379.0
    
    series_co2: str             = None

    coldstart: bool             = False

    job_archive: bool           = False

    AD_spin_up: bool            = False

    continue_run: bool          = False


    def create(self):
        
        """
        To create a case directory.

        """
        import os
        import subprocess
        
        if os.path.isdir(f'{self.dir_script}/{self.name}'): 
            
            print('\nCase directory already exists. \n')

            return

        print('\nCreate case...\n')

        subprocess.call([f'{self.dir_script}/create_newcase', 
                         '--case', self.name, 
                         '--res', 'CLM_USRDAT' , 
                         '--compset', self.compset, 
                         '--run-unsupported'], cwd = self.dir_script)
        
        print('\nCase created.\n')
    

    def setup(self, clean: bool = False):
        
        """
        To setup the case and create respective generic namelist files.

        """

        import os
        import subprocess

        dir_setup           = f'{self.dir_script}/{self.name}'

        if clean: subprocess.call([f'{dir_setup}/case.setup', 
                                   '--clean'], cwd = dir_setup)
        
        if os.path.isdir(f'{dir_setup}/CaseDocs/'): 
            
            print('Case is already set-up. Clean?')
            
            return

        print('\nSet-up case ...\n')

        subprocess.call([f'{dir_setup}/xmlchange',
                         f'NTASKS={self.n_cpu}'], cwd = dir_setup)
        
        subprocess.call(f'{dir_setup}/case.setup', cwd = dir_setup)

        print('\nCase set-up.\n')
    
    
    
    def config(self):
     
        """
        Change the config files in the case directory.
        We use the xmlchange functionality.

        """

        print('\nAdjust case configuration...\n')

        import subprocess
        import numpy as np

        dir_setup           = f'{self.dir_script}/{self.name}'

        n_months            = 12 * (self.year_end - self.year_start) - (24 - (self.month_start + self.month_end))

        resubmit            = (np.ceil(n_months / self.months_per_wallclock) - 1).astype(int)

        keys_config         = { 'ATM_DOMAIN_PATH': self.dir_domain_atm,
                                'LND_DOMAIN_PATH': self.dir_domain_lnd,
                                'ATM_DOMAIN_FILE': self.file_domain_atm,
                                'LND_DOMAIN_FILE': self.file_domain_lnd,
                                'DATM_MODE': self.mode_datm,
                                'DATM_CLMNCEP_YR_ALIGN': self.year_start_forcing,
                                'DATM_CLMNCEP_YR_START': self.year_start_forcing,
                                'DATM_CLMNCEP_YR_END': self.year_end_forcing,
                                'RUN_STARTDATE': f'{self.year_start:04d}-{self.month_start:02d}-01',
                                'STOP_OPTION': 'nmonths',
                                'STOP_N': self.months_per_wallclock,
                                'STOP_DATE': -1,
                                'JOB_WALLCLOCK_TIME': self.wallclock,
                                'CLM_ACCELERATED_SPINUP': self.AD_spin_up,
                                'RESUBMIT': resubmit,
                                'CLM_FORCE_COLDSTART': self.coldstart,
                                'ATM_NCPL': self.ncpl,
                                'LND_NCPL': self.ncpl,
                                'DOUT_S': self.job_archive,
                                'CCSM_BGC': self.mode_co2,
                                'CLM_CO2_TYPE': self.type_co2,
                                'CCSM_CO2_PPMV': self.ppmv_co2,
                                'DATM_CO2_TSERIES': self.series_co2,
                                'CONTINUE_RUN': self.continue_run,
                                }
        
        for k, v in keys_config.items():
            
            print(f'Set {k}...')

            if v is None: v = 'none'
            if k in ('CLM_FORCE_COLDSTART', 'CLM_ACCELERATED_SPINUP') and v is False: v = 'off'
            if k in ('CLM_FORCE_COLDSTART', 'CLM_ACCELERATED_SPINUP') and v is True: v = 'on'
            if k in ('DOUT_S', 'CONTINUE_RUN') and v is False: v = 'FALSE'
            if k in ('DOUT_S', 'CONTINUE_RUN') and v is True: v = 'TRUE'

            subprocess.call([f'{dir_setup}/xmlchange',
                         f'{k}={v}'], cwd = dir_setup)
            
        print('\nCase configuration adjusted.\n')


    def namelists(self):

        """
        Change the user namelist files in the case directory.
        We use blueprint files from this repository, change them,
        and copy them to the case directory.

        """

        print('\nCreate case namelists...\n')

        dir_setup           = f'{self.dir_script}/{self.name}'
        
        file_init           = f"finidat = '{self.dir_init}/{self.file_init}'" if self.file_init is not None else ''

        hist_vars_grid      = "'" + "', '".join(self.hist_vars_grid) + "'"

        dt_limit            = (24 + self.timestep_forcing_hours) / self.timestep_forcing_hours

        if self.hist_vars_pft:

            hist_vars_pft_0 = f'hist_dov2xy(2) = .false.'
            hist_vars_pft_1 = f"hist_type1d_pertape(2) = 'PFTS'"
            hist_vars_pft_2 = f'hist_nhtfrq(2) = {self.hist_frq_pft}'
            hist_vars_pft_3 = f'nhist_mfilt(2) = {self.hist_flt_pft}'
            hist_vars_pft_4 = "'" + "', '".join(self.hist_vars_pft) + "'"

            hist_pft_str    = '\n'.join([hist_vars_pft_0, 
                                        hist_vars_pft_1,
                                        hist_vars_pft_2,
                                        hist_vars_pft_3,
                                        hist_vars_pft_4,])
        else:
            
            hist_pft_str    = ''


        keys_namelist_clm   = { 'file_surf': f"'{self.dir_surf}/{self.file_surf}'",
                                'file_init': file_init,
                                'hist_frq': self.hist_frq_grid,
                                'hist_flt': self.hist_flt_grid,
                                'hist_vars_grid': hist_vars_grid,
                                'hist_vars_pft': hist_pft_str,
                                }
        
        keys_namelist_datm  = { 'year_start': self.year_start_forcing,
                                'year_end': self.year_end_forcing,
                                'dt_limit': dt_limit,
                                }

        self.search_replace('config_files/user_nl/', 'user_nl_clm', keys_namelist_clm, dir_setup)
        self.search_replace('config_files/user_nl/', 'user_nl_datm', keys_namelist_datm, dir_setup)


        print('\nNamelists created and copied.\n')
    

    def search_replace(self, path_in, name_file, search_replace_dict, path_out):
        
        with open(f'{path_in}/{name_file}', 'r') as file:
        
            content         = file.read()

            for k, v in search_replace_dict.items():

                content     = content.replace(k, str(v))

        with open(f'{path_out}/{name_file}', 'w') as file:

            file.write(content)


    def streams(self):

        """
        Create and adjust the datm stream files files.
        This is to run CLM5 with your own forcings.
        We use the blueprint files in this repository, change them,
        and copy them to the case directory.

        """

        if not self.custom_forcings: print('\nNo stream files necessary.\n'); return
        
        print('\nCreate case stream files...\n')

        import subprocess

        dir_setup           = f'{self.dir_script}/{self.name}'

        year_files          = [f'{y}-{m:02d}.nc' for y in range(self.year_start_forcing, self.year_end_forcing + 1) for m in range(1,13)]

        keys_streams        = { 'dir_domain': self.dir_domain_atm,
                                'file_domain': self.file_domain_atm, 
                                'dir_forcing': self.dir_forcing,
                                'year_files': '\n'.join(year_files),
                               }
        
        self.search_replace('config_files/user_datm/', 'user_datm.streams.txt.CLMCRUNCEPv7.Precip', keys_streams, dir_setup)
        self.search_replace('config_files/user_datm/', 'user_datm.streams.txt.CLMCRUNCEPv7.Solar', keys_streams, dir_setup)
        self.search_replace('config_files/user_datm/', 'user_datm.streams.txt.CLMCRUNCEPv7.TPQW', keys_streams, dir_setup)

        subprocess.call(f'{dir_setup}/preview_namelists', cwd = dir_setup)
        subprocess.call(f'cp user_datm.streams.* Buildconf/datmconf/', shell = True, cwd = dir_setup)

        print('\nCase stream files created.\n')


    def build(self, clean: bool = False):

        """
        Build the model case with the case.build script.

        """

        import subprocess
        import mmap

        dir_setup           = f'{self.dir_script}/{self.name}'

        with open(f'{dir_setup}/CaseStatus', 'r') as file, \
            mmap.mmap(file.fileno(), 0, access = mmap.ACCESS_READ) as s:
            
            if s.find(b'case.build success') != -1:

                print('Case was already built. Clean?')
                
                return

        if clean:

            print('Cleaning case build...')

            subprocess.call([f'{dir_setup}/case.build', '--clean-all'], cwd = dir_setup)

            print('Case build cleaned.')

        print('Build case...')

        subprocess.call([f'{dir_setup}/case.build'], cwd = dir_setup)

        print('Case built.')


    def submit(self):

        """
        Submit your case for simulation with the case.submit script.
        
        """

        import subprocess

        dir_setup           = f'{self.dir_script}/{self.name}'

        print('\nCase submit...\n')

        subprocess.call([f'{dir_setup}/case.submit'], cwd = dir_setup)

        print('\nCase submitted. All done!\n')


@dataclass
class restart:

    """
    Yes, under heavy contrsuction, does not work yet

    """

    
    dir_output: str
    files_output : list | str
    n_lat: int
    n_lon: int

    names_pft: list = field(default_factory=lambda: ['BG',      #1
                                                    'NEF_Te',   #2
                                                    'NEF_Bo',   #3
                                                    'NDF_Bo',   #4
                                                    'BEF_Tr',   #5
                                                    'BEF_Te',   #6
                                                    'BDF_Tr',   #7
                                                    'BDF_Te',   #8
                                                    'BDT_Bo',   #9
                                                    'BES_Te',   #10
                                                    'BDS_Te',   #11
                                                    'BDS_Bo',   #12
                                                    'C3arct',   #13
                                                    'C3',       #14
                                                    'C4',       #15
                                                    'C3_rain',  #16
                                                    'C3_irr'])  #17
    


    def dataset(self):

        import xarray as xr
        from glob import glob

        files   = glob(f'{self.dir_output}/{self.files_output}')

        args    = {'chunks': {'time': 365}, 'decode_times': True}

        dataset = xr.open_dataset(files[0], **args) if len(files) == 1 else xr.open_mfdataset(files, **args)

        return dataset


    def to_sparse(self, data, vegtype, jxy, ixy, shape):

        import numpy as np
        import sparse as sp

        """
        Takes an input numpy array and converts it to a sparse array.

        Parameters
        ----------
        data: numpy.ndarray
            1D or 2D Data stored in compressed form.
        vegtype: numpy.ndarray

        jxy: numpy.ndarray
            Latitude index
        ixy: numpy.ndarray
            Longitude index
        shape: tuple
            Shape provided as sizes of (vegtype, jxy, ixy) in uncompressed
            form.

        Returns
        -------
        sparse.COO
            Sparse nD array
        """

        # This constructs a list of coordinate locations at which data exists
        # it works for arbitrary number of dimensions but assumes that the last dimension
        # is the "stacked" dimension i.e. "pft"

        if ((data.ndim == 1)):

            coords = np.stack([vegtype, jxy - 1, ixy - 1], axis = 0)
           
        else:

            raise NotImplementedError

        sparse_coo          = sp.COO(coords = coords,
                                    data = data.ravel(),
                                    shape = data.shape[:-1] + shape,
                                    fill_value = np.nan)

        return sparse_coo


    def convert_pft_variables_to_sparse(self):

        import xarray as xr
        import numpy as np
        import sparse as sp

        from my_resources.CLM5_carbon_pools import pft, soil

        """
        Convert 2D PFT variables in dataset to 4D sparse arrays.

        Parameters
        ----------
        dataset: xarray.Dataset
            Dataset with DataArrays that have a `pft` dimension.

        Returns
        -------
        xarray.Dataset
            Dataset whose "PFT" arrays are now sparse arrays
            with `pft` dimension expanded out to (type, lat, lon)
        """

        variables = pft #| soil

        dataset = self.dataset()

        # extract PFT variables
        pfts = xr.Dataset({k: v for k, v in dataset.items() if (("pft" in v.dims) and (k in variables.keys()))})

        # extract coordinate index locations
        ixy = dataset.pfts1d_ixy.astype(int)
        jxy = dataset.pfts1d_jxy.astype(int)
        vegtype = dataset.pfts1d_itypveg.astype(int)
        npft = len(self.names_pft)

        # expected shape of sparse arrays to pass to `to_sparse` (excludes time)
        output_sizes = {'vegtype': npft, 'lat': self.n_lat, 'lon': self.n_lon}

        result = xr.Dataset()
        # we loop over variables so we can specify the appropriate dtype
        for var in pfts:
            result[var] = xr.apply_ufunc(
                self.to_sparse,
                pfts[var],
                vegtype,
                jxy,
                ixy,
                kwargs = {'shape': tuple(output_sizes.values())},
                input_core_dims = [["pft"]] * 4,
                output_core_dims = [["vegtype", "lat", "lon"]],
                dask = "parallelized",
                dask_gufunc_kwargs = dict(
                    meta = sp.COO(np.array([], dtype = pfts[var].dtype)),
                    output_sizes = output_sizes,
                ),
                keep_attrs = True,
            )

        # copy over coordinate variables lat, lon
        # result = result.update(dataset[["lat", "lon"]])

        result["vegtype"] = self.names_pft

        # save the dataset attributes
        result.attrs = dataset.attrs

        return result

