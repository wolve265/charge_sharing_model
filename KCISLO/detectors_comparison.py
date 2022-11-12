#type: ignore
import matplotlib.pyplot as plt
import numpy as np

from detectors import Detector, ALL_DETECTORS, SI_DETECTORS, CDTE_DETECTORS

def bar_plots(detector: Detector, hit_positions, means_erfinv, means_taylor, means_lut) -> None:
    y = np.arange(len(hit_positions))
    width = 0.3  # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.barh(y + width, means_erfinv, width, label='Ideal')
    rects2 = ax.barh(y, means_taylor, width, label='Taylor')
    rects3 = ax.barh(y - width, means_lut, width, label='Lut')
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xlabel('Calculated hit position [μm]')
    ax.set_ylabel('Real hit position [μm]')
    ax.set_title(f'Hit calculating methods comparison for {detector.name}')
    ax.set_yticks(y, hit_positions)
    ax.legend()

    ax.bar_label(rects1, padding=3, fmt="%.2f")
    ax.bar_label(rects2, padding=3, fmt="%.2f")
    ax.bar_label(rects3, padding=3, fmt="%.2f")

    fig.tight_layout()

def plots(ax: plt.Axes, detector: Detector, hit_positions, means_list, labels) -> None:
    for means, label in zip(means_list, labels):
        ax.plot(hit_positions, means, label=label)
    ax.plot(hit_positions, hit_positions, label="Real")
    ax.set_xlabel('Real hit position [μm]')
    ax.set_ylabel('Calculated hit position [μm]')
    ax.set_title(f'{detector.name}')
    ax.legend()

def err_plots(ax: plt.Axes, detector: Detector, hit_positions, means_list, labels) -> None:
    for means, label in zip(means_list, labels):
        ax.plot(hit_positions, [abs(mean-hit) for (mean, hit) in zip(means, hit_positions)], label=label)
    ax.set_xlabel('Real hit position [μm]')
    ax.set_ylabel('Absolute error [μm]')
    ax.set_title(f'Error: {detector.name}')
    ax.legend()

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
