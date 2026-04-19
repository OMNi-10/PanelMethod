import numpy as np


def normal_vector(start: type[np.array], end: type[np.array]) -> type[np.array]:
    mag = np.linalg.norm(end - start)
    vec = np.array([
        -(end[1] - start[1]),
        (end[0] - start[0])
    ]) / mag
    return vec

def projection_coef(eval_pos: type[np.array],vortex_loc : type[np.array]) -> type[np.array]:
    norm = normal_vector(vortex_loc, eval_pos)
    disp = vortex_loc - eval_pos
    proj_coef = norm / (2 * np.pi * np.linalg.norm(disp))
    return proj_coef
