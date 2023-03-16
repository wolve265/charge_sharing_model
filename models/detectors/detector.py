from dataclasses import dataclass


@dataclass
class Detector:
    pixel_size: float
    charge_cloud_sigma: float
    num_of_charges: float
    noise_sigma: float
    name: str
    material: str

    def get_str(self) -> str:
        return (
            f"""pixel size = {self.pixel_size}μm, charge cloud σ = {self.charge_cloud_sigma}μm\n"""
            f"""number of charges = {self.num_of_charges}e, noise σ = {self.noise_sigma}e RMS"""
        )
