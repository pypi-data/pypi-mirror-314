import argparse
from functools import reduce
import glob
import numpy as np
import os
import pandas as pd
import tables
from tqdm import tqdm
from typing import Optional

from smack_app.variant_filters.strand_correlation import compute_correlation_matrix
from smack_app.variant_filters.vmr import compute_vmr
from smack_app.variant_filters.position_bias import compute_position_bias
from smack_app.utils.utils import (
    initialize_pseudocount_matrix,
    parse_coverage_vector,
    get_position_from_variant,
    UMI_Mode,
)
from smack_app.genotyping.eUMI import deconstruct_eUMI_id
from smack_app.genotyping.UMI import deconstruct_UMI_id


HETEROPLASMY_CUTOFFS = [5, 10, 20, 95]
N_CELLS_DETECTED_THRESHOLD = 2
POSITION_WINDOW_SIZE = 100


def compute_variant_matrices(
    variants: list[str],
    barcodes: list[str],
    h5_files: list[str],
    sample_id_map: Optional[dict[str, str]],
    mode: UMI_Mode,
    min_consensus_group_size: int,
    n_genome: int,
):

    variants_to_index = {v: i for (i, v) in enumerate(variants)}
    index_to_variants = {i: v for (i, v) in enumerate(variants)}
    N = len(variants)
    barcodes_to_index = {b: i for (i, b) in enumerate(barcodes)}
    M = len(barcodes)

    alt_counts_matrix = np.zeros((N, M))
    fwd_counts_matrix = np.zeros((N, M))
    rev_counts_matrix = np.zeros((N, M))

    alt_position_matrix = np.zeros((N, POSITION_WINDOW_SIZE))
    ref_position_matrix = np.zeros((N, POSITION_WINDOW_SIZE))

    # because more than one variant can be at each position, its a list of indexes
    # and not a single index
    variant_positions_to_indexes = {}
    for i, v in enumerate(variants):
        pos = get_position_from_variant(v)
        if pos not in variant_positions_to_indexes:
            variant_positions_to_indexes[pos] = []
        variant_positions_to_indexes[pos].append(i)

    print("Populating variants x cells table")

    for f in tqdm(h5_files):
        with tables.open_file(f, driver="H5FD_CORE") as h5file:
            molecules = h5file.get_node("/molecules", "alt_molecules")
            for row in molecules.iterrows():

                barcode = row["barcode"].decode()

                if sample_id_map:
                    barcode = sample_id_map[f] + "_" + barcode

                # skip barcodes that didn't make it into final barcodes list
                if barcode not in barcodes_to_index:
                    continue
                barcode_idx = barcodes_to_index[barcode]

                # TODO: add more consensus calling requirements, see REDEEM supplement pg 21
                # min group size = 1 for now
                group_size = row["consensus_group_size"]
                if group_size < min_consensus_group_size:
                    continue

                variant = row["variant"].decode()
                variant_idx = variants_to_index[variant]

                alt_counts_matrix[variant_idx, barcode_idx] += 1

                if int(row["fwd_count"]) > 0:
                    fwd_counts_matrix[variant_idx, barcode_idx] += 1

                if int(row["rev_count"]) > 0:
                    rev_counts_matrix[variant_idx, barcode_idx] += 1

                position = row["position"] - 1

                if mode == UMI_Mode.eUMI:
                    (_, start, end) = deconstruct_eUMI_id(row["group_id"].decode())
                else:
                    (_, _, start, end) = deconstruct_UMI_id(row["group_id"].decode())

                normalized_position = POSITION_WINDOW_SIZE * (
                    (position - start) / (end - 1 - start)
                )

                # bin position which is WINDOW_SIZE*[0-1]
                # into integer index [0-WINDOW_SIZE)
                normalized_position = min(
                    round(normalized_position), POSITION_WINDOW_SIZE - 1
                )
                alt_position_matrix[variant_idx, normalized_position] += 1

    print("Building Coverage Matrix from consensus groups data")
    full_coverage_matrix = initialize_pseudocount_matrix(n_genome, M)

    for f in tqdm(h5_files):
        with tables.open_file(f, driver="H5FD_CORE") as h5file:
            consensus_groups = h5file.get_node("/molecules", "consensus_groups")
            for row in consensus_groups.iterrows():

                if mode == UMI_Mode.eUMI:

                    (barcode, start, end) = deconstruct_eUMI_id(
                        row["group_id"].decode()
                    )
                else:
                    (barcode, _, start, end) = deconstruct_UMI_id(
                        row["group_id"].decode()
                    )

                if sample_id_map:
                    barcode = sample_id_map[f] + "_" + barcode

                # skip barcodes that didn't make it into final barcodes list
                if barcode not in barcodes_to_index:
                    continue

                coverage_vector = parse_coverage_vector(row["encoding_vector"].decode())

                assert len(coverage_vector) == (
                    end - start
                ), f"Coverage vector is length {len(coverage_vector)} but eUMI is  {end-start}"

                # Coverage is counted where we have high confidence ref or alt alleles, which is 1 or 2
                # alts = (np.array(coverage_vector) == 2).astype(int)
                # refs = (np.array(coverage_vector) == 1).astype(int)
                cov = (np.array(coverage_vector) > 0).astype(int)

                full_coverage_matrix[start:end, barcodes_to_index[barcode]] += cov

                coverage_vector_arr = np.array(coverage_vector)
                for idx in np.flatnonzero(coverage_vector_arr == 1):
                    position = start + idx

                    # we don't care about ref calls when there was no variant recorded at the same
                    # position
                    if position not in variant_positions_to_indexes:
                        continue

                    normalized_position = POSITION_WINDOW_SIZE * (
                        (position - start) / (end - 1 - start)
                    )
                    # bin position which is WINDOW_SIZE*[0-1]
                    # into integer index [0-WINDOW_SIZE)
                    normalized_position = min(
                        round(normalized_position), POSITION_WINDOW_SIZE - 1
                    )

                    pos_idxs = variant_positions_to_indexes[position]

                    for pos_idx in pos_idxs:
                        ref_position_matrix[pos_idx, normalized_position] += 1

    print("Building Heteroplasmy matrix from alt counts and coverage")
    variant_coverage_matrix = initialize_pseudocount_matrix(N, M)
    for variant in tqdm(variants):
        for barcode in barcodes_to_index:

            position = get_position_from_variant(variant)
            variant_coverage_matrix[
                variants_to_index[variant], barcodes_to_index[barcode]
            ] = full_coverage_matrix[position, barcodes_to_index[barcode]]

    heteroplasmy_matrix = alt_counts_matrix / variant_coverage_matrix

    print("Calculating molecular position bias for ref and alt calls")
    position_df = compute_position_bias(
        alt_position_matrix,
        ref_position_matrix,
        index_to_variants,
        POSITION_WINDOW_SIZE,
    )

    # TODO: remove this?
    alt_position_matrix_df = pd.DataFrame(data=alt_position_matrix, index=variants)
    alt_position_matrix_df.to_csv(f"{args.outdir}/alt_position_matrix.csv")
    ref_position_matrix_df = pd.DataFrame(data=ref_position_matrix, index=variants)
    ref_position_matrix_df.to_csv(f"{args.outdir}/ref_position_matrix.csv")

    return (
        heteroplasmy_matrix,
        alt_counts_matrix,
        fwd_counts_matrix,
        rev_counts_matrix,
        variant_coverage_matrix,
        position_df,
    )


def get_all_potential_variants(
    h5_files: list[str], barcodes: list, sample_id_map: Optional[dict[str, str]]
) -> list[str]:
    print("Getting list of variants from h5 files")
    valid_barcodes = set(barcodes)
    variants = set()
    for f in tqdm(h5_files):
        with tables.open_file(f, driver="H5FD_CORE") as h5file:
            molecules = h5file.get_node("/molecules", "alt_molecules")
            for row in molecules.iterrows():
                barcode = row["barcode"].decode()

                if sample_id_map:
                    barcode = sample_id_map[f] + "_" + barcode

                # skip barcodes that didn't make it into final barcodes list
                if barcode not in valid_barcodes:
                    continue
                variants.add(row["variant"].decode())

    return list(variants)


def get_h5_to_sample_id_map(h5_files: list[str]) -> dict[str, str]:
    sample_id_map = {}
    for f in h5_files:
        with tables.open_file(f, driver="H5FD_CORE") as h5file:
            metadata = h5file.get_node("/metadata", "metadata")
            for row in metadata.iterrows():
                sample_id = row["sample_id"].decode()
                sample_id_map[f] = sample_id
    return sample_id_map


def get_genome_length(h5_files: list[str]) -> str:
    genome_path = None
    genome_length = None
    for f in tqdm(h5_files):
        with tables.open_file(f, driver="H5FD_CORE") as h5file:
            metadata = h5file.get_node("/metadata", "metadata")
            for row in metadata.iterrows():
                _genome_path = row["genome_path"].decode()
                if genome_path is None:
                    genome_path = _genome_path
                else:
                    assert (
                        genome_path == _genome_path
                    ), f"All H5 files must have the same reference genome, but paths {genome_path} and {_genome_path} are not the same"

                _genome_length = row["genome_length"]
                if genome_length is None:
                    genome_length = _genome_length
                else:
                    assert (
                        genome_length == _genome_length
                    ), f"All H5 files must have the same genome length, but lengths {genome_length} and {_genome_length} are not the same"

    return genome_length


def get_all_barcodes(
    h5_files: list[str],
    barcode_depth_df: pd.DataFrame,
    sample_id_map: Optional[dict[str, str]],
) -> list[str]:
    print("Getting barcodes from h5 files")

    # barcodes in H5 files
    h5_barcodes = set()
    for f in tqdm(h5_files):
        with tables.open_file(f, driver="H5FD_CORE") as h5file:
            bcs = h5file.get_node("/barcodes", "barcodes")
            for bc in bcs.col("barcode"):
                _barcode = bc.decode()
                if sample_id_map:
                    _barcode = sample_id_map[f] + "_" + _barcode
                h5_barcodes.add(_barcode)
    print("Getting barcodes depth from input barcodes depth CSV")

    # Barcodes in CSV
    all_csv_barcodes = set(barcode_depth_df["barcode"])

    # Discrepancies between the 2 sets
    missing_barcodes = all_csv_barcodes.symmetric_difference(h5_barcodes)

    # Intersection between the 2 sets
    overlapped_barcodes = all_csv_barcodes.intersection(h5_barcodes)

    if len(missing_barcodes) != 0:
        print("WARNING: Cell barcodes are different between h5 files and depth CSV")
        print(
            f"Using only the  {len(overlapped_barcodes)} barcodes that are in both, and throwing out {len(missing_barcodes)} cells"
        )
    filtered_csv_barcodes = set(barcode_depth_df[barcode_depth_df["pass"]]["barcode"])

    filtered_csv_barcodes = filtered_csv_barcodes.intersection(overlapped_barcodes)
    removed_barcodes = overlapped_barcodes - filtered_csv_barcodes
    print(f"Filtered out {len(removed_barcodes)} / {len(overlapped_barcodes)} barcodes due to low depth")
    if len(list(filtered_csv_barcodes)) == 0:
        raise Exception("All Barcodes have been filtered out. Cannot proceed. Consider lowering --min-barcode-depth")
    return list(filtered_csv_barcodes)


def main(args):

    subdirs = args.h5dir.split(",")
    print(f"Found {len(subdirs)} h5 sample subdirectories")
    multi_sample_mode = len(subdirs) > 1

    h5_files = []
    for subdir in subdirs:
        h5_files += glob.glob(os.path.join(subdir, "*.h5"))

    print(f"Found {len(h5_files)} total h5 files")

    barcode_depth_df = pd.read_csv(args.barcode_depth_file)

    if multi_sample_mode:
        sample_id_map = get_h5_to_sample_id_map(h5_files)
    else:
        sample_id_map = None

    barcodes = get_all_barcodes(h5_files, barcode_depth_df, sample_id_map)
    variants = get_all_potential_variants(h5_files, barcodes, sample_id_map)

    genome_length = get_genome_length(h5_files)

    (
        heteroplasmy_matrix,
        alt_counts_matrix,
        fwd_counts_matrix,
        rev_counts_matrix,
        variant_coverage_matrix,
        position_df,
    ) = compute_variant_matrices(
        variants,
        barcodes,
        h5_files,
        sample_id_map,
        args.umi_mode,
        min_consensus_group_size=args.min_consensus_group_size,
        n_genome=genome_length,
    )

    print("Loading Results into DataFrames...")

    heteroplasmy_df = pd.DataFrame(
        data=heteroplasmy_matrix, index=variants, columns=barcodes
    )

    variant_counts_df = pd.DataFrame(
        data=alt_counts_matrix, index=variants, columns=barcodes
    )

    fwd_counts_df = pd.DataFrame(
        data=fwd_counts_matrix, index=variants, columns=barcodes
    )

    rev_counts_df = pd.DataFrame(
        data=rev_counts_matrix, index=variants, columns=barcodes
    )

    variant_coverage_df = pd.DataFrame(
        data=variant_coverage_matrix, index=variants, columns=barcodes
    )

    print("Computing variant statistics...")

    # strand correlation
    correlation_matrix_df = compute_correlation_matrix(fwd_counts_df, rev_counts_df)

    (means_df, variances_df, vmr_df) = compute_vmr(heteroplasmy_df)

    heteroplasmy_maxes = heteroplasmy_df.max(axis=1).reset_index()[[0]]
    heteroplasmy_maxes.index = heteroplasmy_df.index
    heteroplasmy_maxes.columns = ["max_heteroplasmy"]

    cutoff_df = pd.DataFrame(index=heteroplasmy_df.index)

    for cutoff in HETEROPLASMY_CUTOFFS:
        cutoff_df[f"n_cells_over_{cutoff}"] = heteroplasmy_df.apply(
            lambda row: sum((row > cutoff / 100.0).astype(int)), axis=1
        )

    cutoff_df["n_cells_conf_detected"] = (
        (fwd_counts_df >= N_CELLS_DETECTED_THRESHOLD)
        & (rev_counts_df >= N_CELLS_DETECTED_THRESHOLD)
    ).sum(axis=1)

    print(f"Writing results to CSVs in {args.outdir}. This may take a while...")

    variant_counts_df.to_csv(f"{args.outdir}/variant_counts.csv", index_label="variant")
    variant_coverage_df.to_csv(
        f"{args.outdir}/all_variants_coverage.csv", index_label="variant"
    )

    heteroplasmy_df.to_csv(
        f"{args.outdir}/all_variants_heteroplasmy_matrix.csv", index_label="variant"
    )

    fwd_counts_df.to_csv(
        f"{args.outdir}/all_variants_fwd_counts_matrix.csv", index_label="variant"
    )

    rev_counts_df.to_csv(
        f"{args.outdir}/all_variants_rev_counts_matrix.csv", index_label="variant"
    )

    dfs = [
        correlation_matrix_df,
        variances_df,
        vmr_df,
        position_df,
        heteroplasmy_maxes,
        cutoff_df,
        means_df,
    ]
    variant_df = reduce(
        lambda df1, df2: pd.merge(
            df1, df2, left_index=True, right_index=True, how="outer"
        ),
        dfs,
    )

    variant_df["mean_coverage"] = variant_coverage_df.apply(np.mean, axis=1).loc[
        variant_df.index
    ]

    variant_df.to_csv(
        f"{args.outdir}/all_variants_statistics.csv", index_label="variant"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-h5dir",
        type=str,
        required=True,
        help="Directory containing h5 files, or comma separated list of directories. Will read in all files ending in ext .h5",
    )
    parser.add_argument("-outdir", type=str, required=True, help="output directory")
    parser.add_argument(
        "-barcode-depth-file",
        type=str,
        required=True,
        help="path to barcode depth file (usually {outdir}/barcode_depth.csv)",
    )
    parser.add_argument(
        "-min-consensus-group-size",
        type=int,
        required=True,
        help="min group size for consensus group",
    )

    parser.add_argument(
        "-umi-mode",
        type=UMI_Mode,
        required=True,
        help="eUMI mode or UMI mode",
    )

    args = parser.parse_args()

    main(args)
