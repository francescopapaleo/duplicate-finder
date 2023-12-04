# core.py

import os
import sys
import hashlib
import pickle
import pandas as pd

from tqdm import tqdm
from collections import defaultdict

from .utils import get_hash, format_path, filelist, hashtable, preselect, save_csv


def check_for_duplicates(paths, hash=hashlib.sha1):
    """Find duplicate files in the specified directories.

    Args:
        paths (list): List of directories to search for duplicate files.
        hash: The hash function to use. Defaults to hashlib.sha1.
    """
    hashes_by_size = defaultdict(list)
    hashes_on_1k = defaultdict(list)
    hashes_full = {}
    duplicates_list = []

    for path in tqdm(paths):
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                if os.path.basename(filename) == ".DS_Store":
                    continue
                full_path = os.path.join(dirpath, filename)
                try:
                    full_path = os.path.realpath(full_path)
                    file_size = os.path.getsize(full_path)
                    hashes_by_size[file_size].append(full_path)
                except OSError:
                    continue

    for size_in_bytes, files in hashes_by_size.items():
        if len(files) < 2:
            continue

        for filename in files:
            try:
                small_hash = get_hash(filename, first_chunk_only=True)
                hashes_on_1k[(small_hash, size_in_bytes)].append(filename)
            except OSError:
                continue

    for __, files_list in hashes_on_1k.items():
        if len(files_list) < 2:
            continue

        for filename in files_list:
            try:
                full_hash = get_hash(filename, first_chunk_only=False)
                duplicate = hashes_full.get(full_hash)
                if duplicate:
                    sys.stdout.write(
                        "Duplicate found: {} \n ---> {}".format(filename, duplicate)
                    )
                    duplicates_list.append(duplicate)
                else:
                    hashes_full[full_hash] = filename
            except OSError:
                continue

    with open("duplicates_list.pkl", "wb") as f:
        pickle.dump(duplicates_list, f)


def create_table(folder: str, ext: str = None, pre: bool = False) -> pd.DataFrame:
    """Create a Pandas dataframe with a column 'file' for the path to a file and a
    column 'hash' with the corresponding hash identifier."""
    folder = format_path(folder)
    input_files = filelist(folder, ext=ext)

    if pre is True:
        input_files = preselect(input_files)

    summary_df = pd.DataFrame(columns=["file", "hash"])

    summary_df["file"] = input_files
    summary_df["hash"] = hashtable(input_files)

    return summary_df


def list_all_duplicates(
    folder: str,
    to_csv: bool = False,
    csv_path: str = "./",
    ext: str = None,
    fastscan: bool = False,
) -> pd.DataFrame:
    """Go through a folder and find all duplicate files.
    The returned dataframe contains all files, not only the duplicates.
    With the 'to_csv' parameter the results can also be saved in a .csv file.
    The location of that .csv file can be specified by the 'csv_path' parameter.
    To improve performance when handling large files the fastscan parameter
    can be set to True. In this case files are pre-selected based on their size."""
    duplicate_files = create_table(folder, ext, pre=fastscan)
    duplicate_files = duplicate_files[duplicate_files["hash"].duplicated(keep=False)]
    duplicate_files.sort_values(by="hash", inplace=True)

    if to_csv is True:
        save_csv(csv_path, duplicate_files)

    return duplicate_files


def find_duplicates(file: str, folder: str) -> pd.DataFrame:
    """Search a folder for duplicates of a file of interest.
    In contrast to 'list_all_duplicates', this allows
    limiting the search to one particular file."""
    file = format_path(file)
    folder = format_path(folder)

    file_hash = hashtable(file)

    duplicate_files = list_all_duplicates(folder)

    if len(file_hash) == 1:
        file_hash = file_hash[0]

    return duplicate_files[duplicate_files["hash"] == file_hash]


def compare_folders(
    reference_folder: str,
    compare_folder: str,
    to_csv: bool = False,
    csv_path: str = "./",
    ext: str = None,
) -> pd.DataFrame:
    """Directly compare two folders of interest and identify duplicates between them.
    With the 'to_csv' parameter the results can also be saved in a .csv file.
    The location of that .csv file can be specified by the 'csv_path' parameter.
    Further the search can be limited to files with a specific extension via the 'ext' parameter.
    """
    df_reference = create_table(reference_folder, ext)
    df_compare = create_table(compare_folder, ext)

    ind_duplicates = [x == df_reference["hash"] for x in df_compare["hash"].values]
    duplicate_files = df_compare.iloc[ind_duplicates]

    duplicate_files.drop_duplicates(subset="file", inplace=True)

    if to_csv is True:
        save_csv(csv_path, duplicate_files)

    return duplicate_files
