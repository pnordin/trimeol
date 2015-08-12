
import subprocess

g_use_file_command = True

def is_binary_file(fname):
    """Determine if 'fname' is a binary file.

    If the file command is available, it will be used,
    otherwise, a heuristic approach is taken.

    Returns True if 'fname' appears to be a binary file.
    """
    if (g_use_file_command and
            is_binary_file_f(fname)):
        return True

    if is_binary_file_h(fname):
        return True

    return False

def is_binary_file_h(fname):
    """Attempt to guess if 'fname' is a binary file heuristically.

    The algorithm has many flaws. Use with caution.
    It assumes that if a part of the file has NUL bytes
    or has more control characters than text characters,
    it is probably a binary file.
    An ASCII compatible character set is assumed.

    Returns True if 'fname' appears to be a binary file.
    """
    with open(fname, 'rb') as fh:
        chunk = fh.read(1024)

        if not chunk: # Empty file
            return False

        if b'\x00' in chunk: # Has NUL bytes
            return True

        ncontrol = control_char_count(chunk)
        ntext = len(chunk) - ncontrol
        return ncontrol > ntext

def is_binary_file_f(fname):
    """Determine if 'fname' is a binary file using the file command.

    If the file command does not exist,
    the global variable g_use_file_command is set to False
    and no more attempts to use the file command should be made.

    Returns True if'fname' appears to be a binary file.
    """
    try:
        proc = subprocess.Popen(["file", fname], stdout=subprocess.PIPE)
        for line in proc.stdout.readlines():
            if "text" in line.lower():
                return False
    except:
        g_use_file_command = False
        return False
    return True

def is_control_char(c):
    """Return True if 'c' is a control character.

    c is considered a control character if
    it is outside of the extended ASCII set or
    is a control character below 33.
    An ASCII compatible character set is assumed.
    """
    charcode = ord(c)
    return (charcode < 33 or
            charcode > 255)

def control_char_count(data):
    """Return the count of control characters in 'data'."""
    n = 0
    for c in data:
        if is_control_char(c):
            n += 1
    return n
