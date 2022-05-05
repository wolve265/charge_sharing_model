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


def OneD_calc_hit(mean, electron_count, pixel_dim):
    sig = 35

    y = norm.rvs(mean, sig, electron_count)

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

mean = 95
sig = 35
electron_count = 2200
pixel_dim = 100

x0, y = OneD_calc_hit(mean, electron_count, pixel_dim)
x = np.linspace(-pixel_dim, 2*pixel_dim, 3*pixel_dim + 1)
print(f"{x0=}")

plt.title(f"1D charge distribution.\n Real hit at {mean}um. Calculated hit at {x0:.3f}um")
plt.hist(y, bins=len(x))
plt.vlines(-100, 0, 30,  colors="black")
plt.vlines(0,    0, 30,  colors="black")
plt.vlines(100,  0, 30,  colors="black")
plt.vlines(200,  0, 30,  colors="black")
plt.vlines(mean, 0, 15,         colors="red",   label="hit position")
plt.vlines(mean - 3*sig, 0, 15, colors="green", label="+-3sig")
plt.vlines(mean + 3*sig, 0, 15, colors="green")
plt.xlabel("x[um]")
plt.ylabel("nr of electrons")
plt.legend()
plt.show()

