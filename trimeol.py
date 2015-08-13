#!/usr/bin/python3
"""Remove all end of line whitespace and tabs in a given text file(s).
Usage:
    trimeol.py [input_files]
    If no input_files are supplied, the program reads from stdin.
"""

import os
import stat
import sys
import time

import binarycheck

def process_file(fname):
    """Remove all end of line whitespace and tabs from the text file 'name'.

    Returns:
        -1 if error.
        0 if file changed.
        1 if file skipped.
        2 if file not changed.
    """
    lines = []
    original_len = 0

    if binarycheck.is_binary_file(fname):
        print("Skipping {} - it appears to be a binary file.".format(fname))
        return 1

    try:
        with open(fname, 'r') as fin:
            for line in fin:
                original_len += len(line)
                lines.append(line.rstrip(" \t\n") + "\n")
        data = "".join(lines)
        if original_len == len(data): # No changes made
            return 2

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
        with open(tmpfile, "w") as fout:
            fout.write(data)
            fout.flush()
            os.fsync(fout.fileno())
        try:
            os.rename(tmpfile, destination)
        except OSError:
            # Probably a Windows machine, try to remove destination first.
            os.remove(destination)
            os.rename(tmpfile, destination)
    except IOError:
        print("An error occured writing {}".format(destination))
        return -1

    return 0

def usage():
    """Print usage information."""
    print("Usage: {} [input_files]\n"
          "If no input_files are supplied, the program reads "
          "from stdin.".format(os.path.basename(sys.argv[0])))

def main():
    time1 = time.clock()
    counters = {"processed": 0,
                "skipped": 0,
                "changed": 0,
                "errors": 0}
    files = []

    if len(sys.argv) == 1:
        if stat.S_ISFIFO(os.fstat(0).st_mode): # Check for piped stdin.
            files = sys.stdin
        else: # No input - print usage.
            usage()
            sys.exit(0)
    else:
        files = sys.argv[1:]

    for file in files:
        res = process_file(file.strip(" \r\n\r"))
        if res >= 0:
            counters["processed"] += 1
            if res == 0:
                counters["changed"] += 1
            elif res == 1:
                counters["skipped"] += 1
        else:
            counters["errors"] += 1


    time2 = time.clock()
    print("Finished processing after {} seconds.".format(round(time2 - time1, 4)))

    col_width = max(len(row) for row in counters.keys()) + 2
    print("=== Summary ===")
    for key, value in counters.iteritems():
        print("{}: {}".format(key.capitalize().ljust(col_width), value))

if __name__ == "__main__":
    main()
