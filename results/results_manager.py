import argparse
import sys
from pathlib import Path
from tkinter import filedialog as fd

import matplotlib.pyplot as plt
import pandas as pd
import yaml

# append charge_sharing_model directory
sys.path.append(str(Path(sys.path[0]).parents[0]))

from simulations.sample_1d import Sample1D


class ResultsMgr:
    CSV_TYPES = [("CSV", "*.csv")]
    INITIALDIR = Path(__file__).resolve().parent
    RESULTS_RAW = Path("results/raw")
    RESULTS_MEAN = Path("results/mean")
    RESULTS_ABS_ERR = Path("results/abs_err")
    SETTINGS = Path("results/settings.yaml")
    SEP = ";"

    def __init__(self) -> None:
        self.args = self.parse_args()
        self.plot: bool = self.args.plot
        self.gen: bool = self.args.gen
        with self.SETTINGS.open(encoding="utf8") as f:
            self.settings = yaml.safe_load(f)

    def parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-g", "--gen", action="store_true", help="Generates other data")
        parser.add_argument(
            "-p", "--plot", action="store_true", help="Plots selected result file or files"
        )
        return parser.parse_args()

    def gen_mean(self, src: Path, dest: Path) -> None:
        for file in src.iterdir():
            df = pd.read_csv(file, sep=self.SEP, header=None)
            df_mean = pd.DataFrame(df.mean()).T

            meanfile = dest.joinpath(file.name)
            dest.mkdir(parents=True, exist_ok=True)
            df_mean.to_csv(meanfile, sep=self.SEP, index=False, header=False)

    def gen_abs_err(self, src: Path, dest: Path) -> None:
        for file in src.iterdir():
            df = pd.read_csv(file, sep=self.SEP, header=None)
            df_abs_err = pd.DataFrame(df - df.columns).abs()

            abs_err_file = dest.joinpath(file.name)
            dest.mkdir(parents=True, exist_ok=True)
            df_abs_err.to_csv(abs_err_file, sep=self.SEP, index=False, header=False)

    def read_dialog(self) -> tuple[list[Path], list[pd.DataFrame]]:
        filenames = fd.askopenfilenames(filetypes=self.CSV_TYPES, initialdir=self.INITIALDIR)
        if not filenames:
            sys.exit("No input given")
        dfs = [pd.read_csv(file, sep=self.SEP, header=None) for file in filenames]
        paths = [Path(file) for file in filenames]
        return paths, dfs

    def title_from_samples(self) -> str:
        return self.samples[0].model.detector.get_str()

    def get_data(self) -> pd.DataFrame:
        paths, dfs = self.read_dialog()
        filenames = [path.stem for path in paths]
        [print(file) for file in filenames]
        self.samples = [Sample1D.from_file(file) for file in filenames]
        new_dfs: list[pd.DataFrame] = []
        for df in dfs:
            if df.shape[0] > 1:
                df = pd.DataFrame(df.mean()).T
            new_dfs.append(df)
        concat_df = pd.concat(new_dfs, ignore_index=True)
        concat_df: pd.DataFrame = concat_df.set_axis(self.settings["labels"])
        return concat_df.T

    def plot_raw(self, ax: plt.Axes) -> None:
        df = self.get_data()
        df.plot(ax=ax)
        title = self.settings["title"] if self.settings["title"] else self.title_from_samples()
        ax.set_title(title)
        ax.set_ylabel(self.settings["raw"]["ylabel"])
        ax.set_xlabel(self.settings["raw"]["xlabel"])
        ax.set_ylim(0, self.settings["raw"]["ylim"])

    def plot_err(self, ax: plt.Axes) -> None:
        df = self.get_data()
        df.plot(ax=ax)
        ax.set_ylabel(self.settings["err"]["ylabel"])
        ax.set_xlabel(self.settings["err"]["xlabel"])
        ax.set_ylim(0, self.settings["err"]["ylim"])

    def plot_result(self) -> None:
        fig, col = plt.subplots(2, 1, constrained_layout=True)
        self.plot_raw(col[0])
        self.plot_err(col[1])
        fig.suptitle(self.settings["suptitle"], weight="bold")
        plt.show()

    def run(self):
        if self.gen:
            # self.gen_mean(self.RESULTS_RAW, self.RESULTS_MEAN)
            self.gen_abs_err(self.RESULTS_RAW, self.RESULTS_ABS_ERR)
            print("Generation data done.")
        if self.plot:
            self.plot_result()


if __name__ == "__main__":
    script = ResultsMgr()
    script.run()
