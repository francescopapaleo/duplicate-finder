# main.py
import os
import pandas as pd
from argparse import ArgumentParser

from duplicate_finder.utils import delete_files
from duplicate_finder.core import list_all_duplicates, compare_folders


def main():
    parser = ArgumentParser(description="Utility for finding duplicate files.")
    subparsers = parser.add_subparsers(dest="command")

    # Define the 'compare' command
    compare_parser = subparsers.add_parser(
        "compare", help="Compare two directories for duplicate files."
    )
    compare_parser.add_argument("reference_folder", help="The reference directory.")
    compare_parser.add_argument(
        "compare_folder", help="The directory to compare with the reference directory."
    )
    compare_parser.add_argument(
        "--csv_path", default="./", help="Directory where the CSV file will be saved."
    )
    compare_parser.add_argument(
        "--csv_filename", default="duplicates.csv", help="Name of the CSV file."
    )

    # Define the 'scan' command
    scan_parser = subparsers.add_parser("scan", help="Scan a directory for duplicates.")
    scan_parser.add_argument("folder", help="The directory to scan.")
    scan_parser.add_argument(
        "--csv_path",
        default="./",
        help="Directory where the CSV file will be saved.",
    )
    scan_parser.add_argument(
        "--csv_filename", default="duplicates.csv", help="Name of the CSV file."
    )

    # Define the 'list' command
    list_parser = subparsers.add_parser("list", help="List duplicates from a CSV file.")
    list_parser.add_argument(
        "csv_file", help="The CSV file that contains the list of duplicates."
    )

    # Define the 'delete' command
    delete_parser = subparsers.add_parser("delete", help="Delete the duplicate files.")
    delete_parser.add_argument(
        "csv_file",
        help="The path to the CSV file that contains the list of duplicates to be deleted.",
    )

    args = parser.parse_args()

    # Check if the directory exists, create it if it doesn't
    if not os.path.exists(args.csv_path):
        os.makedirs(args.csv_path)

    if args.command == "compare":
        duplicates = compare_folders(args.reference_folder, args.compare_folder)
        csv_file = os.path.join(args.csv_path, args.csv_filename)
        duplicates.to_csv(csv_file, index=False)
    elif args.command == "scan":
        duplicates = list_all_duplicates(args.folder)
        csv_file = os.path.join(args.csv_path, args.csv_filename)
        duplicates.to_csv(csv_file, index=False)
    elif args.command == "list":
        duplicates = pd.read_csv(args.csv_file)
        print(duplicates)
    elif args.command == "delete":
        duplicates = pd.read_csv(args.csv_file)
        if "file" in duplicates.columns:
            delete_files(duplicates["file"].tolist())
        else:
            print("The provided CSV file does not contain a 'file' column.")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
