# Remove all end of line whitespace and tabs in a text file(s).

## Requirements
    Python 2.7+ (Python 3 recommended)

## Usage:
    trimeol.py [input_files]
    If no input_files are supplied, the program reads from stdin.

## Examples:
    Perform on a single file:
        trimeol.py ~/project/main.c

    Performs on multiple files:
        trimeol.py main.c builtins.h

    Perform on all files in the current directory:
        *nix:
            find . -type f -maxdepth 1 | trimeol.py
        Windows:
            dir /B /A:-D | trimeol.py

    Perform on all files in the current directory recursively:
        *nix:
            find . -type f | trimeol.py
        Windows:
            dir /B /S /A:-D | trimeol.py

    Perform on all .c files in current directory recursively:
        *nix:
            find . -type f | grep ".*\.c$" | trimeol.py
        Windows:
            dir /B /S /A:-D | findstr ".*\.c$" | trimeol.py
