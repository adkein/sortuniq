#!/usr/bin/env python3

import argparse
import curses
from collections import Counter
import time
import sys


VALUE_COUNTS = Counter()


def counts_to_string(height=None):
    """Convert the value counts object to a string for display."""

    value_counts = sorted(VALUE_COUNTS.items(), key=lambda v: v[1], reverse=True)

    if height is not None:
        value_counts = value_counts[:height]

    value_counts = ["{}\t{}".format(v, n) for v, n in value_counts]

    return "\n".join(value_counts)


def read_chunks_by_size(file_):
    """Iterate through the input file, breaking into chunks by row count."""

    while True:
        yield file_.readlines(CHUNK_SIZE)


def read_chunks_by_time(file_):
    """Iterate through the input file, breaking into chunks by timer."""

    while True:
        chunk = []

        start = time.time()
        while time.time() < start + INTERVAL:
            line = file_.readline()
            if not line:
                break
            chunk.append(line.rstrip("\n"))

        yield chunk


def read_chunks(file_):
    """Iterate through the input file, broken into chunks."""

    if CHUNK_SIZE is not None:
        read_chunks_ = read_chunks_by_size
    else:
        read_chunks_ = read_chunks_by_time

    for chunk in read_chunks_(file_):
        if not chunk:
            break
        yield chunk


def count_values():
    """
    Read the next chunk of lines of input and update the count.

    Yields the updated value counts as a string to be displayed.
    """

    f = sys.stdin if INFILE is None else open(INFILE, "r")

    try:
        for chunk in read_chunks(f):
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

    f = sys.stdout if outfile is None else open(outfile, "w")

    try:
        f.write(counts_to_string() + "\n")

    finally:
        f.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--height", "-H", type=int, default=20, help="The number of lines displayed.")
    parser.add_argument("--chunk-size", "-s", type=int, help="The number of lines read before updating the display.")
    parser.add_argument("--interval", "-t", type=float, default=1, help="The wall time in seconds between display updates.")
    parser.add_argument("--infile", "-i")
    parser.add_argument("--outfile", "-o")
    args = parser.parse_args()

    global HEIGHT
    global CHUNK_SIZE
    global INTERVAL
    global INFILE

    HEIGHT = args.height
    CHUNK_SIZE = args.chunk_size
    INTERVAL = args.interval
    INFILE = args.infile

    curses.wrapper(sortuniq)

    write_unabriged_results(args.outfile)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
