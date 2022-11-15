#type: ignore
from dataclasses import dataclass, field

import numpy as np

import model


@dataclass
class Detector:
    """
    Class representing X-ray detector
    """
    name: str
    pixel_size: int  # [um]
    charge_cloud_sigma: int  # [um]
    num_of_charges: int  # [electrons]
    noise_sigma: int  # [electrons RMS]
    px_model: model.PixelChargeSharingModel1D = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.px_model = model.PixelChargeSharingModel1D(self.pixel_size, self.charge_cloud_sigma, self.noise_sigma)

    def hit(self, pos: int) -> None:
        self.px_model.hit(pos, self.num_of_charges)

    def hit_times(self, pos: int, times: int, **kwargs) -> list[float]:
        means: list[float] = []
        for fun in self.px_model.CALC_HIT_FUNCS:
            results = np.empty(times)
            for i in range(times):
                self.hit(pos)
                results[i] = fun(**kwargs)
            mean_result = np.mean(results)
            mean_result = mean_result if mean_result > 0 else 0
            means.append(mean_result)
        return means

    def hit_times_pos(self, hit_positions: list[int], times: int, **kwargs) -> list[list[float]]:
        means: list[list[float]] = []
        for pos in hit_positions:
            inner_means = self.hit_times(pos, times, **kwargs)
            means.append(inner_means)
        return means

SI_DETECTORS = [
    Detector(
        name="Ideal Si detector",
        pixel_size=75,
        charge_cloud_sigma=8,
        num_of_charges=2200,
        noise_sigma=0
    ),
    Detector(
        name="Actual Si detector",
        pixel_size=75,
        charge_cloud_sigma=8,
        num_of_charges=2200,
        noise_sigma=45
    ),
    Detector(
        name="Target Si detector",
        pixel_size=50,
        charge_cloud_sigma=10,
        num_of_charges=2200,
        noise_sigma=45
    ),
]

CDTE_DETECTORS = [
    Detector(
        name="Ideal CdTe detector",
        pixel_size=100,
        charge_cloud_sigma=16,
        num_of_charges=4970,
        noise_sigma=0
    ),
    Detector(
        name="Actual CdTe detector",
        pixel_size=100,
        charge_cloud_sigma=16,
        num_of_charges=4970,
        noise_sigma=200
    ),
    Detector(
        name="Target CdTe detector",
        pixel_size=50,
        charge_cloud_sigma=16,
        num_of_charges=4970,
        noise_sigma=150
    ),
]

ALL_DETECTORS = [*SI_DETECTORS, *CDTE_DETECTORS]
