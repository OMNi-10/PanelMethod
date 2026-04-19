import numpy as np
import matplotlib.pyplot as plt

from utils import normal_vector
from Vortex import PanelVortex

def check_vector(vector: type[np.array]):
    assert(vector.size == 2)


class Panel:
    start: type[np.array] = None
    end: type[np.array] = None

    v_start: type[np.array] = None
    v_end: type[np.array] = None

    normal_vector: type[np.array]

    vortex_distance: float = 0.25
    collocation_distance: float = 0.75
    vortex_circulation: float

    def __init__(self, start, end, v_start = None, v_end = None):
        self.start = start
        self.end = end

        if v_start is None:
            self.v_start = np.array([0, 0])
        else:
            self.v_start = v_start

        if v_end is None:
            self.v_end = np.array([0, 0])
        else:
            self.v_end = v_end

        self._set_normal_vector()

    def _set_start(self, start):
        check_vector(start)
        self.start = start
        self._set_normal_vector()

    def _set_end(self, end):
        check_vector(end)
        self.end = end
        self._set_normal_vector()

    def _set_normal_vector(self):
        self.normal_vector = normal_vector(self.start, self.end)
        return

    @property
    def vortex_location(self) -> type[np.array]:
        return self.start + self.vortex_distance * (self.end - self.start)

    @property
    def collocation_location(self) -> type[np.array]:
        return self.start + self.collocation_distance * (self.end - self.start)

    @property
    def vortex_velocity(self) -> type[np.array]:
        return self.v_start + self.vortex_distance * (self.v_end - self.v_start)

    @property
    def collocation_velocity(self) -> type[np.array]:
        return self.v_start + self.collocation_distance * (self.v_end - self.v_start)

    def display(self, **kwargs):
        X = [self.start[0], self.end[0]]
        Y = [self.start[1], self.end[1]]
        plt.plot(X, Y, **kwargs)

def points_to_panels(points: type[np.array], velocities: type[np.array] = None) -> list[type[Panel]]:
    panels = []
    for i in range(points.shape[0]-1):
        if velocities is None:
            panels.append(Panel(points[i,:], points[i+1,:]))
        else:
            panels.append(Panel(points[i,:], points[i+1,:], velocities[i,:], velocities[i+1,:]))
    return panels


if __name__ == "__main__":
    start = np.array([0, 0])
    end = np.array([10, -10])
    test_panel = Panel(start, end)

    print(test_panel.normal_vector)