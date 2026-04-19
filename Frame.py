from matplotlib import pyplot as plt
import numpy as np

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

    def display(self, **kwargs):
        for panel in self.panels:
            panel.display(**kwargs)

        X = []
        Y = []
        G = []
        for vortex in self.vortices:
            X.append(vortex.position[0])
            Y.append(vortex.position[1])
            G.append(vortex.circulation)
        plt.scatter(X, Y, 10, G, cmap="bwr")
        plt.axis('equal')
        plt.show()

    def lift_coeff(self, u: float = 1):
        L = 0
        for panel in self.panels:
            L += panel.vortex_circulation
        return 2 * L / u
