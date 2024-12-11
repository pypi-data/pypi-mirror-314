import numpy as np
import pandas as pd

# from scipy import stats


# TODO: Parallelize this?
def compute_position_bias(
    alt_position_matrix: np.ndarray,
    ref_position_matrix: np.ndarray,
    key: dict[int, str],
    window_size: int,
) -> pd.DataFrame:

    ks_stats = {
        variant: run_ks_tests(
            alt_position_matrix[idx, :], ref_position_matrix[idx, :], window_size
        )
        for idx, variant in key.items()
    }
    bias_df = pd.DataFrame(ks_stats).T
    bias_df.index.name = "variant"
    bias_df.columns = [
        "alt_ref_statistic",
        "alt_uniform_statistic",
        "ref_uniform_statistic",
    ]
    return bias_df


def run_ks_tests(
    variant_position_counts: np.ndarray,
    ref_position_counts: np.ndarray,
    window_size: int,
) -> tuple[float, float, float, float, float, float]:

    variant_position_cdf = np.cumsum(variant_position_counts) / sum(
        variant_position_counts
    )
    assert len(variant_position_counts) == window_size
    assert len(ref_position_counts) == window_size

    ref_position_cdf = np.cumsum(ref_position_counts) / sum(ref_position_counts)
    uniform_cdf = np.array([i / window_size for i in range(1, window_size + 1)])

    #  max(abs(ref - alt))
    alt_ref = max(np.abs(variant_position_cdf - ref_position_cdf))
    alt_uniform = max(np.abs(variant_position_cdf - uniform_cdf))
    ref_uniform = max(np.abs(ref_position_cdf - uniform_cdf))

    return (alt_ref, alt_uniform, ref_uniform)

    # alt_uniform_result = stats.kstest(variant_positions, stats.uniform.cdf)

    # if ref_positions is None or ref_positions.size == 0:
    #     return (
    #         np.nan,
    #         np.nan,
    #         alt_uniform_result.statistic,
    #         alt_uniform_result.pvalue,
    #         np.nan,
    #         np.nan,
    #     )

    # alt_ref_result = stats.ks_2samp(variant_positions, ref_positions)
    # ref_uniform_result = stats.kstest(ref_positions, stats.uniform.cdf)
    # return (
    #     alt_ref_result.statistic,
    #     alt_ref_result.pvalue,
    #     alt_uniform_result.statistic,
    #     alt_uniform_result.pvalue,
    #     ref_uniform_result.statistic,
    #     ref_uniform_result.pvalue,
    # )
