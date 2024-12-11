import argparse
from collections import defaultdict
import os
import pandas as pd
import pysam
import sys
from tables import open_file
from typing import Optional, IO
from tqdm import tqdm

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ConsensusGroup import ConsensusGroup, ConsensusCallResult
from eUMI import get_eUMIs_and_barcode_depth_from_read_pairs, consensus_call_eUMI
from h5_schema import (
    MetadataSchema,
    MoleculeSchema,
    BarcodeSchema,
    ConsensusGroupSchema,
)
from UMI import get_UMIs_and_barcode_depth_from_read_pairs, consensus_call_UMI

from utils.utils import UMI_Mode, ConsensusCallStrategy


def get_read_pairs(bam_file: str) -> dict:
    bam_input = pysam.AlignmentFile(bam_file, "rb")
    read_pair_dict = defaultdict(list)

    for read in bam_input:
        read_pair_dict[read.query_name].append(read)

    return read_pair_dict


def process_groups(
    groups: list[ConsensusGroup],
    h5file: IO,
    mode: UMI_Mode,
    consensus_call_strategy: ConsensusCallStrategy,
    mito_ref_seq: pd.DataFrame,
    barcode_depth: dict[str, float],
    max_bp: int,
    quality_threshold=30,
) -> None:

    barcode_quality_coverage_counts = {bc: 0 for bc in barcode_depth}

    print("Genotyping Each eUMI")

    group = h5file.create_group("/", "molecules", "Molecule Level Information")
    table = h5file.create_table(
        group, "alt_molecules", MoleculeSchema, "molecule table"
    )
    consensus_group_table = h5file.create_table(
        group,
        "consensus_groups",
        ConsensusGroupSchema,
        "Consensus Groups reference table",
    )

    for g in tqdm(groups):

        # Sanity check to prevent errors
        if not g.readpairs:
            continue

        if mode == UMI_Mode.eUMI:
            result: ConsensusCallResult = consensus_call_eUMI(
                g,
                mito_ref_seq,
                consensus_call_strategy,
                quality_threshold=quality_threshold,
            )
        else:
            result: ConsensusCallResult = consensus_call_UMI(
                g,
                mito_ref_seq,
                consensus_call_strategy,
                quality_threshold=quality_threshold,
            )

        molecule = table.row
        has_data = False

        for row in result.rows:
            has_data = True
            for key in row:
                molecule[key] = row[key]
            molecule.append()
        table.flush()

        entry = consensus_group_table.row
        entry["group_id"] = g.key
        entry["has_alt"] = has_data
        entry["encoding_vector"] = result.encoding_vector
        entry["group_type"] = g.group_type

        entry.append()
        consensus_group_table.flush()

        barcode_quality_coverage_counts[g.cell_barcode] += result.quality_coverage_count

    # Write bar code metadata
    group = h5file.create_group("/", "barcodes", "Cell Level Information")
    barcodes_table = h5file.create_table(
        group, "barcodes", BarcodeSchema, "barcode depth table"
    )
    bc_entry = barcodes_table.row
    for bc, d in barcode_depth.items():
        bc_entry["barcode"] = bc
        bc_entry["average_total_depth"] = d / max_bp
        bc_entry["average_high_quality_depth"] = (
            barcode_quality_coverage_counts[bc] / max_bp
        )
        bc_entry.append()
    barcodes_table.flush()


def call_sample(
    sample_id: str,
    bam_file: str,
    outh5: str,
    mode: UMI_Mode,
    consensus_call_strategy: ConsensusCallStrategy,
    barcodes_file: str,
    mito_ref: str,
    genome_length: int,
    barcode_tag: str,
    umi_tag: Optional[str],
    quality_threshold: int,
    max_eUMI_size: int,
    eUMI_trim: int,
    mapping_quality_threshold: int,
) -> None:
    mito_ref_df = get_mito_reference(mito_ref)

    max_bp = mito_ref_df.shape[0]
    assert (
        genome_length == max_bp
    ), "Mito Ref and Genome Size do not match. Did you set the correct genome?"

    barcodes = []
    with open(barcodes_file) as bf:
        barcodes = [f.strip() for f in bf]

    read_pair_dict = get_read_pairs(bam_file)

    if mode == UMI_Mode.eUMI:

        groups, barcode_depth = get_eUMIs_and_barcode_depth_from_read_pairs(
            read_pair_dict,
            barcode_tag,
            barcodes,
            max_bp,
            max_eUMI_size,
            eUMI_trim,
            mapping_quality_threshold,
        )
    else:
        groups, barcode_depth = get_UMIs_and_barcode_depth_from_read_pairs(
            read_pair_dict,
            barcode_tag,
            umi_tag,
            barcodes,
            max_bp,
            mapping_quality_threshold,
        )

    with open_file(outh5, mode="w", title=f"{bam_file} h5 file") as h5file:
        # Run variant calling on groups
        process_groups(
            groups,
            h5file,
            mode,
            consensus_call_strategy,
            mito_ref_df["base"],
            barcode_depth,
            max_bp,
            quality_threshold=quality_threshold,
        )

        group = h5file.create_group("/", "metadata", "Metadata")
        metadata_table = h5file.create_table(
            group, "metadata", MetadataSchema, "metadata table"
        )
        entry = metadata_table.row
        entry["genome_path"] = mito_ref
        entry["genome_length"] = genome_length
        entry["sample_id"] = sample_id

        entry.append()
        metadata_table.flush()


def get_mito_reference(mito_ref_file: str) -> pd.DataFrame:
    try:
        mito_ref = pd.read_table(mito_ref_file, names=["pos", "base"])
        return mito_ref
    except Exception as e:
        raise FileNotFoundError(
            f"Unable to Read mito reference. Is it located at {mito_ref_file}?"
        ) from e


def main(args):

    barcodes_file = args.barcodes
    bam_file = args.bamfile

    if args.umi_tag:
        assert args.umi_mode == UMI_Mode.UMI, "umi-tag can only be used in UMI mode"

    call_sample(
        args.sample_id,
        bam_file,
        args.outh5,
        args.umi_mode,
        args.consensus_call_strategy,
        barcodes_file,
        args.mito_ref_file,
        args.genome_length,
        args.barcode,
        args.umi_tag,
        args.bq,
        args.max_eUMI_size,
        args.eUMI_trim,
        args.mapq,
    )


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--bamfile", type=str, help="Path to sample BAM file")
    parser.add_argument("--barcodes", type=str, help="Path to barcodes file")
    parser.add_argument(
        "--mito-ref-file",
        type=str,
        help="Path to mito ref TSV",
        required=True,
    )
    parser.add_argument(
        "--sample-id",
        type=str,
        help="Sample ID  - goes in metadata table",
    )
    parser.add_argument(
        "--genome-length",
        type=int,
        help="Size of mito ref genome",
        required=True,
    )
    parser.add_argument(
        "--outh5",
        type=str,
        default="mito_test.hdf5",
        help="The full output path for h5 file",
    )
    parser.add_argument(
        "--barcode",
        type=str,
        default="CB",
        help="Bar Code TAG to identify cell bar code",
    )
    parser.add_argument(
        "--umi-tag",
        type=str,
        default=None,
        help="TAG to identify UMI bar code, only used in UMI mode, not eUMI mode",
    )
    parser.add_argument(
        "--umi-mode",
        type=UMI_Mode,
        default=None,
        help="Which mode, eUMI or UMI",
    )
    parser.add_argument(
        "--consensus-call-strategy",
        type=ConsensusCallStrategy,
        default=ConsensusCallStrategy.CONSENSUS,
        help="How to collapse (e)UMI groups",
    )
    parser.add_argument("--bq", type=int, default=30, help="Base Quality threshold")
    parser.add_argument(
        "--mapq",
        type=int,
        default=30,
        help="Mapping Quality threshold",
    )

    parser.add_argument(
        "--max-eUMI-size",
        type=int,
        default=1000,
        help="Max Size of eUMI. eUMIs larger than this value will be considered misaligned/low quality and thrown out. Not used in UMI mode",
    )

    parser.add_argument(
        "--eUMI-trim",
        type=int,
        default=0,
        help="Number of bp to trim off each side of eUMI for position edge bias",
    )

    args = parser.parse_args()

    main(args)
