from operator import truediv

import numpy as np
from matplotlib import pyplot as plt

from Frame import Frame
from Panel import Panel, points_to_panels
from Structure import Structure
from utils import normal_vector, projection_coef
from Vortex import FlowVortex


def flat_plate_generator(time: float, n: int) -> list[type[Panel]]:
    positions = np.linspace([0,0], [1, -0.4], n+1)
    panels = points_to_panels(positions)
    return panels

structure = Structure(flat_plate_generator)
n: int = 100
dt = 0.01
frames: list[Frame] = []

flow_velocity = np.array([-1, 0])

vortex_shedding = True
shedding_distance = 0.1

flow_vortices: list[FlowVortex] = []

time = 0
while time < 2:
    print("time: ", time)
    # Move flow vortices
    n_vortex = len(flow_vortices)
    vortex_velocities = [None] * n_vortex
    for i in range(n_vortex):
        u = 0
        eval_loc = flow_vortices[i].position
        for j in range(n_vortex):
            if i == j:
                continue
            vortex_loc = flow_vortices[j].position
            a_ij = projection_coef(vortex_loc, eval_loc)
            u += flow_vortices[j].circulation * a_ij
        vortex_velocities[i] = u - flow_velocity

    for i in range(n_vortex):
        flow_vortices[i].position = flow_vortices[i].position + vortex_velocities[i] * dt

    structure.discretize(time, n)

    # Solve for circulations
    if not vortex_shedding:
        A = np.zeros([n, n])
        b = np.zeros([n, 1])
    else:
        A = np.zeros([n+1, n+1])
        b = np.zeros([n+1, 1])

    for panel_ind in range(n):
        panel = structure.panels[panel_ind]
        colloc_loc = panel.collocation_location
        norm_i = panel.normal_vector

        # Construct A matrix
        for vortex_ind in range(n):
            vortex_loc = structure.panels[vortex_ind].vortex_location

            proj_ij = projection_coef(vortex_loc, colloc_loc)
            A[panel_ind, vortex_ind] = np.linalg.vecdot(norm_i, proj_ij)
        # Factor in shedding vortex
        if vortex_shedding:
            vortex_loc = panel.end + shedding_distance * (panel.end - panel.start)
            proj_ij = projection_coef(vortex_loc, colloc_loc)
            A[panel_ind, n] = np.linalg.vecdot(norm_i, proj_ij)

        # Construct B matrix
        b[panel_ind, 0] = np.linalg.vecdot(norm_i, flow_velocity)

    if vortex_shedding:
        A[n, :] = 1
        b[n, 0] = - sum([vortex.circulation for vortex in flow_vortices])

    circulations = np.linalg.solve(A, b)

    if vortex_shedding:
        shed_vortex = FlowVortex(vortex_loc, circulations[-1, 0])
        flow_vortices.insert(0, shed_vortex)

    # print("\nA")
    # print(A)
    # print("\nb")
    # print(b)
    # print("\nG")
    # print(circulations)

    # Save frame
    for panel_ind in range(n):
        panel = structure.panels[panel_ind]
        panel.vortex_circulation = circulations[panel_ind]
    frames.append(Frame(
        time = time,
        panels = structure.panels,
        vortices = flow_vortices
    ))
    time += dt

structure.display()
for vortex in flow_vortices:
    plt.scatter(vortex.position[0], vortex.position[1], marker="x", c="black")
plt.axis('equal')
plt.show()