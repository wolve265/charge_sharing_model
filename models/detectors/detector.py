from dataclasses import dataclass


@dataclass
class Detector:
    pixel_size: int
    charge_cloud_sigma: int
    num_of_charges: int
    noise_sigma: int
    name: str
    material: str

    def get_str(self) -> str:
        return (
            f"""pixel size = {self.pixel_size}μm, charge cloud σ = {self.charge_cloud_sigma}μm\n"""
            f"""number of charges = {self.num_of_charges}e, noise σ = {self.noise_sigma}e RMS"""
        )
