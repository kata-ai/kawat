#!/usr/bin/env python

import argparse
import os

if __name__ == '__main__':
    p = argparse.ArgumentParser(
        description='Make KaWAT analogy task pairs.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument('file', help='path to the file to process')
    p.add_argument('--encoding', default='utf-8', help='file encoding')
    args = p.parse_args()

    with open(args.file, encoding=args.encoding) as f:
        # Get the header entries
        try:
            hentries = next(f).lower().split()
        except StopIteration:
            p.error('file is empty')
        if len(hentries) < 2:
            p.error('file must contain at least 2 columns')

        # Variable to store the data, where each element is a list of tuples
        data = []
        for linum, line in enumerate(f, 2):
            entries = line.lower().split()
            if len(entries) != len(hentries):
                p.error(
                    f'length of entries mismatch in line {linum}, '
                    f'expected {len(hentries)} but got {len(entries)}')
            data.append([(entries[0], e) for e in entries[1:]])

    section = os.path.splitext(os.path.basename(args.file))[0]
    for hent, col in zip(hentries[1:], zip(*data)):
        sec_name = section
        if len(hentries) > 2:
            sec_name = f'{section}-{hent}'
        print(':', sec_name)

        for i in range(len(col)):
            for j in range(i + 1, len(col)):
                if '-' in col[i] or '-' in col[j]:
                    continue
                print(col[i][0], col[i][1], col[j][0], col[j][1])
