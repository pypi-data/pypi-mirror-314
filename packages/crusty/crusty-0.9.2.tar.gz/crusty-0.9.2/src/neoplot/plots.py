from ctypes import Union
import matplotlib.pyplot as plt
from sklearn import base
import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from matplotlib.ticker import MaxNLocator
import matplotlib.dates as mdates
import matplotlib.transforms as mtr
import matplotlib.artist as mpla
import matplotlib.axes as mplax
from cartopy.mpl.geoaxes import GeoAxes
from cartopy.mpl.ticker import LongitudeLocator, LatitudeLocator
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.colors import LogNorm, PowerNorm
from typing import List, Iterable, Sequence

from typing import Literal

@dataclass(kw_only = True)
class base_001:

    ax: plt.Axes

    grid: bool = True 
    grid_which: Literal['major', 'minor', 'both'] = 'major'
    grid_color: str = 'dimgray'
    grid_ls: str = '--'
    grid_alpha: float = 0.8
    tick_pad: float = 10.0

    no_spines: None | list[str] = field(default_factory = 
                                        lambda: ['top', 
                                                 'right', 
                                                 'bottom', 
                                                 'left'])

    y_title: float = 1.0
    fs_title: int = 10 
    title: str = '' 

    axis: bool = False
    axis_color: str = 'k' 
    axis_ls: str = '--' 
    axis_lw: float = 0.7 
    axis_alpha: float = 0.8 
    axis_dashes: tuple = (4, 4)

    xlabel: str = '' 
    ylabel: str = '' 

    fs_label: float = 12.0
    ax_tag: str = ''
    ax_tag_x: float = 0.5
    ax_tag_y: float = 1.0 


    def decoration(self):
        
        if self.grid:
        
            self.ax.grid(which = self.grid_which, 
                         color = self.grid_color, 
                         visible = True, 
                         ls = self.grid_ls, 
                         alpha = self.grid_alpha, 
                         zorder = 0)


        if self.no_spines is not None:
            for spine in self.no_spines:
                    self.ax.spines[spine].set_visible(False)
            
        self.ax.set_title(self.title, 
                          fontsize = self.fs_title, 
                          y = self.y_title)
        
        self.ax.set_ylabel(self.ylabel, 
                           fontsize = self.fs_label)
        
        self.ax.set_xlabel(self.xlabel, 
                           fontsize = self.fs_label)

        self.ax.tick_params(axis = 'both', 
                            which = 'major', 
                            pad = self.tick_pad)
        
        if self.axis:

            self.ax.axline((0, 0), (0, 1),
                           color = self.axis_color, 
                           ls = self.axis_ls, 
                           lw = self.axis_lw, 
                           alpha = self.axis_alpha, 
                           dashes = self.axis_dashes,
                           transform = self.ax.transAxes, 
                           zorder = 0)

            self.ax.axline((0, 0), (1, 0),
                           color = self.axis_color, 
                           ls = self.axis_ls, 
                           lw = self.axis_lw, 
                           alpha = self.axis_alpha, 
                           dashes = self.axis_dashes, 
                           transform = self.ax.transAxes,
                           zorder = 0)
        
        props = dict(facecolor = 'white', 
                     edgecolor = 'none', 
                     alpha = 0.85)

        self.ax.text(self.ax_tag_x, 
                     self.ax_tag_y, 
                     self.ax_tag, 
                     fontsize = self.fs_label, 
                     transform = self.ax.transAxes, 
                     va = 'bottom', 
                     ha = 'center',
                     bbox = props)


@dataclass(kw_only = True)
class time_series(base_001):
    
    xs: np.ndarray | pd.DatetimeIndex
    ys: np.ndarray | pd.Series

    fs_ticks: float = 10.0
    ticks_y: bool = True
    ticks_x: bool = True
    nticks_y: int = 5
    nticks_x: int = 5
    integery: bool = False

    date_limits: None | list[np.datetime64] = None
    y_limits: None | list[float] = None
    y_ticks_rel_b: float = 0.1
    x_ticks_rel_b: float = 0.1

    def ticks(self):

        xlocator = mdates.AutoDateLocator(minticks = self.nticks_x)
        ylocator = MaxNLocator(prune = 'both', 
                               nbins = self.nticks_y, 
                               integer = self.integery)
    
        self.ax.xaxis.set_major_formatter(mdates.AutoDateFormatter(xlocator))

        self.ax.yaxis.set_major_locator(ylocator)
        self.ax.xaxis.set_major_locator(xlocator)

        if not self.ticks_x: self.ax.set_xticklabels([])
        if not self.ticks_y: self.ax.set_yticklabels([])

        self.ax.tick_params(axis = 'both', 
                            which = 'major', 
                            labelsize = self.fs_ticks)


    def limits(self):

        if self.date_limits is None:
        
            tsmax = np.max(self.xs)
            tsmin = np.min(self.xs)


            rel_d = (tsmax - tsmin).days * self.x_ticks_rel_b

            rel_dd = pd.Timedelta(rel_d, 'D')

            self.ax.set_xlim(tsmin - rel_dd, tsmax + rel_dd)
        
        else:

            for id, date in enumerate(self.date_limits):

                if isinstance(date, str):

                    self.date_limits[id] = pd.to_datetime(date).to_datetime64()

            self.ax.set_xlim(self.date_limits[0], 
                             self.date_limits[1])

            
        if self.y_limits is None:
            
            tsmax = np.nanmax(self.ys) 
            tsmin = np.nanmin(self.ys)

            tsabs = np.max(np.abs([tsmax, tsmin]))

            tsmax_rel = tsmax + tsabs * self.y_ticks_rel_b
            tsmin_rel = tsmin - tsabs * self.y_ticks_rel_b

            self.ax.set_ylim(tsmin_rel, tsmax_rel)

        else:

            self.ax.set_ylim(self.y_limits[0], 
                             self.y_limits[1])
            
    
    def create(self):

        super().decoration()
        
        self.ticks()
        self.limits()

        return self

        
    def plot(self,
             xs: np.ndarray | pd.DatetimeIndex,
             ys: np.ndarray | pd.Series,
             colors: str | list[str] = 'k',
             style: str | list[str] = '',
             lw: float | list[float] = 1.0,
             alpha: float = 0.8,
             projection: None | mtr.Transform | ccrs.Projection = None,
             markersize: float = 3.0,
             marker: str | list[str] = 'o',
             fillstyle: str = 'full',
             zorder: int = 5):

        ys = np.stack([y.flatten() for y in ys], axis = 1)
        
        if projection is None: 
            projection = self.ax.transData

        if isinstance(colors, str):
            colors = [colors]
        
        if isinstance(style, str):
            style = [style]
        
        if isinstance(marker, str):
            marker = [marker] 
            
        if isinstance(lw, int) or isinstance(lw, float):
            lw = [lw]

        self.ax.set_prop_cycle(color = colors,
                               linestyle = style,
                               marker = marker,
                               linewidth = lw)

        self.ax.plot(xs, 
                     ys,
                     transform = projection, 
                     markersize = markersize,
                     fillstyle = fillstyle,
                     alpha = alpha, 
                     zorder = zorder)
        
        
    def fillb(self,
              xs: np.ndarray | pd.DatetimeIndex,
              lower: np.ndarray | pd.Series,
              upper: np.ndarray | pd.Series,
              color: str | list[str] = 'k',
              alpha: float = 0.8,
              projection: None | mtr.Transform | ccrs.Projection = None,
              zorder: int = 3):
        
        if projection is None: 
            projection = self.ax.transData
            
        self.ax.fill_between(xs, lower, upper, 
                             color = color, 
                             transform = projection,
                             alpha = alpha,
                             zorder = zorder)



@dataclass(kw_only = True)
class amap(base_001):
    
    ax: GeoAxes

    grid: bool = False

    lon_extents: list[float] = field(default_factory =
                                    lambda: [-180.0, 180.0])
    lat_extents: list[float] = field(default_factory =
                                     lambda: [-90, 90])

    semmj_axis: None | int = 6370000
    semmn_axis: None | int = 6370000 

    fs_ticks: float = 7.0
    ticks_y: bool = True
    ticks_x: bool = True
    nticks_y: int = 2
    nticks_x: int = 2
    integery: bool = True
    integerx: bool = True
    
    feature_land: bool = False
    feature_ocean: bool = False
    
    land_alpha: float = 0.7
    ocean_alpha: float = 0.7
    land_color: str = 'gray'
    ocean_color: str = 'steelblue'
    lw_coast: float = 0.8
    lw_lines: float = 0.8
    color_lines: str = 'grey'
    ls_lines: str = '--'
    label_lines: list[str] = field(default_factory = 
                                        lambda: ['right', 
                                                 'bottom'])
    
    plot_projection: ccrs.Projection = ccrs.PlateCarree()

    def __post_init__(self):

        if isinstance(self.ax, plt.Axes): NotImplementedError('Wrong axis type')

    def features(self):

        if self.feature_ocean:
            self.ax.add_feature(cfeature.OCEAN,
                                color = self.ocean_color, 
                                alpha = self.ocean_alpha, 
                                zorder = 0)
            
        if self.feature_land:
            self.ax.add_feature(cfeature.LAND,
                                color = self.land_color, 
                                alpha = self.land_alpha, 
                                zorder = 0)
            
        self.ax.coastlines(linewidth = self.lw_coast, zorder=2)
            
    def limits(self):

        self.lon_extents, self.lat_extents, _ = self.ax.projection.transform_points(
                                                        self.plot_projection,
                                                        np.array(self.lon_extents),
                                                        np.array(self.lat_extents)).T

        self.ax.set_extent([*self.lon_extents,
                            *self.lat_extents])
            
    
    def lines(self):
        
        gl = self.ax.gridlines(crs = self.plot_projection, 
                               linewidth = self.lw_lines,
                               color = self.color_lines, 
                               linestyle = self.ls_lines, 
                               draw_labels = True, 
                               x_inline = False, 
                               y_inline = False, 
                               zorder = 5)


        if 'right' not in self.label_lines: 
            gl.right_labels = False
        if 'bottom' not in self.label_lines:
            gl.bottom_labels = False
        if 'top' not in self.label_lines:
            gl.top_labels = False
        if 'left' not in self.label_lines:
            gl.left_labels = False

        self.grid_lines = gl


    def ticks(self):

        ylocator = LatitudeLocator(prune = 'both', 
                                   nbins = self.nticks_y, 
                                   integer = self.integery)
        
        xlocator = LongitudeLocator(prune = 'both', 
                                    nbins = self.nticks_x, 
                                    integer = self.integerx)
        
        self.grid_lines.ylocator = ylocator
        self.grid_lines.xlocator = xlocator

        self.grid_lines.xlabel_style = {'size': self.fs_ticks}
        self.grid_lines.ylabel_style = {'size': self.fs_ticks}

    
    def create(self):

        super().decoration()
        
        self.features()
        self.limits()
        self.lines()
        self.ticks()

        return self
    

    def colormesh(self,
                  lon: np.ndarray,
                  lat: np.ndarray,
                  array: np.ndarray,
                  cmap: str = 'viridis',
                  vmin: float | None = None,
                  vmax: float | None = None,
                  norm: Literal['log'] | None = None,
                  alpha: float = 1.0):
        
        if norm == 'log':

            norm_a = LogNorm(vmin = vmin,
                             vmax = vmax)
            
            vmin_a = None
            vmax_a = None

        elif norm == 'power':

            norm_a = PowerNorm(vmin = vmin,
                             vmax = vmax)
            
            vmin_a = None
            vmax_a = None

        else:

            norm_a = norm
            vmin_a = vmin
            vmax_a = vmax
        
        artist = self.ax.pcolormesh(lon, 
                                    lat, 
                                    array, 
                                    cmap = cmap, 
                                    vmin = vmin_a, 
                                    vmax = vmax_a, 
                                    transform = self.plot_projection, 
                                    zorder = 0,
                                    norm = norm_a,
                                    alpha = alpha)
    
        return artist
    
    def scatter(self,
                lats: np.ndarray | list[float],
                lons: np.ndarray | list[float],
                color: str | np.ndarray | list[float] | None = 'k',
                cmap: str | None = None,
                vmin: float | None = None,
                vmax: float | None = None,
                alpha: float = 0.8,
                markersize: float | np.ndarray = 3.0,
                marker: str | list[str] = 'o',
                zorder: int = 5):

        artist = self.ax.scatter(lons, 
                                 lats,
                                 s = markersize,
                                 c = color,
                                 cmap = cmap,
                                 vmin = vmin,
                                 vmax = vmax,
                                 transform = self.plot_projection, 
                                 marker = marker,
                                 alpha = alpha, 
                                 zorder = zorder)
        
        return artist

    def colorbar(self,
                 artist: mpla.Artist,
                 ax: mplax.Axes | Iterable[mplax.Axes],
                 label: str = '',
                 pad: float = 0.01,
                 label_pad: float = 10.0,
                 shrink: float = 1.0,
                 fraction: float = 0.5,
                 fs_label: float = 7.0,
                 aspect: float = 10.0,
                 tick_labels: list | None = None,
                 orientation: Literal['vertical', 'horizontal'] = 'vertical',
                 extend: Literal['both', 'neither', 'min', 'max'] = 'both',
                 label_rotation: float = 270.0):
        
        cbar = plt.colorbar(artist, 
                            ax = ax, 
                            extend = extend, 
                            shrink = shrink, 
                            fraction = fraction,
                            aspect = aspect,
                            orientation = orientation,
                            pad = pad)
        
        cbar.ax.tick_params(labelsize = fs_label)

        cbar.outline.set_visible(False)

        len_tick_labels = len(tick_labels) if tick_labels is not None else 0

        if orientation == 'vertical':

            cbar.ax.set_ylabel(label, 
                               labelpad = label_pad, 
                               rotation = label_rotation, 
                               fontsize = fs_label)

        elif orientation == 'horizontal': 

            cbar.ax.set_xlabel(label, 
                               labelpad = label_pad, 
                               rotation = label_rotation, 
                               fontsize = fs_label)
        
        if len_tick_labels > 0:

            positions = np.linspace(0.5, 
                                    (len_tick_labels - 1) - 0.5, 
                                    len_tick_labels)

            if orientation == 'vertical':
        
                cbar.ax.set_yticks(positions, 
                                   tick_labels, 
                                   fontsize = fs_label)

            if orientation == 'horizontal':
                cbar.ax.set_xticks(positions, 
                                   tick_labels, 
                                   fontsize = fs_label)
            
        return cbar
        

@dataclass(kw_only = True)
class boxplot(base_001):

    fs_ticks: float = 9
    
    def create(self):

        super().decoration()

        self.ax.tick_params(axis = 'both',
                            which = 'major',
                            labelsize = self.fs_ticks)
        
        self.ax.yaxis.get_offset_text().set_fontsize(self.fs_ticks)

        return self
        
    def plot(self,
             data: Sequence[np.ndarray | pd.Series],
             tick_labels: list[str], 
             patches: bool = True,
             fliers: bool = False,
             notch: bool = True,
             colors: str | list[str] = 'k',
             widths: float | list[float] = 0.56,
             ls: str = '-',
             lw: float | list[float] = 1.0,
             median_lw: float = 1.0,
             whisker_lw: float = 1.0,
             line_color = 'k',
             median_color = '#FB9902',
             alpha: float = 0.8,
             zorder: int = 5):

        boxprops = {'linestyle': ls,
                    'linewidth': lw,
                    'color': line_color,
                    'alpha': alpha,}
        
        medianprops = {'linewidth': median_lw,
                       'color': median_color}
        
        whiskerprops = {'linewidth': whisker_lw,
                       'color': line_color}

        boxp = self.ax.boxplot(data,
                               patch_artist = patches,
                               showfliers = fliers,
                               notch = notch,
                               widths = widths,
                               boxprops = boxprops,
                               medianprops = medianprops,
                               whiskerprops = whiskerprops,
                               labels = tick_labels,
                               zorder = zorder,)

        #for element in ['whiskers', 'fliers', 'means', 'medians', 'caps']:
        #    plt.setp(boxp[element], 
        #             color = line_color,
        #             alpha = alpha)
            
        for patch, color in zip(boxp['boxes'], colors):
            plt.setp(patch, 
                     facecolor = color,
                     alpha = alpha)
            
@dataclass(kw_only = True)
class xy_numeric(base_001):
   
    xs: np.ndarray | pd.DatetimeIndex
    ys: np.ndarray | pd.Series

    fs_ticks: float = 10.0
    ticks_y: bool = True
    ticks_x: bool = True
    nticks_y: int = 5
    nticks_x: int = 5
    integery: bool = False
    integerx: bool = False
    invertx: bool = False
    inverty: bool = False

    x_limits: None | list[float] = None
    y_limits: None | list[float] = None
    y_ticks_rel_b: float = 0.1
    x_ticks_rel_b: float = 0.1

    def ticks(self):

        xlocator = MaxNLocator(prune = 'both', 
                               nbins = self.nticks_x, 
                               integer = self.integerx)
        
        ylocator = MaxNLocator(prune = 'both', 
                               nbins = self.nticks_y, 
                               integer = self.integery)

        self.ax.yaxis.set_major_locator(ylocator)
        self.ax.xaxis.set_major_locator(xlocator)

        if not self.ticks_x: self.ax.set_xticklabels([])
        if not self.ticks_y: self.ax.set_yticklabels([])

        self.ax.tick_params(axis = 'both', 
                            which = 'major', 
                            labelsize = self.fs_ticks)


    def limits(self):

        if self.x_limits is None:
            
            tsmax = np.nanmax(self.xs) 
            tsmin = np.nanmin(self.xs)

            tsabs = np.max(np.abs([tsmax, tsmin]))

            tsmax_rel = tsmax + tsabs * self.x_ticks_rel_b
            tsmin_rel = tsmin - tsabs * self.x_ticks_rel_b

            self.ax.set_ylim(tsmin_rel, tsmax_rel)

        else:

            self.ax.set_ylim(self.x_limits[0], 
                             self.x_limits[1])
            
        if self.y_limits is None:
            
            tsmax = np.nanmax(self.ys) 
            tsmin = np.nanmin(self.ys)

            tsabs = np.max(np.abs([tsmax, tsmin]))

            tsmax_rel = tsmax + tsabs * self.y_ticks_rel_b
            tsmin_rel = tsmin - tsabs * self.y_ticks_rel_b

            self.ax.set_ylim(tsmin_rel, tsmax_rel)

        else:

            self.ax.set_ylim(self.y_limits[0], 
                             self.y_limits[1])
        
        if self.invertx: plt.gca().invert_xaxis()
        if self.inverty: plt.gca().invert_yaxis()
    
    def create(self):

        super().decoration()
        
        self.ticks()
        self.limits()

        return self

        
    def plot(self,
             xs: np.ndarray | pd.Series,
             ys: np.ndarray | pd.Series,
             colors: str | list[str] = 'k',
             style: str | list[str] = 'None',
             lw: float | list[float] = 1.0,
             alpha: float = 0.8,
             projection: None | mtr.Transform | ccrs.Projection = None,
             markersize: float = 3.0,
             marker: str | list[str] = 'o',
             fillstyle: str = 'full',
             zorder: int = 5):

        ys = np.stack([y.flatten() for y in ys], axis = 0)
        
        if projection is None: 
            projection = self.ax.transData

        if isinstance(colors, str):
            colors = [colors]
        
        if isinstance(style, str):
            style = [style]
        
        if isinstance(marker, str):
            marker = [marker] 
            
        if isinstance(lw, int) or isinstance(lw, float):
            lw = [lw]

        self.ax.set_prop_cycle(color = colors,
                               linestyle = style,
                               marker = marker,
                               linewidth = lw)

        self.ax.plot(xs, 
                     ys,
                     transform = projection, 
                     markersize = markersize,
                     fillstyle = fillstyle,
                     alpha = alpha, 
                     zorder = zorder)