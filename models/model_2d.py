# type: ignore
import os
import sys
from itertools import product

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from models.model_1d import PixelChargeSharingModel1D


class PixelChargeSharingModel2D:
    """
    The two dimensional model of pixel charge sharing.
    """
    def __init__(
        self,
        pixel_size: int,
        num_of_charges: int,
        charge_cloud_sigma: float = None,
        noise_sigma: float = None
    ):
        # Pixel params
        self.pixel_size = pixel_size
        self.num_of_charges = num_of_charges
        self.charge_cloud_sigma = charge_cloud_sigma if charge_cloud_sigma is not None else pixel_size * 0.35
        self.noise_sigma = noise_sigma if noise_sigma is not None else None
        self.pixel_coordinates = list(np.linspace(-self.pixel_size, 2 * self.pixel_size, 3 * self.pixel_size + 1))

        # 1D Models
        self.x = PixelChargeSharingModel1D(pixel_size, num_of_charges, charge_cloud_sigma, noise_sigma)
        self.y = PixelChargeSharingModel1D(pixel_size, num_of_charges, charge_cloud_sigma, noise_sigma)

        # Hit
        self.hit_posx: int | None = None
        self.hit_posy: int | None = None

    def hit(self, posx: int, posy: int) -> None:
        self.hit_posx = posx
        self.hit_posy = posy
        self.x.hit(posx)
        self.y.hit(posy)

    def get_probabilities(self) -> list[int]:
        probs: list[int] = [0] * 9
        x, y = self.x, self.y
        x_conds = [x.is_left, x.is_mid, x.is_right]
        y_conds = [y.is_left, y.is_mid, y.is_right]
        for i, (y_cond, x_cond) in enumerate(product(y_conds, x_conds)):
            for x_i, y_i in zip(self.x.charge_distribution, self.y.charge_distribution):
                if x_cond(x_i) and y_cond(y_i):
                    probs[i] += 1
        if self.noise_sigma is None:
            return probs
        # Generate noise for each pixel. Unit in electrons RMS
        new_probs = []
        for p in probs:
            noise = abs(int(norm.rvs(loc=0, scale=self.noise_sigma, size=1)))
            new_probs.append(p + noise)
        return new_probs

    def update_probabilities_1D(self) -> None:
        """
        Pixel numeration
        [6][7][8]
        [3][4][5]
        [0][1][2]
        """
        probs = self.get_probabilities()
        self.x.probs = [
            probs[0] + probs[3] + probs[6], # left
            probs[1] + probs[4] + probs[7], # mid
            probs[2] + probs[5] + probs[8], # right
        ]
        self.y.probs = [
            probs[0] + probs[1] + probs[2], # bottom
            probs[3] + probs[4] + probs[5], # mid
            probs[6] + probs[7] + probs[8], # top
        ]

    def calc_hit_2D_erfinv(self) -> tuple[float, float]:
        # remove update to compare method with te same input
        self.update_probabilities_1D()
        x_calc_hit = self.x.calc_hit_1D_erfinv()
        y_calc_hit = self.y.calc_hit_1D_erfinv()
        return x_calc_hit, y_calc_hit

    def calc_hit_2D_taylor(self, taylor_order: int = 10) -> tuple[float, float]:
        self.update_probabilities_1D()
        x_calc_hit = self.x.calc_hit_1D_taylor(taylor_order)
        y_calc_hit = self.y.calc_hit_1D_taylor(taylor_order)
        return x_calc_hit, y_calc_hit

    def calc_hit_2D_lut(self, lut_size: int = 20) -> tuple[float, float]:
        self.update_probabilities_1D()
        x_calc_hit = self.x.calc_hit_1D_lut(lut_size)
        y_calc_hit = self.y.calc_hit_1D_lut(lut_size)
        return x_calc_hit, y_calc_hit

    def set_plt_axis_birds_eye_view(self,
            ax: plt.Axes,
            title: str) -> None:
        ax.set_title(title)
        ax.scatter(self.x.charge_distribution, self.y.charge_distribution, s=4)
        for line in [0, self.pixel_size]:
            ax.hlines(line, -self.pixel_size, 2*self.pixel_size, colors="black")
            ax.vlines(line, -self.pixel_size, 2*self.pixel_size, colors="black")
