from dataclasses import dataclass

from .detector import Detector


@dataclass
class SiSigmaDetector(Detector):
    material: str = "Si_sigma"


target1 = SiSigmaDetector(
    pixel_size=50,
    charge_cloud_sigma=5,
    num_of_charges=2200,
    noise_sigma=45,
    name="target1",
)
target2 = SiSigmaDetector(
    pixel_size=50,
    charge_cloud_sigma=10,
    num_of_charges=2200,
    noise_sigma=45,
    name="target2",
)
target3 = SiSigmaDetector(
    pixel_size=50,
    charge_cloud_sigma=15,
    num_of_charges=2200,
    noise_sigma=45,
    name="target3",
)
target4 = SiSigmaDetector(
    pixel_size=50,
    charge_cloud_sigma=20,
    num_of_charges=2200,
    noise_sigma=45,
    name="target4",
)
target5 = SiSigmaDetector(
    pixel_size=50,
    charge_cloud_sigma=25,
    num_of_charges=2200,
    noise_sigma=45,
    name="target5",
)

all = [target1, target2, target3, target4, target5]
