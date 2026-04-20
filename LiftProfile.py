from matplotlib import pyplot as plt

from Frame import Frame
from Solver import PanelMethodSolver, flapping_plate_generator

# Study Setup
solver = PanelMethodSolver(flapping_plate_generator)
solver.dt = 0.01
n_list = [25, 50, 75]
frames: list[Frame] = []
for n in n_list:
    solver.n_panels = n
    frames = solver.simulate((0, 5))

    time = []
    c_l = []

    for frame in frames[1::]:
        time.append(frame.time)
        c_l.append(frame.lift_coeff())

    plt.plot(time, c_l, label=f"n={solver.n_panels}")
plt.xlabel("Time, t")
plt.ylabel("Lift Coefficient, c_L")
plt.legend()
plt.savefig("Results/LiftProfile.png")
plt.show()

frames[-1].display()
plt.savefig("Results/Wake.png")
plt.show()
