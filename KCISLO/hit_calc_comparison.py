#type: ignore
import matplotlib.pyplot as plt
import numpy as np
import concurrent.futures
import time

from detectors import Detector, ALL_DETECTORS, SI_DETECTORS, CDTE_DETECTORS
from comparison_utils import plots, err_plots

def main() -> None:
    ORDERS = range(2, 50, 5)
    LUTS = range(52, 100, 5)
    TIMES = 1000
    STEP = 1
    fig, ax = plt.subplots(2, 2)

    detector = SI_DETECTORS[2]
    taylors = [[] for i in ORDERS]
    luts = [[] for i in ORDERS]
    hit_posistions = range(0, detector.pixel_size+1, STEP)

    with concurrent.futures.ProcessPoolExecutor() as executor:
        jobs_dict = dict()
        for job_order, (taylor_order, lut_size) in enumerate(zip(ORDERS, LUTS)):
            args = (hit_posistions, TIMES)
            kwargs = {"lut_size": 20, "taylor_order": taylor_order, "lut_size": lut_size}
            job = executor.submit(detector.hit_times_pos, *args, **kwargs)
            jobs_dict[job] = job_order

        for completed_job in concurrent.futures.as_completed(jobs_dict):
            job_order = jobs_dict[completed_job]
            results = completed_job.result()
            inner_taylors = []
            inner_luts = []
            for i, inner_result in enumerate(results):
                inner_taylors.append(inner_result[1])
                inner_luts.append(inner_result[2])
            inner_taylors = np.array(inner_taylors).T.tolist()
            inner_luts = np.array(inner_luts).T.tolist()
            taylors[job_order] = inner_taylors
            luts[job_order] = inner_luts

    labels_taylor = ORDERS
    labels_lut = LUTS
    plots(ax[0, 0], detector, hit_posistions, taylors, labels_taylor)
    print(err_plots(ax[1, 0], detector, hit_posistions, taylors, labels_taylor))
    plots(ax[0, 1], detector, hit_posistions, luts, labels_lut)
    print(err_plots(ax[1, 1], detector, hit_posistions, luts, labels_lut))

    fig.tight_layout()
    fig.suptitle("Hit calculating methods comparison for Si detectors")
    fig.set_size_inches(15, 10)
    plt.savefig("saved.png")
    # plt.show()


if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
    end_time = time.perf_counter()
    total_time = end_time - start_time
    print(f"Script took {total_time:.3f} seconds")
