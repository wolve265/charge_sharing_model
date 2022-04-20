import math
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt


# x = range(-10, 10, 2)
x = np.linspace(0, 9, 10).tolist()
y = []
for i in x:
    y.append(i*2 + 3)

print(f"{y[x.index(4)]}")
# plt.plot(x, y)
# plt.show()