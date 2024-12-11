from cartopy.crs import Projection
import matplotlib.pyplot as plt
import numpy as np


def colormesh(ax, x, y, array, cmap: str = 'coolwarm_r', v0: float = None, v1: float = None, projection = None):

    artist = ax.pcolormesh(x, y, array, cmap = cmap, vmin = v0, vmax = v1, transform = projection, zorder=0)
    
    return artist


def scatter(ax: plt.Axes, 
            xs: np.ndarray, 
            ys: np.ndarray, 
            marker: str | None = None, 
            sizes_marker: int = 50, 
            colors_marker: str = 'black', 
            edgecolor: str | list | None = None,
            face: bool = True, 
            alpha: float = 0.7, 
            projection: Projection | None = None, 
            zorder: int = 5):

    if isinstance(sizes_marker, int): 
        sizes_marker = [sizes_marker] * len(xs)

    if isinstance(colors_marker, str): 
        colors_marker = [colors_marker] * len(xs)

    if isinstance(edgecolor, str):
        edgecolor = [edgecolor] * len(xs)

    if projection == None: 
        projection = ax.transData
    
    artist = ax.scatter(xs, 
                        ys, 
                        marker = marker, 
                        s = sizes_marker, 
                        c = colors_marker,
                        edgecolors = edgecolor,
                        alpha = alpha, 
                        transform = projection, 
                        zorder = zorder)
    
    if not face: artist.set_facecolor("none")

    return artist


def xy(ax, xs, ys, marker, sizes_marker = 50, colors_marker = [], projection = None, 
       axhv_color: str = 'k', axhv_ls: str = '--', axhv_lw: float = 0.7, axhv_alpha: float = 0.8, axhv_dashes: tuple = (4, 4),
       diag_color: str = 'k', diag_ls: str = '--', diag_lw: float = 0.7, diag_alpha: float = 0.8, diag_dashes = (4,4),
       xlabel: str = '', ylabel: str = '', fs_label: int = 9):

    from my_.plot.basic import scatter
    from my_.plot.init_ax import init_xy
    
    init_xy(ax, xs, ys, axhv_color, axhv_ls, axhv_lw, axhv_alpha, axhv_dashes,
       diag_color, diag_ls, diag_lw, diag_alpha, diag_dashes, xlabel, ylabel, fs_label)

    artist = scatter(ax, xs, ys, marker = marker, sizes_markers = sizes_marker, colors_markers = colors_marker, projection = projection)

    return artist


def bar(ax, xs, ys, color, width: float = 0.8, alpha: float = 0.8):

    artist = ax.bar(xs, ys, color = color, width = width, alpha = alpha, zorder = 5)

    return artist


def hist(ax, array, bins = 'auto', density = True,  histtype = 'stepfilled', color= 'dimgray', alpha: float = 0.8, zorder: int = 3):

    artist = ax.hist(array, bins = bins, density = density, histtype = histtype, color = color, alpha = alpha, zorder = zorder)

    return artist


def plot(ax: plt.Axes, 
         xs: np.ndarray, 
         ys: np.ndarray, 
         colors: str | list = 'k', 
         edgecolors: str | list = 'k',
         style: str = '-', 
         lw: float = 1.0, 
         alpha: float = 0.8,
         cycle_direction: int = 0,
         projection: None | Projection = None,
         markersize: float = 1.0,
         marker: str | list = '', 
         fillstyle = 'full',
         zorder = 5):
    
    l = ys.shape[1] if cycle_direction else len(xs)

    if isinstance(lw, float):
        lw = [lw] * l

    if isinstance(markersize, int) \
       or isinstance(markersize, float): 
       markersize = [markersize] * l

    if isinstance(colors, str): 
        colors = [colors] * l

    if len(colors) == 1:
        colors = colors * l

    if projection is None: projection = ax.transData

    ax.set_prop_cycle(color = colors,
                      linewidth = lw,
                      markersize = markersize)

    artist = ax.plot(xs, ys, 
                     transform = projection, 
                     marker = marker, 
                     ls = style,
                     fillstyle = fillstyle,
                     alpha = alpha, 
                     zorder = zorder)

    return artist


def fill(ax, xs, y1s, y2s, colors, alpha: float = 0.4, zorder: int = 2):

    if (y1s.ndim == 2):

        for iy, y1 in enumerate(y1s):
            
            artist = ax.fill_between(xs, y1s[y1], 
                                     y2s.iloc[:,iy], 
                                     color = colors[iy], 
                                     alpha = alpha, 
                                     zorder = zorder)

    return artist


def pie(ax, shares, colors, **kwargs):

    ax.pie(shares, colors = colors, **kwargs)


def error(ax: plt.Axes, 
          xs: np.ndarray, 
          ys: np.ndarray, 
          x_err: np.ndarray | None = None, 
          y_err: np.ndarray | None = None, 
          ecolors: list | str | None = None, 
          elinewidth: str | None = None, 
          capsize: float | None = 0.0, 
          capthick: float | None = None,
          alpha: float = 0.8, 
          zorder: int = 5):
    
    if x_err is None: x_err = [0] * len(y_err)
    if y_err is None: y_err = [0] * len(x_err)
    if isinstance(ecolors, str): ecolors = [ecolors]

    for i in range(len(ecolors)):

        artist = ax.errorbar(xs[i], ys[i], 
                             xerr = x_err[i], yerr = y_err[i], 
                             ecolor = ecolors[i],
                             elinewidth = elinewidth,
                             capsize = capsize, 
                             capthick = capthick,
                             linestyle='', 
                             alpha = alpha, 
                             zorder = zorder)
    
    return artist

def hlines(ax: plt.Axes,
           ys: np.ndarray,
           xmin: np.ndarray,
           xmax: np.ndarray,
           colors: str | list = None,
           linestyle: str = 'solid',
           linewidth: int | float = 2,
           alpha: float = 0.8,
           zorder: int = 5):
    
    artist = ax.hlines(y = ys,
                       xmin = xmin,
                       xmax = xmax,
                       colors = colors,
                       linestyle = linestyle,
                       linewidth = linewidth,
                       alpha = alpha,
                       zorder = zorder)
    
    return artist


def vlines(ax: plt.Axes,
           xs: np.ndarray,
           ymin: np.ndarray,
           ymax: np.ndarray,
           colors: str | list = None,
           linestyle: str = 'solid',
           linewidth: int | float = 2,
           alpha: float = 0.8,
           zorder: int = 5):
    
    artist = ax.axvline(x = xs,
                        ymin = ymin,
                        ymax = ymax,
                        color = colors,
                        linestyle = linestyle,
                        linewidth = linewidth,
                        alpha = alpha,
                        zorder = zorder)
    
    return artist