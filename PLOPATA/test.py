# Necessary imports for model to work
import math
from scipy.stats import norm
from scipy import special
import numpy as np


# Model code
class Model:
    def __init__(self, real_hit, pixel_dim, nr_of_el):
        # Input Parameters
        self.real_hit = real_hit
        self.pixel_dim = pixel_dim
        self.nr_of_el = nr_of_el
        self.sigma = pixel_dim * 0.35
        # charge_distribution holds coordinates at which the electron was detected
        self.charge_distribution = sorted(norm.rvs(self.real_hit, self.sigma, self.nr_of_el))
        self.pixel_coordinates = (np.linspace(-self.pixel_dim, 2 * self.pixel_dim, 3 * self.pixel_dim + 1)).tolist()
        # Output Data
        self.PI, self.PII, self.PIII = self.calc_probabilities(
            self.charge_distribution, self.pixel_dim)
        self.calc_hit = self.OneD_calc_hit(self.PI, self.PII, self.PIII,
                                           self.sigma, self.pixel_dim)
        self.calc_hit_int = self.OneD_calc_hit_int(self.PI, self.PII, self.PIII,
                                           self.sigma, self.pixel_dim)

    def calc_probabilities(self, charge_distribution, pixel_dim):
        PI, PII, PIII = 0, 0, 0
        for i in charge_distribution:
            if -pixel_dim < i < 0:
                PI += 1
            elif 0 < i < pixel_dim:
                PII += 1
            elif pixel_dim < i < 2 * pixel_dim:
                PIII += 1
        return PI, PII, PIII

    def OneD_calc_hit(self, PI, PII, PIII, sigma, pixel_dim):
        PSUM = PI + PII + PIII
        PI = PI / PSUM
        # PII = PII / PSUM
        PIII = PIII / PSUM

        if PI > PIII:
            x0 = -sigma * math.sqrt(2) * special.erfinv(2 * PI - 1)
        else:
            x0 = sigma * math.sqrt(2) * special.erfinv(2 * PIII - 1) + pixel_dim
        return x0

    def OneD_calc_hit_int(self, PI, PII, PIII, sigma, pixel_dim):
        # pixel_dim * 0.35
        PSUM = PI + PII + PIII
        PI = (100 * (PI / PSUM)).__floor__()  # Probabilty in %
        # PII = PII / PSUM
        PIII = (100 * (PIII / PSUM)).__floor__()  # Probability in %

        if PI > PIII:
            x0 = (((-sigma * 100).__floor__() * (math.sqrt(2) * 100).__floor__() * (
                        special.erfinv(2 * (PI / 100) - 1) * 100).__floor__()) / 1000000).__floor__()
        else:
            x0 = (((sigma * 100).__floor__() * (math.sqrt(2) * 100).__floor__() * (
                        special.erfinv(2 * (PIII / 100) - 1) * 100).__floor__() + (
                               pixel_dim * 1000000)) / 1000000).__floor__()
        return x0
