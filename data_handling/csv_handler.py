import sys
from pathlib import Path
from tkinter import filedialog as fd

import pandas as pd


class CsvHandler:
    CSV_TYPES = [
        ("CSV", "*.csv"),
    ]
    INITIALDIR = Path(__file__).resolve().parents[1]

    def __init__(self, sep: str = ";") -> None:
        self.df = pd.DataFrame()
        self.path = Path(".")
        self.sep = sep

    def read(
        self,
        path: str | Path | None = None,
        header: int | None = None,
        dialog: bool = False,
    ) -> pd.DataFrame:
        if dialog:
            path = fd.askopenfilename(filetypes=self.CSV_TYPES, initialdir=self.INITIALDIR)
        if not path:
            sys.exit("[Exit] CsvHandler.read: No path given.")

        self.path = Path(path)
        self.df = pd.read_csv(self.path, sep=self.sep, header=header)
        return self.df

    def write(
        self,
        path: str | Path | None = None,
        df: pd.DataFrame = None,
        mode: str = "w",
        header: bool = False,
        dialog: bool = False,
    ) -> None:
        if dialog:
            path = fd.asksaveasfilename(
                defaultextension="csv", filetypes=self.CSV_TYPES, initialdir=self.INITIALDIR
            )
            if not path:
                return
        if path:
            path = Path(path)
        else:
            path = self.path
        if df is None:
            df = self.df

        df.to_csv(path, sep=self.sep, mode=mode, index=False, header=header)


def main():
    csv_handler = CsvHandler()
    csv_handler.read(dialog=True)
    csv_handler.write()


if __name__ == "__main__":
    main()
