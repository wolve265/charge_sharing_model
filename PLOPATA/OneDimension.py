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
    return x0


# mean = 1
# sig = 35
electron_count = 2200
pixel_dim = 100
avg_nr = 50

err = []
for i in range(1, 100, 1):
    x_sum = 0
    mean = i
    for j in range(avg_nr):
        x_temp = OneD_calc_hit(mean, electron_count,  pixel_dim)
        x_sum += x_temp
    x_avg = x_sum/avg_nr
    err.append(abs(x_avg - mean))

x = np.linspace(1, 100, 99).tolist()

plt.title("Average error vs hit position")
plt.scatter(x, err)
plt.xlabel("x[um]")
plt.ylabel("avg error[um]")
# plt.legend()
plt.show()

# plt.title("1D charge distribution")
# plt.hist(y, bins=len(x))
# plt.vlines(-100, 0, y.max()/5,  colors="black")
# plt.vlines(0,    0, y.max()/5,  colors="black")
# plt.vlines(100,  0, y.max()/5,  colors="black")
# plt.vlines(200,  0, y.max()/5,  colors="black")
# plt.vlines(mean, 0, 20,         colors="red",   label="mean")
# plt.vlines(mean - 3*sig, 0, 20, colors="green", label="+-3sig")
# plt.vlines(mean + 3*sig, 0, 20, colors="green")
# plt.xlabel("x[um]")
# plt.legend()
# plt.show()
