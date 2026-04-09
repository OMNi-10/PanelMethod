
import numpy as np

from utils import normal_vector


class Vortex:
    position: type[np.array]
    circulation: float

class PanelVortex(Vortex):
    position: type[np.array]
    circulation: float

class FlowVortex(Vortex):
    position: type[np.array]
    circulation: float

    def __init__(self, position: type[np.array], circulation: float):
        self.position = position
        self.circulation = circulation