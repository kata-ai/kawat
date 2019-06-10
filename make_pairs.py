#!/usr/bin/env python

##########################################################################
# Copyright 2019 Kata.ai
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##########################################################################

from typing import Iterator, List, Sequence, Tuple
import argparse
import os


def read_data(stream: Iterator[str]) -> Tuple[List[str], List[List[str]]]:
    """Read data from a stream of lines.

    Args:
        stream: Stream that reads the input file line by line, excluding the header.

    Returns:
        List[str]: List of entries in the first column.
        List[List[str]]: Entries in other columns. The k-th element is a list
            of entries in the (k+1)-th column.
    """
    first_col = []
    other_cols = []
    for linum, line in enumerate(stream, 2):
        entries = line.split()
        if other_cols and len(entries) != len(other_cols[-1]) + 1:
            raise ValueError(
                f'line {linum} expected to have {len(other_cols[-1])+1} '
                f'but got {len(entries)}')

        assert entries
        first_col.append(entries[0])
        other_cols.append(entries[1:])

    # Transpose other_cols
    other_cols = [list(col) for col in zip(*other_cols)]

    return first_col, other_cols


def print_pairs(pairs: Sequence[Tuple[str, str]], empty_entry='-') -> None:
    """Print the given pairs to form analogies.

    Args:
        pairs: Pairs to form analogies.
        empty_entry (optional): What considered an empty entry to be skipped.
    """
    for i in range(len(pairs)):
        if empty_entry in pairs[i]:
            continue
        for j in range(i + 1, len(pairs)):
            if empty_entry in pairs[j]:
                continue
            print(pairs[i][0], pairs[i][1], pairs[j][0], pairs[j][1])


if __name__ == '__main__':
    p = argparse.ArgumentParser(
        description='Make KaWAT analogy task pairs.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument('file', help='path to the file to process')
    p.add_argument('--encoding', default='utf-8', help='file encoding')
    p.add_argument('--empty-entry', default='-', help='what represents an empty entry')
    args = p.parse_args()

    with open(args.file, encoding=args.encoding) as f:
        try:
            # Get the header entries
            hentries = next(f).split()
        except StopIteration:
            p.error('file is empty')
        if len(hentries) < 2:
            p.error('file must contain at least 2 columns')

        try:
            first_col, other_cols = read_data(f)
        except ValueError as e:
            p.error(str(e))

    if len(hentries) != len(other_cols) + 1:
        p.error('length of header and content mismatch')

    section = os.path.splitext(os.path.basename(args.file))[0]
    for hent, col in zip(hentries[1:], other_cols):
        sec_name = section
        if len(hentries) > 2:
            sec_name = f'{section}-{hent}'
        print(':', sec_name)
        print_pairs(list(zip(first_col, col)), empty_entry=args.empty_entry)
