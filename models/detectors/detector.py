from dataclasses import dataclass


@dataclass
class Detector:
    pixel_size: float
    charge_cloud_sigma: float
    num_of_charges: float
    noise_sigma: float
    name: str
    material: str
