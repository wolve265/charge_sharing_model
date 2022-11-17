# type: ignore
import os, sys
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

    probs = model_2d.get_probabilities()
    probs_noise = []
    # Generate noise for each pixel. Unit in electrons
    for prob in probs:
        probs_noise.append(prob + norm.rvs(0, 50, 1)[0])

    def plot_prob(probs, probs_name: str, axes: list[plt.Axes]):
        (ax1, ax2) = axes

        xprobs_list = [
            probs[0] + probs[3] + probs[6], # left
            probs[1] + probs[4] + probs[7], # mid
            probs[2] + probs[5] + probs[8], # right
        ]
        yprobs_list = [
            probs[0] + probs[1] + probs[2], # bottom
            probs[3] + probs[4] + probs[5], # mid
            probs[6] + probs[7] + probs[8], # top
        ]

        title = f"X axis electron count integral {probs_name}"
        x.set_plt_axis_charge_integral(ax1, title, xprobs_list, fig_size_integral)
        title = f"y axis electron count integral {probs_name}"
        y.set_plt_axis_charge_integral(ax2, title, yprobs_list, fig_size_integral)

    ax = plt.axes()
    model_2d.set_plt_axis_birds_eye_view(ax, f"Bird's eye view of post hit electron collection")

    fig, (ax1, ax2) = plt.subplots(1, 2)
    for model_1d, axis_name, ax in zip([x, y], ["X", "Y"], [ax1, ax2]):
        title = f"{axis_name} axis 1D charge distribution.\n Real hit at {model_1d.hit_pos:2.3f} μm. Calculated hit at {model_1d.calc_hit_1D_erfinv():2.3f} μm"
        model_1d.set_plt_axis_distribution(ax, title, fig_size)

    fig, (ax12, ax34) = plt.subplots(2, 2)
    for prob, prob_name, axes in zip([probs, probs_noise], ["", "with noise"], [ax12, ax34]):
        plot_prob(prob, prob_name, axes)
    plt.show()
