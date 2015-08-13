"""Module to help guess whether a file is binary or text."""
def is_binary_file(fname):
    """Attempt to guess if 'fname' is a binary file heuristically.

    This algorithm has many flaws. Use with caution.
    It assumes that if a part of the file has NUL bytes
    or has more control characters than text characters,
    it is a binary file.
    Additionally, an ASCII compatible character set is assumed.

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
