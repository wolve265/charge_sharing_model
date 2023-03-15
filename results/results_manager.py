import argparse
import sys
from pathlib import Path
from tkinter import filedialog as fd

import matplotlib.pyplot as plt
import pandas as pd

# append charge_sharing_model directory
sys.path.append(str(Path(sys.path[0]).parents[0]))


class ResultsMgr:
    CSV_TYPES = [
        ("CSV", "*.csv"),
    ]
    INITIALDIR = Path(__file__).resolve().parent
    RESULTS_RAW = Path("results/raw")
    RESULTS_MEAN = Path("results/mean")
    DOT = Path("dot")
    COMMA = Path("comma")
    SEP = ";"

    def __init__(self) -> None:
        self.args = self.parse_args()
        self.plot: bool = self.args.plot
        self.gen: bool = self.args.gen

    def parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-g", "--gen", action="store_true", help="Generates comma, mean data")
        parser.add_argument(
            "-p", "--plot", action="store_true", help="Plots selected result file or files"
        )
        return parser.parse_args()

    def gen_comma(self, basedir: Path) -> None:
        dotdir = basedir / self.DOT
        commadir = basedir / self.COMMA
        for dotfile in dotdir.iterdir():
            content = dotfile.read_text().replace(".", ",")

            commafile = commadir.joinpath(dotfile.name)
            commadir.mkdir(parents=True, exist_ok=True)
            commafile.write_text(content)

    def gen_mean(self, src: Path, dest: Path) -> None:
        for file in src.iterdir():
            df = pd.read_csv(file, sep=self.SEP, header=None)
            df_mean = pd.DataFrame(df.mean()).T

            meanfile = dest.joinpath(file.name)
            dest.mkdir(parents=True, exist_ok=True)
            df_mean.to_csv(meanfile, sep=self.SEP, index=False, header=False)

    def read_dialog(self) -> tuple[list[Path], list[pd.DataFrame]]:
        filenames = fd.askopenfilenames(filetypes=self.CSV_TYPES, initialdir=self.INITIALDIR)
        if not filenames:
            sys.exit("No input given")
        dfs = [pd.read_csv(file, sep=self.SEP, header=None) for file in filenames]
        paths = [Path(file) for file in filenames]
        return paths, dfs

    def plot_result(self) -> None:
        paths, dfs = self.read_dialog()
        filenames = [path.stem for path in paths]
        new_dfs: list[pd.DataFrame] = []
        for df in dfs:
            if df.shape[0] > 1:
                df = pd.DataFrame(df.mean()).T
            new_dfs.append(df)
        concat_df = pd.concat(new_dfs, ignore_index=True)
        concat_df.set_axis(filenames, copy=False)
        print(concat_df)
        concat_df.T.plot()
        plt.show()

    def run(self):
        if self.gen:
            # self.gen_comma(self.RESULTS_RAW)
            self.gen_mean(self.RESULTS_RAW / self.DOT, self.RESULTS_MEAN / self.DOT)
            # self.gen_comma(self.RESULTS_MEAN)
            print("Generation data done.")
        if self.plot:
            self.plot_result()


if __name__ == "__main__":
    script = ResultsMgr()
    script.run()
