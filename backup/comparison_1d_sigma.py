# type: ignore
import time
import matplotlib.pyplot as plt
import numpy as np

from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor

from models.model_1d import PixelChargeSharingModel1D
from detectors.paper import Paper
from utils.hit_calc_comp_plots_1d import plots, err_plots

"""
The script is used to compare dr Krzyzanowska's paper detectors
"""

TIMES = 1000
STEP = 1
LUT_SIZE = 50

SIGMA_STEP = 10
SIGMA_RANGE = np.arange(0.15, 0.55+0.01, 0.10)

MODEL = PixelChargeSharingModel1D
FUNC = MODEL.calc_hit_1D_lut

def hit(pos: int, detector: dict):
    """
    Task which creates model with detector data
    hits model at specified position
    calculates hit position and error with different methods
    Returns list of hits and errors
    """
    calc_hits = []
    calc_errors = []
    for sigma_multiplier in SIGMA_RANGE:
        new_sigma = detector["pixel_size"] * sigma_multiplier
        detector["charge_cloud_sigma"] = new_sigma
        model = MODEL(**detector)
        model.hit(pos)
        calc_hits.append(calc_hit := FUNC(model, LUT_SIZE))
        calc_errors.append(abs(calc_hit - pos))
    # print(pos, calc_hit)
    return calc_hits, calc_errors

def hit_times(pos: int, detector: dict, times: int):
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
    # print(calculated_hits)
    return np.mean(calc_hits, axis=0), np.mean(calc_errors, axis=0)

def hit_and_calc(detector: dict):
    """
    Task which runs processes for every hit position (of detector)
    returns lists which are compatible with plots from utils
    """
    calc_hits = []
    calc_errors = []
    hit_posistions = range(0, detector["pixel_size"]+1, STEP)
    detectors = [detector] * len(hit_posistions)
    times = [TIMES] * len(hit_posistions)
    with ProcessPoolExecutor() as executor:
        for calc_hit, calc_error in executor.map(hit_times, hit_posistions, detectors, times, chunksize=20):
            # calc_hit is [method_1, ..., method_n]
            calc_hits.append(calc_hit)
            calc_errors.append(calc_error)
    # transpose calculations
    calc_hits = np.array(calc_hits).T.tolist()
    calc_errors = np.array(calc_errors).T.tolist()
    return calc_hits, calc_errors


def main() -> None:
    """
    Main function runs processes for every detector.
    After getting data creates figures and saves them
    """
    detectors = [Paper.one, Paper.two, Paper.three, Paper.four]
    # detectors = [Paper.one]

    with ProcessPoolExecutor() as executor:
        for num, (result, detector) in enumerate(zip(executor.map(hit_and_calc, detectors), detectors)):
            calc_hits, calc_errors = result
            fig, col = plt.subplots(2, 1, constrained_layout=True)
            labels = [f"cloud σ {sigma_mult*detector['pixel_size']:.2f}μm" for sigma_mult in SIGMA_RANGE]
            hit_posistions = range(0, detector["pixel_size"]+1, STEP)
            plots(col[0], hit_posistions, calc_hits, labels)
            err_plots(col[1], hit_posistions, calc_errors, labels)
            col[0].set_title(Paper.get_str_cloud_test(detector))
            fig.suptitle(f"Calculating methods comparison after {TIMES} hits", weight="bold")
            fig.savefig(f"{num+1}.png")


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    t = end - start
    print(f"Script took {t:.3f} seconds")
