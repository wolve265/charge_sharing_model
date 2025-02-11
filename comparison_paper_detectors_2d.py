#type: ignore
import time
import matplotlib.pyplot as plt
import numpy as np

from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor

from models.model_2d import PixelChargeSharingModel2D
from detectors.paper import Paper
from utils.hit_calc_comp_plots_2d import plots, err_plots

"""
The script is used to compare dr Krzyzanowska's paper detectors
"""

TIMES = 10
STEP = 1
LUT_SIZE = 50
TAYLOR_ORDER = 10

def calc_error(tup1: tuple[float, float], tup2: tuple[float, float]) -> tuple[float, float]:
    return abs(tup1[0] - tup2[0]), abs(tup1[1] - tup2[1])

def hit(pos: tuple[int, int], detector: dict):
    """
    Task which creates model with detector data
    hits model at specified position
    calculates hit position and error with different methods
    Returns list of hits and errors
    """
    model = PixelChargeSharingModel2D(**detector)
    model.hit(*pos)
    calc_hits = []
    calc_errors = []
    calc_hits.append(calc_hit := model.calc_hit_2D_erfinv())
    calc_errors.append(calc_error(calc_hit, pos))
    calc_hits.append(calc_hit := model.calc_hit_2D_taylor(TAYLOR_ORDER))
    calc_errors.append(calc_error(calc_hit, pos))
    calc_hits.append(calc_hit := model.calc_hit_2D_lut(LUT_SIZE))
    calc_errors.append(calc_error(calc_hit, pos))
    # print(pos, calc_hit)
    return calc_hits, calc_errors

def hit_times(pos: tuple[int, int], detector: dict, times: int):
    """
    Task which runs 'hit task' specified number of times
    calculates the mean of hits and errors
    and returns them
    """
    calc_hits = []
    calc_errors = []
    positions = [pos] * times
    detectors = [detector] * times
    # with ThreadPoolExecutor() as executor:
    #     for result in executor.map(hit, positions, detectors):
    #         calculated_hits.append(result)
    for calc_hit, calc_error in map(hit, positions, detectors):
        calc_hits.append(calc_hit)
        calc_errors.append(calc_error)
    return np.mean(calc_hits, axis=0), np.mean(calc_errors, axis=0)

def hit_and_calc(detector: dict):
    """
    Task which runs processes for every hit position (of detector)
    returns lists which are compatible with plots from utils
    """
    calc_hits = []
    calc_errors = []
    hit_posistions = [(i, i) for i in range(0, detector["pixel_size"]+1, STEP)]
    detectors = [detector] * len(hit_posistions)
    times = [TIMES] * len(hit_posistions)
    with ProcessPoolExecutor() as executor:
        for calc_hit, calc_error in executor.map(hit_times, hit_posistions, detectors, times, chunksize=20):
            # calc_hit is [method_1:(x,y), ..., method_n:(x,y)]
            calc_hits.append(calc_hit)
            calc_errors.append(calc_error)
    # transpose calculations
    calc_hits = np.array(calc_hits).T.tolist()
    calc_errors = np.array(calc_errors).T.tolist()
    hit_posistions = np.array(hit_posistions).T.tolist()
    return calc_hits, calc_errors, hit_posistions


def main() -> None:
    """
    Main function runs processes for every detector.
    After getting data creates figures and saves them
    """
    detectors = [Paper.one, Paper.two, Paper.three, Paper.four]
    # detectors = [Paper.one]

    with ProcessPoolExecutor() as executor:
        for num, (result, detector) in enumerate(zip(executor.map(hit_and_calc, detectors), detectors)):
            calc_hits, calc_errors, hit_posistions = result
            fig, axes = plt.subplots(2, 2, constrained_layout=True)
            labels = [
                f"Erfinv",
                f"Taylor (order={TAYLOR_ORDER})",
                f"LUT (size={LUT_SIZE})",
            ]
            plots(axes[0], hit_posistions, calc_hits, labels)
            err_plots(axes[1], hit_posistions, calc_errors, labels)
            fig.suptitle(
                rf"$\mathbf{{Calculating \ methods \ comparison \ after \ {TIMES} \ hits}}$"
                "\n"
                f"{Paper.get_str(detector)}",
            )
            fig.set_size_inches(12.8, 6.4)
            fig.savefig(f"{num+1}.png")


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    t = end - start
    print(f"Script took {t:.3f} seconds")
