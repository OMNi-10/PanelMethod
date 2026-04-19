import os

from matplotlib import pyplot as plt
import numpy as np

from Panel import Panel
from Vortex import FlowVortex


class Frame:
    time: float
    panels: list[Panel]
    vortices: list[FlowVortex]

    def __init__(self, time: float, panels: list[Panel], vortices: list[FlowVortex]):
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

    def lift_coeff(self, u: float = 1):
        L = 0
        for panel in self.panels:
            L += panel.vortex_circulation
        return 2 * L / u


def saveFrames(directory: str, frames: list[Frame]):
    if not os.path.exists(directory):
        os.makedirs(directory)

    for i in range(len(frames)):
        frame = frames[i]

        csv_name = f"{directory}/Frame_#{i:05}.csv"
        with open(csv_name, "w") as f:
            f.write(f"time:, {frame.time}\n")
            f.write(f"panel_start_X, panel_start_Y, panel_end_X, panel_end_Y, panel_vortex_distance, panel_vortex_circulation, flow_vortex_X, flow_vortex_Y, flow_vortex_simulation\n")

            n_panels = len(frame.panels)
            n_vortex = len(frame.vortices)

            for i in range(max(n_panels, n_vortex)):
                line = ""
                if i < n_panels:
                    panel: Panel = frame.panels[i]
                    line += f"{panel.start[0]}, {panel.start[1]}, {panel.end[0]}, {panel.end[1]}, {panel.vortex_distance}, {panel.vortex_circulation}, "
                else:
                    line += ","*6

                if i < n_vortex:
                    vortex: FlowVortex = frame.vortices[i]
                    line += f"{vortex.position[0]}, {vortex.position[1]}, {vortex.circulation}"
                else:
                    line += ","*2

                f.write(f"{line}\n")

