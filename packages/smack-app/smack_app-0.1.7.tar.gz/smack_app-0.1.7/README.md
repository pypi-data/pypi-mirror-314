# SMACK (Single-cell Mitochondrial Analysis CLI Kit)
Welcome! See https://github.com/jonlevi/smack for more

## Installation
### Pipx (Strongly Recommended)
If you don't have pipx:
```
pip install --user pipx
pipx ensurepath
```
```
pipx install smack-app
```
### Pip User-Level (Not As Recommended)
```
pip install --user smack-app
```

The --user is important, that ensures you install it in your user's directory and not in the global system. Techincally, you can install smack at the env level, but there may be conflicts between SMACKs python dependencies and your env's dependencies. If you installed it in the global system (e.g. with sudo) you could install a version of a library (e.g. a sub-dependency) that is incompatible with your system.


## Auto-Completion
If you want bash auto-completion for smack commands
```
smack --install-completion
```
and then restart the terminal.

## How to Use

### Typer
SMACK is built on top of the python Typer library, https://typer.tiangolo.com/ (MIT License) and is a CLI app with "commands", "options", and "args":

**Usage**:
Smack is run like this:
```console
$ smack [CLI-OPTIONS] COMMAND [COMMAND-ARGS]...
```

### Example
**Quick Start Example for MTSCATAC Data**:

Specify a working directory and output directory:
```console
$  wd="path/to/directory"
$  hdir="${wd}/h5_files"
```
Locate BAM file and barcodes file:
```console
$  BAM="path/to/file.bam"
$  BC="path/to/cells.txt"
```
Run Genotyping
(Note: You may need to change the reference genome and barcode tag based on your data set. You also may want to run this as a bsub/sbatch job or or with the screen command so you can come back to it after it finishes, as it may take a few hours):
```console
$  smack --working-directory $wd genotype $BAM $hdir --barcodes-file $BC --genome hg38 --barcode-tag CB
```

After genotyping is finished, filter for your variants:
```console
$  smack --working-directory $wd filter-variants $hdir mtscATAC
```
Your working directory should have all of the output files you need for downstream analyses


### More Detailed Documentation

**CLI Level Options**:
* `--version`: Prints app version
* `--help`: Show this message and exit.
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `-v, --verbose, --debug / -nv, --no-verbose`: Provides detailed logging about all processess  [default: no-verbose]
* `--keep-temp-files / --no-keep-temp-files`: Keep temp files used throughout the process. If False, only final outputs will be kept and other files will be deleted.  [default: no-keep-temp-files]
* `--dry-run / --no-dry-run`: Verify input data and arguments without executing downstream commands  [default: no-dry-run]
* `-wd, --working-directory TEXT`: Set working directory for temp and final output files  [default: smack_working_directory]


**Commands**:

* `genotype`: Go from a single BAM --&gt; Directory of H5...
* `get-supported-genomes`: Prints which genomes have built-in support
* `get-supported-filter-sets`: Prints the preset filter sets for...
* `filter-variants`: Collect All Possible Variants from the...

## `smack genotype`

Go from a single BAM --&gt; Directory of H5 Files With Variant Calls

**Usage**:

```console
$ smack genotype [OPTIONS] INPUT_BAM H5_DIRECTORY
```

**Arguments**:

* `INPUT_BAM`: Path to input BAM file  [required]
* `H5_DIRECTORY`: Directory to store output H5 files  [required]

**Options**:

* `-bf, --barcodes-file TEXT`: Path to input barcodes file
* `-id, --sample-id TEXT`: Sample ID for metadata. Defaults to path of input BAM
* `-g, --genome [GRCh37|GRCh38|GRCm38|GRCz10|hg19_chrM|hg19|hg38|mm10|mm9|NC_012920|rCRS|CUSTOM]`: Name of genome or &#x27;CUSTOM&#x27;, along with --custom-genome-path &lt;path&gt;. Run get-supported-genomes to see list of built-in genomes.  [default: rCRS]
* `--custom-genome-path TEXT`: Path to valid genome FASTA
* `-bc, --barcode-tag TEXT`: Tag for cell barcodes in BAM file (usually &#x27;BC&#x27; or &#x27;CB&#x27;)  [default: BC]
* `-um, --umi-mode [eUMI|UMI]`: Group molecules based on eUMI (endogenous) or UMI (literal)  [default: eUMI]
* `-ub, --umi-barcode-tag TEXT`: Tag for UMI barcode in BAM file. Ignored if umi-mode=&#x27;eUMI&#x27;
* `-s, --consensus-call-strategy [CONSENSUS|MEAN_QUALITY]`: Strategy for collapsing groups of molecules based on eUMI (endogenous) or UMI (literal)  [default: CONSENSUS]
* `-c, --ncores TEXT`: Number of cores to use. Either integer or &#x27;detect&#x27; for auto-detecting based on system hardware.  [default: detect]
* `-bq, --base-quality INTEGER`: Minimum per base quality score at position X to be considered a valid read at X  [default: 10]
* `-mapq, --map-quality INTEGER`: Minimum map quality for a read pair to be considered valid  [default: 30]
* `-es, --max-eUMI-size INTEGER`: Maximum eUMI size. eUMIs that are too large are likely artifacts from misalignments  [default: 1000]
* `-et, --eUMI-trim INTEGER`: Number of bp to trim off each side of eUMI for position edge bias  [default: 0]
* `--help`: Show this message and exit.

## `smack get-supported-genomes`

Prints which genomes have built-in support

**Usage**:

```console
$ smack get-supported-genomes
```


## `smack get-supported-filter-sets`

Prints the preset filter sets for variants, and which technology it is recommended for

**Usage**:

```console
$ smack get-supported-filter-sets
```


## `smack filter-variants`

Collect All Possible Variants from the split H5 files. Filter variants based on parameters.
H5 directory --&gt; Heteroplasmy, Variants, and Coverage CSVs

**Usage**:

```console
$ smack filter-variants [OPTIONS] H5_DIRECTORY FILTER_SET:{mtscATAC|REDEEM|MAESTER|DLP|SMART_SEQ|CUSTOM}
```

**Arguments**:

* `H5_DIRECTORY`: String path to h5 directory or comma-separated string list of h5 directories. Should usually be the same path(s) output by `genotype` command.  [required]
* `FILTER_SET:{mtscATAC|REDEEM|MAESTER|DLP|SMART_SEQ|CUSTOM}`: Name of filter set to use (or &#x27;CUSTOM&#x27;, along with all parameters set as kwargs). Run get-supported-filter-sets to see list of built-in filter sets.  [required]

**Options**:

* `-um, --umi-mode [eUMI|UMI]`: Group molecules based on `eUMI` (endogenous) or `UMI` (literal)  [default: eUMI]
* `--min-barcode-depth FLOAT`: Minimum depth for a cell/barcode to be kept  [default: 10]
* `--<filter-name> value`: Specify any filter from the filter list manually. 
Filter list includes:
    - "mean-coverage"
    - "min-strand-correlation",
    - "n-cells-over-5",
    - "min-vmr",
    - "min-consensus-group-size",
    - "molecular-position-bias-threshold"
    - "homoplasmic-threshold"

### Note about barcode depth
Before calculating variant statistics, smack filters out barcodes with depth < the value specified at --min-barcode-depth (default=10). To keep all barcodes you can set this value to 0, but then variant statistics will be calculated over all cells, even those that we recommend being discarded.

## For Developers: Pytest Tests
`poetry shell`
`python -m pytest test_app.py -s`
Note: Since printed statements are a key part of the CLI app, the tests rely on stdout and thus will faily if you don't include the "-s" command. You should also run the tests in a poetry venv, by running poetry shell or poetry run. 
Note: These tests are not traditional "unit" tests as not all functionality is mocked out, but are also not "integration" tests. They are not run as part of any CI or pre-commit. They are just to make sure that the app does what it is supposed to do, and should be run manually as part of a check for any new releases of the package. While there are no database or web calls (like in integration tests), there are calls to subprocess/multiprocessing threads that do actual processing and return actual return codes. As a result, some of the tests can take up to 5 minutes to run, but are more representative of real runtime conditions.

   