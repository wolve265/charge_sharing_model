import sys
import time
from pathlib import Path

# append charge_sharing_model directory
sys.path.append(str(Path(sys.path[0]).parents[0]))

from sample_1d import Sample1D

from models.detectors import cdte, si
from models.pcs_model_1d import PcsModel1D


def main():
    samples: list[Sample1D] = []
    # for detector in si.all + cdte.all:
    for detector in [si.target]:
        samples.append(
            Sample1D(
                model=PcsModel1D(detector),
                approx_function=PcsModel1D.calc_hit_1D_taylor,
                approx_function_param=10,
                detector_size_step=1,
                times=10,
            )
        )
    for sample in samples:
        sample.test()
        # sample.test_process()
        return


if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
    end_time = time.perf_counter()
    mm, ss = divmod(end_time - start_time, 60)
    hh, mm = divmod(mm, 60)
    print(f"Script took: {hh:.0f}h {mm:.0f}m {ss:.0f}s")
