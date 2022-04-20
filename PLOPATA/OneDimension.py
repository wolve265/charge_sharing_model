import math
import numpy as np
from scipy.stats import norm
from scipy import special
import matplotlib.pyplot as plt


def calc_x0(PI, PIII, sig, pixel_dim):
    if PI > PIII:
        x0 = -sig * math.sqrt(2) * special.erfinv(2*PI - 1)
    else:
        x0 = sig * math.sqrt(2) * special.erfinv(2*PIII - 1) + pixel_dim
    return x0


pixel_dim = 100     # one pixel is 100um x 100um

mean = 70           #should be between 0 and a 100
sig  = 40
print(f"{mean=}")
print(f"{sig=}")
x = np.linspace(-pixel_dim, 2*pixel_dim, 3*pixel_dim + 1).tolist()
y = norm.pdf(x, mean, sig).tolist()

PI =   sum(y[x.index(-100) : x.index(0)])
PII =  sum(y[x.index(0)    : x.index(100)])
PIII = sum(y[x.index(100)  : x.index(200)])
print(f"{PI=}")
print(f"{PII=}")
print(f"{PIII=}")
print(f"{PI+PII+PIII=}")

x0 = calc_x0(PI, PIII, sig, pixel_dim)
print(f"{x0=}")

plt.title("1D charge distribution")
plt.plot(x, y)
plt.vlines(-100, 0, max(y), colors="black")
plt.vlines(0,    0, max(y), colors="black")
plt.vlines(100,  0, max(y), colors="black")
plt.vlines(200,  0, max(y), colors="black")
plt.vlines(mean        , 0, y[x.index(mean)],         colors="red",   label="mean")
plt.vlines(mean - 3*sig, 0, y[x.index(mean - 3*sig)], colors="green", label="+-3sig")
plt.vlines(mean + 3*sig, 0, y[x.index(mean + 3*sig)], colors="green")
plt.xlabel("x[um]")
plt.legend()
plt.show()
