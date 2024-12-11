import typer
import os


def parse_fasta(filename: str) -> dict[str, str]:
    """
    Imports specified .fasta file
    """
    f = open(filename)
    sequences = {}
    for line in f:
        if line.startswith(">"):
            name = line[1:].strip()
            sequences[name] = ""
        else:
            sequences[name] = sequences[name] + line.strip()
    f.close()
    return sequences


def create_refAllele_file(fasta_path: str, outpath: str) -> tuple[str, str, int]:

    fasta = parse_fasta(fasta_path)
    if len(fasta.keys()) != 1:
        raise typer.BadParameter(
            f"ERROR: {fasta_path} file has multiple chromosomes; supply file with only 1"
        )
    mito_genome, mito_seq = list(fasta.items())[0]
    mito_length = len(mito_seq)

    if os.path.exists(outpath):
        print(
            f"File Already found at {outpath}. Using file that is there already and skipping creation step..."
        )
    else:
        with open(outpath, "w") as f:
            b = 1
            for base in mito_seq:
                f.write(str(b) + "\t" + base + "\n")
                b += 1

    return (outpath, mito_genome, mito_length)
