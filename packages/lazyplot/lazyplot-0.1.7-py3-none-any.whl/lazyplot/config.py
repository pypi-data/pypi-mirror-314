from dataclasses import dataclass, field
from typing import Literal
import numpy as np

FIGURE_LAYOUT = Literal["tight", "constrained"]

PLOT_TYPE_1D = Literal["plot", "hist", "bar"]
PLOT_TYPE_2D = Literal["plot", "scatter", "imshow", "boxplot"]
PLOT_TYPE_3D = Literal["scatter"]

COLOR = ['royalblue', 'olivedrab', 'firebrick', 'teal', 'slateblue', 'goldenrod', 'dimgray']
MARKER_STYLE = [',', '.', 'o', 'v', '^', '<', '>', 's', 'p', '*', 'D', 'd']
LINE_STYLE = ['-', '--', '-.', ':']

#=========================================================================
@dataclass
class FigureConfig:
    figsize: tuple[int, int] = (5, 4)
    layout: FIGURE_LAYOUT = "constrained"
    linewidth : float = 2.0
    columns: int = 1
    
    plot_type_1d: PLOT_TYPE_1D = "plot"
    plot_type_2d: PLOT_TYPE_2D = "imshow"
    plot_type_3d: PLOT_TYPE_3D = "scatter"
    
    dpi: float = 100
    
    # validate after initialize--------------------------------
    def __post_init__(self):
        self.validate()
    
    # validate property----------------------------------------
    def validate(self):
        if self.layout not in ["tight", "constrained"]:
            raise ValueError(f"Invalid figure layout: {self.layout}. Must be 'tight' or 'constrained'.")
        if self.columns <= 0:
            raise ValueError(f"Invalid columns: {self.columns}. Must be greater than 0")
    
    # set value by string key ---------------------------------
    def set_by_key(self, key: str, value: any):
        setattr(self, key, value)
        return
        
    # override config------------------------------------------
    def override(self, new_values: dict | None):
        
        if new_values == None:
            return
        for key, value in new_values.items():
            self.set_by_key(key, value)
            
        self.validate()
        return

#======================================================================
@dataclass
class LazyAxes:
    
    y : np.ndarray  # require
    plot_type: PLOT_TYPE_1D | PLOT_TYPE_2D | PLOT_TYPE_3D   #require
     
    title: str | None = None
    
    t : np.ndarray | None = None  
    labels: list[str] | None = None
    
    x_label: str = "x" 
    y_label: str = "y"
    x_lim: tuple[float|None, float|None] = (None, None)
    y_lim: tuple[float|None, float|None] = (None, None)
    
    color: list[str | tuple[int, int, int]] = field(default_factory=lambda: COLOR)
    alpha: float = 1
    line_style: list[str] = field(default_factory=lambda: LINE_STYLE)
    marker_style: list[str] = field(default_factory=lambda: MARKER_STYLE)
    linewidth: float = 2.0
    
    aspect: float | Literal["auto"] = "auto"
    invert_xaxis: bool = False
    invert_yaxis: bool = False
    
    def __post_init__(self):
        if self.t is not None:
            if self.t.shape != self.y.shape:
                raise ValueError(f"Invalid data. x and y must be same shape")
            
        if self.labels is not None:
            if self.y.shape[0] != len(self.labels):
                raise ValueError("labels must have same length as y")
        
        if isinstance(self.color, list) is False:
            self.color = [self.color]
        if isinstance(self.line_style, list) is False:
            self.line_style = [self.line_style]
        if isinstance(self.marker_style, list) is False:
            self.marker_style = [self.marker_style]
            