#!/usr/bin/env python3

import sys, click

from typing import List


def vez_hist(sequence: List[int], bin_size):
    bins = seq_to_bins(sequence, bin_size)
    filler_chars = ['▓', '░']
    
    y_labels = [f"{val:d} - {(val+bin_size-1):d}" for val in bins.keys()]
    y_l_width = max(map(len, y_labels)) + 1

    print()
    for idx, (_, bin_count) in enumerate(bins.items()):
        label = y_labels[idx]
        label =(' ' * (y_l_width - len(label))) + label
        print(f"{label} ╂ {filler_chars[idx%2] * bin_count}")
    print(' '*y_l_width + '━╋' + '━' * (max(bins.values()) + 3))
    print()


def seq_to_bins(sequence: List[int], bin_size: float) -> dict[int, int]:
    bins_n: int = int((max(sequence) - min(sequence)) / bin_size) + 1
    bins: dict[int, int] = { int(i*bin_size): 0 for i in range(bins_n) }

    for value in sequence:
        bin_idx = int((value - min(sequence)) / bin_size)
        bins[bin_idx * bin_size] += 1

    return bins


@click.command()
@click.argument('sequence_file', type=click.File('r'), required=False)
@click.option('--bin-size', type=int, default=10, help='Size of the bins')
def main(sequence_file: click.File, bin_size: int):
    sequence: List[int] = []

    if sequence_file:
        seq_tmp = open(sys.argv[1]).read().strip().split('\n')
    else:
        seq_tmp = sys.stdin.read().strip().split('\n')
    
    if (len(seq_tmp) == 1):
        sequence = list(map(int, seq_tmp[0].split(' ')))
    else:
        sequence = list(map(int, seq_tmp))

    vez_hist(sequence, bin_size)


if __name__ == "__main__":
    main()