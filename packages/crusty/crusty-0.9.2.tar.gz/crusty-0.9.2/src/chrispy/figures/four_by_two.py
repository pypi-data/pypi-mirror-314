
def vertical_top_cax(fx: float = 6.7, fy: float = 13.4, dpi: int = 300, 
                        layout: str = 'constrained', projection = None, frame: bool = False,
                        hspace: float = 0.05, wspace: float = 0.05,
                        annotation: bool = True, x_an: float = -0.05, y_an: float = 1.05): 

    import matplotlib.pyplot as plt
    from matplotlib.gridspec import GridSpec

    from my_.plot.style import style_1
    from my_.plot.init_ax import init_annotation_ax

    style_1()

    ncols, nrows                    = 2, 5

    figure                          = plt.figure(figsize = (fx, fy), dpi = dpi, layout = layout)

    gs                              = GridSpec(figure = figure, ncols = ncols, nrows = nrows,
                                               height_ratios = [1, 18, 18, 18, 18],
                                               hspace = hspace, wspace = wspace)

    axs_kw                          = {'frameon': frame, 'projection': projection}

    axs                             = gs.subplots(subplot_kw = axs_kw)

    for ax in axs[0,0:2]:
        ax.remove()
    
    axl                             = plt.subplot(gs[0,:], **axs_kw)

    if annotation: init_annotation_ax(axs[1:,:].flatten(), x = x_an, y = y_an)

    return figure, axs[1:,:], axl
