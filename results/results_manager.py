import argparse
import sys
from pathlib import Path

import pandas as pd
import yaml

# append charge_sharing_model directory
sys.path.append(str(Path(sys.path[0]).parents[0]))


class ResultsManager:
    CSV_TYPES = [("CSV", "*.csv")]
    INITIALDIR = Path(__file__).resolve().parent
    RESULTS_RAW = Path("results/raw")
    RESULTS_ABS_ERR = Path("results/abs_err")
    SEP = ";"

    def __init__(self) -> None:
        self.args = self.parse_args()
        self.gen: bool = self.args.gen

    def parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-g", "--gen", action="store_true", help="Generates other data"
        )
        return parser.parse_args()

    def gen_abs_err(self, src: Path, dest: Path) -> None:
        for file in src.iterdir():
            df = pd.read_csv(file, sep=self.SEP, header=None)
            df_abs_err = pd.DataFrame(df - df.columns).abs()

            abs_err_file = dest.joinpath(file.name)
            dest.mkdir(parents=True, exist_ok=True)
            df_abs_err.to_csv(
                abs_err_file, sep=self.SEP, index=False, header=False
            )

    def run(self):
        if self.gen:
            self.gen_abs_err(self.RESULTS_RAW, self.RESULTS_ABS_ERR)
            print("Generation data done.")


if __name__ == "__main__":
    script = ResultsManager()
    script.run()
