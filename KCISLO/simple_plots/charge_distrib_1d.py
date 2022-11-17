#type: ignore
import os, sys
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from models.model_1d import PixelChargeSharingModel1D


if __name__ == "__main__":
    PIXEL_SIZE = 80
    NUM_OF_CHARGES = 2200
    CHARGE_CLOUD_SIGMA = 6.31
    NOISE_SIGMA = 50

    hit_pos = 40
    lut_size = 50
    fig_size = 40

    px_model = PixelChargeSharingModel1D(PIXEL_SIZE, NUM_OF_CHARGES, CHARGE_CLOUD_SIGMA, NOISE_SIGMA)
    px_model.hit(hit_pos)
    calc_hit = px_model.calc_hit_1D_lut(lut_size)
    err = abs(calc_hit - hit_pos)

    print(f"{hit_pos=} μm")
    print(f"{calc_hit=} μm")
    print(f"{err=} μm")

    ax = plt.axes()
    title = f"1D charge distribution.\n Real hit at {hit_pos:2.3f} μm. Calculated hit at {calc_hit:2.3f}μm"
    px_model.set_plt_axis_distribution(ax, title, fig_size)
    plt.show()
