# type: ignore
import os
import sys
from itertools import product

import matplotlib.pyplot as plt
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from models.model_2d import PixelChargeSharingModel2D

def vector_length(a: tuple[float, float], b: tuple[float, float]) -> float:
    ax, ay = a
    bx, by = b
    return np.sqrt((bx - ax)**2 + (by - ay)**2)


if __name__ == "__main__":
    STEP = 1
    PIXEL_SIZE = 75
    NUM_OF_CHARGES = 2200
    CHARGE_CLOUD_SIGMA = 25
    NOISE_SIGMA = 50

    hit_pos = (35, 60)
    fig_size = 40
    fig_size_integral = 1800

    model_2d = PixelChargeSharingModel2D(
        PIXEL_SIZE, NUM_OF_CHARGES, CHARGE_CLOUD_SIGMA, NOISE_SIGMA
    )

    x_arr = [xi for xi in range(0, PIXEL_SIZE+1, STEP)]
    y_arr = [xi for xi in range(0, PIXEL_SIZE+1, STEP)]

    errors = np.empty((len(x_arr), len(y_arr)))
    for (xi, xval), (yi, yval) in product(enumerate(x_arr), enumerate(y_arr)):
        model_2d.hit(xval, yval)
        result = model_2d.calc_hit_2D_erfinv()
        error = vector_length(result, (xval, yval))
        errors[yi, xi] = error


    fig, ax = plt.subplots()
    im = ax.pcolormesh(x_arr, y_arr, errors)
    fig.colorbar(im, ax=ax)
    plt.show()
