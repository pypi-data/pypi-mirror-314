import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from my_.plot.init_ax import init_annotation_ax
from my_.plot.style import style_1

def horizontal(fx: float = 6.7, fy: float = 3.35, dpi: int = 300, projection = None, frame: bool = False):

    import matplotlib.pyplot as plt
    from my_.plot.style import style_1

    style_1()

    nrows                           = 1
    ncols                           = 2

    fig                             = plt.figure(figsize=(fx,fy), dpi= dpi)

    ax1                             = fig.add_subplot(nrows, ncols, 1, projection = projection, frameon = frame)
    ax2                             = fig.add_subplot(nrows, ncols, 2, projection = projection, frameon = frame)

    return fig, [ax1, ax2]


def horizontal_right_cax(fx: float = 6.7, fy: float =3.35, dpi: int = 300, projection = None, frame: bool = False):

    import matplotlib.pyplot as plt
    from matplotlib.gridspec import GridSpec
    from my_.plot.style import style_1

    style_1()

    nrows                           = 1
    ncols                           = 3
    w1, w2                          = 14, 1

    fig                             = plt.figure(figsize=(fx,fy), dpi= dpi)

    gs                              = GridSpec(figure = fig, 
                                                ncols = ncols, nrows = nrows, 
                                                width_ratios = [w1, w1, w2], wspace = 0.3)

    ax1                             = fig.add_subplot(gs[0, 0], projection = projection, frameon = frame)
    ax2                             = fig.add_subplot(gs[0, 1], projection = projection, frameon = frame)

    cax                             = fig.add_subplot(gs[0, 2], frameon = frame)

    return fig, [ax1, ax2], cax


def horizontal_top_cax(fx: float = 6.7, fy: float = 3.4, dpi: int = 300, projection = None,
                       frame: bool = False, annotation: bool = True, hspace = 0.1,
                       x_an: float = 0.05, y_an: float = 1.05):

    import matplotlib.pyplot as plt
    from matplotlib.gridspec import GridSpec
    from my_.plot.init_ax import init_annotation_ax
    from my_.plot.style import style_1

    style_1()

    nrows                           = 2
    ncols                           = 2
    w1, w2                          = 1, 14

    fig                             = plt.figure(figsize=(fx,fy), dpi= dpi)

    gs                              = GridSpec(figure = fig, 
                                                ncols = ncols, nrows = nrows, 
                                                height_ratios = [w1, w2],
                                                hspace = hspace)

    ax1                             = fig.add_subplot(gs[1, 0], projection = projection, frameon = frame)
    ax2                             = fig.add_subplot(gs[1, 1], projection = projection, frameon = frame)

    cax                             = fig.add_subplot(gs[0, :], frameon = frame)

    if annotation: init_annotation_ax([ax1, ax2], x = x_an, y = y_an)

    return fig, [ax1, ax2], cax


def horizontal_2top_cax(fx: float = 6.7, 
                        fy: float = 3.4, 
                        dpi: int = 300, 
                        projection = None,
                        frame: bool = False, 
                        annotation: bool = False, 
                        hspace = 0.1,
                        x_an: float = 0.05, 
                        y_an: float = 1.05):


    style_1()

    nrows = 2
    ncols = 2
    w1, w2 = 1, 14

    fig = plt.figure(figsize = (fx, fy), 
                     dpi = dpi)

    gs = GridSpec(figure = fig, 
                  ncols = ncols, 
                  nrows = nrows, 
                  height_ratios = [w1, w2],
                  hspace = hspace)

    ax1 = fig.add_subplot(gs[1, 0], 
                          projection = projection, 
                          frameon = frame)
    
    ax2 = fig.add_subplot(gs[1, 1], 
                          projection = projection, 
                          frameon = frame)

    cax1 = fig.add_subplot(gs[0, 0], frameon = frame)
    cax2 = fig.add_subplot(gs[0, 1], frameon = frame)

    if annotation: init_annotation_ax([ax1, ax2], x = x_an, y = y_an)

    return fig, [ax1, ax2], [cax1, cax2]

def horizontal_topleft_cax(fx: float = 6.7, 
                           fy: float = 3.4, 
                           dpi: int = 300, 
                           projection = None,
                           frame: bool = False, 
                           annotation: bool = False, 
                           hspace = 0.1,
                           x_an: float = 0.05, 
                           y_an: float = 1.05):


    style_1()

    nrows = 2
    ncols = 2
    w1, w2 = 1, 14

    fig = plt.figure(figsize = (fx, fy), 
                     dpi = dpi)

    gs = GridSpec(figure = fig, 
                  ncols = ncols, 
                  nrows = nrows, 
                  height_ratios = [w1, w2],
                  hspace = hspace)

    ax1 = fig.add_subplot(gs[1, 0], 
                          projection = projection, 
                          frameon = frame)
    
    ax2 = fig.add_subplot(gs[1, 1], 
                          projection = projection, 
                          frameon = frame)

    cax1 = fig.add_subplot(gs[0, 0], frameon = frame)

    if annotation: init_annotation_ax([ax1, ax2], x = x_an, y = y_an)

    return fig, [ax1, ax2], cax1