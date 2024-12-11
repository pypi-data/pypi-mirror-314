import numpy as np
import pandas as pd


def compute_vmr(
    heteroplasmy_matrix: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:

    means = heteroplasmy_matrix.mean(axis=1)
    means_df = pd.DataFrame(
        data=means, index=heteroplasmy_matrix.index, columns=["mean"]
    )

    variances = heteroplasmy_matrix.var(axis=1)
    variances_df = pd.DataFrame(
        data=variances, index=heteroplasmy_matrix.index, columns=["variance"]
    )

    vmr = variances / means
    vmr_df = pd.DataFrame(data=vmr, index=heteroplasmy_matrix.index, columns=["vmr"])
    return (means_df, variances_df, vmr_df)
