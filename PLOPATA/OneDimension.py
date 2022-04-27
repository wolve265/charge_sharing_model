import math
import numpy as np
from scipy.stats import norm
from scipy import special
import matplotlib.pyplot as plt


def calc_probabilities(y, pixel_dim):
    PI, PII, PIII = 0, 0, 0
    for i in y:
        if (-pixel_dim < i < 0):
            PI += 1
        elif (0 < i < pixel_dim):
            PII += 1
        elif (pixel_dim < i < 2*pixel_dim):
            PIII += 1
    return PI, PII, PIII


def OneD_calc_hit(real_hit_pos, electron_count, pixel_dim):
    sig = 35

    y = norm.rvs(real_hit_pos, sig, electron_count)

    PI, PII, PIII = calc_probabilities(y, pixel_dim)

    PSUM = PI + PII + PIII
    PI = PI / PSUM
    # PII = PII / PSUM
    PIII = PIII / PSUM

    if PI > PIII:
        x0 = -sig * math.sqrt(2) * special.erfinv(2*PI - 1)
    else:
        x0 = sig * math.sqrt(2) * special.erfinv(2*PIII - 1) + pixel_dim
    return x0, y

mean = 40
sig = 35
pixel_dim = 100

x0 , y= OneD_calc_hit(mean, 2200, pixel_dim)
print(f"{x0=}")

x = np.linspace(-pixel_dim, 2*pixel_dim, 3*pixel_dim + 1).tolist()

plt.title("1D charge distribution")
plt.hist(y, bins=len(x))
plt.vlines(-100, 0, y.max()/5,  colors="black")
plt.vlines(0,    0, y.max()/5,  colors="black")
plt.vlines(100,  0, y.max()/5,  colors="black")
plt.vlines(200,  0, y.max()/5,  colors="black")
plt.vlines(mean, 0, 20,         colors="red",   label="mean")
plt.vlines(mean - 3*sig, 0, 20, colors="green", label="+-3sig")
plt.vlines(mean + 3*sig, 0, 20, colors="green")
plt.xlabel("x[um]")
plt.legend()
plt.show()
