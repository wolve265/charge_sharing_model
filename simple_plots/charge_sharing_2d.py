# type: ignore
import os
import sys

import matplotlib.pyplot as plt
from scipy.stats import norm

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from models.model_2d import PixelChargeSharingModel2D

if __name__ == "__main__":
    PIXEL_SIZE = 75
    NUM_OF_CHARGES = 2200
    CHARGE_CLOUD_SIGMA = 25
    NOISE_SIGMA = 50

    hit_pos = (35, 60)
    fig_size = 40
    fig_size_integral = 1800

    model_2d = PixelChargeSharingModel2D(PIXEL_SIZE, NUM_OF_CHARGES, CHARGE_CLOUD_SIGMA, NOISE_SIGMA)
    model_2d.hit(*hit_pos)
    x = model_2d.x
    y = model_2d.y

    def plot_prob(axes: list[plt.Axes]):
        (ax1, ax2) = axes
        title = f"X axis electron count integral with noise"
        x.set_plt_axis_charge_integral(ax1, title, fig_size_integral)
        title = f"y axis electron count integral with noise"
        y.set_plt_axis_charge_integral(ax2, title, fig_size_integral)

    ax = plt.axes()
    model_2d.set_plt_axis_birds_eye_view(ax, f"Bird's eye view of post hit electron collection")

    fig, (ax1, ax2) = plt.subplots(1, 2)
    for model_1d, axis_name, ax, calc_hit in zip([x, y], ["X", "Y"], [ax1, ax2], model_2d.calc_hit_2D_erfinv()):
        title = (
            f"{axis_name} axis 1D charge distribution."
            f"\n Real hit at {model_1d.hit_pos:2.3f} μm."
            f"Calculated hit at {calc_hit:2.3f} μm"
        )
        model_1d.set_plt_axis_distribution(ax, title, fig_size)

    fig, axes = plt.subplots(1, 2)
    plot_prob(axes)
    plt.show()
