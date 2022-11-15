#type: ignore
import matplotlib.pyplot as plt
import numpy as np

from detectors import Detector, ALL_DETECTORS, SI_DETECTORS, CDTE_DETECTORS
from comparison_utils import plots, err_plots

def main() -> None:
    TIMES = 10
    STEP = 10
    fig, ax = plt.subplots(2, 3)
    for detector, col in zip(SI_DETECTORS, np.array(ax).T):
        results = []
        hit_posistions = range(0, detector.pixel_size+1, STEP)
        for pos in hit_posistions:
            result = detector.hit_times(pos, TIMES, lut_size=20, taylor_order=10)
            results.append(result)
            # print(f"### {pos=}um {detector.name} ###\n{mean_erfinv=:.5f}\n{mean_taylor=:.5f}\n{mean_lut=:.5f}")
        results = np.array(results).T.tolist()

        # bar_plots(detector, hit_posistions, means_erfinv, means_taylor, means_lut)
        labels = ["Erfinv", "Taylor", "Lut"]
        plots(col[0], detector, hit_posistions, results, labels)
        err_plots(col[1], detector, hit_posistions, results, labels)
    fig.tight_layout()
    fig.suptitle("Hit calculating methods comparison for Si detectors")
    plt.show()


if __name__ == "__main__":
    main()
