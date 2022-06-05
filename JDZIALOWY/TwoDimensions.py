# Importing the necessary modules
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal

plt.style.use('seaborn-dark')
plt.rcParams['figure.figsize'] = 14, 6
fig = plt.figure()

# Setting mean of the distribution
# to be at (0,0)
mean = np.array([0, 0])

# Storing density function values for
# further analysis
pdf_list = []

# Initializing the covariance matrix
cov = np.array([[1, 0], [0, 1]])

# Generating a meshgrid complacent with
# the 3-sigma boundary
mean_1, mean_2 = mean[0], mean[1]
sigma_1, sigma_2 = cov[0, 0], cov[1, 1]

x = np.linspace(-3 * sigma_1, 3 * sigma_1, num=100)
y = np.linspace(-3 * sigma_2, 3 * sigma_2, num=100)
X, Y = np.meshgrid(x, y)

# Generating the density function
# for each point in the meshgrid
pdf = np.zeros(X.shape)
for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        pdf[i, j] = multivariate_normal.pdf([X[i, j], Y[i, j]], cov=cov, mean=mean)

# Plotting the density function values
ax = fig.add_subplot(projection='3d')
ax.plot_surface(X, Y, pdf, cmap='viridis')
plt.xlabel("x1")
plt.ylabel("x2")
plt.title(f'Covariance between x1 and x2 = {0}')
pdf_list.append(pdf)
ax.axes.zaxis.set_ticks([])

plt.tight_layout()
plt.show()