# type: ignore

import numpy as np
from scipy.stats import norm

from .detectors.detector import Detector
from .pcs_model_1d import PcsModel1D

IntFloat = np.integer | np.floating
IntFloatType = type[IntFloat]


class PcsModel1DInt(PcsModel1D):
    """
    The one dimensional model of pixel charge sharing
    with different types enabled
    """

    num_type: IntFloatType = np.uint8
    multiplier_pc = np.iinfo(num_type).max
    multiplier = 2
    dimension = "1D_int"
    gauss_lut: list[IntFloat] = []
    gauss_bin_size: IntFloat = 0

    def __init__(
        self,
        detector: Detector,
    ):
        super().__init__(detector)
        # Hit
        self.hit_pos: int = -1
        # charge_distribution holds coordinates at which electrons were detected
        self.probs_pc: list[IntFloat] = []

    def get_probabilities_percent(self) -> list[IntFloat]:
        psum = sum(self.probs)
        # print(self.probs)
        probs_pc = [
            self.num_type(self.multiplier_pc * p / psum) for p in self.probs
        ]
        return probs_pc

    def create_gauss_lut(self, size: int) -> None:
        if len(PcsModel1DInt.gauss_lut) == size:
            return
        PcsModel1DInt.gauss_lut: list[IntFloat] = []
        # podzial pixela na czesci
        pixel_bins = np.linspace(
            0, self.multiplier * self.pixel_size, size + 1, dtype=self.num_type
        )
        # print(pixel_bins)
        # najmniejszy krok podzialu
        PcsModel1DInt.gauss_bin_size = self.num_type(
            pixel_bins[1] - pixel_bins[0]
        )
        # podzial pixela na czesci bez mnoznika
        pixel_bins = np.linspace(0, self.pixel_size, size + 1)
        # dystrybuanta
        cdf = norm.cdf(pixel_bins, 0, self.charge_cloud_sigma)

        for cdf_i in cdf:
            PcsModel1DInt.gauss_lut.append(
                self.num_type(self.multiplier_pc * (1 - cdf_i))
            )
        # print("[DEBUG] create gauss")
        # print(PcsModel1DTyped.gauss_lut)
        # nonzeros = len([i for i in PcsModel1DTyped.gauss_lut if i > 0])
        # print(nonzeros / size)

    def calc_hit_lut(self, lut_size: int = 20) -> float:
        self.create_gauss_lut(lut_size)
        p1_pc, p2_pc, p3_pc = self.probs_pc

        calc_hit_pos: IntFloat = 0
        if p1_pc == p3_pc:
            calc_hit_pos = self.multiplier * (self.pixel_size / 2)
        elif p1_pc > p3_pc:
            for i, value in enumerate(self.gauss_lut):
                if p1_pc >= value:
                    break
            calc_hit_pos = i * self.gauss_bin_size
        else:
            for i, value in enumerate(self.gauss_lut):
                if p3_pc >= value:
                    break
            calc_hit_pos = (
                self.multiplier * self.pixel_size - i * self.gauss_bin_size
            )
        if not (
            np.iinfo(self.num_type).min
            <= calc_hit_pos
            <= np.iinfo(self.num_type).max
        ):
            print(f"Calculated value outside numeric range! for:{self.hit_pos}")
        calc_hit_pos = self.num_type(calc_hit_pos)
        return calc_hit_pos
