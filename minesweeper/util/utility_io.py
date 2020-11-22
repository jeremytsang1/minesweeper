# Filename    : utility_io.py.py
# Author      : Jeremy Tsang
# Date        : 2020-09-28
# Description : Various helper functions for file IO

# -----------------------------------------------------------------------------
# File Input function

def read_text_file_as_strings(filename):
    """Reads contents of a text file into a list with each line of the file
    corresponding to a string element in said list.

    Parameters
    ----------
    filename: str
        Name of the file. Assumed in the same directory.

    Returns
    -------
    list of str
        Python list of strings with length equal to number of lines of the
        input file.
    """
    lines = []
    with open(f'{filename}', 'r') as infile:
        for line in infile:
            lines.append(line.strip())
    return lines


def read_text_file_as_ints(filename):
    """Reads contents of a text file into a nested list of int.

    Parameters
    ----------
    filename: str
        Name of the file. Assumed in the same directory. Assumed all data is in
        the form of space delimited int.

    Returns
    -------
    list of list of int
        Nested list of int of int with outer list length equal to number of
        lines of the input file.
    """
    lines = read_text_file_as_strings(filename)
    return [[int(number_string) for number_string in line.split()]
            for line in lines]


def read_text_file_as_float(filename):
    """Reads contents of a text file into a nested list of float.

    Parameters
    ----------
    filename: str
        Name of the file. Assumed in the same directory. Assumed all data is in
        the form of space delimited floats.

    Returns
    -------
    list of list of float
        Nested list of int of int with outer list length equal to number of
        lines of the input file.
    """
    lines = read_text_file_as_strings(filename)
    return [[float(number_string) for number_string in line.split()]
            for line in lines]


def move_lines(lines, descriptor, processing_for_each_line):
    """Move data corresponding to lines of the input file to a list. Intended for
    use with the return value of read_text_file_as_ints(). Assuming the first
    element is the number of subsequent lines to move, processes said
    subsequent lines with function `processing_for_each_line` and returns them.

    Parameters
    ----------
    lines: list of list of int
        First element should be a list of a length 1 that whose element
        denotes how many subsequent rows to take. Said element should be
        less than or equal to len(lines) - 1 (i.e. not all subsequent lines
        may be taken).
    descriptor: str
        Name to user in assertion error message.
    processing_for_each_line: function
        Function that describes how to process the rows being moved. Use the
        identity function `lambda row: row` if no processing is desired.

    Returns
    -------
    list
        List of lines being moved processed via processing_for_each_line().

    """
    # Read in the number of lines to move
    msg = f"No line for ({descriptor}) `count` found!"
    assert len(lines) != 0, msg
    count = lines.pop(0)[0]

    # Move the line, process, and store to result
    msg = f"Remaining number of lines less than ({descriptor}) `count`!"
    assert len(lines) != 0, msg
    moved_lines = []
    for line_num in range(count):
        # Remove the line from lines.
        moved_line = lines.pop(0)
        # Process the line before moving it to the result.
        moved_lines.append(processing_for_each_line(moved_line))
    return moved_lines


# -----------------------------------------------------------------------------
# File output functions

def write_strings_to_text_file(lines, filename):
    """Writes contents of `lines` to `filename`.

    Parameters
    ----------
    lines: list of str
        Python list of str with each str element representing a line to
        write to the file.

    filename: str
        Name of the file. Assumed to be in same directory. Prior contents will
        be erased.

    Returns
    -------
    None

    """
    with open(f'{filename}', 'w') as outfile:
        for line in lines:
            outfile.write(f'{line}\n')


def write_ints_to_text_file(rows, filename):
    """Write a nested iterable of int to textfile named `filename`.

    Parameters
    ----------
    rows: 2D iterable of int
        Numbers to write to the file.
    filename: str
        Name of the file. Assumed in same directory. Prior contents will be
        erased.

    Returns
    -------
    None
    """
    lines_of_text = [' '.join([str(elt) for elt in row]) for row in rows]
    write_strings_to_text_file(lines_of_text, filename)
