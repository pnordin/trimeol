#!/usr/bin/python3

# Remove all end of line whitespace and tabs in a text file.
#
# Usage:
#   trimeol.py [input_files]
#   If no input_files are supplied, the program reads from stdin.
#
# Examples:
#    Perform on a single file:
#        trimeol.py ~/project/main.c
#
#    Performs on multiple files:
#        trimeol.py main.c builtins.h
#
#    Perform on all files in the current directory:
#        *nix:
#            find . -type f -maxdepth 1 | trimeol.py
#        Windows:
#            dir /B /A:-D | trimeol.py
#
#    Perform on all files in the current directory recursively:
#        *nix:
#            find . -type f | trimeol.py
#        Windows:
#            dir /B /S /A:-D | trimeol.py
#
#    Perform on all .c files in current directory recursively:
#        *nix:
#            find . -type f | grep ".*\.c$" | trimeol.py
#        Windows:
#            dir /B /S /A:-D | findstr ".*\.c$" | trimeol.py

import sys
import os
import stat
import time

import binarycheck

def process_file(name):
    """Remove all end of line whitespace and tabs from the text file 'name'.

    Returns 0 on success.
    """
    fname = name.rstrip(' \t\n\r')
    indata = ""
    data = ""
    start_size = 0
    end_size = 0

    if (binarycheck.is_binary_file(fname)):
        print("Skipping {} - it appears to be a binary file.".format(fname))
        return -1

    try:
        with open(fname, 'r') as fin:
            for line in fin:
                start_size += len(line)
                data = "".join([data,
                                line.rstrip(' \t\n'),
                                '\n'])
        end_size = len(data)
        if start_size == end_size: # No change in data
            print("Skipping {} - no changes made.".format(fname))
            return -1
            
        return write_data(data, fname)
    except IOError:
        print("An error occurred processing {}".format(fname))
        return -1

def write_data(data, destination):
    """Write (overwrite) 'data' to 'destination' file semi-atomically.

    Returns 0 on success.
    """
    tmpfile = destination + ".tmp"

    try:
        with open(tmpfile, 'w') as fout:
            fout.write(data)
            fout.flush()
            os.fsync(fout.fileno())
        os.remove(destination)
        os.rename(tmpfile, destination)
    except IOError, OSError:
        print("An error occured writing {}".format(destination))
        return -1

    return 0

def print_usage():
    print("Usage: {} [input_files]\n"
          "If no input_files are supplied,"
          "the program reads from stdin.".format(os.path.basename(sys.argv[0])))

def main():
    t1 = time.clock()
    nprocessed = 0

    if (len(sys.argv) == 1):
        if stat.S_ISFIFO(os.fstat(0).st_mode): # Check for piped stdin.
            for line in sys.stdin:
                if process_file(line.rstrip(' \t\n\r')) == 0:
                    nprocessed += 1
        else: # No input - print usage.
            print_usage()
            sys.exit(0)
    else:
        for file in sys.argv[1:]:
            if process_file(file) == 0:
                nprocessed += 1

    t2 = time.clock()
    print("{} files processed successfully in {} seconds.".format(nprocessed, round(t2 - t1, 4)))

if __name__== "__main__":
    main();
