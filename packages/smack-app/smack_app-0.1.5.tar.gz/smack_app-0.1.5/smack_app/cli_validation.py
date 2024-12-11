from enum import Enum
import importlib.metadata
import os
import typer
from typing import Optional, Union

from smack_app.utils.utils import available_cpu_count, REPOPATH

__version__ = importlib.metadata.version("smack-app")


class Genome(str, Enum):
    GRCh37 = "GRCh37"
    GRCh38 = "GRCh38"
    GRCm38 = "GRCm38"
    GRCz10 = "GRCz10"
    hg19_chrM = "hg19_chrM"
    hg19 = "hg19"
    hg38 = "hg38"
    mm10 = "mm10"
    mm9 = "mm9"
    NC_012920 = "NC_012920"
    rCRS = "rCRS"
    CUSTOM = "CUSTOM"


def assert_positive(num: Union[int, float]):
    if num <= 0:
        raise typer.BadParameter(f"{num} must be a positive number")
    return num


def assert_not_negative(num: Union[int, float]):
    if num < 0:
        raise typer.BadParameter(f"{num} cannot be negative")
    return num


def assert_path_exists(path: str):
    try:
        if not os.path.exists(path):
            raise typer.BadParameter(f"{path} does not exist")
    except Exception as e:
        raise typer.BadParameter(f"{path} does not exist") from e
    return path


def assert_list_of_paths_exist(pathList: str):
    paths = pathList.split(",")
    for path in paths:
        if not os.path.exists(path):
            raise typer.BadParameter(f"{path} does not exist")
    return pathList


def assert_is_none_or_path_exists(path: Optional[str]):
    return assert_path_exists(path) if path is not None else path


def name_transform(name: str):
    return name.upper()


def validate_custom_genome_path(fasta_path: str):
    assert_path_exists(fasta_path)
    if not fasta_path.endswith(".fasta"):
        raise typer.BadParameter(f"{fasta_path} must have the .fasta extension")


def get_support_genome_fasta_path(genome: Genome):
    return os.path.join(REPOPATH, f"reference/fasta_files/{genome}.fasta")


def ncores_selection(ncores_option: str) -> int:
    if ncores_option == "detect":
        try:
            num_cores = int(available_cpu_count())
        except Exception as e:
            raise typer.BadParameter(
                "Unable to detect number of cores with 'detect', please set ncores to an integer"
            ) from e
    else:
        try:
            num_cores = int(ncores_option)
        except ValueError as e:
            raise typer.BadParameter(
                f"{num_cores} must be an integer or 'detect'"
            ) from e
    return assert_positive(num_cores)


def version_callback(value: bool):
    if value:
        print(f"SMACK app Version: {__version__}")

        raise typer.Exit()
