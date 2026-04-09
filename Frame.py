from Panel import Panel
from Vortex import FlowVortex


class Frame:
    time: float
    panels: list[type[Panel]]
    vortices: list[FlowVortex]

    def __init__(self, time: float, panels: list[type[Panel]], vortices: list[FlowVortex]):
        self.time = time
        self.panels = panels
        self.vortices = vortices
