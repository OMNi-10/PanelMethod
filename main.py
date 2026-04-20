
from matplotlib import pyplot as plt

n_p = [25, 50, 100, 200, 400, 800]
c_l = [7.908, 2.134, -0.904, -1.508, -1.239, -0.761]

eta = []

for i in range(1, len(n_p)):
    eta.append(abs((c_l[i] - c_l[i-1]) / c_l[i-1]) * 100)

plt.scatter(n_p[1::], eta)
plt.plot([min(n_p[1::]), max(n_p[1::])], [2, 2], c="silver")
plt.xscale('log')
plt.xlabel("Number of Panels, n")
plt.ylabel("Percent Change from Previous Iteration")
plt.ylim([0, 150])
plt.show()