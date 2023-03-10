import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# append charge_sharing_model directory
sys.path.append(str(Path(sys.path[0]).parents[0]))

from data_handling.csv_handler import CsvHandler


class ResultsMgr:
    RESULTS_RAW = Path("results/raw")
    RESULTS_MEAN = Path("results/mean")
    DOT = Path("dot")
    COMMA = Path("comma")

    def __init__(self) -> None:
        self.csv_handler = CsvHandler(sep=";")

        self.args = self.parse_args()
        self.plot: bool = self.args.plot
        self.gen: bool = self.args.gen

    def parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-g", "--gen", action="store_true", help="Generates comma, mean data")
        parser.add_argument("-p", "--plot", action="store_true", help="Plots selected result file")
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
            df = self.csv_handler.read(file)
            df_mean = pd.DataFrame(df.mean()).T

            meanfile = dest.joinpath(file.name)
            dest.mkdir(parents=True, exist_ok=True)
            self.csv_handler.write(meanfile, df_mean)

    def plot_result(self) -> None:
        df = self.csv_handler.read(dialog=True)
        if df.shape[0] > 1:
            df = pd.DataFrame(df.mean()).T
        df.T.plot()
        plt.show()

    def run(self):
        if self.gen:
            self.gen_comma(self.RESULTS_RAW)
            self.gen_mean(self.RESULTS_RAW / self.DOT, self.RESULTS_MEAN / self.DOT)
            self.gen_comma(self.RESULTS_MEAN)
            print("Generation data done.")
        if self.plot:
            self.plot_result()


if __name__ == "__main__":
    script = ResultsMgr()
    script.run()
