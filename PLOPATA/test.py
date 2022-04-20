import math
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt


# x = range(-10, 10, 2)
x1 = np.linspace(0, 9, 10)
x2 = np.linspace(0, 9, 10)

X, Y = np.meshgrid(x1, x2)
print(X)
# plt.plot(x, y)
# plt.show()