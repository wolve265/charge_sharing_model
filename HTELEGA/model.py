# Necessary imports for model to work
import math
from scipy.stats import norm
from scipy import special
import numpy as np


# Model code
class Model:
    # Creation of a model is equivalent to generating a hit.
    def __init__(self, real_hit, pixel_dim, nr_of_el):
        # Input Parameters
        self.real_hit = real_hit
        self.pixel_dim = pixel_dim
        self.nr_of_el = nr_of_el
        self.sigma = pixel_dim * 0.35
        # charge_distribution holds coordinates at which the electron was detected
        self.charge_distribution = norm.rvs(self.real_hit, self.sigma, self.nr_of_el)
        self.pixel_coordinates = (np.linspace(-self.pixel_dim, 2 * self.pixel_dim, 3 * self.pixel_dim + 1)).tolist()
        # Output Data
        self.PI, self.PII, self.PIII = self.calc_probabilities()

    def regenerate_hit(self, real_hit, pixel_dim, nr_of_el):
        self.real_hit = real_hit
        self.pixel_dim = pixel_dim
        self.nr_of_el = nr_of_el
        self.sigma = pixel_dim * nr_of_el
        self.charge_distribution = sorted(norm.rvs(self.real_hit, self.sigma, self.nr_of_el))
        self.pixel_coordinates = (np.linspace(-self.pixel_dim, 2 * self.pixel_dim, 3 * self.pixel_dim + 1)).tolist()
        self.PI, self.PII, self.PIII = self.calc_probabilities()

    def erf_aprox_Taylor(self, probability, aprox_order):
        result = 0
        c = [1, 1]
        current_c = 0
        for c_k in range(aprox_order - 1):
            c_k = c_k + 2
            for m in range(c_k):
                current_c += (c[m] * c[c_k - 1 - m]) / ((m + 1) * (2 * m + 1))
            c.append(current_c)
            current_c = 0
        for k in range(aprox_order):
            result += c[k] / (2 * k + 1) * (math.sqrt(math.pi) * probability / 2) ** (2 * k + 1)
        return result

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

    # Generic model for float data
    def OneD_calc_hit(self):
        PSUM = self.PI + self.PII + self.PIII
        PI = self.PI / PSUM
        # PII = PII / PSUM
        PIII = self.PIII / PSUM

        if PI > PIII:
            x0 = -self.sigma * math.sqrt(2) * special.erfinv(2 * PI - 1)
        else:
            x0 = self.sigma * math.sqrt(2) * special.erfinv(2 * PIII - 1) + self.pixel_dim
        return x0

    def OneD_calc_hit_int(self, mult):
        # pixel_dim * 0.35
        PSUM = self.PI + self.PII + self.PIII
        PI = (100 * (self.PI / PSUM)).__floor__()  # Probabilty in %
        # PII = PII / PSUM
        PIII = (100 * (self.PIII / PSUM)).__floor__()  # Probability in %

        if PI > PIII:
            x0 = (((-self.sigma * mult).__floor__() * (math.sqrt(2) * mult).__floor__() * (
                    special.erfinv(2 * (PI / 100) - 1) * mult).__floor__()) / mult**3).__floor__()
        else:
            x0 = (((self.sigma * mult).__floor__() * (math.sqrt(2) * mult).__floor__() * (
                    special.erfinv(2 * (PIII / 100) - 1) * mult).__floor__() + (
                           self.pixel_dim * mult**3)) / mult**3).__floor__()
        return x0

    def OneD_calc_hit_err_aprox_Taylor(self, order):
        # pixel_dim * 0.35
        PI, PII, PIII = self.calc_probabilities()
        PSUM = PI + PII + PIII
        PI = PI / PSUM
        # PII = PII / PSUM
        PIII = PIII / PSUM

        if PI > PIII:
            x0 = -self.sigma * math.sqrt(2) * self.erf_aprox_Taylor(2 * PI - 1, order)
        else:
            x0 = self.sigma * math.sqrt(2) * self.erf_aprox_Taylor(2 * PIII - 1, order) + self.pixel_dim
        return x0

    def OneD_calc_hit_err_aprox_Taylor_int(self, order):
        # pixel_dim * 0.35
        PI, PII, PIII = self.calc_probabilities()
        PSUM = PI + PII + PIII
        PI = (100 * (PI / PSUM)).__floor__()  # Probabilty in %
        # PII = PII / PSUM
        PIII = (100 * (PIII / PSUM)).__floor__()  # Probability in %

        if PI > PIII:
            x0 = (((-self.sigma * 100).__floor__() * (math.sqrt(2) * 100).__floor__() * (
                        self.erf_aprox_Taylor(2 * (PI / 100) - 1, order) * 100).__floor__()) / 1000000).__floor__()
        else:
            x0 = (((self.sigma * 100).__floor__() * (math.sqrt(2) * 100).__floor__() * (
                        self.erf_aprox_Taylor(2 * (PIII / 100) - 1, order) * 100).__floor__() + (
                               self.pixel_dim * 1000000)) / 1000000).__floor__()
        return x0
