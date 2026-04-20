
import numpy as np
from matplotlib import pyplot as plt
from typing import Callable

from Frame import Frame
from Panel import Panel, points_to_panels
from Structure import Structure
from Vortex import Vortex, FlowVortex
from utils import projection_coef


class PanelMethodSolver:
    n_panels: int = 25
    dt = 0.01

    structure_generator: Callable[[float, int], type[np.array]]
    structure_velocity: type[np.array] = np.array([10, 0])
    shedding_distance: float = 0.01


    def __init__(self, structure_generator: Callable[[float, int], type[np.array]]):
        self.structure_generator = structure_generator

    def simulate(self, time: float | tuple[float, float]) -> list[Frame]:
        if time is float:
            t_i = 0
            t_f = time
        else:
            t_i, t_f = time
        print(f"Starting simulation: n = {self.n_panels}, dt = {self.dt}", end = " ... ")
        structure = Structure(self.structure_generator)
        initial_frame = Frame(
            time[0] - self.dt,
            structure.discretize(time[0] - self.dt, self.n_panels),
            []
        )
        frames = [initial_frame]
        while frames[-1].time <= time[1]:
            frames.append(self.step(frames[-1]))
        print("Done!")
        return frames

    def step(self, prev_frame: Frame) -> Frame:
        """
        Returns the following frame.
        """

        # --- PROPAGATING FLOW FIELD ---
        # Calculating velocity field at each POI
        flow_vortices = prev_frame.vortices.copy()
        n_vortex = len(flow_vortices)
        n_panels = len(prev_frame.panels)

        if n_vortex != 0:
            vortex_velocities: list[type[np.array]] = [None] * n_vortex
            for i in range(n_vortex):
                induced_velocity = np.array([0.0, 0.0])
                eval_loc = flow_vortices[i].position
                # Iterate over all shed vortices
                for j in range(n_vortex):
                    if i == j:
                        continue
                    vort_loc = flow_vortices[j].position
                    a_ij = projection_coef(vort_loc, eval_loc)
                    induced_velocity += flow_vortices[j].circulation * a_ij

                # Iterate over all structure vortices
                for k in range(n_panels):
                    vort_loc = prev_frame.panels[k].vortex_location
                    a_ij = projection_coef(vort_loc, eval_loc)

                    induced_velocity += prev_frame.panels[k].vortex_circulation * a_ij

                # Combine all flow velocities
                vortex_velocities[i] = - induced_velocity + self.structure_velocity

            # Updating Vortex Position
            for i in range(n_vortex):
                flow_vortices[i].position += vortex_velocities[i] * self.dt

        # --- SETUP TIMESTEP PROPERTIES ---
        time = prev_frame.time + self.dt
        structure = Structure(self.structure_generator)
        panels = structure.discretize(time, self.n_panels)


        # --- SOLVE FOR CIRCULATIONS ---
        # Initializing matrices
        A = np.zeros([self.n_panels + 1, self.n_panels + 1])
        B = np.zeros([self.n_panels + 1, 1])

        # Setup panel equations
        for i in range(self.n_panels):
            panel: Panel = panels[i]
            colloc_loc = panel.collocation_location
            norm_i = panel.normal_vector

            # Fill in row of A-matix
            # ToDo: Refactor into reduce copied code
            for j in range(self.n_panels):
                vort_loc = panels[j].vortex_location
                a_ij = projection_coef(vort_loc, colloc_loc)
                A[i, j] = np.linalg.vecdot(norm_i, a_ij)
            vort_loc = panel.end + self.shedding_distance * (panel.end - panel.start)
            a_ij = projection_coef(vort_loc, colloc_loc)
            A[i, self.n_panels] = np.linalg.vecdot(norm_i, a_ij)

            # Set B value
            B[i, 0] = np.linalg.vecdot(norm_i, self.structure_velocity + panel.collocation_velocity)

        # Setup shed vortex equation
        A[self.n_panels, :] = 1
        B[self.n_panels, 0] = - sum([vortex.circulation for vortex in prev_frame.vortices])

        # --- SOLVE FOR CIRCULATIONS ---
        circulations = np.linalg.solve(A, B)
        for i in range(n_panels):
            panels[i].vortex_circulation = circulations[i]

        # --- SAVE FRAME ---
        # Add shed vortex
        shed_vortex_loc = panels[-1].end + self.shedding_distance * (panels[-1].end - panels[0].start)
        shed_vortex = FlowVortex(shed_vortex_loc, circulations[-1, 0])

        # Create flow_vortex list
        flow_vortices = []
        flow_vortices.append(shed_vortex)
        for vortex in prev_frame.vortices:
            flow_vortices.append(FlowVortex(vortex.position, vortex.circulation))

        # Create and return frame
        return Frame(time, panels, flow_vortices)

def flat_plate_generator(time: float, n: int) -> list[type[Panel]]:
    positions = np.linspace([0,0], [1, -0.4], n+1)
    panels = points_to_panels(positions)
    return panels

def flapping_plate_generator(time: float, n: int) -> list[type[Panel]]:
    alpha = -0.75 * np.sin(2 * np.pi * time)
    start = [0, 0]
    end = [np.cos(alpha), np.sin(alpha)]
    v_start = [0, 0]
    v_end = [-np.sin(alpha), np.cos(alpha)]

    positions = np.linspace(start, end, n + 1)
    velocities = np.linspace(v_start, v_end, n + 1)
    panels = points_to_panels(positions, velocities)
    return panels

if __name__ == "__main__":
    from Frame import saveFrames

    solver = PanelMethodSolver(flapping_plate_generator)
    solver.n_panels = 25
    frames = solver.simulate((0, 5))

    print(frames[-1].lift_coeff(10))

    frames[-1].display()
    plt.title(f"Simulation of flapping plate, n = {solver.n_panels}, C_l = {frames[-1].lift_coeff()}")
    plt.savefig(f"Results/SolverTest/{solver.n_panels:05}_panels.png")
    plt.show()

    directory = "Results/SolverTest"
    saveFrames(directory, frames)
