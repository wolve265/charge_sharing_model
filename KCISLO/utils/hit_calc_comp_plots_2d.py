#type: ignore
import matplotlib.pyplot as plt
import numpy as np


def plots(ax: list[plt.Axes], hit_positions, means_list, labels) -> None:
    ax[0].set_title("X axis")
    ax[1].set_title("Y axis")
    for i, (means_list_ax, hit_positions_ax) in enumerate(zip(means_list, hit_positions)):
        for means, label in zip(means_list_ax, labels):
            ax[i].plot(hit_positions_ax, means, label=label)
        ax[i].plot(hit_positions_ax, hit_positions_ax, label="Ideal")
        ax[i].set_xlabel('Real hit position [μm]')
        ax[i].set_ylabel('Calculated hit position [μm]')
        ax[i].set_ylim(0, 120)
        ax[i].legend(loc="upper left", fontsize="small")

def err_plots(ax: list[plt.Axes], hit_positions, means_list, labels) -> None:
    for i, (means_list_ax, hit_positions_ax) in enumerate(zip(means_list, hit_positions)):
        for means, label in zip(means_list_ax, labels):
            ax[i].plot(hit_positions_ax, means, label=label)
        ax[i].set_xlabel('Real hit position [μm]')
        ax[i].set_ylabel('Absolute error [μm]')
        ax[i].set_ylim(0, 50)
        ax[i].legend(loc="upper right", fontsize="small")

def bar_plots(ax: plt.Axes, hit_positions, means_erfinv, means_taylor, means_lut) -> None:
    """A little outdated"""

    y = np.arange(len(hit_positions))
    width = 0.3  # the width of the bars
    rects1 = ax.barh(y + width, means_erfinv, width, label='Ideal')
    rects2 = ax.barh(y, means_taylor, width, label='Taylor')
    rects3 = ax.barh(y - width, means_lut, width, label='Lut')
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xlabel('Calculated hit position [μm]')
    ax.set_ylabel('Real hit position [μm]')
    ax.set_yticks(y, hit_positions)
    ax.legend()

    ax.bar_label(rects1, padding=3, fmt="%.2f")
    ax.bar_label(rects2, padding=3, fmt="%.2f")
    ax.bar_label(rects3, padding=3, fmt="%.2f")
