from matplotlib import pyplot as plt

from Frame import Frame, saveFrames
from Solver import PanelMethodSolver, flapping_plate_generator

# Study Setup
solver = PanelMethodSolver(flapping_plate_generator)
solver.dt = 0.01
time = 3
num_p = []
coeff = []

def run():
    print(f"starting n={solver.n_panels}", end=" ... ")
    frames = solver.simulate((0, time))

    directory = f"Results/ConvergenceStudy/panel_count_{solver.n_panels:06}"
    saveFrames(directory, frames)

    num_p.append(solver.n_panels)
    coeff.append(frames[-1].lift_coeff(10))

    plt.close("all")
    frames[-1].display()
    plt.title(f"Simulation of flapping plate, n = {solver.n_panels}, C_l = {frames[-1].lift_coeff()}")
    plt.savefig(f"Results/ConvergenceStudy/{solver.n_panels:05}_panels.png")
    plt.show(block=False)
    plt.pause(0.1)

    print("Done!")

# First Seed
solver.n_panels = 25
run()

# Second Seed
solver.n_panels *= 2
run()

# Iteration
while abs((coeff[-1] - coeff[-2]) / coeff[-2]) > 0.2:
    print(abs((coeff[-1] - coeff[-2]) / coeff[-2]))
    solver.n_panels *= 2
    run()
print(f"Converged!!! {abs((coeff[-1] - coeff[-2]) / coeff[-2])}")

Y = []
for i in range(1, len(num_p)):
    Y.append(abs((coeff[i] - coeff[i-1])/coeff[i-1]))
plt.plot([min(num_p), max(num_p)], [2e-2, 2e-2], color="silver")
plt.scatter(num_p[1::], Y, color="darkcyan")
plt.xscale('log')
plt.xlabel('Number of panels, n')
plt.ylabel('Change in List Coefficient')
plt.show()