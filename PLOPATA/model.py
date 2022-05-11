import math
from scipy.stats import norm
from scipy import special
import numpy as np

import matplotlib.pyplot as plt


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


real_hit = 35
pixel_dim = 75
# nr_of_el = 2200

E = 8000                        # 8keV
Eeh = [3.62, 4.2, 4.43, 4.6]    # Electron-hole pair generation energy [Si, GaAs, CdTe, CZT]
F = 0.1
N = E/Eeh[0]
sigN = math.sqrt(F*N)
nr_of_photons = 2000

nr_of_el = norm.rvs(N, sigN, nr_of_photons)
nr_of_el.sort()

avg_error = 0
error_function = []
for el_count in nr_of_el:
    mod = Model(real_hit=real_hit, pixel_dim=pixel_dim, nr_of_el=el_count.__floor__())
    error_function.append((mod.real_hit - mod.OneD_calc_hit()).__abs__())
    avg_error += error_function[-1]
avg_error = avg_error/nr_of_photons


plt.title(f"{nr_of_photons} photons hit at {real_hit}")
plt.scatter( np.linspace(0, len(error_function), len(error_function)), error_function, s=5)
plt.hlines(avg_error, 0, nr_of_photons, colors="red", label="average error")
plt.xlabel("Iteration")
plt.ylabel("|real_hit - calculated_hit|")
plt.legend()
plt.show()

# plt.title(f"1D charge distribution.\n Real hit at {mod1.real_hit}um. Calculated hit at {x0:.3f}um")
# plt.hist(mod1.charge_distribution, bins=len(mod1.pixel_coordinates))
# plt.vlines(-mod1.pixel_dim,   0, 30,  colors="black")
# plt.vlines(0,                 0, 30,  colors="black")
# plt.vlines(mod1.pixel_dim,    0, 30,  colors="black")
# plt.vlines(2*mod1.pixel_dim,  0, 30,  colors="black")
# plt.vlines(mod1.real_hit,                0, 15,         colors="red",   label="hit position")
# plt.vlines(mod1.real_hit - 3*mod1.sigma, 0, 15, colors="green", label="+-3sig")
# plt.vlines(mod1.real_hit + 3*mod1.sigma, 0, 15, colors="green")
# plt.xlabel("x[um]")
# plt.ylabel("nr of electrons")
# plt.legend()
# plt.show()
