import os
from multiprocessing import Pool
from rich import print
from rich.panel import Panel
from rich.console import Console
from rich.table import Table
import shutil
import subprocess
import sys
import typer
from typing import Optional
from typing_extensions import Annotated

import smack_app.cli_validation as cli_validation

from smack_app.reference.genome_reference import create_refAllele_file
import smack_app.variant_filters.filter_sets as filter_sets
from smack_app.utils.bam_splitter import BamSplitter
from smack_app.utils.utils import REPOPATH, UMI_Mode, ConsensusCallStrategy


app = typer.Typer(no_args_is_help=True)
_python = sys.executable

state = {}


@app.callback()
def setup(
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose/--no-verbose",
            "--debug",
            "-v/-nv",
            help="Provides detailed logging about all processess",
        ),
    ] = False,
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version",
            help="Prints app version",
            callback=cli_validation.version_callback,
            is_eager=True,
        ),
    ] = None,
    keep_temp_files: Annotated[
        bool,
        typer.Option(
            help="Keep temp files used throughout the process. If False, only final outputs will be kept and other files will be deleted."
        ),
    ] = False,
    dry_run: Annotated[
        bool,
        typer.Option(
            help="Verify input data and arguments without executing downstream commands"
        ),
    ] = False,
    wd: Annotated[
        Optional[str],
        typer.Option(
            "--working-directory",
            "-wd",
            help="Set working directory for temp and final output files",
        ),
    ] = "smack_working_directory",
):
    """
    Hi! Welcome to the SMACK tool - single-cell mitochondrial analysis CLI kit.
    See below for the commands you can run!

    """

    # \b
    # ^__^
    # (oo)\_______
    # (__)\       )\/\\
    # \t||----w |
    # \t||     ||

    # (｡•́︿•̀｡)
    # ¯\_(ツ)_/¯

    state["keep_temp_files"] = keep_temp_files
    state["dry_run"] = dry_run
    state["verbose"] = verbose
    if state["verbose"]:
        print("")
        print("Verbose is set to True. Will write verbose output...")
        print("")

    if not os.path.exists(wd):
        if state["verbose"]:
            print(
                f"Working Directory does not exist. Creating New Folder at path '{wd}'"
            )
        os.makedirs(wd)

    state["wd"] = wd
    if state["verbose"]:
        print(f"Initial CLI App state: {state}")
        print("")

    state["console"] = Console()


def _run_consensus_calling(
    sample_id: str,
    bamfile: str,
    h5_file: str,
    barcodes_file: str,
    mito_genome_path: str,
    umi_mode: UMI_Mode,
    consensus_call_strategy: ConsensusCallStrategy,
    genome_length: int,
    barcode_tag: str,
    umi_barcode_tag: Optional[str],
    base_quality: int,
    map_quality: int,
    max_eUMI_size: int,
    eUMI_trim: int,
):
    if state["verbose"]:
        print(
            "[bold] Running Consensus Calling Subprocess With the following arguments:"
        )
        state["console"].log(bamfile, log_locals=True)
    command_path = os.path.join(REPOPATH, "genotyping/run_consensus_variant_calling.py")
    command = [
        _python,
        command_path,
        "--bamfile",
        bamfile,
        "--barcodes",
        barcodes_file,
        "--outh5",
        h5_file,
        "--sample-id",
        sample_id,
        "--barcode",
        barcode_tag,
        "--bq",
        f"{base_quality}",
        "--consensus-call-strategy",
        consensus_call_strategy,
        "--mapq",
        f"{map_quality}",
        "--mito-ref-file",
        mito_genome_path,
        "--genome-length",
        f"{genome_length}",
        "--max-eUMI-size",
        f"{max_eUMI_size}",
        "--eUMI-trim",
        f"{eUMI_trim}",
    ]

    if umi_mode == UMI_Mode.UMI:
        command.append("--umi-tag")
        command.append(umi_barcode_tag)
        command.append("--umi-mode")
        command.append(UMI_Mode.UMI)
    else:
        command.append("--umi-mode")
        command.append(UMI_Mode.eUMI)

    print(f"Executing: {' '.join(command)}")

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(e.stderr)
        raise Exception("Consensus Calling Failed") from e


@app.command()
def genotype(
    input_bam: Annotated[
        str,
        typer.Argument(
            callback=cli_validation.assert_path_exists, help="Path to input BAM file"
        ),
    ],
    h5_directory: Annotated[
        str,
        typer.Argument(help="Directory to store output H5 files"),
    ],
    barcodes_file: Annotated[
        str,
        typer.Option(
            "--barcodes-file",
            "-bf",
            callback=cli_validation.assert_path_exists,
            help="Path to input barcodes file",
        ),
    ] = None,
    sample_id: Annotated[
        Optional[str],
        typer.Option(
            "--sample-id",
            "-id",
            help="Sample ID for metadata. Defaults to path of input BAM",
        ),
    ] = None,
    mito_genome: Annotated[
        cli_validation.Genome,
        typer.Option(
            "--genome",
            "-g",
            help="Name of genome or 'CUSTOM', along with --custom-genome-path <path>. Run get-supported-genomes to see list of built-in genomes.",
        ),
    ] = "rCRS",
    custom_genome_path: Annotated[
        Optional[str],
        typer.Option(
            "--custom-genome-path",
            help="Path to valid genome FASTA",
        ),
    ] = None,
    barcode_tag: Annotated[
        str,
        typer.Option(
            "--barcode-tag",
            "-bc",
            help="Tag for cell barcodes in BAM file (usually 'BC' or 'CB')",
        ),
    ] = "BC",
    umi_mode: Annotated[
        UMI_Mode,
        typer.Option(
            "--umi-mode",
            "-um",
            help="Group molecules based on eUMI (endogenous) or UMI (literal)",
        ),
    ] = UMI_Mode.eUMI,
    umi_barcode_tag: Annotated[
        Optional[str],
        typer.Option(
            "--umi-barcode-tag",
            "-ub",
            help="Tag for UMI barcode in BAM file. Ignored if umi-mode='eUMI'",
        ),
    ] = None,
    consensus_call_strategy: Annotated[
        ConsensusCallStrategy,
        typer.Option(
            "--consensus-call-strategy",
            "-s",
            help="Strategy for collapsing groups of molecules based on eUMI (endogenous) or UMI (literal)",
        ),
    ] = ConsensusCallStrategy.CONSENSUS,
    num_cores: Annotated[
        str,
        typer.Option(
            "--ncores",
            "-c",
            callback=cli_validation.ncores_selection,
            help="Number of cores to use. Either integer or 'detect' for auto-detecting based on system hardware.",
        ),
    ] = "detect",
    base_quality: Annotated[
        int,
        typer.Option(
            "--base-quality",
            "-bq",
            help="Minimum per base quality score at position X to be considered a valid read at X",
            callback=cli_validation.assert_not_negative,
        ),
    ] = 10,
    map_quality: Annotated[
        int,
        typer.Option(
            "--map-quality",
            "-mapq",
            help="Minimum map quality for a read pair to be considered valid",
            callback=cli_validation.assert_not_negative,
        ),
    ] = 30,
    max_eUMI_size: Annotated[
        int,
        typer.Option(
            "--max-eUMI-size",
            "-es",
            help="Maximum eUMI size. eUMIs that are too large are likely artifacts from misalignments",
            callback=cli_validation.assert_positive,
        ),
    ] = 1000,
    eUMI_trim: Annotated[
        int,
        typer.Option(
            "--eUMI-trim",
            "-et",
            help="Number of bp to trim off each side of eUMI for position edge bias",
            callback=cli_validation.assert_not_negative,
        ),
    ] = 0,
):
    """
    Go from a single BAM --> Directory of H5 Files With Variant Calls
    """

    if umi_mode == UMI_Mode.eUMI:
        if umi_barcode_tag:
            raise typer.BadParameter(
                "Cannot use umi-barcode tag in umi-mode 'eUMI'. Either set umi-mode to UMI or omit umi-barcode"
            )

    if mito_genome == cli_validation.Genome.CUSTOM:
        if not custom_genome_path:
            raise typer.BadParameter(
                "mito-genome set to CUSTOM but no genome was supplied. Either use built-in genome or use CUSTOM together with --custom-genome-path <path>"
            )

        cli_validation.validate_custom_genome_path(custom_genome_path)
        genome_fasta_path = custom_genome_path
        if state["verbose"]:
            print(f"Using custome genome from path {genome_fasta_path}")
    else:
        mito_genome = mito_genome.value
        genome_fasta_path = cli_validation.get_support_genome_fasta_path(mito_genome)
        if state["verbose"]:
            print(f"Using built-in genome from path {genome_fasta_path}")

    (genome_txt_path, genome_name, mito_length) = create_refAllele_file(
        genome_fasta_path,
        os.path.join(REPOPATH, f"reference/{mito_genome}.txt"),
    )
    if state["verbose"]:
        print(f"Contig Name: {genome_name}")
        print(
            f"Using mito reference genome with length {mito_length} written to {genome_txt_path}"
        )

    if state["verbose"]:
        print(f"Attempting to run with {num_cores} cores...")

    if not sample_id:
        sample_id = input_bam
        if state["verbose"]:
            print(f"sample_id not set, setting sample_id to bam path: {input_bam}")

    bam_splitter = BamSplitter(
        input_bam, barcodes_file, genome_name, barcode_tag, umi_barcode_tag
    )

    if state["verbose"]:
        print(f"Splitting input BAM into {num_cores} samples...")

    split_samples = bam_splitter.split(num_cores, state["wd"])

    print(
        f"Split Succeeded. \n Ready to process {len(split_samples)} samples with paths: {split_samples}"
    )

    if state["dry_run"]:
        print(
            Panel.fit(
                "\n [bold green]Dry Run Completed Successfully ✅! \n [red]To run in regular mode remove flag --dry-run. \n",
                border_style="blue",
            )
        )
        return

    p = Pool(num_cores)
    command_args = []

    if not os.path.exists(h5_directory):
        if state["verbose"]:
            print(f"Creating directory {h5_directory}")
        os.makedirs(h5_directory)

    for barcodes_file, bamfile in split_samples:
        h5_file = os.path.join(
            h5_directory, f"{os.path.basename(os.path.splitext(barcodes_file)[0])}.h5"
        )

        command_args.append(
            (
                sample_id,
                bamfile,
                h5_file,
                barcodes_file,
                genome_txt_path,
                umi_mode,
                consensus_call_strategy,
                mito_length,
                barcode_tag,
                umi_barcode_tag,
                base_quality,
                map_quality,
                max_eUMI_size,
                eUMI_trim,
            )
        )
    p.starmap(_run_consensus_calling, command_args)
    p.close()

    print(
        Panel.fit(
            "\n [bold green] Genotyping Completed Successfully ✅! \n [red] To get variants, run the filter-variants command. \n",
            border_style="blue",
        )
    )


@app.command()
def get_supported_genomes():
    """
    Prints which genomes have built-in support
    """
    print("")
    table = Table(title="Supported Genomes", show_lines=True, title_style="bold")
    table.add_column("Name", justify="right", style="cyan", no_wrap=True)
    table.add_column("Path", justify="left", style="magenta", no_wrap=True)

    for g in cli_validation.Genome:
        if g != cli_validation.Genome.CUSTOM:
            table.add_row(g.value, f"{REPOPATH}/reference/fasta_files/{g.value}.fasta")

    table.add_row("CUSTOM", "/path/to/custom_genome.fasta")
    state["console"].print(table)


@app.command()
def get_supported_filter_sets():
    """
    Prints the preset filter sets for variants, and which technology it is recommended for
    """
    print("")
    print("-------------Filter Sets-------------")
    print("")
    for filter_name, filter_dict in filter_sets.FILTER_MAP.items():
        table = Table(title=filter_name, show_lines=True, title_style="bold")
        table.add_column("Key", justify="right", style="cyan", no_wrap=True)
        table.add_column("Value", justify="left", style="magenta", no_wrap=True)
        for key, value in filter_dict.items():
            table.add_row(key, f"{value}")
        state["console"].print(table)


@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def filter_variants(
    ctx: typer.Context,
    h5_directory: Annotated[
        str,
        typer.Argument(
            help="String path to h5 directory or comma-separated string list of h5 directories. Should usually be the same path(s) output by `genotype` command.",
            callback=cli_validation.assert_list_of_paths_exist,
        ),
    ],
    filter_set: Annotated[
        filter_sets.FilterSet,
        typer.Argument(
            help="Name of filter set to use (or 'CUSTOM', along with all parameters set as kwargs). Run get-supported-filter-sets to see list of built-in filter sets.",
        ),
    ],
    umi_mode: Annotated[
        UMI_Mode,
        typer.Option(
            "--umi-mode",
            "-um",
            help="Group molecules based on `eUMI` (endogenous) or `UMI` (literal)",
        ),
    ] = UMI_Mode.eUMI,
    min_barcode_depth: Annotated[
        float,
        typer.Option(
            help="Minimum depth for a cell/barcode to be kept",
            callback=cli_validation.assert_not_negative,
        ),
    ] = 10,
):
    """
    Collect All Possible Variants from the split H5 files. Filter variants based on parameters.
    H5 directory --> Heteroplasmy, Variants, and Coverage CSVs
    """

    filter_dict = {}
    if filter_set != filter_sets.FilterSet.CUSTOM:
        filter_set = filter_set.value
        print(f"Using filter set: {filter_set}")
        filter_dict.update(filter_sets.FILTER_MAP[filter_set])

    for extra_arg in ctx.args:
        try:
            [key, value] = extra_arg.removeprefix("--").replace("-", "_").split("=")
            if key not in filter_sets.known_filters:
                raise typer.BadParameter(
                    f"Unknown Filter Argument {key}. Run get-supported-filter-sets to see the available filters."
                )
            print(f"Overriding default value for {key} with {value}")
            filter_dict[key] = value
        except ValueError:
            raise typer.BadParameter(
                f"Could not understand filter argument {extra_arg}. To add filters, you must use the notation --<key>=<value>"
            )

    if state["dry_run"]:
        print(f"Found the following h5 directories: {h5_directory.split(',')}")
        print(f"Using the following filters: {filter_dict}")
        print(
            Panel.fit(
                "\n [bold green]Dry Run Completed Successfully ✅! \n [red]To run in regular mode remove flag --dry-run. \n",
                border_style="blue",
            )
        )
        return

    intermediate_output_directory = os.path.join(state["wd"], "temp/")
    if not os.path.exists(intermediate_output_directory):
        os.makedirs(intermediate_output_directory)
    final_output_directory = os.path.join(state["wd"], "final/")

    if not os.path.exists(final_output_directory):
        os.makedirs(final_output_directory)

    if state["verbose"]:
        print(f"[bold] Writing temp outputs to ...{intermediate_output_directory}")
        print("[bold] Finding barcodes that meet depth requirements...")

    command_path = os.path.join(REPOPATH, "filter_barcodes.py")

    command = [
        _python,
        command_path,
        "-h5dir",
        h5_directory,
        "-min-depth",
        f"{min_barcode_depth}",
        "-outdir",
        intermediate_output_directory,
    ]

    print(f"Executing: {' '.join(command)}")

    try:
        subprocess.run(command, check=True)
        pass
    except subprocess.CalledProcessError as e:
        print(e.stderr)
        raise Exception("Filtering Barcodes failed") from e

    barcode_depth_csv = os.path.join(intermediate_output_directory, "barcode_depth.csv")

    if state["verbose"]:
        print(
            f"Filtered Barcodes Successfully. Barcode depth CSV at {barcode_depth_csv}"
        )
    command_path = os.path.join(REPOPATH, "collect_variants.py")
    command = [
        _python,
        command_path,
        "-h5dir",
        h5_directory,
        "-barcode-depth-file",
        barcode_depth_csv,
        "-outdir",
        intermediate_output_directory,
        "-min-consensus-group-size",
        f"{filter_dict['min_consensus_group_size']}",
    ]

    if umi_mode == UMI_Mode.UMI:
        command.append("-umi-mode")
        command.append(UMI_Mode.UMI)
    else:
        command.append("-umi-mode")
        command.append(UMI_Mode.eUMI)

    print(f"Executing: {' '.join(command)}")

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(e.stderr)
        raise Exception("Collecting Variants failed") from e

    command_path = os.path.join(REPOPATH, "filter_variants.py")
    command = [
        _python,
        command_path,
        "-variant-statistics",
        os.path.join(f"{intermediate_output_directory}", "all_variants_statistics.csv"),
        "-variant-heteroplasmy-matrix",
        os.path.join(
            f"{intermediate_output_directory}", "all_variants_heteroplasmy_matrix.csv"
        ),
        "-variant-coverage-matrix",
        os.path.join(f"{intermediate_output_directory}", "all_variants_coverage.csv"),
        "-min-strand-correlation",
        f"{filter_dict['min_strand_correlation']}",
        "-min-vmr",
        f"{filter_dict['min_vmr']}",
        "-molecular-position-bias-threshold",
        f"{filter_dict['molecular_position_bias_threshold']}",
        "-homoplasmic-threshold",
        f"{filter_dict['homoplasmic_threshold']}",
        "-mean-coverage",
        f"{filter_dict['mean_coverage']}",
        "-n-cells-over-5",
        f"{filter_dict['n_cells_over_5']}",
        "-outdir",
        final_output_directory,
    ]

    print(f"Executing: {' '.join(command)}")

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(e.stderr)
        raise Exception("Filtering Variants failed") from e

    # Clean Up
    # copy barcode depth to final
    shutil.copy(barcode_depth_csv, final_output_directory)

    # delete tmp files based on flag
    if not state["keep_temp_files"]:
        shutil.rmtree(intermediate_output_directory)


if __name__ == "__main__":
    app()
