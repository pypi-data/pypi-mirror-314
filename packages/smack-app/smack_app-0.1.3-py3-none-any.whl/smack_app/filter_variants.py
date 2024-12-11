import argparse
import os
import pandas as pd


def main(args):

    all_variants = pd.read_csv(args.variant_statistics, index_col="variant")

    coverage = pd.read_csv(args.variant_coverage_matrix, index_col="variant")

    heteroplasmy_matrix = pd.read_csv(
        args.variant_heteroplasmy_matrix, index_col="variant"
    )

    if args.mean_coverage > 0:
        all_variants["pass_mean_coverage"] = all_variants["mean_coverage"].apply(
            lambda v: v >= args.mean_coverage
        )

    if args.min_strand_correlation > 0:
        all_variants["pass_strand_correlation"] = all_variants[
            "strand_correlation"
        ].apply(lambda c: c >= args.min_strand_correlation)

    all_variants["pass_vmr"] = all_variants["vmr"].apply(lambda v: v >= args.min_vmr)

    if args.n_cells_over_5 > 0:
        all_variants["pass_ncells"] = all_variants["n_cells_over_5"].apply(
            lambda c: c >= args.n_cells_over_5
        )

    if args.molecular_position_bias_threshold < 1:
        all_variants["pass_position_bias"] = all_variants[
            "alt_uniform_statistic"
        ].apply(lambda s: s <= args.molecular_position_bias_threshold)

    all_variants["pass_homoplasmic"] = all_variants["mean"].apply(
        lambda h: h <= args.homoplasmic_threshold
    )
    filter_columns = [c for c in all_variants.columns if c.startswith("pass")]

    all_variants["pass_filters"] = all_variants.apply(
        lambda row: all(row[col] for col in filter_columns), axis=1
    )
    all_variants.to_csv(os.path.join(args.outdir, "all_variants_statistics.csv"))

    final_variants_statistics = all_variants[all_variants["pass_filters"]]
    final_variants_statistics.to_csv(
        os.path.join(args.outdir, "final_variants_statistics.csv")
    )
    final_variants_set = set(final_variants_statistics.index)

    heteroplasmy_matrix.to_csv(
        os.path.join(args.outdir, "all_variants_heteroplasmy_matrix.csv")
    )

    heteroplasmy_matrix = heteroplasmy_matrix[
        heteroplasmy_matrix.index.isin(final_variants_set)
    ]

    heteroplasmy_matrix.to_csv(
        os.path.join(args.outdir, "final_variants_heteroplasmy_matrix.csv")
    )
    coverage.to_csv(os.path.join(args.outdir, "all_variants_coverage_matrix.csv"))
    coverage = coverage[coverage.index.isin(final_variants_set)]
    coverage.to_csv(os.path.join(args.outdir, "final_variants_coverage_matrix.csv"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-variant-statistics",
        type=str,
        required=True,
        help="path to variant statistics CSV file",
    )
    parser.add_argument(
        "-variant-heteroplasmy-matrix",
        type=str,
        required=True,
        help="path to heteroplasmy matrix CSV file",
    )
    parser.add_argument(
        "-variant-coverage-matrix",
        type=str,
        required=True,
        help="path to coverage matrix CSV file",
    )

    parser.add_argument(
        "-min-strand-correlation",
        type=float,
        required=True,
        help="Minimum correlation required between fwd and rev strands for a variant to be included",
    )
    parser.add_argument(
        "-min-vmr",
        type=float,
        required=True,
        help="Minimum heteroplasmy variance mean ratio (VMR) required for a variant to be included",
    )

    parser.add_argument(
        "-molecular-position-bias-threshold",
        type=float,
        required=True,
        help="Threshold for position bias KS test",
    )
    parser.add_argument(
        "-homoplasmic-threshold",
        type=float,
        required=True,
        help="Threshold for being considered homoplasmic, and not included in heteroplasmic variants",
    )
    parser.add_argument(
        "-mean-coverage",
        type=float,
        required=True,
        help="Threshold for minimum mean coverage",
    )
    parser.add_argument(
        "-n-cells-over-5",
        type=int,
        required=True,
        help="Threshold for requires number of cells above 5 percent heteroplasmy",
    )

    parser.add_argument("-outdir", type=str, required=True, help="output directory")

    args = parser.parse_args()

    main(args)
