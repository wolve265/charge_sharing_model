# Necessary imports for model to work
import math
from scipy.stats import norm
from scipy import special
import numpy as np


# Imports for model testing
import matplotlib.pyplot as plt


# Model code
class Model:
    def __init__(self, real_hit, pixel_dim, nr_of_el):
        self.real_hit = real_hit
        self.pixel_dim = pixel_dim
        self.nr_of_el = nr_of_el
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

        if PI > PIII:
            x0 = -self.sigma * math.sqrt(2) * special.erfinv(2 * PI - 1)
        else:
            x0 = self.sigma * math.sqrt(2) * special.erfinv(2 * PIII - 1) + self.pixel_dim
        return x0


# Model testing
real_hit = 35
pixel_dim = 75
nr_of_el = 2200

mod = Model(real_hit=real_hit, pixel_dim=pixel_dim, nr_of_el=nr_of_el)
x0 = mod.OneD_calc_hit()

plt.title(f"1D charge distribution for hit at {real_hit}, with σ={mod.sigma}")
plt.hist(mod.charge_distribution, bins=mod.pixel_coordinates)
plt.vlines(   mod.real_hit, 0, 20, colors="red", label="Real Hit")
plt.vlines( -mod.pixel_dim, 0, 40, colors="black")
plt.vlines(              0, 0, 40, colors="black")
plt.vlines(  mod.pixel_dim, 0, 40, colors="black")
plt.vlines(2*mod.pixel_dim, 0, 40, colors="black")
plt.legend()
plt.show()