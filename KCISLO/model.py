#type: ignore
from itertools import product
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy import special
from scipy.stats import norm
from typing import Any


class PixelChargeSharingModel1D:
    """
    The one dimensional model of pixel charge sharing.
    """
    def __init__(self, pixel_size: int, sigma: float = None):
        # Pixel params
        self.pixel_size = pixel_size
        self.sigma = sigma if sigma is not None else pixel_size * 0.35
        self.pixel_coordinates = list(np.linspace(-self.pixel_size, 2 * self.pixel_size, 3 * self.pixel_size + 1))

        self.gauss_lut = []

        # Hit
        self.hit_pos: int | None = None
        self.electrons_num: int | None = None
        # charge_distribution holds coordinates at which the electron was detected
        self.charge_distribution: Any = None

        # Matplotlib
        self.lines_pos = [-pixel_size, 0, pixel_size, 2*pixel_size]

    def hit(self, pos: int, electrons_num: int) -> None:
        self.hit_pos = pos
        self.electrons_num = electrons_num
        self.charge_distribution = norm.rvs(self.hit_pos, self.sigma, self.electrons_num)

    def is_left(self, i: float) -> bool:
        return -self.pixel_size < i < 0

    def is_mid(self, i: float) -> bool:
        return 0 < i < self.pixel_size

    def is_right(self, i: float) -> bool:
        return self.pixel_size < i < 2 * self.pixel_size

    def left(self) -> list[float]:
        return [i for i in self.charge_distribution if self.is_left(i)]

    def mid(self) -> list[float]:
        return [i for i in self.charge_distribution if self.is_mid(i)]

    def right(self) -> list[float]:
        return [i for i in self.charge_distribution if self.is_right(i)]

    def get_probabilities(self) -> tuple[int, int, int]:
        p1: int = len(self.left())
        p2: int = len(self.mid())
        p3: int = len(self.right())
        return p1, p2, p3

    def calc_hit_1D_ideal(self) -> float:
        p1, p2, p3 = self.get_probabilities()
        psum = p1 + p2 + p3
        p1_pc = p1 / psum
        # p2_pc = p2 / psum
        p3_pc = p3 / psum

        calc_hit_pos: float = 0.0
        if p1_pc > p3_pc:
            calc_hit_pos = -self.sigma * math.sqrt(2) * special.erfinv(2 * p1_pc - 1)
        else:
            calc_hit_pos = self.sigma * math.sqrt(2) * special.erfinv(2 * p3_pc - 1) + self.pixel_size
        return calc_hit_pos

    def erfinv_Taylor(self, probability: float, aprox_order: int) -> float:
        result: float = 0.0
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

    def calc_hit_1D_Taylor(self, order: int) -> float:
        p1, p2, p3 = self.get_probabilities()
        psum = p1 + p2 + p3
        p1_pc = p1 / psum
        # p2_pc = p2 / psum
        p3_pc = p3 / psum

        calc_hit_pos: float = 0.0
        if p1_pc > p3_pc:
            calc_hit_pos = -self.sigma * math.sqrt(2) * self.erfinv_Taylor(2 * p1_pc - 1, order)
        else:
            calc_hit_pos = self.sigma * math.sqrt(2) * self.erfinv_Taylor(2 * p3_pc - 1, order) + self.pixel_size
        return calc_hit_pos

    def create_gauss_lut(self, size: int) -> None:
        if len(self.gauss_lut) == size:
            return
        self.gauss_lut = []
        pixel_bins = np.linspace(0, self.pixel_size, size) # podzial pixela na czesci
        self.gauss_bin_size = pixel_bins[1] - pixel_bins[0] # najmniejszy krok podzialu
        cdf = norm.cdf(pixel_bins, 0, self.sigma) # dystrybuanta

        for i in range(len(pixel_bins)):
            self.gauss_lut.append(1 - cdf[i])

    def calc_hit_1D_lut(self, lut_size: int) -> float:
        self.create_gauss_lut(lut_size)
        p1, p2, p3 = self.get_probabilities()
        psum = p1 + p2 + p3
        p1_pc = p1 / psum
        # p2_pc = p2 / psum
        p3_pc = p3 / psum
        index: int = 0
        calc_hit_pos: float = 0.0
        if p1_pc > p3_pc:
            while(p1_pc < self.gauss_lut[index]):
                index += 1
            calc_hit_pos = index*self.gauss_bin_size
        else:
            while(p3_pc < self.gauss_lut[index]):
                index += 1
            calc_hit_pos = self.pixel_size - index*self.gauss_bin_size
        return calc_hit_pos

    def set_plt_axis_distribution(self,
            ax: plt.Axes,
            title: str,
            fig_size: int) -> None:
        ax.set_xlim(-self.pixel_size, 2*self.pixel_size)
        ax.set_ylim(0, fig_size)
        ax.set_xlabel(f'Position (μm)', labelpad=5, size=13)
        ax.set_ylabel('Number of electrons', labelpad=5, size=13)
        ax.set_title(title, size=12)
        ax.hist(self.charge_distribution, bins=len(self.pixel_coordinates))
        for pos in self.lines_pos:
            ax.vlines(pos, 0, fig_size, colors="black")
        ax.vlines(self.hit_pos, 0, fig_size/2, colors="red", label="real hit position")
        ax.legend()

    def set_plt_axis_charge_integral(self,
            ax: plt.Axes,
            title: str,
            probs_list,
            fig_size: int) -> None:
        ax.set_title(title, size=12)
        ax.bar(self.lines_pos[:-1], probs_list, self.pixel_size, align='edge')
        for line in self.lines_pos:
            ax.vlines(line, 0, fig_size, colors="black")
        ax.vlines(self.hit_pos, 0, fig_size/2, colors="red", label="real hit position")
        ax.legend()


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
        x_calc_hit = self.x.calc_hit_1D_ideal()
        y_calc_hit = self.y.calc_hit_1D_ideal()
        return x_calc_hit, y_calc_hit

    def set_plt_axis_birds_eye_view(self,
            ax: plt.Axes,
            title: str) -> None:
        ax.set_title(title)
        ax.scatter(self.x.charge_distribution, self.y.charge_distribution, s=4)
        for line in [0, self.pixel_size]:
            ax.hlines(line, -self.pixel_size, 2*self.pixel_size, colors="black")
            ax.vlines(line, -self.pixel_size, 2*self.pixel_size, colors="black")
