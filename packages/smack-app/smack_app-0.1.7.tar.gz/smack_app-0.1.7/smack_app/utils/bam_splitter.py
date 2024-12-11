from itertools import repeat
import math
from multiprocessing import Pool
import os
import pysam
from typing import Optional


def verify_bai(bamfile: str) -> None:
    """
    Function that indexes bam file from input if missing
    """
    bai_file = bamfile + ".bai"
    if not os.path.exists(bai_file):
        pysam.index(bamfile)


def extract_barcodes(barcode_file: str) -> set[str]:
    with open(barcode_file) as f:
        content = f.readlines()
    return set([x.strip().strip('"').strip("'") for x in content])


def create_mini_bam(
    bf: str,
    bamfile: str,
    bam_dir: str,
    barcode_tag: str,
    umi_barcode_tag: Optional[str],
    mito_chr: str,
) -> tuple[int, int, int]:
    whitelist_codes = extract_barcodes(bf)
    bam = pysam.AlignmentFile(bamfile, "rb")
    outname = os.path.join(bam_dir, f"{os.path.basename(os.path.splitext(bf)[0])}.bam")
    outfile = pysam.AlignmentFile(outname, "wb", template=bam)

    n_discarded_reads = 0
    n_reads = 0
    n_writes = 0
    try:
        Itr = bam.fetch(str(mito_chr), multiple_iterators=False)
        for read in Itr:
            n_reads += 1
            try:
                barcode_id = read.get_tag(barcode_tag)

                if umi_barcode_tag:
                    umi_id = read.get_tag(umi_barcode_tag)

                if barcode_id in whitelist_codes:
                    outfile.write(read)
                    n_writes += 1

            except KeyError:
                # Discarding read {read.query_name} since it does not have barcode_tag
                # (or umi_tag if needed)
                n_discarded_reads += 1

    except OSError:
        pass

    bam.close()
    outfile.close()

    return (n_writes, n_reads, n_discarded_reads)


class BamSplitter:
    """
    Helper class for taking a large .bam file and accompanying list of barcodes .txt file,
    and splitting them into chunks. The class helps split the barcode list evenly and then
    creates matching smaller .bam files with reads for the split barcode sets
    """

    def __init__(
        self,
        bamfile: str,
        barcode_file: str,
        mito_chr: str,
        barcode_tag: str = "BC",
        umi_barcode_tag: Optional[str] = None,
    ) -> None:

        self.barcode_file = barcode_file
        self.bamfile = bamfile
        self.barcode_tag = barcode_tag
        self.mito_chr = mito_chr
        self.umi_barcode_tag = umi_barcode_tag

        verify_bai(bamfile)

    def split(self, N: int, outdir: str, parallel=True) -> list[tuple[str, str]]:

        barcodes_txt_dir = os.path.join(outdir, "barcode_files")
        bam_dir = os.path.join(outdir, "barcoded_bams")
        if not os.path.exists(barcodes_txt_dir):
            os.makedirs(barcodes_txt_dir)
        if not os.path.exists(bam_dir):
            os.makedirs(bam_dir)

        bfs = _split_barcodes_file(self.barcode_file, N, barcodes_txt_dir)

        if parallel and N > 1:
            p = Pool(N)

            pool_result = p.starmap(
                create_mini_bam,
                zip(
                    bfs,
                    repeat(self.bamfile),
                    repeat(bam_dir),
                    repeat(self.barcode_tag),
                    repeat(self.umi_barcode_tag),
                    repeat(self.mito_chr),
                ),
            )

            # Barcodes don't match, split BAM is empty
            if any(result[0] == 0 for result in pool_result):
                raise Exception(
                    "One or more of the split BAMs is empty. Please make sure that barcodes in the .txt file match the barcodes in the BAM. Run with ncores=1 to isolate which barcodes files are messed up"
                )

            nreads = max(result[1] for result in pool_result)
            discarded_reads = max(result[2] for result in pool_result)

            p.close()
        else:
            nreads = 0
            discarded_reads = 0
            for bf in bfs:
                nw, nr, dr = create_mini_bam(
                    bf,
                    self.bamfile,
                    bam_dir,
                    self.barcode_tag,
                    self.umi_barcode_tag,
                    self.mito_chr,
                )
                nreads = max(nreads, nr)
                discarded_reads = max(discarded_reads, dr)
                if nw == 0:
                    raise Exception(
                        f"Barcode matched BAM is empty. Please make sure that barcodes in the {bf} file match the barcodes in the BAM"
                    )

        message_suffix = (
            f"tag {self.barcode_tag}"
            if self.umi_barcode_tag is None
            else f"tag {self.barcode_tag} or tag {self.umi_barcode_tag}"
        )
        print(
            f"Threw out {discarded_reads} / {nreads} reads because they did not have {message_suffix}"
        )
        return [
            (
                bf,
                os.path.join(
                    bam_dir, f"{os.path.basename(os.path.splitext(bf)[0])}.bam"
                ),
            )
            for bf in bfs
        ]


def _split_barcodes_file(barcode_file: str, N: int, outdirectory: str) -> list[str]:

    if N <= 1:
        return [barcode_file]

    with open(barcode_file, "r") as f:
        file_len = sum(1 for _ in f)

    lines_per_file = math.ceil(file_len / N)

    smallfile = None
    outfiles = []
    file_index = 0
    with open(barcode_file) as bigfile:
        for lineno, line in enumerate(bigfile):
            if lineno % lines_per_file == 0:
                if smallfile:
                    smallfile.close()
                file_index += 1
                path = os.path.join(outdirectory, f"barcodes.{file_index}.txt")
                outfiles.append(path)
                smallfile = open(path, "w")
            smallfile.write(line)
    if smallfile:
        smallfile.close()

    return outfiles
