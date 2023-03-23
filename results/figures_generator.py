import argparse
import sys
from pathlib import Path
from tkinter import filedialog as fd

import matplotlib.pyplot as plt
import pandas as pd
import yaml
from matplotlib.figure import Figure

# append charge_sharing_model directory
sys.path.append(str(Path(sys.path[0]).parents[0]))

from simulations.sample_1d import Sample1D


class FiguresGenerator:
    CSV_TYPES = [("CSV", "*.csv")]
    INITIALDIR = Path(__file__).resolve().parent
    FIGURES = Path("figures")
    RESULTS_RAW = Path("results/raw")
    RESULTS_ABS_ERR = Path("results/abs_err")
    SETTINGS = Path("results/fig_settings.yaml")
    SEP = ";"

    def __init__(self) -> None:
        self.args = self.parse_args()
        self.plot: bool = self.args.plot
        with self.SETTINGS.open(encoding="utf8") as f:
            self.settings = yaml.safe_load(f)

    def parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-p",
            "--plot",
            action="store_true",
            help="Plots selected result file or files",
        )
        return parser.parse_args()

    def read_dialog(self) -> list[Path]:
        filenames = fd.askopenfilenames(
            filetypes=self.CSV_TYPES, initialdir=self.INITIALDIR
        )
        if not filenames:
            sys.exit("No input given")
        files = [Path(file) for file in filenames]
        [print(file) for file in files]
        return files

    def title_from_samples(self) -> str:
        return self.samples[0].model.detector.get_str()

    def get_data(self, files: list[Path] | None) -> pd.DataFrame:
        if files is None:
            files = self.read_dialog()
        dfs = [pd.read_csv(file, sep=self.SEP, header=None) for file in files]
        filenames = [path.stem for path in files]
        self.samples = [Sample1D.from_file(file) for file in filenames]
        new_dfs: list[pd.DataFrame] = []
        for df in dfs:
            if df.shape[0] > 1:
                df = pd.DataFrame(df.mean()).T
            new_dfs.append(df)
        concat_df = pd.concat(new_dfs, ignore_index=True)
        concat_df: pd.DataFrame = concat_df.set_axis(self.settings["labels"])
        return concat_df.T

    def plot_raw(self, ax: plt.Axes, df: pd.DataFrame) -> None:
        df.plot(ax=ax)
        title = (
            self.settings["title"]
            if self.settings["title"]
            else self.title_from_samples()
        )
        ax.set_title(title)
        ax.set_ylabel(self.settings["raw"]["ylabel"])
        ax.set_xlabel(self.settings["raw"]["xlabel"])
        ax.set_ylim(0, self.samples[0].model.detector.pixel_size + 10)

    def plot_err(self, ax: plt.Axes, df: pd.DataFrame) -> None:
        df.plot(ax=ax)
        ax.set_ylabel(self.settings["err"]["ylabel"])
        ax.set_xlabel(self.settings["err"]["xlabel"])
        ax.set_ylim(0, self.settings["err"]["ylim"] + 5)

    def make_figure(
        self, files: list[Path] | None = None, plot: bool = False
    ) -> Figure:
        fig, col = plt.subplots(2, 1, constrained_layout=True)
        if files is not None:
            raw_files = [self.RESULTS_RAW / file for file in files]
        df = self.get_data(raw_files)
        self.plot_raw(col[0], df)
        if files is not None:
            err_files = [self.RESULTS_ABS_ERR / file for file in files]
        df = self.get_data(err_files)
        self.plot_err(col[1], df)
        fig.suptitle(self.settings["suptitle"], weight="bold")
        if plot:
            plt.show()
        return fig

    def run(self):
        for figure in self.settings["figures"]:
            fig = self.make_figure(figure["files"], plot=self.plot)
            fig.savefig(self.FIGURES / figure["name"])


if __name__ == "__main__":
    script = FiguresGenerator()
    script.run()
