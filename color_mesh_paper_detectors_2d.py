#type: ignore
import time
import matplotlib.pyplot as plt
import numpy as np

from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
from itertools import product

from models.model_2d import PixelChargeSharingModel2D
from detectors.paper import Paper
from utils.hit_calc_comp_plots_2d import colorbar_plot

"""
The script is used to compare dr Krzyzanowska's paper detectors
"""

"""
| TIMES | TIME  |
| 1     | 120s  |
| 10    | 20m   |
| 100   | 3h15m |
| 1000  | 33h   |
"""
TIMES = 1
STEP = 1
LUT_SIZE = 50
TAYLOR_ORDER = 10

def calc_error(a: tuple[float, float], b: tuple[float, float]) -> float:
    ax, ay = a
    bx, by = b
    return np.sqrt((bx - ax)**2 + (by - ay)**2)

def hit(pos: tuple[int, int], detector: dict):
    """
    Task which creates model with detector data
    then hits model at specified position
    then calculates hit position and error with different methods
    Returns list errors
    """
    model = PixelChargeSharingModel2D(**detector)
    model.hit(*pos)
    calc_errors = []
    calc_hit = model.calc_hit_2D_erfinv()
    calc_errors.append(calc_error(calc_hit, pos))
    calc_hit = model.calc_hit_2D_taylor(TAYLOR_ORDER)
    calc_errors.append(calc_error(calc_hit, pos))
    calc_hit = model.calc_hit_2D_lut(LUT_SIZE)
    calc_errors.append(calc_error(calc_hit, pos))
    # print(pos, calc_hit)
    return calc_errors

def hit_times(pos: tuple[int, int], detector: dict, times: int):
    """
    Task which runs 'hit task' specified number of times
    then calculates the mean errors and returns them
    """
    calc_errors = []
    positions = [pos] * times
    detectors = [detector] * times
    # with ThreadPoolExecutor() as executor:
    #     for result in executor.map(hit, positions, detectors):
    #         calculated_hits.append(result)
    for calc_error in map(hit, positions, detectors):
        calc_errors.append(calc_error)
    return np.mean(calc_errors, axis=0)

def hit_and_calc(detector: dict):
    """
    Task which runs processes for every hit position (of detector)
    returns lists which are compatible with plots from utils
    """
    calc_errors = []
    y_arr = [yi for yi in range(0, detector["pixel_size"]+1, STEP)]
    x_arr = [xi for xi in range(0, detector["pixel_size"]+1, STEP)]
    hit_positions = [pos for pos in product(x_arr, y_arr)]
    detectors = [detector] * len(hit_positions)
    times = [TIMES] * len(hit_positions)
    with ProcessPoolExecutor() as executor:
        for calc_error in executor.map(hit_times, hit_positions, detectors, times, chunksize=2000):
            # calc_hit is [method_1:(x,y), ..., method_n:(x,y)]
            calc_errors.append(calc_error)
    # transpose calculations
    calc_errors = np.array(calc_errors).T.tolist()
    new_calc_errors = []
    for calc_error_list in calc_errors:
        errors = np.empty((len(y_arr), len(x_arr)))
        for i, (x, y) in enumerate(product(x_arr, y_arr)):
            errors[y, x] = calc_error_list[i]
        new_calc_errors.append(errors)
    return new_calc_errors, x_arr, y_arr

def main() -> None:
    """
    Main function runs processes for every detector.
    After getting data creates figures and saves them
    """
    detectors = [Paper.one, Paper.two, Paper.three, Paper.four]
    # detectors = [Paper.one]
    titles = [
        f"Erfinv approx",
        f"Taylor approx (order={TAYLOR_ORDER})",
        f"LUT approx (size={LUT_SIZE})",
    ]

    with ProcessPoolExecutor() as executor:
        for num, (result, detector) in enumerate(zip(executor.map(hit_and_calc, detectors), detectors)):
            calc_errors, x_arr, y_arr = result
            fig, axes = plt.subplots(1, 3, constrained_layout=True)
            colorbar_plot(fig, axes, x_arr, y_arr, calc_errors, titles)
            fig.suptitle(
                rf"$\mathbf{{Cartesian \ errors \ of \ hit \ calculations \ after \ {TIMES} \ hits}}$"
                "\n"
                f"{Paper.get_str(detector)}",
            )
            fig.set_size_inches(14.4, 4.8)
            fig.savefig(f"{num+1}.png")


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    t = end - start
    print(f"Script took {t:.3f} seconds")
