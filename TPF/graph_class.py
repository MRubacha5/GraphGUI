from dataclasses import dataclass, field
from typing import List

@dataclass
class GraphClass:
    title: str = "Graph 1"
    x_label: str = "X-axis"
    y_label: str = "Y-axis"
    x_scale: str = "linear"
    y_scale: str = "linear"
    addGrid: bool = True
    findMax: bool = False
    findMin: bool = False
    scaleFactor: float = 1
    displacementFactor: float = 0
    colors: list = field(default_factory=lambda: ['r', 'b', 'g', 'y'])
    visibility: List[bool] = field(default_factory=lambda: [True, True, True, True])