# Duplicate Finder

## Description

This is a simple script to find duplicate files in a directory. It uses the md5 hash of the files to find duplicates.

## Usage

```terminal
usage: main.py [-h] {compare,find,list,delete} ...

Utility for finding duplicate files.

positional arguments:
  {compare,find,list,delete}
    compare             Compare two directories for duplicate files.
    find                Find duplicates of a specific file in a directory.
    list                List all duplicate files in a directory.
    delete              Delete the duplicate files.
```

### Compare

```terminal
python main.py compare reference_folder compare_folder 
```

### Scan

```terminal
python main.py find myfile.txt search_folder
```

### List

```terminal
python main.py list search_folder
```

### Delete

```terminal

```

## Folder Structure

```terminal
.
├── README.md
├── data
├── duplicate_finder
│   ├── __init__.py
│   ├── core.py
│   └── utils.py
└── main.py
```

## ToDo

- [ ] Add delete functionality
- [ ] Add tests
- [ ] Ignore hidden files and folders
