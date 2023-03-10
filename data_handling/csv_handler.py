from pathlib import Path
from tkinter import filedialog as fd

import pandas as pd
from filelock import FileLock


class CsvHandler:
    CSV_TYPES = [
        ("CSV", "*.csv"),
    ]

    def __init__(self) -> None:
        self.df = pd.DataFrame()
        self.path = Path(".")

    def read(self, path: str | Path | None = None, dialog: bool = False) -> pd.DataFrame:
        if dialog:
            path = fd.askopenfilename(filetypes=self.CSV_TYPES)
        if not path:
            raise Exception("[READ] No path given.")

        self.path = Path(path)
        self.df = pd.read_csv(self.path)
        return self.df

    def write(self, path: str | Path | None = None, mode: str = "w", dialog: bool = False) -> None:
        if dialog:
            path = fd.asksaveasfilename(defaultextension="csv", filetypes=self.CSV_TYPES)
            if not path:
                return
        if path:
            path = Path(path)
        else:
            path = self.path

        lock_path = path.with_suffix(".lock")
        lock = FileLock(lock_path, timeout=1)
        header = False if "a" in mode else True
        with lock:
            self.df.to_csv(path, mode=mode, index=False, header=header)


def main():
    csv_handler = CsvHandler()
    csv_handler.read(dialog=True)
    csv_handler.write()


if __name__ == "__main__":
    main()
