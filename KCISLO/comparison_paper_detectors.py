#type: ignore
import time
import matplotlib.pyplot as plt
import numpy as np

from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor

from models.model_1d import PixelChargeSharingModel1D
from detectors.paper import Paper
from utils.hit_calc_comp_plots import plots, err_plots

"""
Script used to compare dr Krzyzanowska's paper detectors
"""

TIMES = 10000
STEP = 1
LUT_SIZE = 50
TAYLOR_ORDER = 10

def hit(pos: int, detector: dict):
    model = PixelChargeSharingModel1D(**detector)
    model.hit(pos)
    calc_hits = []
    calc_errors = []
    calc_hits.append(calc_hit := model.calc_hit_1D_taylor(TAYLOR_ORDER))
    calc_errors.append(abs(calc_hit - pos))
    calc_hits.append(calc_hit := model.calc_hit_1D_lut(LUT_SIZE))
    calc_errors.append(abs(calc_hit - pos))
    return calc_hits, calc_errors

def hit_times(pos: int, detector: dict, times: int):
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
    detectors = [Paper.one, Paper.two, Paper.three, Paper.four]
    # detectors = [Paper.one]

    with ProcessPoolExecutor() as executor:
        for num, (result, detector) in enumerate(zip(executor.map(hit_and_calc, detectors), detectors)):
            calc_hits, calc_errors = result
            fig, col = plt.subplots(2, 1, constrained_layout=True)
            labels = [f"Taylor (order={TAYLOR_ORDER})", f"LUT (size={LUT_SIZE})"]
            hit_posistions = range(0, detector["pixel_size"]+1, STEP)
            plots(col[0], hit_posistions, calc_hits, labels)
            err_plots(col[1], hit_posistions, calc_errors, labels)
            col[0].set_title(Paper.get_str(detector))
            fig.suptitle(f"Calculating methods comparison after {TIMES} hits", weight="bold")
            fig.savefig(f"{num+1}.png")


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    t = end - start
    print(f"Script took {t:.3f} seconds")
