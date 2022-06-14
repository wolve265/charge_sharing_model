# Necessary imports for model to work
import math
from scipy.stats import norm
from scipy import special
import numpy as np
from ctypes import *


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

    def OneD_calc_hit_int(self):
        # pixel_dim * 0.35
        PI, PII, PIII = self.calc_probabilities()
        PSUM = PI + PII + PIII
        PI = (100 * (PI / PSUM)).__floor__()        # Probabilty in %
        # PII = PII / PSUM
        PIII = (100 * (PIII / PSUM)).__floor__()    # Probability in %

        if PI > PIII:
            x0 = ( ((-self.sigma * 100).__floor__() * (math.sqrt(2) * 100).__floor__() * (special.erfinv(2 * (PI/100) - 1) * 100).__floor__())/1000000).__floor__()
        else:
            x0 = ( ( (self.sigma * 100).__floor__() * (math.sqrt(2) * 100).__floor__() * (special.erfinv(2 * (PIII/100) - 1) * 100).__floor__() + (self.pixel_dim * 1000000) )/1000000 ).__floor__()
        return x0


mod = Model(real_hit=35, pixel_dim=75, nr_of_el=2200)

x0 = mod.OneD_calc_hit_int()

print(x0)