#type: ignore
import matplotlib.pyplot as plt
import numpy as np

from detectors import Detector, ALL_DETECTORS, SI_DETECTORS, CDTE_DETECTORS

def bar_plots(detector: Detector, hit_posistions, means_ideal, means_taylor, means_lut) -> None:
    y = np.arange(len(hit_posistions))
    width = 0.3  # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.barh(y + width, means_ideal, width, label='Ideal')
    rects2 = ax.barh(y, means_taylor, width, label='Taylor')
    rects3 = ax.barh(y - width, means_lut, width, label='Lut')
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xlabel('Calculated hit position [μm]')
    ax.set_ylabel('Real hit position [μm]')
    ax.set_title(f'Hit calculating methods comparison for {detector.name}')
    ax.set_yticks(y, hit_posistions)
    ax.legend()

    ax.bar_label(rects1, padding=3, fmt="%.2f")
    ax.bar_label(rects2, padding=3, fmt="%.2f")
    ax.bar_label(rects3, padding=3, fmt="%.2f")

    fig.tight_layout()

def main() -> None:
    TIMES = 10
    for detector in SI_DETECTORS:
        hit_posistions = range(0, detector.pixel_size+1, 10)
        means_ideal = []
        means_taylor = []
        means_lut = []
        for pos in hit_posistions:
            result = detector.hit_times(pos, TIMES, lut_size=20, taylor_order=10)
            mean_ideal, mean_taylor, mean_lut = result
            means_ideal.append(mean_ideal)
            means_taylor.append(mean_taylor)
            means_lut.append(mean_lut)
            # print(f"### {pos=}um {detector.name} ###\n{mean_ideal=:.5f}\n{mean_taylor=:.5f}\n{mean_lut=:.5f}")

        bar_plots(detector, hit_posistions, means_ideal, means_taylor, means_lut)
    plt.show()



if __name__ == "__main__":
    main()
