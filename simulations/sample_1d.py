import re
import sys
from collections.abc import Callable
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Self

from filelock import FileLock

# append charge_sharing_model directory
sys.path.append(str(Path(sys.path[0]).parents[0]))

from models.detectors import cdte, si  # used in eval()
from models.pcs_model_1d import PcsModel1D

RESULTSDIR = Path("results/raw")


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

    @classmethod
    def from_file(cls, file: str) -> Self:
        file: Path = Path(file)
        pattern = "_".join(
            [
                "(\d\w)",  # model dimension
                "(\w+)",  # model detector material
                "(\w+)",  # model detector name
                "(\w+)(\d+)",  # function with param
                "step(\d+)",  # model detector step size
                "times(\d+)",  # times
                # "size(\d+)",  # model detector pixel size
                # "sigma(\d+)",  # model detector charge cloud sigma in percent
                # "charges(\d+)",  # model detector num of charges
                # "noise(\d+)",  # model detector noise sigma
            ]
        )
        re_obj = re.match(pattern, file.stem)
        (
            model_dimension,
            model_detector_material,
            model_detector_name,
            function_name,
            function_param,
            model_detector_step_size,
            times,
            # size,
            # sigma,
            # charges,
            # noise,
        ) = re_obj.groups()
        model_type = PcsModel1D if model_dimension == "1D" else None
        approx_function = (
            model_type.calc_hit_1D_lut
            if function_name == "lut"
            else model_type.calc_hit_1D_erfinv
            if function_name == "erfinv"
            else model_type.calc_hit_1D_taylor
        )
        detector = eval(f"{model_detector_material.lower()}.{model_detector_name}")
        model = model_type(detector)
        return cls(
            model, approx_function, int(function_param), int(model_detector_step_size), int(times)
        )

    def to_filename(self) -> str:
        function_type_name = self.approx_function.__name__.split("_")[-1]
        function_param = str(self.approx_function_param) if self.approx_function_param else ""
        function_with_param = f"{function_type_name}{function_param}"
        return "_".join(
            [
                f"{self.model.dimension}",
                f"{self.model.detector.material}",
                f"{self.model.detector.name}",
                f"{function_with_param}",
                f"step{self.detector_size_step}",
                f"times{self.times}",
                # f"size{self.model.detector.pixel_size:.0f}",
                # f"sigma{(100 * self.model.detector.charge_cloud_sigma / self.model.detector.pixel_size):.0f}",
                # f"charges{self.model.detector.num_of_charges:.0f}",
                # f"noise{self.model.detector.noise_sigma:.0f}",
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

    def test_process(self, processes: int) -> None:
        """Test sample with ProcessPoolExecutor

        Times:
            - 100 -> 3s
            - 1000 -> 14s
            - 2500 -> 26s
            - 10_000 -> 2m 5s
        """
        self.create_result_file()
        chunksize = self.times // processes
        t = range(self.times)
        with ProcessPoolExecutor() as executor:
            executor.map(self.hit_and_calc, t, chunksize=chunksize)

        print(self.file)
