#type: ignore
import time
import matplotlib.pyplot as plt
import numpy as np

from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor

from models.model_1d import PixelChargeSharingModel1D
from detectors.paper import Paper
from detectors.lut_testing import LutTesting
from utils.hit_calc_comp_plots_1d import plots, err_plots

"""
The script is used to compare dr Krzyzanowska's paper detectors
"""

TIMES = 1000
STEP = 1
LUT_SIZE = 50
LUT_STEP = 10
LUT_RANGE = range(5, LUT_SIZE+1, LUT_STEP)

MODEL = PixelChargeSharingModel1D
FUNC = MODEL.calc_hit_1D_lut

DETECTOR = LutTesting
DETECTORS = [DETECTOR.one, DETECTOR.two, DETECTOR.three, DETECTOR.four, DETECTOR.five]
# DETECTORS = [DETECTOR.one]

def hit(pos: int, detector: dict):
    """
    Task which creates model with detector data
    hits model at specified position
    calculates hit position and error with different methods
    Returns list of hits and errors
    """
    model = MODEL(**detector)
    model.hit(pos)
    calc_hits = []
    calc_errors = []
    for lut_size in LUT_RANGE:
        calc_hits.append(calc_hit := FUNC(model, lut_size))
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

    with ProcessPoolExecutor() as executor:
        for num, (result, detector) in enumerate(zip(executor.map(hit_and_calc, DETECTORS), DETECTORS)):
            calc_hits, calc_errors = result
            fig, col = plt.subplots(2, 1, constrained_layout=True)
            labels = [f"LUT (size={lut_size})" for lut_size in LUT_RANGE]
            hit_posistions = range(0, detector["pixel_size"]+1, STEP)
            plots(col[0], hit_posistions, calc_hits, labels)
            err_plots(col[1], hit_posistions, calc_errors, labels)
            col[0].set_title(DETECTOR.get_str(detector))
            fig.suptitle(f"Calculating methods comparison after {TIMES} hits", weight="bold")
            fig.savefig(f"{num+1}.png")


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    t = end - start
    print(f"Script took {t:.3f} seconds")
