import argparse
import glob
import os
import tables
import pandas as pd
from tqdm import tqdm
from typing import Optional


def get_h5_to_sample_id_map(h5_files: list[str]) -> dict[str, str]:
    sample_id_map = {}
    for f in h5_files:
        with tables.open_file(f, driver="H5FD_CORE") as h5file:
            metadata = h5file.get_node("/metadata", "metadata")
            for row in metadata.iterrows():
                sample_id = row["sample_id"].decode()
                sample_id_map[f] = sample_id
    return sample_id_map


def get_barcode_depth(
    h5_files: list[str], sample_id_map: Optional[dict[str, str]]
) -> pd.DataFrame:
    print("Getting barcodes from h5 files")
    barcode_depth = {}

    for f in tqdm(h5_files):
        with tables.open_file(f, driver="H5FD_CORE") as h5file:
            bcs = h5file.get_node("/barcodes", "barcodes")
            for row in bcs.iterrows():
                _bc = row["barcode"].decode()
                if sample_id_map:
                    _bc = sample_id_map[f] + "_" + _bc

                barcode_depth[_bc] = {
                    "average_total_depth": row["average_total_depth"],
                    "average_high_quality_depth": row["average_high_quality_depth"],
                }
    df = pd.DataFrame(barcode_depth).T
    df.index.name = "barcode"
    return df


def main(args):

    subdirs = args.h5dir.split(",")
    print(f"Found {len(subdirs)} h5 sample subdirectories")
    multi_sample_mode = len(subdirs) > 1

    h5_files = []
    for subdir in subdirs:
        h5_files += glob.glob(os.path.join(subdir, "*.h5"))

    print(f"Found {len(h5_files)} total h5 files")

    if multi_sample_mode:
        sample_id_map = get_h5_to_sample_id_map(h5_files)
    else:
        sample_id_map = None

    depth_df = get_barcode_depth(h5_files, sample_id_map)

    depth_df["pass"] = depth_df.apply(
        lambda row: row[args.depth_column] >= args.min_depth, axis=1
    )
    csv_path = os.path.join(args.outdir, "barcode_depth.csv")
    depth_df.to_csv(csv_path, index_label="barcode")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-h5dir",
        type=str,
        required=True,
        help="Directory (or directories separated by comma) containing h5 files. Will read in all files ending in ext .h5",
    )
    parser.add_argument(
        "-min-depth",
        type=int,
        required=False,
        default=10,
        help="minimum barcode depth to filter on using h5 coolumn specified in -depth_column",
    )
    parser.add_argument(
        "-depth-column",
        type=str,
        required=False,
        help="average_total_depth or average_high_quality_depth",
        default="average_high_quality_depth",
    )
    parser.add_argument("-outdir", type=str, required=True, help="output directory")
    args = parser.parse_args()

    main(args)
