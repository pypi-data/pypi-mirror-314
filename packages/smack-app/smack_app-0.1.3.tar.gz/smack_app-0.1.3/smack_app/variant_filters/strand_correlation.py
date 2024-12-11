import numpy as np
import pandas as pd

from smack_app.utils.utils import pearson_exclude_zeros


def compute_correlation_matrix(
    fwd_matrix: pd.DataFrame, rev_matrix: pd.DataFrame
) -> pd.DataFrame:
    correlation_matrix = fwd_matrix.corrwith(
        rev_matrix, method=pearson_exclude_zeros, axis=1
    )
    return pd.DataFrame(
        data=correlation_matrix, index=rev_matrix.index, columns=["strand_correlation"]
    )
