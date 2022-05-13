import math
from scipy.stats import norm
from scipy import special
import numpy as np

import statistics as stat
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
N = E/Eeh[3]
sigN = math.sqrt(F*N)
nr_of_photons = 100

el_count_min = (N - 4*sigN).__floor__()
el_count_max = (N + 4*sigN).__floor__()
nr_of_el = np.linspace(el_count_min, el_count_max, el_count_max-el_count_min + 1)

error_function = []
stdev_function = []
for el_count in nr_of_el:
    hit_errors = []
    for iter in range(nr_of_photons):
        mod = Model(real_hit=real_hit, pixel_dim=pixel_dim, nr_of_el=el_count.__floor__())
        hit_errors.append((real_hit - mod.OneD_calc_hit()).__abs__())

    error_function.append(stat.mean(hit_errors))
    stdev_function.append(stat.stdev(hit_errors))

avg_error = stat.mean(error_function)
avg_std_error = stat.mean(stdev_function)
# ----------------------------------------------------------------------------------------------------------------------

fig, (ax2, ax3) = plt.subplots(1, 2)
fig.suptitle(f"Electron nr analysis for Silicon. μ={real_hit}, σ={mod.sigma}, pixel size={pixel_dim}\n "
             f"nr of iterations for each electron number = {nr_of_photons}")

# ax1.set_title("List of generated Electron Numbers")
# ax1.set(xlabel="Iteration nr", ylabel="Number of electrons")
# ax1.scatter(np.linspace(0, len(nr_of_el), len(nr_of_el)), nr_of_el, s=5)

ax2.set_title("Average detection error in gaussian range of electron generation")
ax2.set(xlabel="Number of electrons", ylabel="Average error [μm]")
ax2.scatter(nr_of_el, error_function, s=5)
ax2.hlines(avg_error, nr_of_el[0], nr_of_el[-1], colors="red", label="Average Error")
ax2.legend()

ax3.set_title("Average sigma of detection error in gaussian range of electron generation")
ax3.set(xlabel="Number of electrons", ylabel="Average error sigma [μm]")
ax3.scatter(nr_of_el, stdev_function, s=5)
ax3.hlines(avg_std_error, nr_of_el[0], nr_of_el[-1], colors="green", label="Average Error Sigma")
ax3.legend()

plt.show()