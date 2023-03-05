#type: ignore
import time
import matplotlib.pyplot as plt
import numpy as np

from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor

from models.model_1d import PixelChargeSharingModel1D
from models.model_int import PixelChargeSharingModel1DInt
from detectors.paper import Paper
from utils.hit_calc_comp_plots_1d import plots, err_plots

"""
The script is used to compare dr Krzyzanowska's paper detectors
"""

TIMES = 1000
STEP = 1
LUT_SIZE = 50
TAYLOR_ORDER = 10

# MODEL = PixelChargeSharingModel1D
MODEL = PixelChargeSharingModel1DInt
FUNC_ERFINV = MODEL.calc_hit_1D_erfinv
FUNC_TAYLOR = MODEL.calc_hit_1D_taylor
FUNC_LUT = MODEL.calc_hit_1D_lut

DETECTOR = Paper
DETECTORS = [DETECTOR.one, DETECTOR.two, DETECTOR.three, DETECTOR.four]
# DETECTORS = [DETECTOR.one]

# TYPE_CONV_DICT = {
#     "num_type" : float,
#     "multiplier" : 1
# }

TYPE_CONV_DICT = {
    "num_type" : np.int16,
    "multiplier" : 100
}

def hit(pos: int, detector: dict):
    """
    Task which creates model with detector data
    hits model at specified position
    calculates hit position and error with different methods
    Returns list of hits and errors
    """
    model = MODEL(**detector, **TYPE_CONV_DICT)
    model.hit(pos)
    calc_hits = []
    calc_errors = []
    calc_hit = FUNC_ERFINV(model)
    calc_hits.append(calc_hit)
    calc_errors.append(abs(calc_hit - pos))
    calc_hit = FUNC_TAYLOR(model, TAYLOR_ORDER)
    calc_hits.append(calc_hit)
    calc_errors.append(abs(calc_hit - pos))
    calc_hit = FUNC_LUT(model, LUT_SIZE) / TYPE_CONV_DICT["multiplier"]
    calc_hits.append(calc_hit)
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
    detectors = DETECTORS

    with ProcessPoolExecutor() as executor:
        for num, (result, detector) in enumerate(zip(executor.map(hit_and_calc, detectors), detectors)):
            calc_hits, calc_errors = result
            fig, col = plt.subplots(2, 1, constrained_layout=True)
            labels = [
                f"float Erfinv",
                f"float Taylor (order={TAYLOR_ORDER})",
                f"{TYPE_CONV_DICT['num_type'].__name__} LUT (size={LUT_SIZE})",
            ]
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
