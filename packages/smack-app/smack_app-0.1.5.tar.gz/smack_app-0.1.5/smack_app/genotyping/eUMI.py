from collections import defaultdict
import numpy as np
import os
import pandas as pd
import sys
from typing import Union

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from genotyping.h5_schema import eUMI_DELIM
from genotyping.ConsensusGroup import (
    ConsensusGroup,
    DNA_BASES,
    DNA_LETTERS,
    ReadPair,
    ConsensusCallResult,
)
from utils.utils import ConsensusCallStrategy


def build_eUMI_id(
    barcode: str, start_pos: Union[int, str], end_pos: Union[int, str]
) -> str:
    return barcode + eUMI_DELIM + str(start_pos) + eUMI_DELIM + str(end_pos)


def deconstruct_eUMI_id(eUMI_id: str) -> tuple[str, int, int]:
    [barcode, start, end] = eUMI_id.split(eUMI_DELIM)
    return (barcode, int(start), int(end))


class eUMI(ConsensusGroup):
    def __init__(self, cell_barcode: str, start_pos: int, end_pos: int) -> None:
        super().__init__()
        self.cell_barcode = cell_barcode
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.key = build_eUMI_id(cell_barcode, start_pos, end_pos)
        self.group_type = "eUMI"


def get_eUMIs_and_barcode_depth_from_read_pairs(
    read_pair_dict: dict,
    barcode_tag: str,
    barcodes: list,
    max_bp: int,
    max_eUMI_size: int,
    eUMI_trim: int,
    mapping_quality_threshold: int,
) -> tuple[list, dict]:

    eUMIs = {}
    barcode_depth = defaultdict(int)
    barcodes = set(barcodes)

    for read_name, read_list in read_pair_dict.items():

        # disregard singlets and multiplets
        if len(read_list) != 2:
            continue

        # identify fwd and rev in a pair
        read0, read1 = read_list
        if read0.is_reverse and not read1.is_reverse:
            fwd_read, rev_read = read1, read0
        elif not read0.is_reverse and read1.is_reverse:
            fwd_read, rev_read = read0, read1
        else:
            # disregard a pair if both are the same strand
            continue

        if not fwd_read.has_tag(barcode_tag):
            continue
        barcode = fwd_read.get_tag(barcode_tag)

        assert (
            barcode in barcodes
        ), f"Found barcode: {barcode} in BAM file but not in barcodes.txt file. The split BAM and barcodes file must match"

        if fwd_read.tlen > 0:
            start_pos = int(fwd_read.pos)
            end_pos = int(fwd_read.pos) + int(fwd_read.tlen)
        else:
            start_pos = int(fwd_read.pos) - int(fwd_read.tlen)
            end_pos = int(fwd_read.pos)

        # throw out read pairs with low mapping quality
        if (int(fwd_read.mapping_quality) < mapping_quality_threshold) or (
            int(rev_read.mapping_quality) < mapping_quality_threshold
        ):
            continue

        # some readpairs are messed up because of the cicular genome. Throw them out
        if (start_pos >= max_bp) or (end_pos > max_bp):
            continue

        # some readpairs are messed up because they are super far apart from each other
        # some aligners thrown these out, but some keep them and we need to skip them
        if (end_pos - start_pos) > max_eUMI_size:
            continue

        # some readpairs are messed up because the rev read goes past the fwd read or vice versa
        # Throw these out

        out_of_range = lambda p: (p < start_pos) or (p >= end_pos)

        if any(
            out_of_range(int(ref_pos))
            for _, ref_pos in np.asarray(
                rev_read.get_aligned_pairs(matches_only=True, with_seq=False)
            )
        ):
            continue

        if any(
            out_of_range(int(ref_pos))
            for _, ref_pos in np.asarray(
                fwd_read.get_aligned_pairs(matches_only=True, with_seq=False)
            )
        ):
            continue

        start_pos = start_pos + eUMI_trim
        end_pos = end_pos - eUMI_trim

        eUMI_id = build_eUMI_id(barcode, start_pos, end_pos)

        if eUMI_id not in eUMIs:
            eUMIs[eUMI_id] = eUMI(
                cell_barcode=barcode, start_pos=start_pos, end_pos=end_pos
            )
        eUMIs[eUMI_id].add_readpair(
            ReadPair(read_name=read_name, fwd_read=fwd_read, rev_read=rev_read)
        )
        barcode_depth[barcode] += end_pos - start_pos

    return list(eUMIs.values()), barcode_depth


def initialize_position_counts_dict() -> dict[int, dict[str, int]]:
    return {
        "single": {"A": 0, "C": 0, "G": 0, "T": 0, "N": 0},
        "double": {"A": 0, "C": 0, "G": 0, "T": 0, "N": 0},
        "strand": {"fwd": 0, "rev": 0},
    }


def consensus_call_eUMI(
    e: eUMI,
    mito_ref_seq: pd.DataFrame,
    consensus_call_strategy: ConsensusCallStrategy,
    quality_threshold: int,
) -> ConsensusCallResult:

    if consensus_call_strategy == ConsensusCallStrategy.MEAN_QUALITY:
        return consensus_call_eUMI_quality_based(e, mito_ref_seq, quality_threshold)

    return consensus_call_eUMI_consensus_based(e, mito_ref_seq, quality_threshold)


def consensus_call_eUMI_quality_based(
    e: eUMI, mito_ref_seq: pd.DataFrame, quality_threshold: int
) -> ConsensusCallResult:
    """
    Consensus call strategy that is like Picard "MarkDuplicates" and uses highest average quality readpair
    """

    # Initialize Empty Objects
    genotypes_dict = defaultdict(initialize_position_counts_dict)
    encoding_vector = np.zeros(e.end_pos - e.start_pos)
    quality_reads_counts = 0
    molecule_rows = []

    # Find best read_pair
    qualities = [
        np.mean(
            [
                np.mean(read_pair.fwd_read.query_qualities),
                np.mean(read_pair.rev_read.query_qualities),
            ]
        )
        for read_pair in e.readpairs
    ]
    idx = np.argmax(qualities)
    best_read_pair = e.readpairs[idx]

    seq_0 = best_read_pair.fwd_read.seq
    seq_1 = best_read_pair.rev_read.seq
    quality_0 = best_read_pair.fwd_read.query_qualities
    quality_1 = best_read_pair.rev_read.query_qualities

    # split aligned read pair into fwd_only, rev_only, and fwd and rev segments
    pos_array_0 = np.asarray(
        best_read_pair.fwd_read.get_aligned_pairs(matches_only=True, with_seq=False)
    )
    pos_array_1 = np.asarray(
        best_read_pair.rev_read.get_aligned_pairs(matches_only=True, with_seq=False)
    )

    pos_array_overlap = np.intersect1d(pos_array_0[:, 1], pos_array_1[:, 1])

    zero_mask = np.isin(pos_array_0[:, 1], pos_array_overlap)
    one_mask = np.isin(pos_array_1[:, 1], pos_array_overlap)

    pos_array_specific_0 = pos_array_0[~zero_mask]
    pos_array_specific_1 = pos_array_1[~one_mask]
    pos_array_overlap_0 = pos_array_0[zero_mask]
    pos_array_overlap_1 = pos_array_1[one_mask]

    ## fwd strand only
    for read_idx, ref_pos in pos_array_specific_0:
        read_idx = int(read_idx)
        ref_pos = int(ref_pos)

        if quality_0[read_idx] > quality_threshold:

            genotypes_dict[ref_pos]["single"][seq_0[read_idx].upper()] += 1
            genotypes_dict[ref_pos]["strand"]["fwd"] += 1
        else:
            genotypes_dict[ref_pos]["single"]["N"] += 1

    ## both strands
    if len(pos_array_overlap) > 0:
        for (read_idx0, ref_pos0), (read_idx1, ref_pos1) in zip(
            pos_array_overlap_0, pos_array_overlap_1
        ):
            read_idx0 = int(read_idx0)
            ref_pos0 = int(ref_pos0)
            read_idx1 = int(read_idx1)
            ref_pos1 = int(ref_pos1)

            assert (
                ref_pos0 == ref_pos1
            ), f"overlapped read pair requires ref_pos0 == ref_pos1, but here we have {ref_pos0} and {ref_pos1}"

            if (seq_0[read_idx0].upper() == seq_1[read_idx1].upper()) and (
                quality_0[read_idx0] > quality_threshold
                or quality_1[read_idx1] > quality_threshold
            ):

                genotypes_dict[ref_pos0]["double"][seq_0[read_idx0].upper()] += 1
                genotypes_dict[ref_pos0]["strand"]["fwd"] += 1
                genotypes_dict[ref_pos0]["strand"]["rev"] += 1

            else:
                genotypes_dict[ref_pos0]["single"]["N"] += 1

    ## rev strand only
    for read_idx, ref_pos in pos_array_specific_1:
        read_idx = int(read_idx)
        ref_pos = int(ref_pos)

        if quality_1[read_idx] > quality_threshold:
            genotypes_dict[ref_pos]["single"][seq_1[read_idx].upper()] += 1
            genotypes_dict[ref_pos]["strand"]["rev"] += 1
        else:
            genotypes_dict[ref_pos]["single"]["N"] += 1

    for position in genotypes_dict:

        # may be out of range if we clipped/trimmed eUMIs, if so throw it out
        if position < e.start_pos:
            continue
        if position >= e.end_pos:
            continue

        ref = mito_ref_seq[position].upper()

        single_reads = genotypes_dict[position]["single"]
        double_reads = genotypes_dict[position]["double"]

        counts = {
            base: (single_reads[base]) + (double_reads[base]) for base in DNA_LETTERS
        }
        called_base = max(counts, key=counts.get)

        if ref == called_base:
            encoding_vector[position - e.start_pos] = 1
            quality_reads_counts += 1
            continue

        if "N" == called_base:
            encoding_vector[position - e.start_pos] = -1
            continue

        single_counts = {base: (single_reads[base]) for base in DNA_BASES}
        double_counts = {base: (double_reads[base]) for base in DNA_BASES}

        # does group size incude N calls? Here we say no
        group_size = sum((counts[base] for base in DNA_BASES))
        # group_size_with_Ns = sum((counts[base] for base in DNA_LETTERS))

        if group_size < 1:
            encoding_vector[position - e.start_pos] = -1
            continue

        # record alt
        encoding_vector[position - e.start_pos] = 2
        quality_reads_counts += 1

        single_group_size = sum(single_counts.values())
        double_group_size = sum(double_counts.values())

        total_supporting_counts = counts[called_base]
        single_supporting_counts = single_reads[called_base]
        double_supporting_counts = double_reads[called_base]

        fwd_count = genotypes_dict[position]["strand"]["fwd"]
        rev_count = genotypes_dict[position]["strand"]["rev"]

        fraction_supporting_call = total_supporting_counts / group_size
        fraction_supporting_ref = 0 if ref == "N" else counts[ref] / group_size

        single_fraction_supporting_call = (
            0
            if single_group_size == 0
            else single_supporting_counts / single_group_size
        )
        double_fraction_supporting_call = (
            0
            if double_group_size == 0
            else double_supporting_counts / double_group_size
        )
        single_fraction_supporting_ref = (
            0
            if (single_group_size == 0 or ref == "N")
            else single_counts[ref] / single_group_size
        )
        double_fraction_supporting_ref = (
            0
            if (double_group_size == 0 or ref == "N")
            else double_counts[ref] / double_group_size
        )

        result = {
            # 0 indexing so have to add 1 to get actual genomic position
            "position": position + 1,
            "barcode": e.cell_barcode,
            "variant": str(position + 1) + "_" + ref + "_" + called_base,
            "group_id": e.key,
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


def consensus_call_eUMI_consensus_based(
    e: eUMI, mito_ref_seq: pd.DataFrame, quality_threshold: int
) -> ConsensusCallResult:

    # Initialize Empty Objects
    genotypes_dict = defaultdict(initialize_position_counts_dict)
    encoding_vector = np.zeros(e.end_pos - e.start_pos)
    quality_reads_counts = 0
    molecule_rows = []

    # Iterate over the read_pairs in the eUMI
    for read_pair in e.readpairs:

        seq_0 = read_pair.fwd_read.seq
        seq_1 = read_pair.rev_read.seq
        quality_0 = read_pair.fwd_read.query_qualities
        quality_1 = read_pair.rev_read.query_qualities

        # split aligned read pair into fwd_only, rev_only, and fwd and rev segments
        pos_array_0 = np.asarray(
            read_pair.fwd_read.get_aligned_pairs(matches_only=True, with_seq=False)
        )
        pos_array_1 = np.asarray(
            read_pair.rev_read.get_aligned_pairs(matches_only=True, with_seq=False)
        )

        pos_array_overlap = np.intersect1d(pos_array_0[:, 1], pos_array_1[:, 1])

        zero_mask = np.isin(pos_array_0[:, 1], pos_array_overlap)
        one_mask = np.isin(pos_array_1[:, 1], pos_array_overlap)

        pos_array_specific_0 = pos_array_0[~zero_mask]
        pos_array_specific_1 = pos_array_1[~one_mask]
        pos_array_overlap_0 = pos_array_0[zero_mask]
        pos_array_overlap_1 = pos_array_1[one_mask]

        ## fwd strand only
        for read_idx, ref_pos in pos_array_specific_0:
            read_idx = int(read_idx)
            ref_pos = int(ref_pos)

            if quality_0[read_idx] > quality_threshold:

                genotypes_dict[ref_pos]["single"][seq_0[read_idx].upper()] += 1
                genotypes_dict[ref_pos]["strand"]["fwd"] += 1
            else:
                genotypes_dict[ref_pos]["single"]["N"] += 1

        ## both strands
        if len(pos_array_overlap) > 0:
            for (read_idx0, ref_pos0), (read_idx1, ref_pos1) in zip(
                pos_array_overlap_0, pos_array_overlap_1
            ):
                read_idx0 = int(read_idx0)
                ref_pos0 = int(ref_pos0)
                read_idx1 = int(read_idx1)
                ref_pos1 = int(ref_pos1)

                assert (
                    ref_pos0 == ref_pos1
                ), f"overlapped read pair requires ref_pos0 == ref_pos1, but here we have {ref_pos0} and {ref_pos1}"

                if (seq_0[read_idx0].upper() == seq_1[read_idx1].upper()) and (
                    quality_0[read_idx0] > quality_threshold
                    or quality_1[read_idx1] > quality_threshold
                ):

                    genotypes_dict[ref_pos0]["double"][seq_0[read_idx0].upper()] += 1
                    genotypes_dict[ref_pos0]["strand"]["fwd"] += 1
                    genotypes_dict[ref_pos0]["strand"]["rev"] += 1

                else:
                    genotypes_dict[ref_pos0]["single"]["N"] += 1

        ## rev strand only
        for read_idx, ref_pos in pos_array_specific_1:
            read_idx = int(read_idx)
            ref_pos = int(ref_pos)

            if quality_1[read_idx] > quality_threshold:
                genotypes_dict[ref_pos]["single"][seq_1[read_idx].upper()] += 1
                genotypes_dict[ref_pos]["strand"]["rev"] += 1
            else:
                genotypes_dict[ref_pos]["single"]["N"] += 1

    for position in genotypes_dict:

        # may be out of range if we clipped/trimmed eUMIs, if so throw it out
        if position < e.start_pos:
            continue
        if position >= e.end_pos:
            continue

        ref = mito_ref_seq[position].upper()

        single_reads = genotypes_dict[position]["single"]
        double_reads = genotypes_dict[position]["double"]

        counts = {
            base: (single_reads[base]) + (double_reads[base]) for base in DNA_LETTERS
        }
        called_base = max(counts, key=counts.get)

        if ref == called_base:
            encoding_vector[position - e.start_pos] = 1
            quality_reads_counts += 1
            continue

        if "N" == called_base:
            encoding_vector[position - e.start_pos] = -1
            continue

        single_counts = {base: (single_reads[base]) for base in DNA_BASES}
        double_counts = {base: (double_reads[base]) for base in DNA_BASES}

        # does group size incude N calls? Here we say no
        group_size = sum((counts[base] for base in DNA_BASES))
        # group_size_with_Ns = sum((counts[base] for base in DNA_LETTERS))

        if group_size < 1:
            encoding_vector[position - e.start_pos] = -1
            continue

        # record alt
        encoding_vector[position - e.start_pos] = 2
        quality_reads_counts += 1

        single_group_size = sum(single_counts.values())
        double_group_size = sum(double_counts.values())

        total_supporting_counts = counts[called_base]
        single_supporting_counts = single_reads[called_base]
        double_supporting_counts = double_reads[called_base]

        fwd_count = genotypes_dict[position]["strand"]["fwd"]
        rev_count = genotypes_dict[position]["strand"]["rev"]

        fraction_supporting_call = total_supporting_counts / group_size
        fraction_supporting_ref = 0 if ref == "N" else counts[ref] / group_size

        single_fraction_supporting_call = (
            0
            if single_group_size == 0
            else single_supporting_counts / single_group_size
        )
        double_fraction_supporting_call = (
            0
            if double_group_size == 0
            else double_supporting_counts / double_group_size
        )
        single_fraction_supporting_ref = (
            0
            if (single_group_size == 0 or ref == "N")
            else single_counts[ref] / single_group_size
        )
        double_fraction_supporting_ref = (
            0
            if (double_group_size == 0 or ref == "N")
            else double_counts[ref] / double_group_size
        )

        result = {
            # 0 indexing so have to add 1 to get actual genomic position
            "position": position + 1,
            "barcode": e.cell_barcode,
            "variant": str(position + 1) + "_" + ref + "_" + called_base,
            "group_id": e.key,
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
