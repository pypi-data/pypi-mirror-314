from enum import Enum
import multiprocessing
import numpy as np
import os
import re
from scipy.stats import pearsonr


PSEUDOCOUNT = 0.0001

APPDIR = "smack-app"
APPNAME = "smack_app"
current_file_path = os.path.abspath(__file__)
current_file_dir = os.path.dirname(current_file_path)
REPOPATH = os.path.abspath(os.path.join(current_file_dir, "../"))


# Note: also hard coded in h5_schema.py due to circular imports
# if changed, change there too
class UMI_Mode(str, Enum):
    eUMI = "eUMI"
    UMI = "UMI"


class ConsensusCallStrategy(str, Enum):
    CONSENSUS = "CONSENSUS"
    MEAN_QUALITY = "MEAN_QUALITY"


def pearson_exclude_zeros(vec1: np.ndarray, vec2: np.ndarray) -> float:
    excluded_indexes = (vec1 <= PSEUDOCOUNT) & (vec2 <= PSEUDOCOUNT)
    x = vec1[~excluded_indexes]
    y = vec2[~excluded_indexes]
    assert len(x) == len(y), "x and y must be the same length"
    if len(x) < 2:
        return np.nan
    return pearsonr(x, y).statistic


def initialize_pseudocount_matrix(n: int, m: int) -> np.ndarray:
    return PSEUDOCOUNT * np.ones((n, m))


def get_position_from_variant(variant: str) -> int:
    # returns 0-indexed position from variant str
    [pos, _, _] = variant.split("_")
    return int(pos) - 1


def parse_coverage_vector(vec: str) -> list[int]:
    result = []
    idx = 0
    while idx < len(vec):
        try:
            el = int(vec[idx])
            result.append(el)
            idx += 1

        except ValueError as e:
            # negative numbers hit value error for "-" character. Read it together with next char
            el = int(vec[idx : idx + 2])
            result.append(el)
            idx += 2
    return result


# see mgatk https://github.com/caleblareau/mgatk/blob/master/mgatk/mgatkHelp.py
# can use multiprocessing.cpu_count() but depending on system might need to check cpuset first for restrictions
def available_cpu_count():
    """
    Number of available virtual or physical CPUs on this system, i.e.
    user/real as output by time(1) when called with an optimally scaling
    userspace-only program
    """
    # cpuset
    # cpuset may restrict the number of *available* processors
    try:
        m = re.search(r"(?m)^Cpus_allowed:\s*(.*)$", open("/proc/self/status").read())
        if m:
            res = bin(int(m.group(1).replace(",", ""), 16)).count("1")
            if res > 0:
                return res
    except IOError:
        pass

    try:
        import multiprocessing

        return multiprocessing.cpu_count()
    except (ImportError, NotImplementedError):
        pass

    raise OSError(
        "Can not determine number of CPUs on this system. Please set -ncores manually"
    )
