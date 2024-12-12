
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable

def marker_legend(ax: plt.axes, 
                  dict_labels_markers: dict, 
                  marker_color: str = 'grey', 
                  marker_sizes: float | dict = 10.0, 
                  labelcolor: str = 'k',
                  title: str | None = None,
                  anchor: tuple = (0.5, 0), 
                  markerfirst: bool = True, 
                  fs_labels: float = 12.0, 
                  handletextpad: float = 0.2,
                  columnspacing: float = 0.9, 
                  loc: str = 'lower center', 
                  handlelength: float = 1.2):

    from matplotlib.lines import Line2D
    
    ax.set_yticks([])
    ax.set_xticks([])

    handles = [Line2D([0], [0], 
                       marker = dict_labels_markers[ll], 
                       color = 'white', 
                       markeredgecolor = marker_color, 
                       markersize = marker_sizes[ll], 
                       label = ll) 
                       for ll in dict_labels_markers]
    
    labels = list(dict_labels_markers.keys())

    ax.legend(handles, 
              labels, 
              fontsize = fs_labels, 
              ncol = len(handles),
              frameon = False, 
              title = title,
              labelcolor = labelcolor,
              loc = loc, 
              bbox_to_anchor = anchor, 
              handletextpad = handletextpad, 
              columnspacing = columnspacing,
              handlelength = handlelength, 
              bbox_transform = ax.transAxes, 
              markerfirst = markerfirst)
    

def color_legend(ax: plt.axes,
                 dict_labels_colors: dict,
                 cmap: ScalarMappable | list,
                 linewidth: float = 5.0, 
                 fs_labels: float = 10.0,
                 anchor: tuple = (0.5, 0), 
                 markerfirst: bool = True,
                 handletextpad: float = 0.35,
                 columnspacing: float = 0.9, 
                 loc: str = 'lower center', 
                 handlelength: float = 1.0,
                 ncols: int = 1):

    from matplotlib.lines import Line2D
    
    ax.set_yticks([])
    ax.set_xticks([])

    handles                     = [Line2D([0], [0], color = cmap[v],
                                        linewidth = linewidth, label = k) 
                                        for k, v in dict_labels_colors.items()]

    labels                      = list(dict_labels_colors.keys())

    short_labels                = [l.replace('-EU3', '') for l in labels]

    ax.legend(handles, short_labels, 
            fontsize = fs_labels, 
            ncol = ncols, 
            frameon = False, 
            loc = loc, 
            bbox_to_anchor = anchor, 
            handletextpad = handletextpad, 
            columnspacing = columnspacing,
            handlelength = handlelength, 
            bbox_transform = ax.transAxes, 
            markerfirst = markerfirst)