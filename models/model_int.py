#type: ignore
import numpy as np
from scipy.stats import norm

import model


class PixelChargeSharingModel1DInt(model.PixelChargeSharingModel1D):
    """
    The one dimensional model of pixel charge sharing.
    """
    def __init__(self, pixel_size: int, num_type, multiplier):
        super().__init__(pixel_size)
        self.num_type = num_type
        self.multiplier = num_type(multiplier)

    def create_gauss_lut(self, size: int) -> None:
        if len(self.gauss_lut) == size:
            return
        self.gauss_lut = []
        pixel_bins = np.linspace(0, self.pixel_size, size) # podzial pixela na czesci
        cdf = norm.cdf(pixel_bins, 0, self.charge_cloud_sigma) # dystrybuanta

        pixel_bins = np.linspace(0, self.pixel_size*self.multiplier, size) # podzial pixela na czesci
        self.gauss_bin_size = self.num_type(pixel_bins[1] - pixel_bins[0]) # najmniejszy krok podzialu
        for i in cdf:
            self.gauss_lut.append(self.num_type(self.multiplier *(1 - i)))

    def calc_hit_1D_lut(self, lut_size: int):
        self.create_gauss_lut(lut_size)
        p1, p2, p3 = self.get_probabilities()
        psum = p1 + p2 + p3
        p1_pc = self.multiplier * p1 // psum
        # p2_pc = p2 / psum
        p3_pc = self.multiplier * p3 // psum
        index = self.num_type(0)
        calc_hit_pos = self.num_type(0)
        if p1_pc > p3_pc:
            while(p1_pc < self.gauss_lut[index]):
                index += self.num_type(1)
            calc_hit_pos = index*self.gauss_bin_size
        else:
            while(p3_pc < self.gauss_lut[index]):
                index += self.num_type(1)
            calc_hit_pos = self.num_type(self.multiplier * self.pixel_size) - index*self.gauss_bin_size
        return calc_hit_pos


if __name__ == "__main__":
    pixel_size = 75 # um
    hit_pos = 70
    electrons_num = 2200
    lut_size = 1000

    num_type = np.uint16
    multiplier = 100

    model_1d = PixelChargeSharingModel1DInt(pixel_size, num_type, multiplier)
    model_1d.hit(hit_pos, electrons_num)
    calc_hit_ideal = model_1d.calc_hit_1D_erfinv()
    calc_hit_lut = model_1d.calc_hit_1D_lut(lut_size)
    print()
    print(f"{type(calc_hit_lut)=}")
    calc_hit_lut = 1000//multiplier * calc_hit_lut
    print()
    print(f"{hit_pos=} μm")
    print(f" {calc_hit_ideal=:.3f} μm")
    print(f"   {calc_hit_lut=:,} nm ({lut_size=})")
