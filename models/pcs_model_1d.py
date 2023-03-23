# type: ignore
import math
from typing import Any

import numpy as np
from scipy import special
from scipy.stats import norm

from .detectors.detector import Detector


class PcsModel1D:
    """
    The one dimensional model of pixel charge sharing.
    """

    dimension = "1D"
    gauss_lut: list[float] = []
    gauss_bin_size: float = 0.0

    def __init__(self, detector: Detector):
        # Pixel params
        self.detector = detector
        self.pixel_size = detector.pixel_size
        self.num_of_charges = detector.num_of_charges
        self.charge_cloud_sigma = detector.charge_cloud_sigma
        self.noise_sigma = detector.noise_sigma
        self.pixel_coordinates = list(
            np.linspace(
                -self.pixel_size,
                2 * self.pixel_size,
                3 * self.pixel_size + 1,
            )
        )

        # Hit
        self.hit_pos: int = -1
        # charge_distribution holds coordinates at which electrons were detected
        self.charge_distribution: Any = None
        self.probs: list[int] = []
        self.probs_pc: list[float] = []

        # Matplotlib
        self.lines_pos = [
            -self.pixel_size,
            0,
            self.pixel_size,
            2 * self.pixel_size,
        ]

    def hit(self, pos: int) -> None:
        self.hit_pos = pos
        self.charge_distribution = norm.rvs(
            self.hit_pos, self.charge_cloud_sigma, self.num_of_charges
        )
        self.probs = self.get_probabilities()
        self.probs_pc = self.get_probabilities_percent()

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

    def get_probabilities(self) -> list[int]:
        p1: int = len(self.left())
        p2: int = len(self.mid())
        p3: int = len(self.right())
        probs = [p1, p2, p3]
        if not self.noise_sigma:
            return probs
        # Generate noise for each part. Unit in electrons RMS
        new_probs = []
        for p in probs:
            noise = abs(int(norm.rvs(loc=0, scale=self.noise_sigma, size=1)))
            new_probs.append(p + noise)
        return new_probs

    def get_probabilities_percent(self) -> list[float]:
        psum = sum(self.probs)
        # print(self.probs)
        probs_pc = [p / psum for p in self.probs]
        return probs_pc

    def calc_hit_erfinv(self, param: int = 0) -> float:
        del param
        p1_pc, p2_pc, p3_pc = self.probs_pc

        calc_hit_pos: float = 0.0
        if p1_pc == p3_pc == 0:
            calc_hit_pos = self.pixel_size / 2
        if p1_pc > p3_pc:
            calc_hit_pos = (
                -self.charge_cloud_sigma
                * math.sqrt(2)
                * special.erfinv(2 * p1_pc - 1)
            )
        else:
            calc_hit_pos = (
                self.charge_cloud_sigma
                * math.sqrt(2)
                * special.erfinv(2 * p3_pc - 1)
                + self.pixel_size
            )
        return calc_hit_pos

    def erfinv_taylor(self, probability: float, aprox_order: int):
        result: float = 0.0
        c = [1, 1]
        for c_k in range(aprox_order - 1):
            current_c = 0
            c_k = c_k + 2
            for m in range(c_k):
                current_c += (c[m] * c[c_k - 1 - m]) / ((m + 1) * (2 * m + 1))
            c.append(current_c)
        for k in range(aprox_order):
            result += (
                c[k]
                / (2 * k + 1)
                * (math.sqrt(math.pi) * probability / 2) ** (2 * k + 1)
            )
        return result

    def calc_hit_taylor(self, taylor_order: int = 10) -> float:
        p1_pc, p2_pc, p3_pc = self.probs_pc

        calc_hit_pos: float = 0.0
        if p1_pc == p3_pc == 0:
            calc_hit_pos = self.pixel_size / 2
        elif p1_pc > p3_pc:
            calc_hit_pos = (
                -self.charge_cloud_sigma
                * math.sqrt(2)
                * self.erfinv_taylor(2 * p1_pc - 1, taylor_order)
            )
        else:
            calc_hit_pos = (
                self.charge_cloud_sigma
                * math.sqrt(2)
                * self.erfinv_taylor(2 * p3_pc - 1, taylor_order)
                + self.pixel_size
            )
        return calc_hit_pos

    def create_gauss_lut(self, size: int) -> None:
        if len(PcsModel1D.gauss_lut) == size:
            return
        # print("[DEBUG] create gauss")
        PcsModel1D.gauss_lut = []
        # podzial pixela na czesci
        pixel_bins = np.linspace(0, self.pixel_size, size)
        # najmniejszy krok podzialu
        PcsModel1D.gauss_bin_size = pixel_bins[1] - pixel_bins[0]
        # dystrybuanta
        cdf = norm.cdf(pixel_bins, 0, self.charge_cloud_sigma)

        for cdf_i in cdf:
            PcsModel1D.gauss_lut.append(1 - cdf_i)

    def calc_hit_lut(self, lut_size: int = 20) -> float:
        self.create_gauss_lut(lut_size)
        # print(PcsModel1D.gauss_lut)
        p1_pc, p2_pc, p3_pc = self.probs_pc

        calc_hit_pos: float = 0.0
        if p1_pc == p3_pc == 0:
            calc_hit_pos = self.pixel_size / 2
        elif p1_pc > p3_pc:
            for i, value in enumerate(self.gauss_lut):
                if p1_pc >= value:
                    break
            calc_hit_pos = i * self.gauss_bin_size
        else:
            for i, value in enumerate(self.gauss_lut):
                if p3_pc >= value:
                    break
            calc_hit_pos = self.pixel_size - i * self.gauss_bin_size
        return calc_hit_pos
