import sys
from collections.abc import Callable
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from pathlib import Path

from filelock import FileLock

# append charge_sharing_model directory
sys.path.append(str(Path(sys.path[0]).parents[0]))

from models.pcs_model_1d import PcsModel1D

RESULTSDIR = Path("results/raw/dot")


@dataclass
class Sample1D:
    model: PcsModel1D
    approx_function: Callable[[PcsModel1D, int], float]
    approx_function_param: int
    detector_size_step: int
    times: int

    def __post_init__(self) -> None:
        self.sep = ";"
        self.file = Path()
        self.filelock = Path()
        self.positions_to_test = range(
            0, self.model.detector.pixel_size + 1, self.detector_size_step
        )

    def to_filename(self) -> str:
        function_type_name = self.approx_function.__name__.split("_")[-1]
        function_param = str(self.approx_function_param) if self.approx_function_param else ""
        function_with_param = f"{function_type_name}{function_param}"
        return "_".join(
            [
                f"{self.model.dimension}",
                f"{self.model.detector.material}",
                f"{function_with_param}",
                f"step{self.detector_size_step}",
                f"times{self.times}",
                f"size{self.model.detector.pixel_size:.0f}",
                f"sigma{(100 * self.model.detector.charge_cloud_sigma / self.model.detector.pixel_size):.0f}",
                # f"charges{self.model.detector.num_of_charges:.0f}",
                f"noise{self.model.detector.noise_sigma:.0f}",
                f"{self.model.detector.name}",
            ]
        )

    def create_result_file(self) -> None:
        self.file = RESULTSDIR.joinpath(self.to_filename()).with_suffix(".csv")
        self.filelock = self.file.with_suffix(".lock")
        self.file.parent.mkdir(parents=True, exist_ok=True)
        if self.file.exists():
            self.file.unlink()
        self.file.touch()

    def hit_and_calc(self, t: int) -> float:
        lock = FileLock(self.filelock, timeout=10)
        results = []

        for x in self.positions_to_test:
            self.model.hit(x)
            result = self.approx_function(self.model, self.approx_function_param)
            results.append(f"{result}")

        with lock, self.file.open("a") as f:
            print(self.sep.join(results), file=f)

    def test(self) -> None:
        """Test sample

        One process, no lock:
            - 10 -> 0.75s
            - 100 -> 8s
            - 1000 -> 1m 15s

        One process, with lock:
            - 100 -> 8s
            - 1000 -> 1m 18s
        """
        self.create_result_file()

        for t in range(self.times):
            self.hit_and_calc(t)

    def test_process(self) -> None:
        """Test sample with ProcessPoolExecutor

        Chunksize = 1:
            - 100 -> 3s
            - 1000 -> 14s

        Chunksize = 5:
            - 1000 -> 14s

        Chunksize = 10:
            - 1000 -> 14s
            - 10_000 -> 2m 4s

        Chunksize = 100:
            - 10_000 -> 2m 5s
        """
        self.create_result_file()

        t = range(self.times)
        with ProcessPoolExecutor() as executor:
            executor.map(self.hit_and_calc, t, chunksize=100)
