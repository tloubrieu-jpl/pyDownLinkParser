"""Utility to convert a downlink CCSDS binary file to excel."""
import argparse
import os.path

import pandas as pd
from pydownlinkparser.parse_ccsds_downlink import parse_ccsds_file
from pydownlinkparser.remove_non_ccsds_headers import strip_non_ccsds_headers


def get_parser():
    """Parser for the command line utility."""
    parser = argparse.ArgumentParser(description="Parse Files")
    parser.add_argument("--file", type=str, required=True, help="Input File")
    parser.add_argument(
        "--bdsem",
        action="store_true",
        help="Mode BDSEM, with specific, non-CCSDS, packet wrappers, "
        "if not present, RAW mode is assumed, "
        "with other specific non CCSDS markers in betwwen packets",
    )
    parser.add_argument(
        "--header",
        action="store_true",
        help="When additional non CCSDS header are added between packets",
    )
    return parser


def export_dfs_to_xlsx(dfs, filename1):
    """Export a dictionnary of pandas dataframes to an Excel file."""
    with pd.ExcelWriter(filename1) as writer:
        for name, df in dfs.items():
            df.to_excel(writer, sheet_name=name, index=True)


def export_ccsds_to_excel(ccsds_file, output_filename):
    """Export a binary file of CCSDS packets into an Excel file."""
    dfs = parse_ccsds_file(ccsds_file)
    export_dfs_to_xlsx(dfs, output_filename)


def main():
    """Command line interface to parse downlink binary file and export to Excel file."""
    parser = get_parser()
    args = parser.parse_args()

    ccsds_file = strip_non_ccsds_headers(args.file, args.bdsem, args.header)

    file_base, _ = os.path.splitext(args.file)
    xlsx_filename = file_base + ".xlsx"
    export_ccsds_to_excel(ccsds_file, xlsx_filename)


if __name__ == "__main__":
    main()
