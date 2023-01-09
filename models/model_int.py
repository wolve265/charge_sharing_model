#type: ignore
import math
import numpy as np
import os
import sys
from scipy import special
from scipy.stats import norm
from typing import Never


sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from models.model_1d import PixelChargeSharingModel1D


class PixelChargeSharingModel1DInt(PixelChargeSharingModel1D):
    """
    The one dimensional model of pixel charge sharing.
    """
    def __init__(
        self,
        pixel_size: int,
        num_of_charges: int,
        charge_cloud_sigma: float = None,
        noise_sigma: float = None,
        num_type: type = int,
        multiplier: int = 100
    ) -> None:
        super().__init__(pixel_size, num_of_charges, charge_cloud_sigma, noise_sigma)
        self.num_type = num_type
        self.multiplier = num_type(multiplier)
        self.gauss_lut: list[self.num_type] = []

    def get_probabilities_percent_new(self) -> list[int]:
        psum = sum(self.probs)
        probs_pc = [self.multiplier * p // psum for p in self.probs]
        return probs_pc

    def create_gauss_lut(self, size: int) -> None:
        if len(self.gauss_lut) == size:
            return
        self.gauss_lut = []
        pixel_bins = np.linspace(0, self.pixel_size, size) # podzial pixela na czesci
        cdf = norm.cdf(pixel_bins, 0, self.charge_cloud_sigma) # dystrybuanta

        pixel_bins = np.linspace(0, self.pixel_size*self.multiplier, size) # podzial pixela na czesci
        self.gauss_bin_size = self.num_type(pixel_bins[1] - pixel_bins[0]) # najmniejszy krok podzialu
        for i in cdf:
            self.gauss_lut.append(self.num_type(self.multiplier *(1 - i)))

    def calc_hit_1D_lut(self, lut_size: int):
        self.probs = self.get_probabilities()
        self.create_gauss_lut(lut_size)
        p1_pc, p2_pc, p3_pc = self.get_probabilities_percent_new()

        calc_hit_pos = self.num_type(0)
        if p1_pc > p3_pc:
            for i, value in enumerate(self.gauss_lut):
                if p1_pc >= value:
                    break
            calc_hit_pos = i*self.gauss_bin_size
        else:
            for i, value in enumerate(self.gauss_lut):
                if p3_pc >= value:
                    break
            calc_hit_pos = self.num_type(self.multiplier * self.pixel_size) - i*self.gauss_bin_size
        return calc_hit_pos
