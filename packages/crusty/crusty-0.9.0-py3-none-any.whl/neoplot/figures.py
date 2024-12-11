
from dataclasses import dataclass, field
import matplotlib as mpl
import matplotlib.transforms as mtr
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import cartopy.crs as ccrs
from matplotlib.gridspec import GridSpec
import matplotlib.axes as maxes
from mpl_toolkits.axes_grid1 import make_axes_locatable
import string
import os
import numpy as np
from pathlib import Path, PosixPath
from cartopy.mpl.geoaxes import GeoAxes
from typing import Union, List, Literal, Iterable

# Hier kann man viel mehr zusammenfassen, da in den
# sub-classen viel wiederholt wird

@dataclass(kw_only = True)
class fig_001:

    fy: float = 6.7
    fx: float = 6.7

    dpi: int = 300
    font_color: str = 'dimgray'
    font_dir: Path = Path('/p/scratch/cjibg31/jibg3105/projects/my_py/src/my_/plot/fonts/')
    font: str = 'Montserrat-Medium'
    constrained: bool = True

    def create(self):
        
        font_files = fm.findSystemFonts(fontpaths = [self.font_dir])
    
        for font_file in font_files:
            fm.fontManager.addfont(font_file)
    
        prop = fm.FontProperties(fname = PosixPath(str(self.font_dir) + 
                                         '/Montserrat-Medium.otf'))

        mpl.rcParams['font.family'] = prop.get_name()
        mpl.rcParams['xtick.color'] = self.font_color
        mpl.rcParams['ytick.color'] = self.font_color

        fig_ = plt.figure(figsize = (self.fx, self.fy), 
                          constrained_layout = self.constrained,
                          dpi = self.dpi)
        
        self.fig = fig_
        
        return self

    def save(self, 
             path: os.PathLike,
             fformat: str = 'png'):

        self.fig.savefig(f'{path}.{fformat}',
                         dpi = self.dpi,
                         bbox_inches = 'tight')
        
        plt.close()

        

@dataclass(kw_only = True)
class single_001(fig_001):

    color_bar: None | list[str] = None
    projection: mtr.Transform | ccrs.Projection | \
                None | Literal['EU3'] = None
    frame: bool = False
    aspect_factor: float = 12.0
    cax_pad: float = 0.8
    cax_size: str = '8%'


    def create(self):

        super().create()

        nrows = 1
        ncols = 1
        args = {'width_ratios': None,
                'height_ratios': None}
        axs = []
        caxs = []

        if self.projection == 'EU3':
    
            rotnpole_lat: float = 39.25 
            rotnpole_lon: float = -162.0

            semmj_axis: None | int = 6370000
            semmn_axis: None | int = 6370000 

            globe = ccrs.Globe(semimajor_axis = semmj_axis,
                           semiminor_axis = semmn_axis)

            self.rp = ccrs.RotatedPole(pole_longitude = rotnpole_lon,
                                   pole_latitude = rotnpole_lat,
                                   globe = globe)
            
            self.projection = self.rp


        gs = GridSpec(figure = self.fig, 
                      ncols = ncols, 
                      nrows = nrows, 
                      **{k: v for k, v in args.items()
                         if v is not None})

        axs.append(self.fig.add_subplot(gs[0, 0], 
                                        projection = self.projection, 
                                        frameon = self.frame))
        

        if not self.color_bar: 

            self.caxs = None
        
        else:

            if 'right' in self.color_bar: 
                
                divider = make_axes_locatable(axs[0])

                caxs.append(divider.append_axes('right', 
                                                size = self.cax_size, 
                                                pad = self.cax_pad, 
                                                frameon = self.frame, 
                                                axes_class = maxes.Axes))

            if 'top' in self.color_bar: 
                
                divider = make_axes_locatable(axs[0])

                caxs.append(divider.append_axes('top', 
                                                size = self.cax_size, 
                                                pad = self.cax_pad, 
                                                frameon = self.frame, 
                                                axes_class = maxes.Axes))

        
        self.axs = axs
        self.caxs = caxs

        return self

    


@dataclass(kw_only = True)
class triple_001(fig_001):
    
    color_bar: None | list[str] = None
    projection: List[Union[mtr.Transform, ccrs.Projection, Literal['EU3'], None]] | \
                    mtr.Transform | ccrs.Projection | Literal['EU3'] | None = None
    frame: bool = False
    aspect_factor: float = 12.0
    cax_pad: float = 0.8
    cax_size: str = '8%'

    def create(self):

        super().create()

        axs = []
        axtype = []
        caxs = []

        nrows = 1
        ncols = 3

        w1, w2, = 12, 1

        if not self.color_bar: 

            self.caxs = []
            
            ncols_c = ncols

            args = {'width_ratios': None,
                    'height_ratios': None}
        
        else:

            if 'right' in self.color_bar: 

                widths = [w1] * ncols + [w2]

                ncols_c = ncols + 1

                args = {'width_ratios': widths,
                        'height_ratios': None}
                
                gs_c = [0, -1]

        if not isinstance(self.projection, list): 
            
            self.projection = [self.projection for i in range(ncols)]

        if 'EU3' in self.projection:
    
            rotnpole_lat: float = 39.25 
            rotnpole_lon: float = -162.0

            semmj_axis: None | int = 6370000
            semmn_axis: None | int = 6370000 

            globe = ccrs.Globe(semimajor_axis = semmj_axis,
                               semiminor_axis = semmn_axis)

            self.rp = ccrs.RotatedPole(pole_longitude = rotnpole_lon,
                                       pole_latitude = rotnpole_lat,
                                       globe = globe)

        
            self.active_proj = [self.rp if p == 'EU3' else p 
                                for p in self.projection]
            
        else:
            self.active_proj = self.projection

        gs = GridSpec(figure = self.fig, 
                      nrows = nrows,
                      ncols = ncols_c,
                      **{k: v for k, v in args.items()
                         if v is not None})

        for iax in range(ncols):

            axs.append(self.fig.add_subplot(gs[0, iax], 
                                            projection = self.active_proj[iax], 
                                            frameon = self.frame))
            
        if self.color_bar:

            caxs.append(self.fig.add_subplot(gs[*gs_c], 
                                             frameon = self.frame))

        self.axs = axs
        self.caxs = caxs

        return self

        
    def annotation(self, 
                   x : float = 0.05, 
                   y : float = 1.05, 
                   fs: float = 12.0):

        abc = string.ascii_lowercase
    
        list_abc = list(abc)

        for iax, ax in enumerate(self.axs):

            ax.text(x, y, list_abc[iax] + ')', 
                    fontsize = fs,
                    transform = ax.transAxes, 
                    va = 'bottom', 
                    ha = 'center')


@dataclass(kw_only = True)      
class double_001(fig_001):
    
    color_bar: None | list[str] = None
    projection: List[Union[mtr.Transform, ccrs.Projection, Literal['EU3'], None]] | \
                    mtr.Transform | ccrs.Projection | Literal['EU3'] | None = None
    frame: bool = False
    aspect_factor: float = 12.0
    cax_pad: float = 0.8
    cax_size: str = '8%'

    def create(self):

        super().create()

        axs = []
        axtype = []
        caxs = []

        nrows = 1
        ncols = 2

        w1, w2, = 12, 1

        if not self.color_bar: 

            self.caxs = []
            
            ncols_c = ncols

            args = {'width_ratios': None,
                    'height_ratios': None}
        
        else:

            if 'right' in self.color_bar: 

                widths = [w1] * ncols + [w2]

                ncols_c = ncols + 1

                args = {'width_ratios': widths,
                        'height_ratios': None}
                
                gs_c = [0, -1]

        if not isinstance(self.projection, list): 
            
            self.projection = [self.projection for i in range(ncols)]

        if 'EU3' in self.projection:
    
            rotnpole_lat: float = 39.25 
            rotnpole_lon: float = -162.0

            semmj_axis: None | int = 6370000
            semmn_axis: None | int = 6370000 

            globe = ccrs.Globe(semimajor_axis = semmj_axis,
                               semiminor_axis = semmn_axis)

            self.rp = ccrs.RotatedPole(pole_longitude = rotnpole_lon,
                                       pole_latitude = rotnpole_lat,
                                       globe = globe)

        
            self.active_proj = [self.rp if p == 'EU3' else p 
                                for p in self.projection]
            
        else:
            self.active_proj = self.projection

        gs = GridSpec(figure = self.fig, 
                      nrows = nrows,
                      ncols = ncols_c,
                      **{k: v for k, v in args.items()
                         if v is not None})

        for iax in range(ncols):

            axs.append(self.fig.add_subplot(gs[0, iax], 
                                            projection = self.active_proj[iax], 
                                            frameon = self.frame))
            
        if self.color_bar:

            caxs.append(self.fig.add_subplot(gs[*gs_c], 
                                             frameon = self.frame))

        self.axs = axs
        self.caxs = caxs

        return self
        
    def annotation(self, 
                   x : float = 0.05, 
                   y : float = 1.05, 
                   fs: float = 12.0):

        abc = string.ascii_lowercase
    
        list_abc = list(abc)

        for iax, ax in enumerate(self.axs):

            ax.text(x, y, list_abc[iax] + ')', 
                    fontsize = fs,
                    transform = ax.transAxes, 
                    va = 'bottom', 
                    ha = 'center')         
            
@dataclass(kw_only = True)
class quatro_001(fig_001):
    
    projection: List[Union[mtr.Transform, ccrs.Projection, Literal['EU3'], None]] | \
                    mtr.Transform | ccrs.Projection | Literal['EU3'] | None = None
    frame: bool = False
    aspect_factor: float = 12.0
    cax_pad: float = 0.8
    cax_size: str = '8%'

    wspace: float = 0.1
    hspace: float = 0.05

    def create(self):

        super().create()

        axs = []

        nrows = 2
        ncols = 2

        if not isinstance(self.projection, list): 
            
            self.projection = [self.projection for i in range(ncols*nrows)]

        if 'EU3' in self.projection:
    
            rotnpole_lat: float = 39.25 
            rotnpole_lon: float = -162.0

            semmj_axis: None | int = 6370000
            semmn_axis: None | int = 6370000 

            globe = ccrs.Globe(semimajor_axis = semmj_axis,
                               semiminor_axis = semmn_axis)

            self.rp = ccrs.RotatedPole(pole_longitude = rotnpole_lon,
                                       pole_latitude = rotnpole_lat,
                                       globe = globe)

        
            self.active_proj = [self.rp if p == 'EU3' else p 
                                for p in self.projection]
            
        else:
            self.active_proj = self.projection

        gs = GridSpec(figure = self.fig, 
                      nrows = nrows,
                      ncols = ncols,
                      wspace = self.wspace,
                      hspace = self.hspace)
        
        positions = [gs[0, 0], gs[0, 1], gs[1, 0], gs[1, 1]]

        for iax, ax in enumerate(positions):

            axs.append(self.fig.add_subplot(ax, 
                                            projection = self.active_proj[iax], 
                                            frameon = self.frame))

        self.axs = axs

        return self
        
    def annotation(self, 
                   x : float = 0.05, 
                   y : float = 1.05, 
                   fs: float = 12.0):

        abc = string.ascii_lowercase
    
        list_abc = list(abc)

        for iax, ax in enumerate(self.axs):

            ax.text(x, y, list_abc[iax] + ')', 
                    fontsize = fs,
                    transform = ax.transAxes, 
                    va = 'bottom', 
                    ha = 'center')