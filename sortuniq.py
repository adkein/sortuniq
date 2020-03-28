#!/usr/bin/env python3

import argparse
from curses import wrapper
from collections import Counter
import sys


VALUE_COUNTS = Counter()


def counts_to_string(height=None):
    """Convert the value counts object to a string for display."""

    value_counts = sorted(VALUE_COUNTS.items(), key=lambda v: v[1], reverse=True)

    if height is not None:
        value_counts = value_counts[:height]

    value_counts = ["{}\t{}".format(v, n) for v, n in value_counts]

    return "\n".join(value_counts)


def count_values():
    """
    Read the next chunk of lines of input and update the count.

    Yields the updated value counts as a string to be displayed.
    """

    f = sys.stdin if INFILE is None else open(INFILE, 'r')

    try:
        while True:
            chunk = f.readlines(PERIOD)

            if not chunk:
                break

            values = [line.rstrip("\n") for line in chunk]

            VALUE_COUNTS.update(values)

            yield counts_to_string(HEIGHT)

    finally:
        f.close()


def sortuniq(stdscr):
    """Iterate over over intermediate result sets and display them."""

    for results in count_values():
        stdscr.clear()
        stdscr.addstr(results)
        stdscr.refresh()


def write_unabriged_results(outfile):
    """Write results once all input has been processed."""

    f = sys.stdout if outfile is None else open(outfile, 'w')

    try:
        f.write(counts_to_string() + "\n")

    finally:
        f.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--height", "-H", type=int, default=20, help="The number of lines displayed.")
    parser.add_argument("--period", "-p", type=int, default=20, help="The number of lines read before updating the display.")
    parser.add_argument("--infile", "-i")
    parser.add_argument("--outfile", "-o")
    args = parser.parse_args()

    global HEIGHT
    global PERIOD
    global INFILE

    HEIGHT = args.height
    PERIOD = args.period
    INFILE = args.infile

    wrapper(sortuniq)

    write_unabriged_results(args.outfile)


if __name__ == "__main__":
    main()
