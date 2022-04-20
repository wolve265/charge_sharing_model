import math
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

mean = 72
sig  = 40
pixel_dim = 100
x = np.linspace(-pixel_dim, 2*pixel_dim, 3*pixel_dim + 1).tolist()
y = norm.pdf(x, mean, sig).tolist()


plt.title("Normal distribution")
plt.plot(x, y)
plt.vlines(mean, 0, y[x.index(mean)], colors="black", label="mean")
plt.vlines(mean - sig,   0, y[x.index(mean -   sig)], colors="red", label="+-sig")
plt.vlines(mean + sig,   0, y[x.index(mean +   sig)], colors="red")
plt.vlines(mean - 2*sig, 0, y[x.index(mean - 2*sig)], colors="red")
plt.vlines(mean + 2*sig, 0, y[x.index(mean + 2*sig)], colors="red")
plt.vlines(mean - 3*sig, 0, y[x.index(mean - 3*sig)], colors="red")
plt.vlines(mean + 3*sig, 0, y[x.index(mean + 3*sig)], colors="red")
plt.legend()
plt.show()
