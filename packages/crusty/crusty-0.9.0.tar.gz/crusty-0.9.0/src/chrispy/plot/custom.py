import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import colorcet as cc

def map_EU3_point_locations_lc_hclim(lats, lons, landcover, hydroclimate, rotnpole_lat: float, rotnpole_lon: float, semmj_axis: int, semmn_axis: int,
                        lon_extents: list, lat_extents: list, lw_grid: float = 0.5, lw_coast: float = 0.5,  color_grid: str = 'gray',
                        ls_grid: str = '--', xticks: list = [], yticks: list = [], fs_label: float = 10, size_marker: float = 4.0, 
                        marker: str = 'x', color_marker: str = 'firebrick', alpha: float = 0.85, zorder: int = 5, title: str = '',
                        marker_legend_args: dict = {}):

    from my_.figures.single import square_top_right_cax
    from my_.plot.style import style_1
    from my_.plot.maps import EU3_plot_lines, map_point_locations
    from my_.plot.init_ax import EU3_plot_init
    from my_.plot.colors import colorbar
    from my_.plot.legend import marker_legend
    from user_in.options_analyses import selected_landcover, markers
    
    import matplotlib.pyplot as plt
    import matplotlib as mpl

    print('Plot locations map...\n')

    style_1()
    
    rp, pc, xs, ys              = EU3_plot_init(rotnpole_lat, rotnpole_lon, semmj_axis, semmn_axis, lon_extents, lat_extents)

    figure, ax, caxt, caxr      = square_top_right_cax(projection = rp, fy = 5.0)

    ax.set_title(title)
    
    sizes                       = [size_marker] * len(lats)

    cmap                        = plt.get_cmap('BrBG', 6)

    EU3_plot_lines(ax, pc, xs, ys, lw_grid, lw_coast, color_grid, ls_grid, xticks, yticks, fs_label)

    for lc in landcover.unique():
        
        if lc not in selected_landcover: continue

        lat_lc                  = lats.where(landcover == lc)
        lon_lc                  = lons.where(landcover == lc)
        hclim_lc                = hydroclimate.where(landcover == lc)

        colors                  = [cmap(hc/6) for hc in hclim_lc]

        map_point_locations(ax, 
                            lat_lc, 
                            lon_lc, 
                            sizes, 
                            marker = markers[lc], 
                            color = 'None',
                            edgecolor = colors, 
                            projection = pc, 
                            alpha = alpha, 
                            zorder = zorder)

        a = mpl.cm.ScalarMappable(norm = mpl.colors.Normalize(vmin=0, vmax=5), cmap = cmap) 
        ticks = ['Very arid', 'Arid', 'Semi arid', 'Semi humid', 'Humid', 'Very humid']

    colorbar(caxr, a, '', pad = 10, extend = 'neither', fs_label = 12, tick_labels = ticks)
    marker_legend(caxt, markers, **marker_legend_args)

    return figure


def map_EU3_point_locations_hclim(lats, lons, hydroclimate, rotnpole_lat: float, rotnpole_lon: float, semmj_axis: int, semmn_axis: int,
                        lon_extents: list, lat_extents: list, lw_grid: float = 0.5, lw_coast: float = 0.5,  color_grid: str = 'gray',
                        ls_grid: str = '--', xticks: list = [], yticks: list = [], fs_label: float = 10, size_marker: float = 45, 
                        marker: str = 'o', alpha: float = 0.85, zorder: int = 5, title: str = ''):

    from my_.figures.single import square_right_cax
    from my_.plot.style import style_1
    from my_.plot.maps import EU3_plot_lines, map_point_locations
    from my_.plot.init_ax import EU3_plot_init
    from my_.plot.colors import colorbar
    
    import matplotlib.pyplot as plt
    import matplotlib as mpl

    print('Plot locations map...\n')

    style_1()
    
    rp, pc, xs, ys              = EU3_plot_init(rotnpole_lat, rotnpole_lon, semmj_axis, semmn_axis, lon_extents, lat_extents)

    figure, ax, cax             = square_right_cax(projection = rp, fy = 5.0)

    ax.set_title(title)
    
    sizes                       = [size_marker] * len(lats)

    cmap                        = plt.get_cmap('BrBG', 6)

    EU3_plot_lines(ax, pc, xs, ys, lw_grid, lw_coast, color_grid, ls_grid, xticks, yticks, fs_label)
    
    colors                  = [cmap(hc/6) for hc in hydroclimate]

    map_point_locations(ax, lats, lons, sizes, marker = marker, color = colors, projection = pc, alpha = alpha, zorder = zorder)

    a = mpl.cm.ScalarMappable(norm = mpl.colors.Normalize(vmin=0, vmax=5), cmap = cmap) 
    ticks = ['Very arid', 'Arid', 'Semi arid', 'Semi humid', 'Humid', 'Very humid']

    colorbar(cax, a, '', pad = 10, extend = 'neither', fs_label = 12, tick_labels = ticks)

    return figure


def map_EU3_point_locations(lats, lons, rotnpole_lat: float, rotnpole_lon: float, semmj_axis: int, semmn_axis: int,
                        lon_extents: list, lat_extents: list, lw_grid: float = 0.5, lw_coast: float = 0.5,  color_grid: str = 'gray',
                        ls_grid: str = '--', xticks: list = [], yticks: list = [], fs_label: float = 10, size_marker: float = 4.0, 
                        marker: str = 'x', color_marker: str = 'firebrick', alpha: float = 0.7, zorder: int = 5, title: str = ''):

    from my_.figures.single import square
    from my_.plot.style import style_1
    from my_.plot.maps import EU3_plot_lines, map_point_locations
    from my_.plot.init_ax import EU3_plot_init

    print('Plot locations map...\n')

    style_1()
    
    rp, pc, xs, ys              = EU3_plot_init(rotnpole_lat, rotnpole_lon, semmj_axis, semmn_axis, lon_extents, lat_extents)

    figure, ax                  = square(projection = rp)

    ax.set_title(title)
    
    sizes                       = [size_marker] * len(lats)

    EU3_plot_lines(ax, pc, xs, ys, lw_grid, lw_coast, color_grid, ls_grid, xticks, yticks, fs_label)

    map_point_locations(ax, 
                        lats, 
                        lons, 
                        sizes, 
                        marker = marker, 
                        color = 'w',
                        edgecolor = color_marker, 
                        projection = pc, 
                        alpha = alpha, 
                        zorder = zorder)

    

    return figure


def double_EU3_mesh_div_cbar(arrays, lat, lon,
                            rotnpole_lat: float, rotnpole_lon: float, semmj_axis: int, semmn_axis: int,
                            lon_extents: list, lat_extents: list,
                            lw_grid: float = 0.5, lw_coast: float = 0.5,  color_grid: str = 'gray',
                            ls_grid: str = '--', xticks: list = [], yticks: list = [], fs_label: float = 10,
                            cmap: str = 'coolwarm_r', cmap_n: int = 1000, v0: float = None, v1: float = None, 
                            extend: str = 'both', title: str = '', subtitles: list = [], clabel: str = '',
                            fs_title: float = 12, fs_subtitle: float = 10, fs_cbar_label: float = 10):
    

    from my_.plot.style import style_1
    from my_.figures.double import horizontal_cax
    from my_.plot.basic import colormesh
    from my_.plot.maps import EU3_plot_lines
    from my_.plot.init_ax import EU3_plot_init
    from my_.plot.colors import colormap, colorbar

    style_1()

    rp, pc, xs, ys              = EU3_plot_init(rotnpole_lat, rotnpole_lon, semmj_axis, semmn_axis, lon_extents, lat_extents)

    fig, axes, cax              = horizontal_cax(projection = rp)

    label_sides                 = [['bottom'], ['bottom', 'right']]

    cmap_c                      = colormap(cmap, cmap_n)

    fig.suptitle(title, fontsize = fs_title)

    for i_ax, ax in enumerate(axes):

        ax.set_title(subtitles[i_ax], fontsize = fs_subtitle)
        
        EU3_plot_lines(ax, pc, xs, ys, lw_grid, lw_coast, color_grid, ls_grid, xticks, yticks,
                       fs_label, label_sides = label_sides[i_ax])

        artist                  = colormesh(ax, lon, lat, arrays[i_ax], cmap_c, v0, v1, projection = pc)

    colorbar(cax, artist, clabel, pad = 10, extend = extend, fs_label = fs_cbar_label)

    return fig

def single_EU3_mesh_div_cbar(array, lat, lon,
                            rotnpole_lat: float, rotnpole_lon: float, semmj_axis: int, semmn_axis: int,
                            lon_extents: list, lat_extents: list,
                            lw_grid: float = 0.5, lw_coast: float = 0.5,  color_grid: str = 'gray',
                            ls_grid: str = '--', xticks: list = [], yticks: list = [], fs_label: float = 10,
                            cmap: str = 'coolwarm_r', cmap_n: int = 1000, v0: float = None, v1: float = None, 
                            extend: str = 'both', title: str = '', subtitle: str = '', clabel: str = '',
                            fs_title: float = 12, fs_subtitle: float = 10, fs_cbar_label: float = 10):
    

    from my_.plot.style import style_1
    from my_.figures.single import square_right_cax
    from my_.plot.basic import colormesh
    from my_.plot.maps import EU3_plot_lines
    from my_.plot.init_ax import EU3_plot_init
    from my_.plot.colors import colormap, colorbar

    rp, pc, xs, ys              = EU3_plot_init(rotnpole_lat, rotnpole_lon, semmj_axis, semmn_axis, lon_extents, lat_extents)

    fig, ax, cax                = square_right_cax(projection = rp)

    label_sides                 = ['bottom', 'right']

    cmap_c                      = colormap(cmap, cmap_n)

    fig.suptitle(title, fontsize = fs_title)


    ax.set_title(subtitle, fontsize = fs_subtitle)
        
    EU3_plot_lines(ax, pc, xs, ys, lw_grid, lw_coast, color_grid, ls_grid, xticks, yticks,
                    fs_label, label_sides = label_sides)

    artist                  = colormesh(ax, lon, lat, array, cmap_c, v0, v1, projection = pc)

    colorbar(cax, artist, clabel, pad = 10, extend = extend, fs_label = fs_cbar_label)

    return fig

def pie_location_lc_clim_map(df_static: pd.DataFrame,
                            lats: np.ndarray | list | tuple | pd.Series,
                            lons: np.ndarray | list | tuple | pd.Series,
                            landcover: np.ndarray | list | tuple | pd.Series,
                            hydroclimate: np.ndarray | list | tuple | pd.Series,
                            basemap_args: dict, 
                            baselines_args: dict, 
                            map_args: dict,
                            markers: dict,
                            marker_legend_args: dict,
                            selected_landcover: list[str], 
                            colors: dict,
                            color_legend_args:dict) -> plt.figure:
    
    from my_.figures.one_by_three import horizontal_right_map_two_cax
    from my_.series.aggregate import concat
    from my_.plot.basic import pie
    from my_.plot.init_ax import init_pie, EU3_plot_init
    from my_.plot.legend import color_legend, marker_legend
    from my_.plot.colors import colorbar
    from my_.resources.sources import query_static
    from my_.plot.maps import EU3_plot_lines, map_point_locations

    rp, pc, xs, ys              = EU3_plot_init(**basemap_args)

    fig, axs, axl1, axl2, axc   = horizontal_right_map_two_cax(projection = rp)

    landcover                   = df_static['landcover'].where(df_static['landcover'].isin(selected_landcover))

    pct_crop                    = df_static['PCT_CROP'] / 100

    pct_nat                     = df_static['PCT_NATVEG'] / 100

    pft_cols                    = [col for col in df_static.columns if 'PCT_NAT_PFT_' in col]

    cft_cols                    = [col for col in df_static.columns if 'PCT_CFT_' in col]

    pft_rel                     = df_static[pft_cols].multiply(pct_nat, axis = 0)

    cft_rel                     = df_static[cft_cols].multiply(pct_crop, axis = 0)

    df_tot                      = concat([pft_rel, cft_rel], sort = False)

    ind_landcover               = query_static('CLM5-EU3-surf', 'sel_agg_layer_PFT')

    shares_surf                 = [df_tot.iloc[:, ind_landcover[lc]].sum(axis = 1).mean() for lc in selected_landcover]

    shares_surf_o               = shares_surf + [100 - sum(shares_surf)] 

    shares_lc                   = landcover.value_counts(normalize = True)

    cmapc                       = plt.get_cmap('Set2').colors

    colors                      = {k: v for k,v in colors.items()}
    colorsc                     = [cmapc[colors[lc]] for lc in list(selected_landcover)]

    colors['other']             = 7

    colorsc_o                   = colorsc + [cmapc[7]]

    color_legend(axl1, colors, cmapc, **color_legend_args)

    init_pie(axs[0], ax_tag = 'ICOS network')
    init_pie(axs[1], ax_tag = 'CLM5 surface')

    pie(axs[0], shares_lc, colorsc, autopct='%1.1f%%')
    pie(axs[1], shares_surf_o, colorsc_o, autopct='%1.1f%%')

    sizes                       = [map_args['size_marker']] * len(lats)

    cmap                        = plt.get_cmap('BrBG', 6)

    EU3_plot_lines(axs[-1], pc, xs, ys, **baselines_args)
    
    for lc in landcover.unique():
        
        if lc not in selected_landcover: continue

        lat_lc                  = lats.where(landcover == lc)
        lon_lc                  = lons.where(landcover == lc)
        hclim_lc                = hydroclimate.where(landcover == lc)

        colors                  = [cmap(hc/6) for hc in hclim_lc]

        map_point_locations(axs[2], 
                            lat_lc, 
                            lon_lc, 
                            sizes, 
                            marker = markers[lc], 
                            color = 'w', #colors, 
                            edgecolor = colors,
                            projection = pc, 
                            alpha = map_args['alpha'], 
                            zorder = map_args['zorder'])

        a = mpl.cm.ScalarMappable(norm = mpl.colors.Normalize(vmin=0, vmax=5), cmap = cmap) 
        ticks = ['Very\narid', 'Arid', 'Semi\narid', 'Semi\nhumid', 'Humid', 'Very\nhumid']

    colorbar(axc, a, '', pad = 10, extend = 'neither', fs_label = 8, tick_labels = ticks, orientation = 'horizontal')
    marker_legend(axl2, markers, **marker_legend_args)

    return fig



def single_EU3_mesh_cat_cbar(array, lat, lon,
                            rotnpole_lat: float, rotnpole_lon: float, semmj_axis: int, semmn_axis: int,
                            lon_extents: list, lat_extents: list,
                            lw_grid: float = 0.5, lw_coast: float = 0.5,  color_grid: str = 'gray',
                            ls_grid: str = '--', xticks: list = [], yticks: list = [], fs_label: float = 10,
                            cmap: str = 'cet_glasbey_hv', extend: str = 'neither', title: str = '', clabel: str = '', 
                            fs_title: float = 12, fs_cbar_label: float = 10, cbar_tick_labels: list = []): 

    import numpy as np
    from my_.plot.style import style_1
    from my_.plot.maps import EU3_plot_lines
    from my_.plot.init_ax import EU3_plot_init
    from my_.figures.single import square_right_cax
    from my_.plot.colors import colormap, colorbar
    from my_.plot.basic import colormesh

    import cartopy.feature as cfeature

    label_sides                 =  ['bottom', 'right']

    style_1()

    rp, pc, xs, ys              = EU3_plot_init(rotnpole_lat, rotnpole_lon, semmj_axis, semmn_axis, lon_extents, lat_extents)

    figure, ax, cax             = square_right_cax(projection = rp)

    ax.add_feature(cfeature.OCEAN, edgecolor='face', facecolor='white', zorder = 2)

    cmap_n                      = np.max(array) + 1 # "maybe better": length of unique values. But not sure

    cmap_c                      = colormap(cmap, cmap_n)

    ax.set_title(title, fontsize = fs_title)

    EU3_plot_lines(ax, pc, xs, ys, lw_grid, lw_coast, color_grid, ls_grid, xticks, yticks,
                       fs_label, label_sides = label_sides)

    artist                      = colormesh(ax, lon, lat, array, cmap_c, projection = pc)

    colorbar(cax, artist, clabel, pad = 10, extend = extend, 
            fs_label = fs_cbar_label, tick_labels = cbar_tick_labels)

    return figure


def single_EU3_mesh_cont_cbar(array, lat, lon,
                            rotnpole_lat: float, rotnpole_lon: float, semmj_axis: int, semmn_axis: int,
                            lon_extents: list, lat_extents: list,
                            lw_grid: float = 0.5, lw_coast: float = 0.5,  color_grid: str = 'gray',
                            ls_grid: str = '--', xticks: list = [], yticks: list = [], fs_label: float = 10,
                            cmap: str = 'Greens', extend: str = 'neither', title: str = '', clabel: str = '', 
                            fs_title: float = 12, fs_cbar_label: float = 10, cbar_tick_labels: list = []): 

    import numpy as np
    from my_.plot.style import style_1
    from my_.plot.maps import EU3_plot_lines
    from my_.plot.init_ax import EU3_plot_init
    from my_.figures.single import square_right_cax
    from my_.plot.colors import colormap, colorbar
    from my_.plot.basic import colormesh

    import cartopy.feature as cfeature

    label_sides                 =  ['bottom', 'right']

    style_1()

    rp, pc, xs, ys              = EU3_plot_init(rotnpole_lat, rotnpole_lon, semmj_axis, semmn_axis, lon_extents, lat_extents)

    figure, ax, cax             = square_right_cax(projection = rp)

    ax.add_feature(cfeature.OCEAN, edgecolor='face', facecolor='white', zorder = 2)

    cmap_n                      = np.max(array) + 1 # "maybe better": length of unique values. But not sure

    cmap_c                      = colormap(cmap, cmap_n)

    ax.set_title(title, fontsize = fs_title)

    EU3_plot_lines(ax, pc, xs, ys, lw_grid, lw_coast, color_grid, ls_grid, xticks, yticks,
                       fs_label, label_sides = label_sides)

    artist                      = colormesh(ax, lon, lat, array, cmap_c, projection = pc)

    colorbar(cax, artist, clabel, pad = 10, extend = extend, 
            fs_label = fs_cbar_label, tick_labels = cbar_tick_labels)

    return figure


def taylor_landcover(df: pd.DataFrame,
                     obs: str,
                     variables: list[str],
                     colors: dict,
                     markers: dict,
                     landcover: list[str],
                     std_range: tuple = (0, 1.5),
                     marker_legend_args: dict = {},
                     color_legend_args: dict = {}):
    
    from my_.series.group import select_multi_index, nona_level
    from my_.plot.legend import marker_legend, color_legend
    from my_.series.aggregate import single_level_wise, groupwise
    from my_.math.stats import rmse, r, pbias
    from matplotlib.projections import PolarAxes
    from mpl_toolkits.axisartist import floating_axes, grid_finder
    from my_.plot.style import style_1
    from matplotlib.gridspec import GridSpec
    from my_.plot.limits import axgrid
    from my_.resources.sources import query_variables
    from sklearn.preprocessing import MinMaxScaler

    scaler = MinMaxScaler(feature_range = (0, 1))

    print('Plot Taylor diagram...\n')

    cmapc = cc.glasbey_hv[:] + [[0.0, 0.0, 0.0]]

    sources = df.columns.unique(level = 'Source')

    labels_sources = {s: query_variables(s, 'name_label') 
                      for s in sources}

    colorscc = {labels_sources[k]: v 
              for k, v in colors.items() if k in sources}

    stations_uq = df.columns.unique(level = 'Station')
    
    stations_count = df.columns\
                       .get_level_values('Station')\
                       .value_counts()

    
    for s in stations_uq:
        
        if stations_count[s] == 1:

            df = df.drop(s, axis = 1, level = 'Station')
        
    df_nona = nona_level(df, 
                         ['Variable', 'Station'],
                         axis = 1,
                         how = 'any')

    df_n = select_multi_index(df_nona, 
                              ['Variable', 'Landcover'],
                              keys = [variables, landcover],
                              axis = 1)
    
    for var in variables: 

        var_units = query_variables(sources[0], 
                                'var_units')[var]

        var_df = select_multi_index(df_n,
                                    levels = ['Variable'],
                                    keys = [var],
                                    axis = 1)
        
        std_df = var_df.T.groupby(level = ['Landcover', 
                                            'Source'])\
                         .apply(groupwise,
                                [pd.DataFrame.to_numpy,
                                 np.nanstd])

        r_df = var_df.T.groupby(level = ['Landcover'])\
                       .apply(single_level_wise,
                              level = 'Source',
                              key = obs,
                              ffunc = r,
                              axis = 0)

        pbias_df = var_df.T.groupby(level = ['Landcover'])\
                       .apply(single_level_wise,
                              level = 'Source',
                              key = obs,
                              ffunc = pbias,
                              axis = 0)
        
        rmse_df = var_df.T.groupby(level = ['Landcover'])\
                          .apply(single_level_wise,
                                 level = 'Source',
                                 key = obs,
                                 ffunc = rmse,
                                 axis = 0)

        ref_std = select_multi_index(std_df,
                                     levels = ['Source'],
                                     keys = [obs],
                                     axis  = 0)

        tr = PolarAxes.PolarTransform()

        pbias_ms_scale = scaler.fit_transform(np.abs(pbias_df))

        pbias_ms = pbias_df.copy()

        pbias_ms.iloc[:, :] = 6 + np.abs(pbias_ms_scale) * 10
    
        if (r_df < 0).values.any():
            
            extend = True
            tmax = np.pi
            rlocs = [-1, -0.99, -0.95, -0.9, -0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 0.9 ,0.95, 0.99, 1]

        else:
            
            extend = False
            tmax = np.pi/2
            rlocs = [0, 0.2, 0.4, 0.6, 0.8, 0.9 ,0.95, 0.99, 1]

        tlocs = np.arccos(rlocs)

        gl1 = grid_finder.FixedLocator(tlocs)
        tf1 = grid_finder.DictFormatter(dict(zip(tlocs, 
                                        map(str, rlocs))))
    
        std_min = std_range[0] * ref_std.min().item()
        std_max = std_range[1] * ref_std.max().item()

        ghelper = floating_axes.GridHelperCurveLinear(
                                tr,
                                extremes = (0, 
                                          tmax, 
                                          std_min, 
                                          std_max),
                                grid_locator1 = gl1, 
                                tick_formatter1 = tf1)

        markers_l = {10: 'o', 20: 'o', 30: 'o', 40: 'o'}

        markers_s = {k: 6 + scaler.transform([[float(k)]]) * 10 
                     for k in markers_l.keys()}
    
        style_1()
     
        nrows = 3
        ncols = 2
        w1, w2 = 1, 14

        fig = plt.figure(figsize=(6.7, 8), dpi = 300)

        gs = GridSpec(figure = fig, 
                      ncols = ncols, nrows = nrows, 
                      height_ratios = [w1, w2, w2])
        
        
        axl_l = fig.add_subplot(gs[0, 0], frameon = False)
        axl_r = fig.add_subplot(gs[0, 1], frameon = False)

        marker_legend(axl_l, 
                      markers_l, 
                      marker_color = 'gray',
                      marker_sizes = markers_s,
                      title = 'absolute PBIAS [%]',
                      anchor = (0.5, 0.5), 
                      markerfirst = True, 
                      fs_labels = 10,
                      labelcolor = 'k',
                      handletextpad = 0.2,
                      columnspacing = 0.9, 
                      loc = 'center',
                      handlelength = 1.2)
    
        color_legend(axl_r, 
                     colorscc,
                     cmapc, 
                     ncols = 2,
                     **color_legend_args)
        
        i_ax = [[1, 0], [1, 1], [2, 0], [2, 1]]

        order = ['ENF', 'DBF', 'GRA', 'CRO']

        lcs_df = std_df.index.unique(level = 'Landcover')

        lcs = [lc for lc in order if lc in lcs_df]
        
        for ilc, lc in enumerate(lcs):
            
            ref_std_lc = ref_std.loc[(lc, obs)].item()
            r_lc = r_df.loc[lc]
            std_lc = std_df.loc[lc]
            pbias_lc = pbias_df.loc[lc]
            ms_lc = pbias_ms.loc[lc]
            marker = markers[lc]

            ax = fig.add_subplot(gs[*i_ax[ilc]], 
                                 axes_class = floating_axes.FloatingAxes,
                                 grid_helper = ghelper,
                                 frameon = False)
        
            axgrid(ax)
                                     
            # Adjust axes
            ax.axis["top"].set_axis_direction("bottom")   # "Angle axis"
            ax.axis["top"].toggle(ticklabels = True, label=True)
            ax.axis["top"].major_ticklabels.set_axis_direction("top")
            ax.axis["top"].label.set_axis_direction("top")
            ax.axis["top"].label.set_text("Correlation [-]")

            ax.axis["left"].set_axis_direction("bottom")  # "X axis"
            ax.axis["left"].label.set_text(f"Standard deviation [{var_units}]")

            ax.axis["right"].set_axis_direction("top")    # "Y-axis"
            ax.axis["right"].toggle(ticklabels = True)
            ax.axis["right"].major_ticklabels.set_axis_direction(
                "bottom" if extend else "left")

            if std_min:
                ax.axis["bottom"].toggle(ticklabels=False, label=False)
            else:
                ax.axis["bottom"].set_visible(False)            

            ax = ax.get_aux_axes(tr)  
        
            #l_, = ax.plot([0], ref_std_lc, marker = marker,
            #             color = 'k', ls = '', ms = 10, label = '',
            #             clip_on = False, alpha = 0.7)
            t_ = np.linspace(0, tmax)
            r_ = np.zeros_like(t_) + ref_std_lc
            ax.plot(t_, r_, 'k--', alpha = 0.7, label = '_')

            colorsc = {k: cmapc[d] 
                       for k, d in colors.items()}
            
            rs, ts = np.meshgrid(np.linspace(std_min, std_max),
                             np.linspace(0, tmax))
            
            rms = np.sqrt(ref_std_lc**2 + 
                          rs ** 2 - 2 * ref_std_lc *
                          rs * np.cos(ts))
            
            contours = ax.contour(ts, 
                                  rs, 
                                  rms, 
                                  4, 
                                  colors = 'k', 
                                  linestyles = '--',
                                  linewidths = 0.6, 
                                  alpha = 0.5)
            
            ax.clabel(contours, 
                      inline = True, 
                      fmt = f'%.1f {var_units}',
                      fontsize = 8)

            props = dict(facecolor = 'white', 
                         edgecolor = 'none', 
                         alpha = 0.85)

            ax.text(0.5, 
                    1.0, 
                    lc, 
                    fontsize = 12, 
                    transform = ax.transAxes, 
                    va = 'bottom', 
                    ha = 'center', 
                    bbox = props)
            
            for src in std_df.index.get_level_values('Source'):

                r_src_lc = r_lc.loc[src].item()
                std_src_lc = std_lc.loc[src].item()
                pbias_src_lc = pbias_lc.loc[src].item()
                ms_src_lc = ms_lc.loc[src].item()

                

                if src == obs:
                    ms_src_lc = 5
                
                color = colorsc[src]
                
                ax.plot(np.arccos(r_src_lc), 
                        std_src_lc, 
                        marker = marker, 
                        color = color, 
                        markerfacecolor = "None",
                        markeredgewidth = 2.4,
                        ls = '', 
                        ms = ms_src_lc, 
                        label = '',
                        alpha = 0.8,
                        clip_on = False)

    return fig

def xy_landcover_moments(df: pd.DataFrame, 
                         variable: str, 
                         sources_insitu: list = [], 
                         sources_grids: list = [], 
                         sel_landcover: list = [], 
                         markers: dict = {}, 
                         colors: dict = {},
                         xy_init_args: dict = {}, 
                         xy_args: dict = {}, 
                         marker_legend_args: dict = {}, 
                         color_legend_args: dict = {},
                         moments: list = ['mean', 
                                          'variance', 
                                          'skewness', 
                                          'kurtosis']) -> plt.Figure:

    from my_.figures.two_by_two import square_two_top_cax
    from my_.series.group import select_multi_index, nona_level
    from my_.plot.init_ax import init_xy
    from my_.plot.basic import scatter, error
    from my_.plot.legend import marker_legend, color_legend
    #from my_.series.convert import tile_df_to_list

    from my_.resources.sources import query_variables

    from my_.math import stats

    import colorcet as cc
    import numpy as np

    print('Plot land cover aggregated xy plots...\n')

    stations_uq = df.columns.unique(level = 'Station')
    
    stations_count = df.columns\
                       .get_level_values('Station')\
                       .value_counts()
    
    
    for s in stations_uq:
        
        if stations_count[s] <= len(sources_grids):

            df = df.drop(s, axis = 1, level = 'Station')
            
    df_nona = nona_level(df, ['Variable', 'Station'], 
                         how = 'any', 
                         axis = 1)
    

    df_i = select_multi_index(df_nona, 
                              levels = ['Source', 
                                        'Variable', 
                                        'Landcover'],
                              keys = [sources_insitu, 
                                      [variable], 
                                      sel_landcover])
    

    df_d = select_multi_index(df_nona, 
                              levels = ['Source', 
                                        'Variable', 
                                        'Landcover'],
                              keys = [sources_grids, 
                                      [variable], 
                                      sel_landcover])
    
    df_i_lc = df_i.groupby(axis = 1, 
                           level = ['Source', 'Landcover'])
    
    df_d_lc = df_d.groupby(axis = 1, 
                           level = ['Source', 'Landcover'])

    i_sources = df_i_lc.obj.columns.unique(level = 'Source')

    d_sources = df_d_lc.obj.columns.unique(level = 'Source')

    cmapc = cc.glasbey_hv[:] + [[0.0, 0.0, 0.0]]

    var_units = query_variables(i_sources[0], 
                                'var_units')[variable]

    mom_units = [f'[{var_units}]', 
                 f'[{var_units}]²', '[-]', '[-]']

    if len(i_sources) > 1: raise NotImplementedError

    fig, axs, axs_l = square_two_top_cax(fy = 8)

    labels_sources = {s: query_variables(s, 'name_label') 
                      for s in d_sources}

    colors = {labels_sources[k]: v 
              for k,v in colors.items() if k in d_sources}
    


    marker_legend(axs_l[0], 
                  markers, 
                  **marker_legend_args)
    
    color_legend(axs_l[1], 
                 colors,
                 cmapc, 
                 ncols = (len(d_sources) // 2) + 1, 
                 **color_legend_args)

    for iax, ax in enumerate(axs):

        agg_moment = moments[iax]

        agg_method = getattr(stats, agg_moment)
        err_method = getattr(stats, f'std_error_{agg_moment}')
        
        df_i_lc_agg = df_i_lc.apply(agg_method)
        df_d_lc_agg = df_d_lc.apply(agg_method)

        df_i_lc_agg_err = df_i_lc.apply(err_method)
        df_d_lc_agg_err = df_d_lc.apply(err_method)

        title_fig = ''

        xlabel = f'Observation {mom_units[iax]}'
        ylabel = f'Model {mom_units[iax]}'

        init_xy(ax = ax, 
                xs = df_i_lc_agg, 
                ys = df_d_lc_agg,
                xerr = df_i_lc_agg_err,
                yerr = df_d_lc_agg_err,
                title = title_fig, 
                xlabel = xlabel, 
                ylabel = ylabel, 
                ax_tag = agg_moment,
                **xy_init_args)

        for lc in df_i.columns.unique(level = 'Landcover'):

            ys = select_multi_index(df_d_lc_agg, 
                                    'Landcover', 
                                    lc, 
                                    axis = 0)
            
            colorsc = [cmapc[colors[labels_sources[d]]] 
                    for d in ys\
                        .index\
                        .get_level_values('Source')]

            xs = select_multi_index(df_i_lc_agg, 
                                    'Landcover', 
                                    lc, 
                                    axis = 0).values.flatten()

            x_err = select_multi_index(df_i_lc_agg_err, 
                                       'Landcover', 
                                       lc, 
                                       axis = 0).values.flatten()

            y_err = select_multi_index(df_d_lc_agg_err, 
                                       'Landcover', 
                                       lc, 
                                       axis = 0).values.flatten()
            
            xs_tile = np.tile(xs, len(d_sources))
            
            x_err_tile = np.tile(x_err, len(d_sources))

            if len(ys) == 0: continue

            scatter(ax, 
                    xs_tile, 
                    ys.values.flatten(), markers[lc], 
                    colors_marker = colorsc, 
                    **xy_args)
            
            print(x_err_tile, y_err)

            error(ax, 
                  xs_tile, 
                  ys.values.flatten(), 
                  x_err = x_err_tile, 
                  y_err = y_err, 
                  ecolors = colorsc, 
                  elinewidth = 2)
    
    return fig


def bar_rmse_landcover(df, variable, sources_insitu, sources_grids, sel_landcover,
                       colors: dict = {}, bar_init_args = {}, bar_args = {},
                       color_legend_args = {}):

    from my_.series.group import select_multi_index, nona_level
    from my_.series.aggregate import column_wise
    from my_.math.stats import rmse, mean, std_deviation
    from my_.resources.sources import query_variables

    from my_.figures.two_by_two import square_top_cax
    from my_.plot.basic import bar, error
    from my_.plot.init_ax import init_bar
    from my_.plot.legend import color_legend

    import numpy as np
    import colorcet as cc

    print('Plot land cover aggregated rmse bar plots...\n')

    df_nona                     = nona_level(df, ['Variable', 'Station'],
                                             axis = 1,
                                             how = 'any')

    df_s                        = select_multi_index(df_nona, ['Variable', 'Landcover'],
                                                      keys = [variable, sel_landcover])
    
    df_s                        = df_s.reindex(labels = sources_insitu + sources_grids, axis = 1, level = 'Source')
    
    df_lc_rmse                  = df_s.groupby(axis = 1, level = ['Source', 'Landcover']).apply(column_wise, ffunc = rmse)

    df_lc_rmse_mean             = df_lc_rmse.groupby(axis = 1, level = ['Source', 'Landcover']).apply(mean, axis = (0, 1))
    df_lc_rmse_std             = df_lc_rmse.groupby(axis = 1, level = ['Source', 'Landcover']).apply(std_deviation, axis = (0, 1))

    sources                     = df_lc_rmse_mean.index.unique(level = 'Source')

    var_units                   = query_variables(sources[0], 'var_units')[variable]
    labels_sources              = {s: query_variables(s, 'name_label') for s in sources}
    
    fig, axs, axs_l             = square_top_cax()

    cmapc = cc.glasbey_hv[:] + [[0.0, 0.0, 0.0]]

    colors                      = {labels_sources[k]: v for k,v in colors.items() if k in sources}


    xs                          = np.arange(len(sources))

    ys                          = df_lc_rmse_mean

    ys = ys.reindex(sources_insitu + sources_grids, axis = 1, level = 'Source')

    color_legend(axs_l, colors, cmapc, **color_legend_args)

    y_err                       = df_lc_rmse_std

    y_err = y_err.reindex(sources_insitu + sources_grids, axis = 1, level = 'Source')
    
    for iax, ax in enumerate(axs):

        lc                      = sel_landcover[iax]

        ys_lc                   = select_multi_index(ys, levels = ['Landcover'], keys = [lc], axis = 0)

        colorsc = [cmapc[colors[labels_sources[d]]] 
                for d in ys_lc\
                    .index\
                    .get_level_values('Source')]

        y_err_lc                = select_multi_index(y_err, levels = ['Landcover'], keys = [lc], axis = 0)

        ecolors                 = ['gray'] * len(ys_lc)

        init_bar(ax, xs, ys + y_err, ax_tag = lc, ylabel = f'RMSD [{var_units}]', **bar_init_args)

        bar(ax, xs, ys_lc.values.flatten(), color = colorsc, **bar_args)
        
        error(ax, xs, ys_lc.values, y_err = y_err_lc.values, ecolors = ecolors, 
              capsize = 4, alpha = 0.8, zorder = 6)
    
    return fig


def doy_doy_landcover(name: str, 
                      df: pd.DataFrame,
                      variable: str,
                      sources_insitu: list[str], 
                      sources_grids: list[str], 
                      sel_landcover: list[str],
                      colors: dict = {}, 
                      doy_init_args: dict = {}, 
                      doy_args: dict = {}, 
                      color_legend_args: dict = {}) -> plt.Figure:

    from my_.series.group import select_multi_index, nona_level
    from my_.series.aggregate import column_wise
    from my_.math.stats import pbias, rmse
    from my_.resources.sources import query_variables
    from my_.figures.four_by_two import vertical_top_cax
    from my_.figures.two_by_two import square_two_top_cax
    from my_.plot.init_ax import init_ts
    from my_.plot.legend import color_legend
    from my_.plot.basic import plot
    from my_.files.handy import save_df 
    from scipy.signal import find_peaks
    from scipy.ndimage import gaussian_filter1d

    import colorcet as cc

    print('Plot land cover aggregated DOY and distribution plots...\n')

    stations_uq = df.columns.unique(level = 'Station')
    
    stations_count = df.columns\
                       .get_level_values('Station')\
                       .value_counts()
    
    for s in stations_uq:
        
        if stations_count[s] == 1:

            df = df.drop(s, axis = 1, level = 'Station')
    
    df_nona = nona_level(df, 
                         ['Variable', 'Station'],
                         axis = 1,
                         how = 'any')

    df_nona = df_nona.dropna(axis = 1, 
                             how = 'all')


    df_s = select_multi_index(df_nona, 
                              ['Variable', 'Landcover'],
                              keys = [variable, sel_landcover])
 
    df_s = df_s.reindex(labels = sources_insitu + sources_grids, 
                        axis = 1, 
                        level = 'Source')

    sources = df_s.columns.unique(level = 'Source')

    df_doy = df_s.groupby(df_s.index.dayofyear).mean()

    df_doy_lc = df_doy.groupby(axis = 1, level = ['Source', 
                                          'Landcover'])

    df_doy_lc_mean = df_doy_lc.mean()

    modes = df_doy_lc_mean.apply(find_peaks, distance = 46)

    df_doy_lc_mean_d2 = df_doy_lc_mean.apply(gaussian_filter1d, sigma = 100).apply(np.gradient).apply(np.gradient)

    df_doy_lc_mean_infl = df_doy_lc_mean_d2.apply(np.sign).apply(np.diff).apply(np.nonzero)

    df_doy_lc_mean_rmse = column_wise(df_doy_lc_mean, 
                                      ffunc = rmse)
    
    df_doy_lc_mean_pbias = column_wise(df_doy_lc_mean, 
                                       ffunc = pbias)

    save_df(df_doy_lc_mean, 
            f'out/{name}/csv/doy_lc_mean_{variable}.csv',
            format = 'csv')

    save_df(df_doy_lc_mean_rmse, 
            f'out/{name}/csv/doy_lc_mean_rmse_{variable}.csv', 
            format = 'csv')
    
    save_df(df_doy_lc_mean_pbias, 
            f'out/{name}/csv/doy_lc_mean_pbias_{variable}.csv', 
            format = 'csv')

    df_doy_lc_std = df_doy_lc.std()

    var_units = query_variables(sources[0], 
                                'var_units')[variable]
    
    labels_sources = {s: query_variables(s, 'name_label') 
                      for s in sources}

    cmapc = cc.glasbey_hv[:] + [[0.0, 0.0, 0.0]]
    
    colors = {labels_sources[k]: v 
              for k, v in colors.items() if k in sources}

    fig, axs, axs_l = vertical_top_cax(fy = 8)

    color_legend(axs_l, colors, cmapc, **color_legend_args)


    for ilc, lc in enumerate(sel_landcover):

        xs_doy = df_doy_lc_mean.index

        ys_doy = select_multi_index(df_doy_lc_mean, 
                                    levels = ['Landcover'], 
                                    keys = [lc])
        
        if len(ys_doy.columns) < 2: continue
        
        ys_doy = ys_doy.reindex(labels = sources_insitu + sources_grids, 
                        axis = 1, 
                        level = 'Source')
        
        colorsc = [cmapc[colors[labels_sources[d]]] 
                    for d in ys_doy\
                        .columns\
                        .get_level_values('Source')]
        
        err_doy = select_multi_index(df_doy_lc_std, 
                                     levels = ['Landcover'], 
                                     keys = [lc])
        
        err_doy = err_doy.reindex(labels = sources_insitu + sources_grids, 
                        axis = 1, 
                        level = 'Source')

        var_label = f'{variable} [{var_units}]'

        init_ts(ax = axs[ilc, 0], 
                xs = np.arange(1, 365, 8), 
                ys = df_doy_lc_mean, 
                ylabel = f'mean {var_label}', 
                ax_tag = lc, 
                **doy_init_args)
        
        init_ts(ax = axs[ilc, 1], 
                xs = np.arange(1, 365, 8), 
                ys = df_doy_lc_std, 
                ylabel = f'std {var_label}', 
                ax_tag = lc, 
                **doy_init_args)

        plot(ax = axs[ilc, 0], 
             xs = xs_doy, 
             ys = ys_doy,
             lw = [3] + [1.5] * len(sources_grids), 
             colors = colorsc, 
             **doy_args)
        
        plot(ax = axs[ilc, 1], 
             xs = xs_doy, 
             ys = err_doy, 
             lw = [3] + [1.5] * len(sources_grids),
             colors = colorsc, 
             **doy_args)

    return fig


def knee(xy: pd.Series, 
        interp_method = 'interp1d',
        degree: int = 7,
        curve: str = 'convex',
        direction: str = 'increasing'):
    
    from kneed import KneeLocator

    kneeds = KneeLocator(x = xy.index,
                         y = xy.values,
                         polynomial_degree = degree,
                         interp_method = interp_method,
                         curve = curve,
                         direction = direction)
    
    return kneeds.knee



def doy_lollipop(df: pd.DataFrame,
                 variable: str,
                 sel_landcover: list[str],
                 sources_insitu: list[str],
                 sources_grids: list[str],
                 color_legend_args: dict,
                 colors: dict):

    from my_.series.group import select_multi_index, nona_level
    from my_.resources.sources import query_variables
    from my_.figures.two_by_two import square_top_cax
    from my_.plot.init_ax import init_lol
    from my_.plot.legend import color_legend
    from my_.plot.basic import scatter, hlines, vlines, error
    from my_.files.handy import save_df 
    from my_.math.stats import peaks, inflictions
    from scipy.ndimage import gaussian_filter1d
    from mpl_toolkits.axes_grid1 import make_axes_locatable

    


    import colorcet as cc

    import string

        
    abc                     = string.ascii_lowercase
    
    list_abc                = list(abc)

    print('Plot land cover aggregated DOY lollipop...\n')

    stations_uq = df.columns.unique(level = 'Station')
    
    stations_count = df.columns\
                       .get_level_values('Station')\
                       .value_counts()
    
    for s in stations_uq:
        
        if stations_count[s] == 1:

            df = df.drop(s, axis = 1, level = 'Station')
    
    df_nona = nona_level(df, 
                         ['Variable', 'Station'],
                         axis = 1,
                         how = 'any')

    df_nona = df_nona.dropna(axis = 1, 
                             how = 'all')

    df_s = select_multi_index(df_nona, 
                              ['Variable', 'Landcover'],
                              keys = [variable, sel_landcover])
 
    df_s = df_s.reindex(labels = sources_insitu + sources_grids, 
                        axis = 1, 
                        level = 'Source')

    sources = df_s.columns.unique(level = 'Source')

    df_doy = df_s.groupby(df_s.index.dayofyear).mean()

    df_doy_modes = df_doy.apply(peaks, distance = 46)

    df_doy_modes_lc_mean = df_doy_modes.groupby(level = ['Source', 
                                                'Landcover']).mean()
    
    df_doy_modes_lc_mean = pd.DataFrame(df_doy_modes_lc_mean).T
    
    df_doy_modes_lc_std = df_doy_modes.groupby(level = ['Source', 
                                               'Landcover']).std()
    
    df_doy_modes_lc_std = pd.DataFrame(df_doy_modes_lc_std).T

    df_doy_infl = df_doy.apply(inflictions)

    df_doy_infl_lc_mean = df_doy_infl.groupby(axis = 1,
                                              level = ['Source', 
                                              'Landcover']).mean()
    
    df_doy_infl_lc_std = df_doy_infl.groupby(axis = 1,
                                             level = ['Source', 
                                             'Landcover']).std()
    
    save_df(df_doy_infl_lc_mean, f'infl_mean_{variable}.csv')
    save_df(df_doy_infl_lc_std, f'infl_std_{variable}.csv')
    save_df(df_doy_modes_lc_mean, f'modes_mean_{variable}.csv')
    save_df(df_doy_modes_lc_std, f'modes_std_{variable}.csv')

    labels_sources = {s: query_variables(s, 'name_label') 
                      for s in sources}

    cmapc = cc.glasbey_hv[:] + [[0.0, 0.0, 0.0]]
    
    colors = {labels_sources[k]: v 
              for k, v in colors.items() if k in sources_grids}

    fig, axs, axs_l = square_top_cax(fx = 9.4,
                                     annotation = False)

    color_legend(axs_l, 
                 colors, 
                 cmapc, 
                 **color_legend_args)


    for ilc, lc in enumerate(sel_landcover):

        xs_mode = select_multi_index(df_doy_modes_lc_mean, 
                                    levels = ['Landcover'], 
                                    keys = [lc])
        
        err_mode = select_multi_index(df_doy_modes_lc_std, 
                                    levels = ['Landcover'], 
                                    keys = [lc])
        
        xs_infl = select_multi_index(df_doy_infl_lc_mean, 
                                    levels = ['Landcover'], 
                                    keys = [lc])
        
        err_infl = select_multi_index(df_doy_infl_lc_std, 
                                      levels = ['Landcover'], 
                                      keys = [lc])
        
        ys_source = np.arange(len(sources_grids))

        ys_obs = np.arange(len(sources_grids))
        
        if len(xs_mode.columns) < 2: continue
        
        xmin = select_multi_index(xs_mode,
                                  levels = ['Source',
                                            'Landcover'],
                                  keys = [sources_insitu[0],
                                          lc]).T * 8
        
        xmin_err = select_multi_index(err_mode,
                                  levels = ['Source',
                                            'Landcover'],
                                  keys = [sources_insitu[0],
                                          lc]).T * 8

        xmax = select_multi_index(xs_mode,
                                  levels = ['Source',
                                            'Landcover'],
                                  keys = [sources_grids,
                                          lc]).T * 8

        xmax_err = select_multi_index(err_mode,
                                  levels = ['Source',
                                            'Landcover'],
                                  keys = [sources_grids,
                                          lc]).T * 8
        
        xinfl = select_multi_index(xs_infl,
                                  levels = ['Source',
                                            'Landcover'],
                                  keys = [sources_grids,
                                          lc]).T * 8
        
        err_xinfl = select_multi_index(err_infl,
                                  levels = ['Source',
                                            'Landcover'],
                                  keys = [sources_grids,
                                          lc]).T * 8
        
        xinfl_o = select_multi_index(xs_infl,
                                  levels = ['Source',
                                            'Landcover'],
                                  keys = [sources_insitu[0],
                                          lc]).T * 8
        
        err_xinfl_o = select_multi_index(err_infl,
                                  levels = ['Source',
                                            'Landcover'],
                                  keys = [sources_insitu[0],
                                          lc]).T * 8
        
        xmax = xmax.reindex(sources_grids, 
                            axis = 0,
                            level = 'Source')
        
        xmax_err = xmax_err.reindex(sources_grids, 
                                    axis = 0,
                                     level = 'Source')
        
        xinfl = xinfl.reindex(sources_grids, 
                                     axis = 0, 
                                     level = 'Source')

        err_xinfl = err_xinfl.reindex(sources_grids, 
                                      axis = 0,
                                     level = 'Source')
        
        colorsc = [cmapc[colors[labels_sources[d]]] 
                    for d in xmax\
                        .index\
                        .get_level_values('Source')]
        
        init_lol(ax = axs[ilc], 
                 xs = xmax, 
                 ys = ys_source,
                 title = lc,
                 ax_tag = 'Peak', 
                 axhv_ls = '--',
                 axhv_lw = 1,
                 axhv_dashes = (4, 4),
                 fs_title = 14,
                 y_title = 1.05,
                 fs_label = 10,
                 fs_ticks = 10,
                 ax_tag_x = 0.5,
                 ax_tag_y = 1,
                 ylabel = '',
                 xlabel = 'Day of year')
        
        hlines(axs[ilc],
               ys = ys_source,
               xmin = xmin,
               xmax = xmax,
               colors = colorsc,
               linewidth = 7,
               alpha = 0.9)
        
        vlines(axs[ilc],
               xs = xmin.values,
               ymin = -1,
               ymax = 0.95,
               colors = 'k',
               linewidth = 3,
               linestyle = 'solid',
               alpha = 0.7)
        
        axs[ilc].vlines(
               x = [0, 1],
               ymin = -1,
               ymax = 0.95,
               colors = 'k',
               linewidth = 2,
               linestyle = 'dashed',
               alpha = 0.7,
               transform = axs[ilc].transAxes)
        
        scatter(axs[ilc],
                xs = xmax.values,
                ys = ys_source,
                colors_marker = colorsc,
                marker = 'o',
                sizes_marker = 150,
                alpha = 0.9)

        error(axs[ilc],
              xs = xmax.values,
              ys = ys_source,
              x_err = xmax_err.values,
              ecolors = ['darkgray'] * len(ys_source),
              elinewidth = 2.5,
              capsize = 6, 
              alpha = 0.9, 
              zorder = 6)
        
        error(axs[ilc],
              xs = xmin.values,
              ys = [-0.35],
              x_err = xmin_err.values,
              ecolors = ['k'],
              capsize = 6,
              elinewidth = 2.5, 
              alpha = 0.8, 
              zorder = 6)

        axs[ilc].set_ylim((-0.5, len(sources_grids)))
        axs[ilc].set_xlim((np.min(np.concatenate([xmax.values - xmax_err.values, 
                         xmin.values - xmin_err.values])) - 16, 
                         np.max(np.concatenate([xmax.values + xmax_err.values, 
                         xmin.values + xmin_err.values])) + 16))
        axs[ilc].set_yticks([], labels =[])

        divider = make_axes_locatable(axs[ilc])
        axinfl1 = divider.append_axes("left", size="100%", pad=0.1, sharey=axs[ilc])
        axinfl2 = divider.append_axes("right", size="100%", pad=0.1, sharey=axs[ilc])

        init_lol(ax = axinfl1, 
                 xs = xinfl_o, 
                 ys = ys_source,
                 ax_tag = 'Season start', 
                 axhv_ls = '--',
                 axhv_lw = 1,
                 axhv_dashes = (4, 4),
                 fs_title = 14,
                 y_title = 1.05,
                 fs_label = 10,
                 fs_ticks = 10,
                 ax_tag_x = 0.5,
                 ax_tag_y = 1,
                 ylabel = '',
                 xlabel = '')
        
        hlines(axinfl1,
               ys = ys_source,
               xmin = xinfl_o.iloc[:, 0],
               xmax = xinfl.iloc[:, 0],
               colors = colorsc,
               linewidth = 7,
               alpha = 0.9)
        
        vlines(axinfl1,
               xs = xinfl_o.iloc[:, 0].values,
               ymin = -1,
               ymax = 0.95,
               colors = 'k',
               linewidth = 3,
               linestyle = 'solid',
               alpha = 0.8)
        
        axinfl1.vlines(
               x = [1],
               ymin = -1,
               ymax = 0.95,
               colors = 'k',
               linewidth = 2,
               linestyle = 'dashed',
               alpha = 0.7,
               transform = axinfl1.transAxes)
        
        scatter(axinfl1,
                xs = xinfl.iloc[:,0],
                ys = ys_source,
                colors_marker = colorsc,
                marker = 'o',
                sizes_marker = 150,
                alpha = 0.9)
        
        error(axinfl1,
              xs = xinfl.iloc[:, 0],
              ys = ys_source,
              x_err = err_xinfl.iloc[:, 0],
              ecolors = ['darkgray'] * len(ys_source),
              elinewidth = 2.5,
              capthick = 2,
              capsize = 6, 
              alpha = 0.9, 
              zorder = 6)
        
        error(axinfl1,
              xs = xinfl_o.iloc[:, 0],
              ys = [-0.35],
              x_err = err_xinfl_o.iloc[:, 0],
              ecolors = ['k'],
              capsize = 6,
              capthick = 2,
              elinewidth = 2.5, 
              alpha = 0.8, 
              zorder = 6)
        
        axinfl1.set_ylim((-0.5, len(sources_grids)))
        axinfl1.set_xlim(np.min(np.concatenate([xinfl.iloc[:, 0].values - err_xinfl.iloc[:, 0].values, 
                         xinfl_o.iloc[:, 0].values - err_xinfl_o.iloc[:, 0].values])) - 16, 
                         np.max(np.concatenate([xinfl.iloc[:, 0].values + err_xinfl.iloc[:, 0].values, 
                         xinfl_o.iloc[:, 0].values + err_xinfl_o.iloc[:, 0].values])) + 16)
        axinfl1.set_yticklabels([])

        axinfl1.text(0.5, 1.10, list_abc[ilc] + ')', fontsize = 14,
                transform = axinfl1.transAxes,
                va = 'bottom', 
                ha = 'center')

        init_lol(ax = axinfl2, 
                 xs = xinfl_o, 
                 ys = ys_source,
                 ax_tag = 'Season end', 
                 axhv_ls = '--',
                 axhv_lw = 1,
                 axhv_dashes = (4, 4),
                 fs_title = 14,
                 y_title = 1.05,
                 fs_label = 10,
                 fs_ticks = 10,
                 ax_tag_x = 0.5,
                 ax_tag_y = 1,
                 ylabel = '',
                 xlabel = '')
        
        hlines(axinfl2,
               ys = ys_source,
               xmin = xinfl_o.iloc[:, 1],
               xmax = xinfl.iloc[:, 1],
               colors = colorsc,
               linewidth = 7,
               alpha = 0.9)
        
        vlines(axinfl2,
               xs = xinfl_o.iloc[:, 1].values,
               ymin = -1,
               ymax = 0.95,
               colors = 'k',
               linewidth = 3,
               linestyle = 'solid',
               alpha = 0.7)
        
        axinfl2.vlines(
               x = [0],
               ymin = -1,
               ymax = 0.95,
               colors = 'k',
               linewidth = 2,
               linestyle = 'dashed',
               alpha = 0.8,
               transform = axinfl2.transAxes)
        
        scatter(axinfl2,
                xs = xinfl.iloc[:, 1],
                ys = ys_source,
                colors_marker = colorsc,
                marker = 'o',
                sizes_marker = 150,
                alpha = 0.9)
        
        error(axinfl2,
              xs = xinfl.iloc[:, 1],
              ys = ys_source,
              x_err = err_xinfl.iloc[:, 1],
              ecolors = ['darkgray'] * len(ys_source),
              elinewidth = 2.5,
              capthick = 2,
              capsize = 6, 
              alpha = 0.9, 
              zorder = 6)
        
        error(axinfl2,
              xs = xinfl_o.iloc[:, 1],
              ys = [-0.35],
              x_err = err_xinfl_o.iloc[:, 1],
              ecolors = ['k'],
              capsize = 6,
              capthick = 2,
              elinewidth = 2.5, 
              alpha = 0.8, 
              zorder = 6)
        
        axinfl2.set_ylim((-0.5, len(sources_grids)))
        axinfl2.set_xlim(np.min(np.concatenate([xinfl.iloc[:, 1].values - err_xinfl.iloc[:, 1].values, 
                         xinfl_o.iloc[:, 1].values - err_xinfl_o.iloc[:, 1].values])) - 16, 
                         np.max(np.concatenate([xinfl.iloc[:, 1].values + err_xinfl.iloc[:, 1].values, 
                         xinfl_o.iloc[:, 1].values + err_xinfl_o.iloc[:, 1].values])) + 16)
        axinfl2.set_yticklabels([])

    return fig

def doy_dist_landcover(name, df, variable, sources_insitu, sources_grids, sel_landcover,
                       colors: dict = {}, doy_init_args = {}, dist_init_args = {},
                       doy_args = {}, dist_args = {}, doy_fill_args = {},
                       color_legend_args = {}, do_fill = True, do_line_bounds = False):


    from my_.series.group import select_multi_index, nona_level
    from my_.series.aggregate import column_wise
    from my_.math.stats import gauss_kde_pdf, pbias, rmse
    from my_.resources.sources import query_variables
    from my_.figures.four_by_two import vertical_top_cax
    from my_.plot.init_ax import init_ts, init_dist
    from my_.plot.legend import color_legend
    from my_.plot.basic import plot, fill 
    from my_.files.handy import save_df 

    import colorcet as cc

    print('Plot land cover aggregated DOY and distribution plots...\n')
    
    df_nona                     = nona_level(df,
                                             ['Variable', 'Station'],
                                             axis = 1,
                                             how = 'any')

    df_s                        = select_multi_index(df_nona, ['Variable', 'Landcover'],
                                                      keys = [variable, sel_landcover])
    
    df_s                        = df_s.reindex(labels = sources_insitu + sources_grids, axis = 1, level = 'Source')

    sources                     = df_s.columns.unique(level = 'Source')

    df_doy                      = df_s.groupby(df_s.index.dayofyear).mean()

    df_doy_lc                   = df_doy.groupby(axis = 1, level = ['Source', 'Landcover'])

    df_doy_lc_mean              = df_doy_lc.mean()

    df_doy_lc_mean_rmse         = column_wise(df_doy_lc_mean, ffunc = rmse)
    df_doy_lc_mean_pbias        = column_wise(df_doy_lc_mean, ffunc = pbias)
    save_df(df_doy_lc_mean_rmse, f'out/{name}/csv/doy_lc_mean_rmse_{variable}.csv', format = 'csv')
    save_df(df_doy_lc_mean_pbias, f'out/{name}/csv/doy_lc_mean_pbias_{variable}.csv', format = 'csv')

    df_doy_lc_std               = df_doy_lc.std()

    df_dist_lc                  = df_s.groupby(axis = 1, level = ['Source', 'Landcover']).apply(gauss_kde_pdf, return_dict=True)

    df_dist_lc.columns          = df_dist_lc.columns.set_names('pdf', level = -1)

    all_xs                      = select_multi_index(df_dist_lc, 'pdf', 'xs')
    all_ys                      = select_multi_index(df_dist_lc, 'pdf', 'ys')

    fig, axs, axs_l             = vertical_top_cax(fy = 8)

    var_units                   = query_variables(sources[0], 'var_units')[variable]
    labels_sources              = {s: query_variables(s, 'name_label') for s in sources}

    cmapc                       = cc.glasbey_hv[:]
    colors                      = {labels_sources[k]: v for k,v in colors.items() if k in sources}
    colorsc                     = [cmapc[colors[d]] for d in colors.keys()]

    color_legend(axs_l, colors, cmapc, **color_legend_args)

    for ilc, lc in enumerate(sel_landcover):

        xs_doy                  = df_doy_lc_mean.index

        ys_doy                  = select_multi_index(df_doy_lc_mean, levels = ['Landcover'], keys = [lc])
        
        err_doy                 = select_multi_index(df_doy_lc_std, levels = ['Landcover'], keys = [lc])

        xs_dist                 = select_multi_index(df_dist_lc, levels = ['Landcover', 'pdf'], keys = [lc, 'xs'])

        ys_dist                 = select_multi_index(df_dist_lc, levels = ['Landcover', 'pdf'], keys = [lc, 'ys'])

        var_label               = f'{variable} [{var_units}]'

        lower                   = ys_doy - err_doy
        upper                   = ys_doy + err_doy

        init_ts(axs[ilc, 0], xs_doy, df_doy_lc_mean, ylabel = var_label, ax_tag = lc, **doy_init_args)
        init_dist(axs[ilc, 1], all_xs, all_ys, xlabel = var_label, ax_tag = lc, **dist_init_args)

        plot(axs[ilc, 0], xs_doy, ys_doy, colors = colorsc, **doy_args)
        if do_fill : fill(axs[ilc, 0], xs_doy, lower, upper, colors = colorsc, **doy_fill_args)

        if do_line_bounds:
            plot(axs[ilc, 0], xs_doy, lower, colors = colorsc, style = '-.', alpha = 0.6, lw = 1.0, zorder = 6)
            plot(axs[ilc, 0], xs_doy, upper, colors = colorsc, style = '-.', alpha = 0.6, lw = 1.0, zorder = 6)
        plot(axs[ilc, 1], xs_dist, ys_dist, colors = colorsc, **dist_args)
        
    return fig

def dist_landcover(name: str, 
                   df: pd.DataFrame, 
                   variable: str, 
                   sources_insitu: list[str], 
                   sources_grids: list[str], 
                   sel_landcover: list[str],
                   colors: dict = {}, 
                   dist_init_args: dict = {},
                   dist_args: dict = {},
                   color_legend_args: dict = {}):
    
    from my_.series.group import select_multi_index, nona_level
    from my_.series.aggregate import column_wise
    from my_.math.stats import gauss_kde_pdf, pbias, rmse
    from my_.resources.sources import query_variables
    from my_.figures.two_by_two import square_top_cax
    from my_.plot.init_ax import init_ts, init_dist
    from my_.plot.legend import color_legend
    from my_.plot.basic import plot, fill 
    from my_.files.handy import save_df

    import colorcet as cc

    print('Plot land cover aggregated DOY and distribution plots...\n')
    
    df_nona                     = nona_level(df,
                                             ['Variable', 'Station'],
                                             axis = 1,
                                             how = 'any')

    df_s                        = select_multi_index(df_nona, ['Variable', 'Landcover'],
                                                      keys = [variable, sel_landcover])
    
    #df_s                        = df_s.reindex(sources_insitu + sources_grids, axis = 1, level = 'Source')

    sources                     = df_s.columns.unique(level = 'Source')

    df_dist_lc                  = df_s.groupby(axis = 1, level = ['Source', 'Landcover']).apply(gauss_kde_pdf, return_dict=True)


    df_dist_lc.columns          = df_dist_lc.columns.set_names('pdf', level = -1)

    all_xs                      = select_multi_index(df_dist_lc, 'pdf', 'xs')
    all_ys                      = select_multi_index(df_dist_lc, 'pdf', 'ys')

    var_units                   = query_variables(sources[0], 'var_units')[variable]
    labels_sources              = {s: query_variables(s, 'name_label') for s in sources}

    cmapc                       = cc.glasbey_hv[:] + [[0.0, 0.0, 0.0]]
    colorsp                     = {labels_sources[k]: v for k, v in colors.items() if k in sources}

    fig, axs, axl               = square_top_cax(fy = 5.5)

    color_legend(axl, colorsp, cmapc, **color_legend_args)

    for ilc, lc in enumerate(sel_landcover):

        lw = [3] + [1.5] * len(sources_grids)

        xs_dist = select_multi_index(df_dist_lc, levels = ['Landcover', 'pdf'], keys = [lc, 'xs'])

        xs_dist = xs_dist.reindex(sources_insitu + sources_grids, axis = 1, level = 'Source')

        ys_dist = select_multi_index(df_dist_lc, levels = ['Landcover', 'pdf'], keys = [lc, 'ys'])

        ys_dist = ys_dist.reindex(sources_insitu + sources_grids, axis = 1, level = 'Source')

        colorsc = [cmapc[colorsp[labels_sources[d]]] 
                    for d in ys_dist\
                        .columns\
                        .get_level_values('Source')]

        var_label               = f'{variable} [{var_units}]'

        init_dist(axs[ilc], all_xs, all_ys, xlabel = var_label, ax_tag = lc, **dist_init_args)

        plot(axs[ilc], xs_dist, ys_dist, lw = lw, colors = colorsc, **dist_args)

    return fig

def pie_landcover(df_static, selected_landcover, colors = {}, color_legend_args = {}):

    print('Plot network land cover pie plots\n')

    from my_.series.aggregate import concat
    from my_.resources.sources import query_static
    from my_.figures.double import horizontal_top_cax
    from my_.plot.basic import pie
    from my_.plot.legend import color_legend
    from my_.plot.init_ax import init_pie
    import matplotlib.pyplot as plt

    landcover                   = df_static['landcover'].where(df_static['landcover'].isin(selected_landcover))

    pct_crop                    = df_static['PCT_CROP'] / 100

    pct_nat                     = df_static['PCT_NATVEG'] / 100

    pft_cols                    = [col for col in df_static.columns if 'PCT_NAT_PFT_' in col]

    cft_cols                    = [col for col in df_static.columns if 'PCT_CFT_' in col]

    pft_rel                     = df_static[pft_cols].multiply(pct_nat, axis = 0)

    cft_rel                     = df_static[cft_cols].multiply(pct_crop, axis = 0)

    df_tot                      = concat([pft_rel, cft_rel], sort = False)

    ind_landcover               = query_static('CLM5-EU3-surf', 'sel_agg_layer_PFT')

    shares_surf                 = [df_tot.iloc[:, ind_landcover[lc]].sum(axis = 1).mean() for lc in selected_landcover]

    shares_surf_o               = shares_surf + [100 - sum(shares_surf)] 

    shares_lc                   = landcover.value_counts(normalize = True)

    fig, axs, axl               = horizontal_top_cax(x_an = 0.1, y_an = 0.8)

    cmapc                       = plt.get_cmap('Set2').colors

    colors                      = {k: v for k,v in colors.items()}
    colorsc                     = [cmapc[colors[lc]] for lc in list(selected_landcover)]

    colors['other']             = 7

    colorsc_o                   = colorsc + [cmapc[7]]

    color_legend(axl, colors, cmapc, **color_legend_args)

    init_pie(axs[0], ax_tag = 'ICOS network')
    init_pie(axs[1], ax_tag = 'Corresponding CLM5 surface')

    pie(axs[0], shares_lc, colorsc, autopct='%1.1f%%')
    pie(axs[1], shares_surf_o, colorsc_o, autopct='%1.1f%%')

    return fig


def doy_landcover(df, variable, sources_insitu, sources_grids, sel_landcover,
                       stat: str = 'mean', stat_err: str = 'std',
                       colors: dict = {}, doy_init_args = {},
                       doy_args = {}, doy_fill_args = {},
                       color_legend_args = {}, do_fill = False):
    
    print('Plot network land cover DOY plots\n')

    from my_.series.group import select_multi_index, nona_level
    from my_.resources.sources import query_variables
    from my_.figures.two_by_two import square_top_cax
    from my_.plot.init_ax import init_ts
    from my_.plot.legend import color_legend
    from my_.plot.basic import plot, fill 

    import colorcet as cc

    df_nona                     = nona_level(df, 
                                             ['Variable', 'Station'],
                                             axis = 1,
                                             how = 'any')

    df_s                        = select_multi_index(df_nona, ['Variable', 'Landcover'],
                                                      keys = [variable, sel_landcover])
    
    df_s                        = df_s.reindex(labels = sources_insitu + sources_grids, axis = 1, level = 'Source')

    sources                     = df_s.columns.unique(level = 'Source')

    df_doy                      = df_s.groupby(df_s.index.dayofyear).mean()

    df_doy_lc                   = df_doy.groupby(axis = 1, level = ['Source', 'Landcover'])

    df_doy_lc_agg               = df_doy_lc.agg(stat)

    df_doy_lc_agg_err           = df_doy_lc.agg(stat_err)

    fig, axs, axl               = square_top_cax(fx = 8)

    var_units                   = query_variables(sources[0], 'var_units')[variable]
    labels_sources              = {s: query_variables(s, 'name_label') for s in sources}

    cmapc                       = cc.glasbey_hv[:]
    colors                      = {labels_sources[k]: v for k,v in colors.items() if k in sources}
    colorsc                     = [cmapc[colors[d]] for d in colors.keys()]

    color_legend(axl, colors, cmapc, **color_legend_args)

    for ilc, lc in enumerate(sel_landcover):

        xs_doy                  = df_doy_lc_agg.index

        ys_doy                  = select_multi_index(df_doy_lc_agg, levels = ['Landcover'], keys = [lc])
        
        err_doy                 = select_multi_index(df_doy_lc_agg_err, levels = ['Landcover'], keys = [lc])

        var_label               = f'{variable} [{var_units}]'

        lower                   = ys_doy - err_doy
        upper                   = ys_doy + err_doy

        init_ts(axs[ilc], xs_doy, df_doy_lc_agg, ylabel = var_label, ax_tag = lc, **doy_init_args)
        plot(axs[ilc], xs_doy, ys_doy, colors = colorsc, **doy_args)

        if do_fill: fill(axs[ilc], xs_doy, lower, upper, colors = colorsc, **doy_fill_args)

    return fig


def plot_ts(df, variable, station, colors: dict = {}, color_legend_args: dict = {},
            fig_args: dict = {}, ts_init_args: dict = {}, plot_args: dict = {}):

    print(f'Plot station time-series: {station}, {variable}\n')

    from my_.series.group import select_multi_index, nona_level
    from my_.figures.single import square_top_cax
    from my_.plot.init_ax import init_ts_2
    from my_.plot.basic import plot
    from my_.plot.legend import color_legend
    from my_.resources.sources import query_variables

    import colorcet as cc
    import numpy as np


    stations_uq = df.columns.unique(level = 'Station')
    
    stations_count = df.columns\
                       .get_level_values('Station')\
                       .value_counts()
    
    for s in stations_uq:
        
        if stations_count[s] == 1:

            df = df.drop(s, axis = 1, level = 'Station')

    df_nona                     = nona_level(df, 
                                             ['Variable', 'Station'],
                                             axis = 1,
                                             how = 'any')

    df_s                        = select_multi_index(df_nona, ['Variable', 'Station'],
                                                      keys = [variable, station])
    
    sources                     = df_s.columns.unique(level = 'Source')

    fig, ax, axl, gs            = square_top_cax(**fig_args)

    if len(sources) == 0 : return fig
    
    cmapc                       = cc.glasbey_hv[:] + [[0.0, 0.0, 0.0]]
    colors                      = {k: v for k,v in colors.items() if k in sources}
    colorsc                     = [cmapc[colors[d]] for d in list(sources)]

    var_units                   = query_variables(sources[0], 'var_units')[variable]

    xs                          = df_s.index
    ys                          = df_s

    if np.all(np.isnan(ys)): return fig
    
    color_legend(axl, colors, cmapc, **color_legend_args)

    init_ts_2(ax, df_s.dropna(how = 'all').index, df_s.dropna(how = 'all'),
            title = f'{station} {variable} [{var_units}]', **ts_init_args)
    
    plot(ax, xs, ys, colors = colorsc, cycle_direction = 1, **plot_args)

    return  fig


def plot_ts_2(x, y, labels, variable, colors: dict = {}, color_legend_args: dict = {},
            fig_args: dict = {}, ts_init_args: dict = {}, plot_args: dict = {}):

    print(f'Plot station time-series: {variable}\n')

    from my_.figures.single import square_top_cax
    from my_.plot.init_ax import init_ts_2
    from my_.plot.basic import plot
    from my_.plot.legend import color_legend
    from my_.resources.sources import query_variables

    import colorcet as cc
    import numpy as np

    cmapc                       = cc.glasbey_hv[:]
    colors                      = {k: v for k, v in colors.items() if k in labels}
    colorsc                     = [cmapc[colors[d]] for d in list(labels)]

    fig, ax, axl, gs            = square_top_cax(**fig_args)

    #var_units                   = query_variables('CLM5-EU3', 'var_units')[variable]

    if np.all(np.isnan(y)): return fig
    
    color_legend(axl, colors, cmapc, **color_legend_args)

    init_ts_2(ax, x, y, **ts_init_args)

    plot(ax, x, y, colors = colorsc, **plot_args)

    return  fig