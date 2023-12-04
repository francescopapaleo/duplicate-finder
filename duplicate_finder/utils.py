# utils.py

import os
import hashlib
import pandas as pd
import sys

from typing import List


def chunk_reader(fobj, chunk_size=1024):
    """Generator that reads a file in chunks of bytes"""
    while True:
        chunk = fobj.read(chunk_size)
        if not chunk:
            return
        yield chunk


def get_hash(filename, first_chunk_only=False, hash=hashlib.sha1):
    """Calculate the hash of a file.

    Args:
        filename (str): The path to the file.
        first_chunk_only (bool): Whether to hash only the first chunk of the file. Defaults to False.
        hash: The hash function to use. Defaults to hashlib.sha1.

    Returns:
        bytes: The file hash.
    """
    hashobj = hash()

    with open(filename, "rb") as file_object:
        if first_chunk_only:
            hashobj.update(file_object.read(1024))
        else:
            for chunk in chunk_reader(file_object):
                hashobj.update(chunk)

    return hashobj.digest()


def format_path(file: str) -> str:
    """Format a path according to the systems separator."""
    return os.path.abspath([file.replace("/", os.path.sep)][0])


def filelist(filepath: str, ext: str = None) -> list:
    """Lists all files in a folder including sub-folders.
    If only files with a specific extension are of interest
    this can be specified by the 'ext' parameter."""
    file_list = []
    for path, _, files in os.walk(filepath):
        for name in files:
            _, extension = os.path.splitext(name)
            if ext is None or extension == ext:
                file_list.append(os.path.join(path, name))

    return file_list


def hashfile(file: str, block_size: int = 65536) -> str:
    """Generate the hash of any file according to the sha256 algorithm."""
    with open(file, "rb") as message:
        m = hashlib.sha256()
        block = message.read(block_size)
        while len(block) > 0:
            m.update(block)
            block = message.read(block_size)
        digest = m.hexdigest()

    return digest


def hashtable(files: list) -> list:
    """Go through a list of files and calculate their hash identifiers."""
    if isinstance(files, list) is False:
        files = [files]

    hash_identifier = []
    for file in files:
        sys.stdout.write(file + "\r")
        try:  # Avoid crash in case a file name is too long
            hash_identifier.extend([hashfile(file)])
        except OSError:
            hash_identifier.extend(["No hash could be generated"])

    return hash_identifier


def preselect(input_files: list) -> list:
    """Pre-select potential duplicate files based on their size."""
    checked_files = []
    for file in input_files:
        if os.path.isfile(file):
            checked_files.append(file)

    summary_df = pd.DataFrame(columns=["file", "size"])

    summary_df["file"] = checked_files
    summary_df["size"] = [os.path.getsize(file) for file in checked_files]

    summary_df = summary_df[summary_df["size"].duplicated(keep=False)]

    return summary_df["file"].tolist()


def save_csv(path: str, df: pd.DataFrame) -> str:
    """Save a DataFrame to a csv file and returns the path of the saved file."""

    if not path.endswith(".csv"):
        path += ".csv"

    df.to_csv(path, index=False)
    return path


def delete_files(duplicate_files: List[str]):
    """
    Delete duplicate files, preserving the first occurrence.

    Args:
        duplicate_files (List[str]): A list of duplicate file paths.
    """
    checked_hashes = {}
    for file_path in duplicate_files:
        file_hash = get_hash(file_path)
        if file_hash not in checked_hashes:
            # If this hash is new, store the file and don't delete anything
            checked_hashes[file_hash] = file_path
        elif file_path != checked_hashes[file_hash]:
            # If this hash is already known and the current file is not the one we stored, delete it
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(
                    f"Error occurred while deleting file {file_path}. Error: {str(e)}"
                )
