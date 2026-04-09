
# Project 4

For this project, you ill need to adapt the unsteady panel method code provided by Guest Lecturer Tianjun Han to simulate a rel-world engineering problem. The code provided is MATLAB code, but feel free to convert to a different language if you'd prefer. You are free to choose the problem to simulate. Examples include the accelerating or decelerating of a foil with a fixed angle of attack, periodically pitching or heaving of a foil, a foil ith a fixed angle of attack gliding toards the groun, and so on.

If your foil has a periodical motion, nondimensionalize time by $t^* = t/T$, where $t$ is time, $T$ is the period. If your foil has a non-periodic motion, nondimensionalize time by $t^*=tU_0/c$, where $t$ is the time, $U_0$ is the intitial speed of the foil, and $c$ is the chord of the foil. Simulate the time from $t^*=0$ to $5$. Additionally, set your time step $\Delta t^* = 0.01$.

1. Describe the problem you simulate and how this problem is related to real world engineering problem.
2. Conduct a convergence study on the number of panels, $N_p$. Start from $N_p=25$, then double $N_p$ until the lift of the foil changes by less than $2\%$. To be more specific, you ill find that there is a value of $N_p=x$ where the lift of the foil changes by less than $2\%$ after you increase the number of panels from $x$ to $2x$. Plot the lift coefficient $C_L = L/(0.5 \rho U^2 c), versus $t^*$ for $N_p =x$, $N_p =x/2$, $N_p =x/4$ on the same figure (Figure 1).
3. Describe the trend of the lift coefficient with the foil's motion in Figure 1.
Plot the foil and the wke vortices at the last time step of your simulation (Figure 2). Use a color legend to distinguish the strength and sign of the wke vortices. Show the color legend in Figure 2.
5. Submit a document that contains the answers to questions 1 to 4 along with your source code.