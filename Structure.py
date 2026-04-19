import matplotlib.pyplot as plt
import numpy as np

from typing import Callable
from Panel import Panel

class Structure:
    panels: list[type[Panel]]
    generator: Callable[[float, int], list[type[Panel]]]  # A function which returns N panels approximating the structure.

    def __init__(self, generator: Callable[[float, int], list[type[Panel]]]) -> None:
        self.generator = generator

    def discretize(self, time: float, n: int):
        self.panels = self.generator(time, n)
        return self.panels

    def display(self, **kwargs):
        for panel in self.panels:
            panel.display(**kwargs)
            # plt.scatter(panel.collocation_location[0], panel.collocation_location[1], c="black", marker="s")
            # plt.scatter(panel.vortex_location[0], panel.vortex_location[1], c="black", marker="x")