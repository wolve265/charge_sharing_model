from dataclasses import dataclass

from .detector import Detector


@dataclass
class CdTeDetector(Detector):
    material: str = "CdTe"


ideal = CdTeDetector(
    pixel_size=100,
    charge_cloud_sigma=16,
    num_of_charges=4970,
    noise_sigma=0,
    name="ideal",
)
actual = CdTeDetector(
    pixel_size=100,
    charge_cloud_sigma=16,
    num_of_charges=4970,
    noise_sigma=200,
    name="actual",
)
target = CdTeDetector(
    pixel_size=50,
    charge_cloud_sigma=16,
    num_of_charges=4970,
    noise_sigma=150,
    name="target",
)

all = [ideal, actual, target]
