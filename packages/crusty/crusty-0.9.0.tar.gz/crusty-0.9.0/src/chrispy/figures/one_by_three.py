import matplotlib as mpl
import matplotlib.pyplot as plt
import cartopy.crs as ccrs


def horizontal_right_map_two_cax(fx: float = 6.7,
                                 fy: float = 6.7,
                                 dpi: int = 300, 
                                 layout: str = 'constrained', 
                                 projection: None | ccrs.Projection = None, 
                                 frame: bool = False,
                                 hspace: float = 0.05, 
                                 wspace: float = 0.05,
                                 annotation: bool = True, 
                                 x_an: float = -0.05, 
                                 y_an: float = 1.05): 

    from matplotlib.gridspec import GridSpec
    from matplotlib.patches import ConnectionPatch

    from my_.plot.style import style_1
    from my_.plot.init_ax import init_annotation_ax

    style_1()

    ncols, nrows                    = 2, 6

    figure                          = plt.figure(figsize = (fx, fy), 
                                                 dpi = dpi, 
                                                 layout = layout)

    gs                              = GridSpec(figure = figure, 
                                               ncols = ncols, 
                                               nrows = nrows,
                                               height_ratios = [1, 15, 4, 1.5, 11, 11],
                                               width_ratios = [10, 10],
                                               hspace = hspace, 
                                               wspace = wspace)
    

    
    axp_kw                          = {'frameon': frame}
    axm_kw                          = {'frameon': frame, 'projection': projection}

    axp1                            = plt.subplot(gs[1, 0], **axp_kw)
    axp2                            = plt.subplot(gs[1, 1], **axp_kw)
    axm                             = plt.subplot(gs[4:6, 0:2], **axm_kw)
    
    axl1                            = plt.subplot(gs[0, :2], **axp_kw)
    axl2                            = plt.subplot(gs[3, 0], **axp_kw)
    axc                             = plt.subplot(gs[3, 1], **axp_kw)

    transFigure                     = figure.transFigure.inverted()

    line                            = ConnectionPatch(xyA=(0, 0), xyB=(0, 1), coordsA="axes fraction", coordsB="axes fraction",
                                                    axesA=axp1, axesB=axp2, color="red")
    
    axp2.add_artist(line)

    axs                             = [axp1, axp2, axm]

    if annotation: init_annotation_ax(axs, x = x_an, y = y_an)

    return figure, axs, axl1, axl2, axc