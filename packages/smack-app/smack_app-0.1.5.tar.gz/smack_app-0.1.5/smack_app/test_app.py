from typer.testing import CliRunner
import os
import pytest
import shutil
import sys
from unittest.mock import patch, MagicMock
from smack_app.app import app

from smack_app.utils.utils import REPOPATH

WELCOME_TEXT_SUBSET = "Hi! Welcome to the SMACK tool"
TEST_BAM = "test_fixtures/sample_bam.bam"
TEST_BC = "test_fixtures/sample_bc.txt"
TEST_UMI_BC = "test_fixtures/UMI_barcodes.txt"
TEST_UMI_BAM = "test_fixtures/UMI.bam"
TEST_h5_DIR = "test_fixtures/sample_h5_dir"
TEST_WD = "test_fixtures/sample_working_dir"
CUSTOM_GENOME_chrM = "test_fixtures/custom_genome_chrM.fasta"
CUSTOM_GENOME_MT = "test_fixtures/custom_genome_MT.fasta"
FULL_TEST_BAM = "test_fixtures/full_size_bam.bam"
FULL_TEST_BC = "test_fixtures/full_size_barcodes.txt"


def clear_folder(folder_path, delete_top=True):
    if not os.path.exists(folder_path):
        return

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)

    if delete_top:
        os.rmdir(folder_path)


@pytest.fixture()
def test_wd():
    yield TEST_WD
    clear_folder(TEST_WD)
    clear_folder("./smack_working_directory")


@pytest.fixture()
def test_h5_dir():
    yield TEST_h5_DIR
    clear_folder(TEST_h5_DIR, delete_top=False)


@pytest.fixture()
def app_runner():
    with patch("smack_app.cli_validation.available_cpu_count") as mock_cpu_count:
        mock_cpu_count.return_value = 4
        runner = CliRunner()
        yield runner


def test_empty_entry(app_runner):
    result = app_runner.invoke(app)
    assert WELCOME_TEXT_SUBSET in result.stdout
    assert result.exit_code == 0


def test_get_supported_genomes(app_runner, test_wd):
    result = app_runner.invoke(app, ["-wd", test_wd, "get-supported-genomes"])
    assert "Supported Genomes" in result.stdout
    assert result.exit_code == 0


def test_default_working_directory(app_runner):
    result = app_runner.invoke(app, ["--verbose", "get-supported-genomes"])
    assert "smack_working_directory" in result.stdout


def test_custom_working_directory(app_runner, test_wd):
    result = app_runner.invoke(
        app, ["-wd", test_wd, "--verbose", "get-supported-genomes"]
    )
    assert "smack_working_directory" not in result.stdout
    assert test_wd in result.stdout


def test_genotype_missing_BAM(app_runner, test_wd):
    result = app_runner.invoke(app, ["-wd", test_wd, "genotype"])
    assert "Missing argument 'INPUT_BAM'" in result.stdout
    assert result.exit_code != 0


def test_genotype_bad_BAM(app_runner, test_wd):
    result = app_runner.invoke(app, ["-wd", test_wd, "genotype", "dummy/path"])
    assert "Invalid value for 'INPUT_BAM': dummy/path does not exist " in result.stdout
    assert result.exit_code != 0


def test_genotype_missing_h5dir(app_runner, test_wd):
    result = app_runner.invoke(app, ["-wd", test_wd, "genotype", TEST_BAM])
    assert "Missing argument 'H5_DIRECTORY'" in result.stdout
    assert result.exit_code != 0


def test_genotype_missing_bc(app_runner, test_wd, test_h5_dir):
    result = app_runner.invoke(
        app,
        ["-wd", test_wd, "genotype", TEST_BAM, test_h5_dir],
    )
    assert "Invalid value for '--barcodes-file'" in result.stdout
    assert result.exit_code != 0


def test_genotype_illegal_umi_mode(app_runner, test_wd, test_h5_dir):
    result = app_runner.invoke(
        app,
        [
            "-wd",
            test_wd,
            "genotype",
            TEST_BAM,
            test_h5_dir,
            "-bf",
            TEST_BC,
            "-um",
            "eUMI",
            "-ub",
            "UB",
        ],
    )
    assert (
        "Cannot use umi-barcode tag in umi-mode 'eUMI'. Either set umi-mode to UMI or omit umi-barcode"
        in result.stdout
    )
    assert result.exit_code != 0


def test_dry_run_verbose(app_runner, test_wd, test_h5_dir):
    result = app_runner.invoke(
        app,
        [
            "-wd",
            test_wd,
            "--dry-run",
            "--verbose",
            "genotype",
            TEST_BAM,
            test_h5_dir,
            "-bf",
            TEST_BC,
        ],
    )
    assert "Verbose is set to True. Will write verbose output" in result.stdout

    result = app_runner.invoke(
        app,
        [
            "-wd",
            test_wd,
            "--dry-run",
            "genotype",
            TEST_BAM,
            test_h5_dir,
            "-bf",
            TEST_BC,
        ],
    )
    assert "Verbose is set to True. Will write verbose output" not in result.stdout


def test_dry_run_default_genome(app_runner, test_wd, test_h5_dir):
    result = app_runner.invoke(
        app,
        [
            "-wd",
            test_wd,
            "--dry-run",
            "--verbose",
            "genotype",
            TEST_BAM,
            test_h5_dir,
            "-bf",
            TEST_BC,
        ],
    )
    assert "Using built-in genome from path" in result.stdout
    assert "reference/rCRS.txt" in result.stdout


def test_dry_run_built_in_genome(app_runner, test_wd, test_h5_dir):
    result = app_runner.invoke(
        app,
        [
            "-wd",
            test_wd,
            "--dry-run",
            "--verbose",
            "genotype",
            TEST_BAM,
            test_h5_dir,
            "-bf",
            TEST_BC,
            "-g",
            "hg19",
        ],
    )
    assert "Using built-in genome from path" in result.stdout
    assert "reference/rCRS.txt" not in result.stdout
    assert "reference/hg19.txt" in result.stdout


def test_dry_run_custom_genome_no_path(app_runner, test_wd, test_h5_dir):
    result = app_runner.invoke(
        app,
        [
            "-wd",
            test_wd,
            "--dry-run",
            "--verbose",
            "genotype",
            TEST_BAM,
            test_h5_dir,
            "-bf",
            TEST_BC,
            "-g",
            "CUSTOM",
        ],
    )
    assert (
        "mito-genome set to CUSTOM but no genome was supplied. Either use built-in genome or use CUSTOM together with --custom-genome-path <path>"
        in result.stdout
    )
    assert result.exit_code != 0


def test_dry_run_custom_genome_bad_path(app_runner, test_wd, test_h5_dir):
    result = app_runner.invoke(
        app,
        [
            "-wd",
            test_wd,
            "--dry-run",
            "--verbose",
            "genotype",
            TEST_BAM,
            test_h5_dir,
            "-bf",
            TEST_BC,
            "-g",
            "CUSTOM",
            "--custom-genome-path",
            "bad/path",
        ],
    )
    assert "bad/path does not exist" in result.stdout

    assert result.exit_code != 0

    result = app_runner.invoke(
        app,
        [
            "-wd",
            test_wd,
            "--dry-run",
            "--verbose",
            "genotype",
            TEST_BAM,
            test_h5_dir,
            "-bf",
            TEST_BC,
            "-g",
            "CUSTOM",
            "--custom-genome-path",
            TEST_BC,
        ],
    )
    assert f"{TEST_BC} must have the .fasta extension" in result.stdout

    assert result.exit_code != 0


def test_dry_run_custom_genome_wrong_contig(app_runner, test_wd, test_h5_dir):
    result = app_runner.invoke(
        app,
        [
            "-wd",
            test_wd,
            "--dry-run",
            "--verbose",
            "genotype",
            TEST_BAM,
            test_h5_dir,
            "-bf",
            TEST_BC,
            "-g",
            "CUSTOM",
            "--custom-genome-path",
            CUSTOM_GENOME_MT,
        ],
    )
    assert "ValueError" in str(result.exc_info)
    assert "invalid contig" in str(result.exc_info)

    assert result.exit_code != 0
    if os.path.exists("reference/CUSTOM.txt"):
        os.remove("reference/CUSTOM.txt")


def test_dry_run_custom_genome(app_runner, test_wd, test_h5_dir):
    result = app_runner.invoke(
        app,
        [
            "-wd",
            test_wd,
            "--dry-run",
            "--verbose",
            "genotype",
            TEST_BAM,
            test_h5_dir,
            "-bf",
            TEST_BC,
            "-g",
            "CUSTOM",
            "--custom-genome-path",
            CUSTOM_GENOME_chrM,
        ],
    )
    assert f"Using mito reference genome with length 540" in result.stdout

    assert result.exit_code == 0


def test_dry_run_set_cores(app_runner, test_wd, test_h5_dir):
    result = app_runner.invoke(
        app,
        [
            "-wd",
            test_wd,
            "--dry-run",
            "--verbose",
            "genotype",
            TEST_BAM,
            test_h5_dir,
            "-bf",
            TEST_BC,
            "-c",
            "8",
        ],
    )
    assert "Attempting to run with 8 cores..." in result.stdout


def test_dry_run_infer_cores(app_runner, test_wd, test_h5_dir):

    result = app_runner.invoke(
        app,
        [
            "-wd",
            test_wd,
            "--dry-run",
            "--verbose",
            "genotype",
            TEST_BAM,
            test_h5_dir,
            "-bf",
            TEST_BC,
        ],
    )
    assert "Attempting to run with 4 cores..." in result.stdout


def test_dry_run_full(app_runner, test_wd, test_h5_dir):
    result = app_runner.invoke(
        app,
        [
            "-wd",
            test_wd,
            "--dry-run",
            "--verbose",
            "genotype",
            TEST_BAM,
            test_h5_dir,
            "-bf",
            TEST_BC,
            "-c",
            "2",
        ],
    )
    assert "Split Succeeded" in result.stdout
    assert "Dry Run Completed Successfully" in result.stdout


def test_genotyper_mocked(app_runner, test_wd, test_h5_dir):

    with patch("multiprocessing.pool.Pool") as mock_pool_class:
        mock_pool_instance = mock_pool_instance = MagicMock()
        mock_pool_class.return_value.__enter__.return_value = mock_pool_instance
        mock_pool_instance.starmap.return_value = [3, 7]

        result = app_runner.invoke(
            app,
            [
                "-wd",
                test_wd,
                "--verbose",
                "genotype",
                TEST_BAM,
                test_h5_dir,
                "-bf",
                TEST_BC,
                "-c",
                "1",
            ],
        )
        assert "Split Succeeded" in result.stdout
        assert "Ready to process 1 samples with paths:" in result.stdout
        assert (
            f"('{TEST_BC}', '{test_wd}/barcoded_bams/sample_bc.bam')" in result.stdout
        )
        assert "Genotyping Completed Successfully" in result.stdout


def test_genotyper_full_run(app_runner, test_wd, test_h5_dir):

    result = app_runner.invoke(
        app,
        [
            "-wd",
            test_wd,
            "--verbose",
            "genotype",
            TEST_BAM,
            test_h5_dir,
            "-bf",
            TEST_BC,
            "-c",
            "4",
        ],
    )
    assert "Split Succeeded" in result.stdout
    assert "Ready to process 4 samples with paths:" in result.stdout
    assert "Genotyping Completed Successfully" in result.stdout

    for i in range(1, 5):
        assert f"{test_wd}/barcode_files/barcodes.{i}.txt" in result.stdout
        assert f"{test_wd}/barcoded_bams/barcodes.{i}.bam" in result.stdout
        assert os.path.exists(os.path.join(test_h5_dir, f"barcodes.{i}.h5"))


def test_genotyper_UMI_full_run(app_runner, test_wd, test_h5_dir):

    result = app_runner.invoke(
        app,
        [
            "-wd",
            test_wd,
            "--verbose",
            "genotype",
            TEST_UMI_BAM,
            test_h5_dir,
            "-bf",
            TEST_UMI_BC,
            "--genome",
            "hg38",
            "--barcode-tag",
            "CR",
            "--umi-mode",
            "UMI",
            "-ub",
            "UR",
            "-c",
            "4",
        ],
    )
    assert "Split Succeeded" in result.stdout
    assert "Genotyping Completed Successfully" in result.stdout

    assert f"{test_wd}/barcode_files/barcodes.1.txt" in result.stdout
    assert f"{test_wd}/barcoded_bams/barcodes.1.bam" in result.stdout
    assert os.path.exists(os.path.join(test_h5_dir, "barcodes.1.h5"))


def test_genotyper_full_run_quality_based(app_runner, test_wd, test_h5_dir):

    result = app_runner.invoke(
        app,
        [
            "-wd",
            test_wd,
            "--verbose",
            "genotype",
            TEST_BAM,
            test_h5_dir,
            "-bf",
            TEST_BC,
            "-c",
            "4",
            "-s",
            "MEAN_QUALITY",
        ],
    )
    assert "Split Succeeded" in result.stdout
    assert "Ready to process 4 samples with paths:" in result.stdout
    assert "Genotyping Completed Successfully" in result.stdout

    for i in range(1, 5):
        assert f"{test_wd}/barcode_files/barcodes.{i}.txt" in result.stdout
        assert f"{test_wd}/barcoded_bams/barcodes.{i}.bam" in result.stdout
        assert os.path.exists(os.path.join(test_h5_dir, f"barcodes.{i}.h5"))


def test_genotyper_UMI_full_run_quality_based(app_runner, test_wd, test_h5_dir):

    result = app_runner.invoke(
        app,
        [
            "-wd",
            test_wd,
            "--verbose",
            "genotype",
            TEST_UMI_BAM,
            test_h5_dir,
            "-bf",
            TEST_UMI_BC,
            "--genome",
            "hg38",
            "--barcode-tag",
            "CR",
            "--umi-mode",
            "UMI",
            "-ub",
            "UR",
            "-c",
            "4",
            "-s",
            "MEAN_QUALITY",
        ],
    )

    assert "Genotyping Completed Successfully" in result.stdout

    assert f"{test_wd}/barcode_files/barcodes.1.txt" in result.stdout
    assert f"{test_wd}/barcoded_bams/barcodes.1.bam" in result.stdout
    assert os.path.exists(os.path.join(test_h5_dir, f"barcodes.1.h5"))


def test_get_supported_filters(app_runner, test_wd):
    result = app_runner.invoke(app, ["-wd", test_wd, "get-supported-filter-sets"])
    assert "Filter Sets" in result.stdout
    assert "SMART_SEQ" in result.stdout
    assert result.exit_code == 0


def test_filter_variants_missing_h5dir(app_runner, test_wd):
    result = app_runner.invoke(app, ["-wd", test_wd, "filter-variants"])
    assert "Missing argument 'H5_DIRECTORY'" in result.stdout
    assert result.exit_code != 0


def test_filter_variants_missing_filter_set(app_runner, test_wd, test_h5_dir):
    result = app_runner.invoke(
        app,
        ["-wd", test_wd, "--verbose", "--dry-run", "filter-variants", test_h5_dir],
    )
    assert "Missing argument 'FILTER_SET" in result.stdout
    assert result.exit_code != 0


def test_filter_variants_bad_filter_set(app_runner, test_wd, test_h5_dir):
    result = app_runner.invoke(
        app,
        [
            "-wd",
            test_wd,
            "--verbose",
            "--dry-run",
            "filter-variants",
            test_h5_dir,
            "BAD_NAME",
        ],
    )
    assert "Invalid value for 'FILTER_SET" in result.stdout
    assert result.exit_code != 0


def test_filter_variants_smart_seq_filter_set(app_runner, test_wd, test_h5_dir):
    result = app_runner.invoke(
        app,
        [
            "-wd",
            test_wd,
            "--verbose",
            "--dry-run",
            "filter-variants",
            test_h5_dir,
            "SMART_SEQ",
        ],
    )
    assert "Using filter set: SMART_SEQ" in result.stdout
    assert result.exit_code == 0


def test_filter_variants_mtscatac_filter_set_plus_custom(
    app_runner, test_wd, test_h5_dir
):
    result = app_runner.invoke(
        app,
        [
            "-wd",
            test_wd,
            "--verbose",
            "--dry-run",
            "filter-variants",
            test_h5_dir,
            "mtscATAC",
            "--min-strand-correlation=0.50",
        ],
    )
    assert "Using filter set: mtscATAC" in result.stdout
    assert "Overriding default value for min_strand_correlation with 0.50"
    assert result.exit_code == 0
    result = app_runner.invoke(
        app,
        [
            "-wd",
            test_wd,
            "--verbose",
            "--dry-run",
            "filter-variants",
            test_h5_dir,
            "mtscATAC",
            "--min_strand_correlation=0.50",
        ],
    )
    assert "Using filter set: mtscATAC" in result.stdout
    assert "Overriding default value for min_strand_correlation with 0.50"
    assert result.exit_code == 0


def test_filter_variants_smart_seq_filter_set_bad_extra_param1(
    app_runner, test_wd, test_h5_dir
):
    result = app_runner.invoke(
        app,
        [
            "-wd",
            test_wd,
            "--verbose",
            "--dry-run",
            "filter-variants",
            test_h5_dir,
            "SMART_SEQ",
            "something",
        ],
    )
    assert "Using filter set: SMART_SEQ" in result.stdout
    assert (
        "Could not understand filter argument something. To add filters, you must use the notation --<key>=<value>"
        in result.stdout
    )
    assert result.exit_code != 0


def test_filter_variants_smart_seq_filter_set_bad_extra_param2(
    app_runner, test_wd, test_h5_dir
):
    result = app_runner.invoke(
        app,
        [
            "-wd",
            test_wd,
            "--verbose",
            "--dry-run",
            "filter-variants",
            test_h5_dir,
            "SMART_SEQ",
            "--some_filter=5",
        ],
    )
    assert "Using filter set: SMART_SEQ" in result.stdout
    assert (
        "Unknown Filter Argument some_filter. Run get-supported-filter-sets to see the available filters."
        in result.stdout
    )
    assert result.exit_code != 0
    result = app_runner.invoke(
        app,
        [
            "-wd",
            test_wd,
            "--verbose",
            "--dry-run",
            "filter-variants",
            test_h5_dir,
            "SMART_SEQ",
            "--some-filter=5",
        ],
    )
    assert "Using filter set: SMART_SEQ" in result.stdout
    assert (
        "Unknown Filter Argument some_filter. Run get-supported-filter-sets to see the available filters."
        in result.stdout
    )
    assert result.exit_code != 0


def test_filter_variants_single_h5dir_dry_run(app_runner, test_wd, test_h5_dir):
    result = app_runner.invoke(
        app, ["-wd", test_wd, "--dry-run", "filter-variants", test_h5_dir, "mtscATAC"]
    )
    assert f"Found the following h5 directories: ['{test_h5_dir}']" in result.stdout
    assert result.exit_code == 0


def test_filter_variants_multi_h5dir_dry_run(app_runner, test_wd, test_h5_dir):
    multi_dir = f"{test_h5_dir},{test_h5_dir},{test_h5_dir}"
    result = app_runner.invoke(
        app, ["-wd", test_wd, "--dry-run", "filter-variants", multi_dir, "mtscATAC"]
    )
    assert (
        f"Found the following h5 directories: ['{test_h5_dir}', '{test_h5_dir}', '{test_h5_dir}']"
        in result.stdout
    )
    assert result.exit_code == 0


def test_filter_variants_single_h5dir(app_runner, test_wd, test_h5_dir):
    with patch("subprocess.run") as mock_run:
        result = app_runner.invoke(
            app, ["-wd", test_wd, "filter-variants", test_h5_dir, "mtscATAC"]
        )
        assert mock_run.call_count == 3

        command_path = f"{REPOPATH}/filter_variants.py"
        command = [
            sys.executable,
            command_path,
            "-variant-statistics",
            os.path.join(
                "test_fixtures/sample_working_dir/temp", "all_variants_statistics.csv"
            ),
            "-variant-heteroplasmy-matrix",
            os.path.join(
                "test_fixtures/sample_working_dir/temp",
                "all_variants_heteroplasmy_matrix.csv",
            ),
            "-variant-coverage-matrix",
            os.path.join(
                "test_fixtures/sample_working_dir/temp",
                "all_variants_coverage.csv",
            ),
            "-min-strand-correlation",
            "0.65",
            "-min-vmr",
            "0.01",
            "-molecular-position-bias-threshold",
            "0.35",
            "-homoplasmic-threshold",
            "0.95",
            "-mean-coverage",
            "10",
            "-n-cells-over-5",
            "3",
            "-outdir",
            "test_fixtures/sample_working_dir/final/",
        ]
        mock_run.assert_called_with(command, check=True)


def test_filter_variants_single_h5dir_override(app_runner, test_wd, test_h5_dir):
    with patch("subprocess.run") as mock_run:
        result = app_runner.invoke(
            app,
            [
                "-wd",
                test_wd,
                "filter-variants",
                test_h5_dir,
                "mtscATAC",
                "--min_strand_correlation=0.50",
                "--min-vmr=0.03",
            ],
        )
        assert mock_run.call_count == 3

        command_path = f"{REPOPATH}/filter_variants.py"
        command = [
            sys.executable,
            command_path,
            "-variant-statistics",
            os.path.join(
                "test_fixtures/sample_working_dir/temp", "all_variants_statistics.csv"
            ),
            "-variant-heteroplasmy-matrix",
            os.path.join(
                "test_fixtures/sample_working_dir/temp",
                "all_variants_heteroplasmy_matrix.csv",
            ),
            "-variant-coverage-matrix",
            os.path.join(
                "test_fixtures/sample_working_dir/temp",
                "all_variants_coverage.csv",
            ),
            "-min-strand-correlation",
            "0.50",
            "-min-vmr",
            "0.03",
            "-molecular-position-bias-threshold",
            "0.35",
            "-homoplasmic-threshold",
            "0.95",
            "-mean-coverage",
            "10",
            "-n-cells-over-5",
            "3",
            "-outdir",
            "test_fixtures/sample_working_dir/final/",
        ]
        mock_run.assert_called_with(command, check=True)


def test_full_app_run_with_mock_data(app_runner, test_wd, test_h5_dir):
    result = app_runner.invoke(
        app,
        [
            "--keep-temp-files",
            "-wd",
            test_wd,
            "--verbose",
            "genotype",
            FULL_TEST_BAM,
            test_h5_dir,
            "-bf",
            FULL_TEST_BC,
            "-g",
            "hg38",
            "--barcode-tag",
            "RG",
        ],
    )
    assert "Split Succeeded" in result.stdout
    assert "Genotyping Completed Successfully" in result.stdout

    result = app_runner.invoke(
        app,
        [
            "--keep-temp-files",
            "-wd",
            test_wd,
            "filter-variants",
            test_h5_dir,
            "mtscATAC",
            "--min_strand_correlation=0.50",
            "--min-vmr=0.03",
            "--mean_coverage=1",
        ],
    )
    for temp_path in [
        "barcode_depth",
        "all_variants_coverage",
        "all_variants_fwd_counts_matrix",
        "all_variants_rev_counts_matrix",
        "all_variants_heteroplasmy_matrix",
        "all_variants_statistics",
        "alt_position_matrix",
        "ref_position_matrix",
        "variant_counts",
    ]:
        assert os.path.exists(os.path.join(test_wd, f"temp/{temp_path}.csv"))
    for final_path in [
        "final_variants_heteroplasmy_matrix",
        "final_variants_statistics",
        "final_variants_coverage_matrix",
        "barcode_depth",
        "all_variants_heteroplasmy_matrix",
        "all_variants_coverage_matrix",
        "all_variants_statistics",
    ]:
        assert os.path.exists(os.path.join(test_wd, f"final/{final_path}.csv"))


def test_full_app_run_with_mock_data_no_temp_files(app_runner, test_wd, test_h5_dir):
    result = app_runner.invoke(
        app,
        [
            "-wd",
            test_wd,
            "--verbose",
            "genotype",
            FULL_TEST_BAM,
            test_h5_dir,
            "-bf",
            FULL_TEST_BC,
            "-g",
            "hg38",
            "--barcode-tag",
            "RG",
        ],
    )
    assert "Split Succeeded" in result.stdout
    assert "Genotyping Completed Successfully" in result.stdout

    result = app_runner.invoke(
        app,
        [
            "-wd",
            test_wd,
            "filter-variants",
            test_h5_dir,
            "mtscATAC",
            "--min_strand_correlation=0.50",
            "--min-vmr=0.03",
            "--mean_coverage=1",
        ],
    )
    assert not os.path.exists(os.path.join(test_wd, "temp"))
    for final_path in [
        "final_variants_heteroplasmy_matrix",
        "final_variants_statistics",
        "final_variants_coverage_matrix",
        "barcode_depth",
        "all_variants_heteroplasmy_matrix",
        "all_variants_coverage_matrix",
        "all_variants_statistics",
    ]:
        assert os.path.exists(os.path.join(test_wd, f"final/{final_path}.csv"))
