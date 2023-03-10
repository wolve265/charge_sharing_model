from dataclasses import dataclass

from .detector import Detector


@dataclass
class SiDetector(Detector):
    material: str = "Si"


ideal = SiDetector(
    pixel_size=75,
    charge_cloud_sigma=8,
    num_of_charges=2200,
    noise_sigma=0,
    name="ideal",
)
actual = SiDetector(
    pixel_size=75,
    charge_cloud_sigma=8,
    num_of_charges=2200,
    noise_sigma=45,
    name="actual",
)
target = SiDetector(
    pixel_size=50,
    charge_cloud_sigma=10,
    num_of_charges=2200,
    noise_sigma=45,
    name="target",
)

all = [ideal, actual, target]
