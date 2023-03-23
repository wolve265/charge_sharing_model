import sys
import time
from pathlib import Path

import numpy as np

# append charge_sharing_model directory
sys.path.append(str(Path(sys.path[0]).parents[0]))

from sample_1d import Sample1D

from models.detectors import cdte, si
from models.pcs_model_1d import PcsModel1D
from models.pcs_model_1d_int import PcsModel1DInt

# model = PcsModel1D
model = PcsModel1DInt


def main():
    samples: list[Sample1D] = []
    # for detector in [si.target]:
    for detector in si.all + cdte.all:
        # for param in range(1, 50, 1):
        for param in [25, 50, 75]:
            samples.append(
                Sample1D(
                    model=model(detector),
                    approx_function=model.calc_hit_lut,
                    approx_function_param=param,
                    detector_size_step=1,
                    times=2500,
                )
            )
    for sample in samples:
        # sample.test()
        sample.test_process(processes=20)
        # return


if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
    end_time = time.perf_counter()
    mm, ss = divmod(end_time - start_time, 60)
    hh, mm = divmod(mm, 60)
    print(f"Script took: {hh:.0f}h {mm:.0f}m {ss:.0f}s")
