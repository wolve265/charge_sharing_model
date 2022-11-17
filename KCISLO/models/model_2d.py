# type: ignore
import os, sys
from itertools import product
import matplotlib.pyplot as plt
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from models.model_1d import PixelChargeSharingModel1D

class PixelChargeSharingModel2D:
    """
    The two dimensional model of pixel charge sharing.
    """
    def __init__(self, pixel_size: int):
        # Pixel params
        self.pixel_size = pixel_size
        self.sigma: float = pixel_size * 0.35
        self.pixel_coordinates = list(np.linspace(-self.pixel_size, 2 * self.pixel_size, 3 * self.pixel_size + 1))

        # 1D Models
        self.x = PixelChargeSharingModel1D(pixel_size)
        self.y = PixelChargeSharingModel1D(pixel_size)

        # Hit
        self.hit_posx: int | None = None
        self.hit_posy: int | None = None
        self.electrons_num: int | None = None

    def hit(self, posx: int, posy: int, electrons_num: int) -> None:
        self.hit_posx = posx
        self.hit_posy = posy
        self.electrons_num = electrons_num
        self.x.hit(posx, electrons_num)
        self.y.hit(posy, electrons_num)

    def get_probabilities(self) -> list[int]:
        probs: list[int] = []
        x, y = self.x, self.y
        x_conds = [x.is_left, x.is_mid, x.is_right]
        y_conds = [y.is_left, y.is_mid, y.is_right]
        for i, (y_cond, x_cond) in enumerate(product(y_conds, x_conds)):
            probs.append(0)
            for x_i, y_i in zip(self.x.charge_distribution, self.y.charge_distribution):
                if x_cond(x_i) and y_cond(y_i):
                    probs[i] += 1
        return probs

    def calc_hit_2D(self) -> tuple[float, float]:
        x_calc_hit = self.x.calc_hit_1D_erfinv()
        y_calc_hit = self.y.calc_hit_1D_erfinv()
        return x_calc_hit, y_calc_hit

    def set_plt_axis_birds_eye_view(self,
            ax: plt.Axes,
            title: str) -> None:
        ax.set_title(title)
        ax.scatter(self.x.charge_distribution, self.y.charge_distribution, s=4)
        for line in [0, self.pixel_size]:
            ax.hlines(line, -self.pixel_size, 2*self.pixel_size, colors="black")
            ax.vlines(line, -self.pixel_size, 2*self.pixel_size, colors="black")
