# Necessary imports for model to work
import math
from scipy.stats import norm
from scipy import special
import numpy as np


# Imports for model testing
import matplotlib.pyplot as plt
from matplotlib import cm, projections


# Model code
class Model:
    def __init__(self, real_hit, pixel_dim, nr_of_el, list_size):
        self.real_hit = real_hit
        self.pixel_dim = pixel_dim
        self.nr_of_el = nr_of_el
        self.list_size = list_size
        self.sigma = pixel_dim * 0.35
        self.charge_distribution = norm.rvs(self.real_hit, self.sigma, self.nr_of_el)
        self.pixel_coordinates = np.linspace(-self.pixel_dim, 2 * self.pixel_dim, 3 * self.pixel_dim + 1)

    def calc_probabilities(self):
        PI, PII, PIII = 0, 0, 0
        for i in self.charge_distribution:
            if -self.pixel_dim < i < 0:
                PI += 1
            elif 0 < i < self.pixel_dim:
                PII += 1
            elif self.pixel_dim < i < 2 * self.pixel_dim:
                PIII += 1
        return PI, PII, PIII

    def OneD_calc_hit(self):
        # pixel_dim * 0.35
        PI, PII, PIII = self.calc_probabilities()
        PSUM = PI + PII + PIII
        PI = PI / PSUM
        # PII = PII / PSUM
        PIII = PIII / PSUM
        gauss_list, bin_size = self.create_gauss_list()
        index = 0
        if PI > PIII:
            while(PI < gauss_list[index]) :
                index += 1
            x_gauss = index*bin_size
            # x0 = -self.sigma * math.sqrt(2) * special.erfinv(2 * PI - 1)
        else:
            while(PIII < gauss_list[index]) :
                index += 1
            x_gauss = self.pixel_dim - index*bin_size
            # x0 = self.sigma * math.sqrt(2) * special.erfinv(2 * PIII - 1) + self.pixel_dim
        return x_gauss

    def create_gauss_list(self) :
        y = []
        pixel_bins = np.linspace(0, self.pixel_dim, self.list_size) # podzial pixela na czesci
        pixel_bin_size = pixel_bins[1] - pixel_bins[0] # najmniejszy krok podzialu
        cdf = norm.cdf(pixel_bins, 0, self.sigma) # dystrybuanta

        for i in range(len(pixel_bins)) :
            y.append(1 - cdf[i])

        return y, pixel_bin_size

# Model testing
real_hit = 22
pixel_dim = 75
nr_of_el = 2200
# results = []
# x = []
# positions = []
X = []
Y = []
Z = []
for real_hit in range(60,61,1) :
    results = []
    x = []
    positions = []
    positions.append(real_hit)
    for i in range(5, 200, 1) :
        x_mean = 0
        for j in range(20) :
            mod = Model(real_hit=real_hit, pixel_dim=pixel_dim, nr_of_el=nr_of_el, list_size=i)
            x0 = mod.OneD_calc_hit()
            x_mean += x0
        x_mean = x_mean/20
        x.append(i)
        results.append(abs(real_hit-x_mean))
        print("Size: ", i, " Calculated position: ", x_mean)
    X.append(positions)
    Y.append(x)
    Z.append(results)

# Z = np.array(Z)
# ax = plt.gca(projection="3d")
# ax.plot_wireframe(X, Y, Z)
# ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,linewidth=0, antialiased=False)
# ax.set_xlabel("Hit position")
# ax.set_ylabel("Size of array")
# ax.set_zlabel("Error")
# plt.show()

plt.plot(x, results)
plt.title(f"Error for hit at {real_hit} um")
plt.xlabel("Size of array")
plt.ylabel("Error")
plt.show()

# plt.title(f"1D charge distribution for hit at {real_hit}, with σ={mod.sigma}")
# plt.hist(mod.charge_distribution, bins=mod.pixel_coordinates)
# plt.vlines(   mod.real_hit, 0, 20, colors="red", label="Real Hit")
# plt.vlines( -mod.pixel_dim, 0, 40, colors="black")
# plt.vlines(              0, 0, 40, colors="black")
# plt.vlines(  mod.pixel_dim, 0, 40, colors="black")
# plt.vlines(2*mod.pixel_dim, 0, 40, colors="black")
# plt.legend()
# plt.show()