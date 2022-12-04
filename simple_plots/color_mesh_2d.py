# type: ignore
import os
import sys
import time
from itertools import product

import matplotlib.pyplot as plt
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from models.model_2d import PixelChargeSharingModel2D
from utils.hit_calc_comp_plots_2d import colorbar_plot

def vector_length(a: tuple[float, float], b: tuple[float, float]) -> float:
    ax, ay = a
    bx, by = b
    return np.sqrt((bx - ax)**2 + (by - ay)**2)

STEP = 10
TIMES = 1

def main() -> None:

    detector = {
        "pixel_size": 75,
        "charge_cloud_sigma": 25,
        "num_of_charges": 2200,
        "noise_sigma": 50,
    }

    y_arr = [yi for yi in range(0, detector["pixel_size"]+1, STEP)]
    x_arr = [xi for xi in range(0, detector["pixel_size"]+1, STEP)]

    errors = np.empty((len(y_arr), len(x_arr)))
    for (xi, xval), (yi, yval) in product(enumerate(x_arr), enumerate(y_arr)):
        model_2d = PixelChargeSharingModel2D(**detector)
        model_2d.hit(xval, yval)
        result = model_2d.calc_hit_2D_erfinv()
        error = vector_length(result, (xval, yval))
        errors[yi, xi] = error


    fig, ax = plt.subplots()
    fig.suptitle(f"Cartesian errors of hit calculation after {TIMES} hits")
    colorbar_plot(fig, ax, x_arr, y_arr, errors, "Erfinv approx")
    fig.savefig("1.png")
    # plt.show()


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    t = end - start
    print(f"Script took {t:.3f} seconds")
