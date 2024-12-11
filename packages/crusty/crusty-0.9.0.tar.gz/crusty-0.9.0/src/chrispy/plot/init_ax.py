

import matplotlib.pyplot as plt
import numpy as np
from cartopy import crs
import pandas as pd

def init_xy(ax: plt.Axes, 
            xs: np.ndarray | pd.Series | pd.DataFrame, 
            ys: np.ndarray | pd.Series | pd.DataFrame, 
            xerr: np.ndarray | pd.Series | pd.DataFrame | None = None, 
            yerr: np.ndarray | pd.Series | pd.DataFrame | None = None, 
            axhv_color: str = 'k', 
            axhv_ls: str = '--', 
            axhv_lw: float = 0.7, 
            axhv_alpha: float = 0.8, 
            axhv_dashes: tuple = (4, 4),
            diag_color: str = 'k', 
            diag_ls: str = '--', 
            diag_lw: float = 0.7, 
            diag_alpha: float = 0.8, 
            diag_dashes: tuple = (4,4),
            title: str = '', 
            xlabel: str = '', 
            ylabel: str = '', 
            y_title: float = 1.1, 
            fs_title: int = 14, 
            fs_label: int = 12, 
            fs_ticks: int = 10,
            ax_tag: str | None = None, 
            ax_tag_x: float = 0.5, 
            ax_tag_y: float = 1.0):
    
    from my_.plot.limits import axgrid, common_free_lims, numeric_ticks
    from my_.plot.style import nospines

    axgrid(ax)
    nospines(ax)

    plt.suptitle(title, fontsize = fs_title, y = y_title)
    
    ax.set_ylabel(ylabel, fontsize = fs_label)
    ax.set_xlabel(xlabel, fontsize = fs_label)
    
    ax.tick_params(axis='both', which='major', pad=10)

    ax.axhline(0, color = axhv_color, 
                ls = axhv_ls, 
                lw = axhv_lw, 
                alpha = axhv_alpha, 
                dashes = axhv_dashes, 
                zorder = 1)
    
    ax.axvline(0, color = axhv_color, 
                ls = axhv_ls, 
                lw = axhv_lw, 
                alpha = axhv_alpha, 
                dashes = axhv_dashes, 
                zorder = 1)

    ax.plot([-1.1, 1.1], [-1.1, 1.1], 
            transform = ax.transAxes, 
            color = diag_color, 
            ls = diag_ls, 
            lw = diag_lw, 
            alpha = diag_alpha, 
            dashes = diag_dashes, 
            zorder = 1)
    
    props = dict(facecolor='white', edgecolor='none', alpha=0.85)

    if ax_tag is not None:

        ax.text(ax_tag_x, 
                ax_tag_y, 
                ax_tag, 
                fontsize = fs_label, 
                transform = ax.transAxes, 
                va = 'bottom', 
                ha = 'center', 
                bbox = props)
    
    ax.axis('square')
    
    common_free_lims(ax = ax, 
                     xs = xs, 
                     ys = ys,
                     xerr = xerr,
                     yerr = yerr)

    numeric_ticks(ax, fs_ticks = fs_ticks)


def init_bar(ax, xs, ys, title: str = '', fs_title: float = 14, y_title: float = 1.0, ylabel: str = '', xlabel: str = '', fs_label: float = 12,
             axhv_color: str = 'k', axhv_ls: str = '--', axhv_lw: float = 0.7, axhv_alpha: float = 0.8, axhv_dashes: tuple = (4, 4),
             ax_tag = '', ax_tag_x: float = 0.5, ax_tag_y: float = 1.0, fs_ticks: float = 10,):

    from my_.plot.limits import axgrid, bar_lims, numeric_ticks
    from my_.plot.style import nospines

    import matplotlib.pyplot as plt

    axgrid(ax)
    nospines(ax)

    plt.suptitle(title, fontsize = fs_title, y = y_title)
    
    ax.set_ylabel(ylabel, fontsize = fs_label)
    ax.set_xlabel(xlabel, fontsize = fs_label)

    ax.axhline(0, color = axhv_color, 
                ls = axhv_ls, lw = axhv_lw, 
                alpha = axhv_alpha, dashes = axhv_dashes, zorder = 0)
    
    props = dict(facecolor='white', edgecolor='none', alpha=0.85)

    ax.text(ax_tag_x, ax_tag_y, ax_tag, fontsize = fs_label, transform = ax.transAxes, va = 'bottom', ha = 'center', bbox = props)

    bar_lims(ax, xs, ys)

    numeric_ticks(ax, nticks_x = len(ys), nticks_y = 5, fs_ticks = fs_ticks, integerx = True, x = False)


def EU3_plot_init(rotnpole_lat: float = 39.25, 
                  rotnpole_lon: float = -162.0, 
                  semmj_axis: int = 6370000, 
                  semmn_axis: int = 6370000, 
                  lon_extents: list = [351.1, 57], 
                  lat_extents: list = [27, 65.7]):

    rp = crs.RotatedPole(pole_longitude = rotnpole_lon,
                         pole_latitude = rotnpole_lat,
                         globe = crs.Globe(semimajor_axis = semmj_axis,
                         semiminor_axis = semmn_axis))
    
    pc = crs.PlateCarree()

    xs, ys, _ = rp.transform_points(pc, np.array(lon_extents), np.array(lat_extents)).T
    
    return rp, pc, xs, ys


def init_ts(ax: plt.Axes, 
            xs: np.ndarray | pd.Series | pd.DataFrame, 
            ys: np.ndarray | pd.Series | pd.DataFrame, 
            axhv_color: str = 'k', 
            axhv_ls: str = '--', 
            axhv_lw: float = 0.7, 
            axhv_alpha: float = 0.8, 
            axhv_dashes: tuple = (4, 4),
            title: str = '', 
            xlabel: str = '', 
            ylabel: str = '', 
            y_title: float = 1.1, 
            fs_title: int = 14, 
            fs_label: int = 12, 
            fs_ticks = 10,
            ax_tag = '', 
            ax_tag_x: float = 0.5, 
            ax_tag_y: float = 1.0):
    
    from my_.plot.style import nospines
    from my_.plot.limits import axgrid, numeric_ticks, free_lims

    axgrid(ax)
    nospines(ax)

    plt.suptitle(title, 
                 fontsize = fs_title, 
                 y = y_title)
    
    ax.set_ylabel(ylabel, 
                  fontsize = fs_label)
    
    ax.set_xlabel(xlabel, 
                  fontsize = fs_label)
    
    ax.tick_params(axis='both', 
                   which='major', 
                   pad=10)

    ax.axhline(0, color = axhv_color, 
               ls = axhv_ls, 
               lw = axhv_lw, 
               alpha = axhv_alpha, 
               dashes = axhv_dashes, 
               zorder = 1)
    
    ax.axvline(0, color = axhv_color, 
                ls = axhv_ls, 
                lw = axhv_lw, 
                alpha = axhv_alpha, 
                dashes = axhv_dashes, 
                zorder = 1)
    
    props = dict(facecolor = 'white', 
                 edgecolor = 'none', 
                 alpha = 0.85)

    ax.text(ax_tag_x, 
            ax_tag_y, 
            ax_tag, 
            fontsize = fs_label, 
            transform = ax.transAxes, 
            va = 'bottom', 
            ha = 'center', 
            bbox = props)

    numeric_ticks(ax, fs_ticks = fs_ticks)
    free_lims(ax, xs, ys)


def init_lol(ax: plt.Axes, 
             xs: np.ndarray | pd.Series | pd.DataFrame, 
             ys: np.ndarray | pd.Series | pd.DataFrame, 
             axhv_color: str = 'k', 
             axhv_ls: str = '--', 
             axhv_lw: float = 0.7, 
             axhv_alpha: float = 0.8, 
             axhv_dashes: tuple = (4, 4),
             title: str = '', 
             xlabel: str = '', 
             ylabel: str = '', 
             y_title: float = 1.1, 
             fs_title: int = 14, 
             fs_label: int = 12, 
             fs_ticks = 10,
             ax_tag = '', 
             ax_tag_x: float = 0.5, 
             ax_tag_y: float = 1.0):
    
    from my_.plot.style import nospines
    from my_.plot.limits import axgrid, numeric_ticks, free_lims, bar_lims

    axgrid(ax)
    nospines(ax)

    ax.set_title(title, 
                 fontsize = fs_title, 
                 y = y_title)
    
    ax.set_ylabel(ylabel, 
                  fontsize = fs_label)
    
    ax.set_xlabel(xlabel, 
                  fontsize = fs_label)
    
    ax.tick_params(axis='both', 
                   which='major', 
                   pad=10)
    
    props = dict(facecolor = 'white', 
                 edgecolor = 'none', 
                 alpha = 0.8)

    ax.text(ax_tag_x, 
            ax_tag_y, 
            ax_tag, 
            fontsize = fs_label, 
            transform = ax.transAxes, 
            va = 'bottom', 
            ha = 'center', 
            bbox = props)

    numeric_ticks(ax, 
                  nticks_x = 4, 
                  nticks_y = len(ys) + 1, 
                  fs_ticks = fs_ticks, 
                  integery = True,
                  integerx = True)
    

def init_ts_2(ax, xs, ys, axhv_color: str = 'k', axhv_ls: str = '--', axhv_lw: float = 0.7, axhv_alpha: float = 0.8, axhv_dashes: tuple = (4, 4),
       title: str = '', xlabel: str = '', ylabel: str = '', y_title: float = 1.1, fs_title: int = 14, fs_label: int = 12, fs_ticks = 10,
       ax_tag = '', ax_tag_x: float = 0.5, ax_tag_y: float = 1.0, grid: bool = True, spines: bool = False):
    
    from my_.plot.style import nospines
    from my_.plot.limits import axgrid, numeric_ticks_2, free_date_lim, free_numeric_lim

    import matplotlib.pyplot as plt

    if grid: axgrid(ax)
    if not spines: nospines(ax)

    plt.suptitle(title, fontsize = fs_title, y = y_title)
    
    ax.set_ylabel(ylabel, fontsize = fs_label)
    ax.set_xlabel(xlabel, fontsize = fs_label)
    
    ax.tick_params(axis='both', which='major', pad=10)

    ax.axhline(0, color = axhv_color, 
                ls = axhv_ls, lw = axhv_lw, 
                alpha = axhv_alpha, dashes = axhv_dashes, zorder = 0)
    
    ax.axvline(0, color = axhv_color, 
                ls = axhv_ls, lw = axhv_lw, 
                alpha = axhv_alpha, dashes = axhv_dashes, zorder = 0)
    
    props = dict(facecolor='white', edgecolor='none', alpha=0.85)

    ax.text(ax_tag_x, ax_tag_y, ax_tag, fontsize = fs_label, transform = ax.transAxes, va = 'bottom', ha = 'center', bbox = props)

    numeric_ticks_2(ax, fs_ticks = fs_ticks, time_x = True)
    free_date_lim(ax, xs)
    free_numeric_lim(ax, ys)



def init_dist(ax: plt.axes,
                xs: np.ndarray | pd.Series | pd.DataFrame,
                ys: np.ndarray | pd.Series | pd.DataFrame,
                axhv_color: str = 'k',
                axhv_ls: str = '--', 
                axhv_lw: float = 0.7, 
                axhv_alpha: float = 0.8, 
                axhv_dashes: tuple = (4, 4),
                title: str = '', 
                xlabel: str = '', 
                ylabel: str = '', 
                y_title: float = 1.1, 
                fs_title: float = 14.0, 
                fs_label: float = 12.0, 
                fs_ticks: float = 10.0,
                ax_tag: str = '', 
                ax_tag_x: float = 0.5, 
                ax_tag_y: float = 1.0) -> None:
    
    from my_.plot.style import nospines
    from my_.plot.limits import axgrid, numeric_ticks, free_lims

    axgrid(ax)
    nospines(ax)

    plt.suptitle(title, fontsize = fs_title, y = y_title)
    
    ax.set_ylabel(ylabel, fontsize = fs_label)
    ax.set_xlabel(xlabel, fontsize = fs_label)
    
    ax.tick_params(axis='both', which='major', pad=10)

    ax.axhline(0, color = axhv_color, 
                ls = axhv_ls, lw = axhv_lw, 
                alpha = axhv_alpha, dashes = axhv_dashes, zorder = 0)
    
    ax.axvline(0, color = axhv_color, 
                ls = axhv_ls, lw = axhv_lw, 
                alpha = axhv_alpha, dashes = axhv_dashes, zorder = 0)
    
    props = dict(facecolor='white', edgecolor='none', alpha=0.85)

    ax.text(ax_tag_x, ax_tag_y, ax_tag, fontsize = fs_label, transform = ax.transAxes, va = 'bottom', ha = 'center', bbox = props)

    numeric_ticks(ax, fs_ticks = fs_ticks)
    free_lims(ax, xs, ys)


def init_annotation_ax(axs, x : float = 0.05, y : float = 1.05, fs = 12):

    import string
    
    abc                     = string.ascii_lowercase
    
    list_abc                = list(abc)

    for iax, ax in enumerate(axs):

        ax.text(x, y, list_abc[iax] + ')', fontsize = fs,
                transform = ax.transAxes,va = 'bottom', ha = 'center')


def init_pie(ax, fs_label = 10, ax_tag = '', ax_tag_x: float = 0.5, ax_tag_y: float = 0.95):
    
    props = dict(facecolor='white', edgecolor='none', alpha=0.85)

    ax.text(ax_tag_x, ax_tag_y, ax_tag, fontsize = fs_label, transform = ax.transAxes, va = 'bottom', ha = 'center', bbox = props)