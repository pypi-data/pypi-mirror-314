from collections import defaultdict
import numpy as np
import os
import pandas as pd
import sys
from typing import Union
from tqdm import tqdm

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.utils import ConsensusCallStrategy
from genotyping.h5_schema import UMI_DELIM

from genotyping.ConsensusGroup import (
    ConsensusGroup,
    DNA_BASES,
    DNA_LETTERS,
    ReadPair,
    ConsensusCallResult,
)


def build_UMI_id(
    barcode: str, umi: str, start_pos: Union[int, str], end_pos: Union[int, str]
) -> str:
    return (
        barcode
        + UMI_DELIM
        + umi
        + UMI_DELIM
        + str(start_pos)
        + UMI_DELIM
        + str(end_pos)
    )


def deconstruct_UMI_id(UMI_id: str) -> tuple[str, str, int, int]:
    [barcode, umi, start, end] = UMI_id.split(UMI_DELIM)
    return (barcode, umi, int(start), int(end))


class UMI(ConsensusGroup):
    def __init__(
        self, cell_barcode: str, umi_barcode, start_pos: int, end_pos: int
    ) -> None:
        super().__init__()
        self.cell_barcode = cell_barcode
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.umi_barcode = umi_barcode
        self.key = build_UMI_id(cell_barcode, umi_barcode, start_pos, end_pos)
        self.group_type = "UMI"


def get_UMIs_and_barcode_depth_from_read_pairs(
    read_pair_dict: dict,
    barcode_tag: str,
    umi_tag: str,
    barcodes: list,
    max_bp: int,
    mapping_quality_threshold: int,
) -> tuple[list, dict]:

    groups = {}
    barcode_depth = defaultdict(int)
    barcodes = set(barcodes)

    for read_name, read_list in tqdm(read_pair_dict.items()):

        # disregard reads that did not map cleanly to one line in the BAM
        if len(read_list) != 1:
            continue

        read = read_list[0]

        if not read.has_tag(barcode_tag):
            continue
        barcode = read.get_tag(barcode_tag)

        assert (
            barcode in barcodes
        ), f"Found barcode: {barcode} in BAM file but not in barcodes.txt file. The split BAM and barcodes file must match"

        umi = read.get_tag(umi_tag)

        aligned_array = np.asarray(
            read.get_aligned_pairs(matches_only=True, with_seq=False)
        )

        start_pos = int(read.pos)
        end_pos = start_pos + len(aligned_array)

        # throw out read pairs with low mapping quality
        if int(read.mapping_quality) < mapping_quality_threshold:
            continue

        # some readpairs are messed up because of the cicular genome. Throw them out
        if (start_pos >= max_bp) or (end_pos > max_bp):
            continue

        # some readpairs are messed up because the rev read goes past the fwd read or vice versa
        # Throw these out

        out_of_range = lambda p: (p < start_pos) or (p >= end_pos)

        if any(out_of_range(int(ref_pos)) for _, ref_pos in aligned_array):
            continue

        group_id = build_UMI_id(barcode, umi, start_pos, end_pos)

        if group_id not in groups:
            groups[group_id] = UMI(
                cell_barcode=barcode,
                umi_barcode=umi,
                start_pos=start_pos,
                end_pos=end_pos,
            )
        groups[group_id].add_readpair(
            ReadPair(read_name=read_name, fwd_read=read, rev_read=None)
        )
        barcode_depth[barcode] += end_pos - start_pos

    return list(groups.values()), barcode_depth


def initialize_position_counts_dict() -> dict[str, int]:
    return {"A": 0, "C": 0, "G": 0, "T": 0, "N": 0}


def consensus_call_UMI(
    g: UMI,
    mito_ref_seq: pd.DataFrame,
    consensus_call_strategy: ConsensusCallStrategy,
    quality_threshold: int,
) -> ConsensusCallResult:

    if consensus_call_strategy == ConsensusCallStrategy.MEAN_QUALITY:
        return consensus_call_UMI_quality_based(g, mito_ref_seq, quality_threshold)

    return consensus_call_UMI_consensus_based(g, mito_ref_seq, quality_threshold)


def consensus_call_UMI_quality_based(
    g: UMI, mito_ref_seq: pd.DataFrame, quality_threshold: int
) -> ConsensusCallResult:
    """
    Consensus call strategy that is like Picard "MarkDuplicates" and uses highest average quality readpair
    """
    # Initialize Empty Objects
    encoding_vector = np.zeros(g.end_pos - g.start_pos)
    genotypes_dict = defaultdict(initialize_position_counts_dict)
    molecule_rows = []
    quality_reads_counts = 0

    # Find best read_pair
    qualities = [
        np.mean(read_pair.fwd_read.query_qualities) for read_pair in g.readpairs
    ]
    idx = np.argmax(qualities)
    best_read_pair = g.readpairs[idx]

    read = best_read_pair.fwd_read
    seq_0 = read.seq

    quality_0 = read.query_qualities

    # split aligned read pair into fwd_only, rev_only, and fwd and rev segments
    pos_array_0 = np.asarray(read.get_aligned_pairs(matches_only=True, with_seq=False))

    ## fwd strand only
    for read_idx, ref_pos in pos_array_0:
        read_idx = int(read_idx)
        ref_pos = int(ref_pos)

        if quality_0[read_idx] > quality_threshold:
            genotypes_dict[ref_pos][seq_0[read_idx].upper()] += 1
        else:
            genotypes_dict[ref_pos]["N"] += 1

    for position in genotypes_dict:
        ref = mito_ref_seq[position].upper()

        reads = genotypes_dict[position]

        counts = {base: (reads[base]) for base in DNA_LETTERS}
        called_base = max(counts, key=counts.get)

        if ref == called_base:
            encoding_vector[position - g.start_pos] = 1
            quality_reads_counts += 1
            continue

        if "N" == called_base:
            encoding_vector[position - g.start_pos] = -1
            continue

        # does group size incude N calls? Here we say no
        group_size = sum((counts[base] for base in DNA_BASES))
        # group_size_with_Ns = sum((counts[base] for base in DNA_LETTERS))

        if group_size < 1:
            encoding_vector[position - g.start_pos] = -1
            continue

        # record alt
        encoding_vector[position - g.start_pos] = 2
        quality_reads_counts += 1

        single_group_size = sum(counts.values())
        double_group_size = 0

        total_supporting_counts = counts[called_base]
        single_supporting_counts = counts[called_base]
        double_supporting_counts = 0

        fwd_count = counts[called_base]
        rev_count = 0

        fraction_supporting_call = total_supporting_counts / group_size
        fraction_supporting_ref = 0 if ref == "N" else counts[ref] / group_size

        single_fraction_supporting_call = (
            0
            if single_group_size == 0
            else single_supporting_counts / single_group_size
        )
        double_fraction_supporting_call = 0

        single_fraction_supporting_ref = (
            0
            if (single_group_size == 0 or ref == "N")
            else counts[ref] / single_group_size
        )
        double_fraction_supporting_ref = 0

        result = {
            # 0 indexing so have to add 1 to get actual genomic position
            "position": position + 1,
            "barcode": g.cell_barcode,
            "variant": str(position + 1) + "_" + ref + "_" + called_base,
            "group_id": g.key,
            "call": called_base,
            "ref": ref,
            # joined single and double
            "consensus_group_size": group_size,
            "supporting_counts": total_supporting_counts,
            "fraction_supporting_call": fraction_supporting_call,
            "fraction_supporting_ref": fraction_supporting_ref,
            # just single
            "single_group_size": single_group_size,
            "single_supporting_counts": single_supporting_counts,
            "single_fraction_supporting_call": single_fraction_supporting_call,
            "single_fraction_supporting_ref": single_fraction_supporting_ref,
            # just double
            "double_group_size": double_group_size,
            "double_supporting_counts": double_supporting_counts,
            "double_fraction_supporting_call": double_fraction_supporting_call,
            "double_fraction_supporting_ref": double_fraction_supporting_ref,
            # fwd rev info
            "fwd_count": fwd_count,
            "rev_count": rev_count,
        }

        molecule_rows.append(result)

    encoding_vector_str = "".join([str(num) for num in encoding_vector.astype(int)])
    return ConsensusCallResult(
        encoding_vector=encoding_vector_str,
        rows=molecule_rows,
        quality_coverage_count=quality_reads_counts,
    )


def consensus_call_UMI_consensus_based(
    g: UMI, mito_ref_seq: pd.DataFrame, quality_threshold: int
) -> ConsensusCallResult:
    """
    Consensus call strategy that is really a "consensus" and uses all read pairs
    """
    # Initialize Empty Objects
    genotypes_dict = defaultdict(initialize_position_counts_dict)
    encoding_vector = np.zeros(g.end_pos - g.start_pos)
    quality_reads_counts = 0
    molecule_rows = []

    # Iterate over the read_pairs in the eUMI
    for read_pair in g.readpairs:

        read = read_pair.fwd_read
        seq_0 = read.seq
        quality_0 = read.query_qualities

        # split aligned read pair into fwd_only, rev_only, and fwd and rev segments
        pos_array_0 = np.asarray(
            read.get_aligned_pairs(matches_only=True, with_seq=False)
        )

        ## fwd strand only
        for read_idx, ref_pos in pos_array_0:
            read_idx = int(read_idx)
            ref_pos = int(ref_pos)

            if quality_0[read_idx] > quality_threshold:
                genotypes_dict[ref_pos][seq_0[read_idx].upper()] += 1
            else:
                genotypes_dict[ref_pos]["N"] += 1

    for position in genotypes_dict:
        ref = mito_ref_seq[position].upper()

        reads = genotypes_dict[position]

        counts = {base: (reads[base]) for base in DNA_LETTERS}
        called_base = max(counts, key=counts.get)

        if ref == called_base:
            encoding_vector[position - g.start_pos] = 1
            quality_reads_counts += 1
            continue

        if "N" == called_base:
            encoding_vector[position - g.start_pos] = -1
            continue

        # does group size incude N calls? Here we say no
        group_size = sum((counts[base] for base in DNA_BASES))
        # group_size_with_Ns = sum((counts[base] for base in DNA_LETTERS))

        if group_size < 1:
            encoding_vector[position - g.start_pos] = -1
            continue

        # record alt
        encoding_vector[position - g.start_pos] = 2
        quality_reads_counts += 1

        single_group_size = sum(counts.values())
        double_group_size = 0

        total_supporting_counts = counts[called_base]
        single_supporting_counts = counts[called_base]
        double_supporting_counts = 0

        fwd_count = counts[called_base]
        rev_count = 0

        fraction_supporting_call = total_supporting_counts / group_size
        fraction_supporting_ref = 0 if ref == "N" else counts[ref] / group_size

        single_fraction_supporting_call = (
            0
            if single_group_size == 0
            else single_supporting_counts / single_group_size
        )
        double_fraction_supporting_call = 0

        single_fraction_supporting_ref = (
            0
            if (single_group_size == 0 or ref == "N")
            else counts[ref] / single_group_size
        )
        double_fraction_supporting_ref = 0

        result = {
            # 0 indexing so have to add 1 to get actual genomic position
            "position": position + 1,
            "barcode": g.cell_barcode,
            "variant": str(position + 1) + "_" + ref + "_" + called_base,
            "group_id": g.key,
            "call": called_base,
            "ref": ref,
            # joined single and double
            "consensus_group_size": group_size,
            "supporting_counts": total_supporting_counts,
            "fraction_supporting_call": fraction_supporting_call,
            "fraction_supporting_ref": fraction_supporting_ref,
            # just single
            "single_group_size": single_group_size,
            "single_supporting_counts": single_supporting_counts,
            "single_fraction_supporting_call": single_fraction_supporting_call,
            "single_fraction_supporting_ref": single_fraction_supporting_ref,
            # just double
            "double_group_size": double_group_size,
            "double_supporting_counts": double_supporting_counts,
            "double_fraction_supporting_call": double_fraction_supporting_call,
            "double_fraction_supporting_ref": double_fraction_supporting_ref,
            # fwd rev info
            "fwd_count": fwd_count,
            "rev_count": rev_count,
        }

        molecule_rows.append(result)

    encoding_vector_str = "".join([str(num) for num in encoding_vector.astype(int)])
    return ConsensusCallResult(
        encoding_vector=encoding_vector_str,
        rows=molecule_rows,
        quality_coverage_count=quality_reads_counts,
    )
