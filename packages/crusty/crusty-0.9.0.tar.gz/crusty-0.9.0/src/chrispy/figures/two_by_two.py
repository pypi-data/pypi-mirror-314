

def square_two_top_cax(fx: float = 6.7, fy: float = 6.7, dpi: int = 300, 
                        layout: str = 'constrained', projection = None, frame: bool = False,
                        hspace: float = 0.3, wspace: float = 0.4, annotation: bool = True):

    import matplotlib.pyplot as plt
    from matplotlib.gridspec import GridSpec

    from my_.plot.style import style_1
    from my_.plot.init_ax import init_annotation_ax

    style_1()

    ncols, nrows = 2, 3

    figure = plt.figure(figsize = (fx, fy), 
                        dpi = dpi, )
                        #layout = layout)

    gs                              = GridSpec(figure = figure, 
                                               ncols = ncols, 
                                               nrows = nrows,
                                               height_ratios = [1, 20, 20],
                                               hspace = hspace, 
                                               wspace = wspace)

    axs_kw                          = {'frameon': frame, 'projection': projection}

    axs                             = gs.subplots(subplot_kw = axs_kw).flatten()

    if annotation: init_annotation_ax(axs[2:])

    return figure, axs[2:], axs[0:2]


def square_top_cax(fx: float = 6.7, fy: float = 6.7, dpi: int = 300, 
                        layout: str = 'constrained', projection = None, frame: bool = False,
                        hspace: float = 0.05, wspace: float = 0.05, annotation: bool = True,
                        x_an: float = 0.05, y_an: float = 1.05):

    import matplotlib.pyplot as plt
    from matplotlib.gridspec import GridSpec

    from my_.plot.style import style_1
    from my_.plot.init_ax import init_annotation_ax

    style_1()

    ncols, nrows                    = 2, 3

    figure                          = plt.figure(figsize = (fx, fy), dpi = dpi, layout = layout)

    gs                              = GridSpec(figure = figure, ncols = ncols, nrows = nrows,
                                               height_ratios = [1, 20, 20],
                                               hspace = hspace, wspace = wspace)

    axs_kw                          = {'frameon': frame, 'projection': projection}

    axs                             = gs.subplots(subplot_kw = axs_kw).flatten()

    for ax in axs[0:2]:
        ax.remove()

    if annotation: init_annotation_ax(axs[2:], x = x_an, y = y_an)
    
    axl                             = plt.subplot(gs[0,:], **axs_kw)

    return figure, axs[2:], axl


