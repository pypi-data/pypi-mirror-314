

def style_1(font_dir: str = '/p/scratch/cjibg31/jibg3105/projects/my_py/src/my_/plot/fonts'):

    import matplotlib as mpl
    import matplotlib.font_manager as fm


    
    font_files = fm.findSystemFonts(fontpaths = font_dir)
    
    for font_file in font_files:
        fm.fontManager.addfont(font_file)
    
    prop = fm.FontProperties(fname=font_dir+'/Montserrat-Medium.otf')

    mpl.rcParams['font.family']     = prop.get_name()
    text_color                      = 'dimgrey'
    mpl.rcParams['xtick.color']     = text_color
    mpl.rcParams['ytick.color']     = text_color


def nospines(ax):

    ax.spines.right.set_visible(False)
    ax.spines.top.set_visible(False)
    ax.spines.bottom.set_visible(False)
    ax.spines.left.set_visible(False)

    