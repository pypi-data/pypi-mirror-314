import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from io import BytesIO
from copy import deepcopy
from PIL import Image
import math
import numpy as np

from lazyplot.config import FigureConfig, LazyAxes

GLOBAL_CONFIG = FigureConfig()


#=======================================================================
def set_global_config(user_config):
    """
    set PlotConfig globally (not saved)
    """
    GLOBAL_CONFIG.override(user_config)
    return

#====================================================================
def generate_local_config(user_config):
    """
    regenerate PlotConfig for lazy_plot() and custom_plot()
    input: dict{ key of PlotConfig : value}
    output: PlotConfig override by user defined value 
    """
    cfg = deepcopy(GLOBAL_CONFIG)
    cfg.override(user_config)
    return cfg

#================================================================================
def init_figure(num_axes: int, cfg):
    """
    make matplotlib.Figure and number of columns and rows for subplot
    """
    
    fig = plt.figure(figsize=cfg.figsize, linewidth=cfg.linewidth, layout=cfg.layout, dpi=cfg.dpi)
    ax_cols = cfg.columns
    ax_rows = math.ceil(num_axes /cfg.columns)
    
    return fig, ax_cols, ax_rows


#=================================================================================
def custom_plot(lazy_axes: list[LazyAxes],
                out_path: str = None,
                figure_config: dict | None = None):
    """
    Draw more detailed graph by using user-specified LazyAxes
    
    -------input-------
    lazy_axes (LazyAxes or list[LazyAxes]) > User-specified LazyAxes
    out_path (str or None) >  Output path of the image file. if None, no image file is output
    figure_config (dict) > Value to override FigureConfig.
    
    -------output------
    img (PIL image data)
    
    """
    if isinstance(lazy_axes, list) == False:
        lazy_axes = [lazy_axes]
        
    cfg = generate_local_config(figure_config)
    fig, ax_cols, ax_rows = init_figure(len(lazy_axes), cfg)
    
    for i, data in enumerate(lazy_axes, 1):
        _ax = fig.add_subplot(ax_rows, ax_cols, i)
        plot_ax(_ax, data)
    
    if out_path is not None:
        fig.savefig(out_path, dpi=cfg.dpi)

    #render PIL --------------------------
    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    img = Image.open(buf)

    plt.close(fig)
    
    return img

#=================================================================================
def lazy_plot(input_data: np.ndarray | list[np.ndarray], 
              out_path: str | None = None,
              figure_config: dict | None = None) :
    """
    Draw graphs by entering only data.
    
    -----input--------
    input_data (np.ndarray or list[np.ndarray]) > 
    out_path (str or None) >  Output path of the image file. if None, no image file is output
    figure_config (dict) > Value to override FigureConfig.
    
    -------output------
    img (PIL image data)
    
    """
    if isinstance(input_data, list) is False:
        input_data = [input_data]
    
    cfg = generate_local_config(figure_config)    # local config within this function
    fig, ax_cols, ax_rows = init_figure(len(input_data), cfg)
    
    for i, data in enumerate(input_data, 1):
        _title = f'data {i}'
        _ax = fig.add_subplot(ax_rows, ax_cols, i)
        _lazy_axes = create_lazy_axes(data, _title, cfg)
        
        plot_ax(_ax, _lazy_axes)
        
    if out_path is not None:
        fig.savefig(out_path, dpi=cfg.dpi)

    #render PIL --------------------------
    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    img = Image.open(buf)

    plt.close(fig)
        
    return img
        
#====================================================================================
def create_lazy_axes(data: np.ndarray, title: str, cfg: FigureConfig):
    
    if data.ndim == 1:
        plot_type = cfg.plot_type_1d
    elif data.ndim == 2:
        plot_type = cfg.plot_type_2d
    elif data.ndim == 3:
        plot_type = cfg.plot_type_3d
    else:
        raise ValueError("Invalid data dimension. Data is limited to 3 dimensions or less")
    
    lazy_axes = LazyAxes(y=data, plot_type=plot_type, title=title, linewidth=cfg.linewidth)
    
    return lazy_axes


#=======================================================================================
def plot_ax(ax: Axes, data: LazyAxes):
    
    require_legend = False
    
    match data.plot_type:
        #-------------------------------------------------------------------------------
        case "plot":
            if data.y.ndim > 2:
                raise ValueError(f"Invalid data shape: {data.y.shape}. plot_type: \"plot\" require (N) or (M, N) data")
            
            if data.y.ndim == 1:
                data.y = np.expand_dims(data.y, axis=0)
                
            #plot----------------------------------------
            require_legend = True if len(data.y) != 1 else False
            for i, y in enumerate(data.y):
                _color = data.color[i % len(data.color)]
                _linestyle = data.line_style[(i // len(data.color)) % len(data.line_style)]
                _t = np.arange(len(y)) if data.t is None else data.t
                _label = f"graph {i+1}" if data.labels is None else data.labels[i]
                ax.plot(_t, y, label=_label, color=_color, alpha=data.alpha,
                        linewidth=data.linewidth, linestyle=_linestyle)
        #---------------------------------------------------------------------------------
        case "hist":
            if data.y.ndim != 1:
                raise ValueError(f"Invalid data shape: {data.y.shape}. plot_type: \"hist\" require (N) data")
            ax.hist(data.y, color=data.color[0])
        #---------------------------------------------------------------------------------
        case "bar":
            if data.y.ndim != 1:
                raise ValueError(f"Invalid data shape: {data.y.shape}. plot_type: \"bar\" require (N) data")
            label = [f"data {i + 1}" for i in range(len(data.y))] if data.labels is None else data.labels
            color = [data.color[i % len(data.color)] for i in range(len(data.y))]
            ax.bar(label, data.y, color=color)
            
        #----------------------------------------------------------------------------------
        case "boxplot":
            if data.y.ndim != 2:
                raise ValueError(f"Invalid data shape: {data.y.shape}. plot_type: \"boxplot\" require (M, N) data")
            
            #plot--------------------
            label = [f"data {i + 1}" for i in range(len(data.y))] if data.labels is None else data.labels
            color = [data.color[i & len(data.color)] for i in range(len(data.y))]
            bplot = ax.boxplot(data.y.T, labels=label, patch_artist=True, medianprops=dict(color="white", linewidth=3))
            #paint facecolor
            for i, patch in enumerate(bplot['boxes']):
                color = data.color[i % len(data.color)]
                patch.set_facecolor(color)
            
        #----------------------------------------------------------------------------------
        case "scatter":
            if data.y.ndim == 1 or data.y.ndim > 3:
                raise ValueError(f"Invalid data shape: {data.y.shape}. plot_type: \"scatter\" require (M, 2, N) or (2, N) data")
            elif data.y.ndim == 2:
                data.y = np.expand_dims(data.y, axis=0)
            
            if data.y.shape[1] != 2:
                print("WARNING: cannot plot 3D data. z or higher dimension axis is ignored. Valid shape of data is (M, 2, N) or (2, N)")
            
            #plot-----------------------------------------
            require_legend = True if len(data.y) != 1 else False
            for i, y in enumerate(data.y):
                _color = data.color[i % len(data.color)]
                _markerstyle = data.marker_style[(i // len(data.color)) % len(data.marker_style)]
                _label = f"graph {i+1}" if data.labels is None else data.labels[i]
                ax.scatter(y[0], y[1], label=_label, color=_color, alpha=data.alpha,
                        linewidth=data.linewidth, marker=_markerstyle)
        #--------------------------------------------------------------------------------    
        case "imshow":
            if data.y.ndim == 1 or data.y.ndim > 3:
                raise ValueError(f"Invalid data shape: {data.y.shape}. plot_type: \"imshow\" require (M, N) or (M, N, 3[RGB] | 4[RGBA]) data")
            
            if data.y.ndim == 3:
                if data.y.shape[2] != 3 and data.y.shape[2] != 4:
                    raise ValueError(f"Invalid data shape: {data.y.shape}. plot_type: \"imshow\" require (M, N) or (M, N, 3[RGB] | 4[RGBA]) data")
            
            #plot------------------------      
            ax.imshow(data.y)           
        #--------------------------------------------------------------------------------
        case _:
            raise ValueError(f"Invalid plot_type: {data.plot_type}.")
    
    
    # ax setting --------------------------------------
    if data.title is not None:
        ax.set_title(data.title)
    ax.set_xlabel(data.x_label)
    ax.set_ylabel(data.y_label)
    ax.set_xlim(data.x_lim)
    ax.set_ylim(data.y_lim)
    ax.set_aspect(data.aspect)
    
    if data.invert_xaxis:
        ax.invert_xaxis()
    if data.invert_yaxis:
        ax.invert_yaxis()
    if require_legend:   
        ax.legend()
    
#=======================================================================