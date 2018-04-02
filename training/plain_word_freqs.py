#!/usr/bin/env python
from __future__ import unicode_literals

import codecs
import glob
from pathlib import Path
from collections import Counter

import plac
from multiprocessing import Pool
from tqdm import tqdm


def count_words(fpath):
    with codecs.open(fpath, encoding="utf8") as f:
        words = f.read().split()
        counter = Counter(words)
    return counter


@plac.annotations(
    input_loc=("Location of input file list", "positional", None, Path),
    out_loc=("Directory for frequency files", "positional", None, Path),
    workers=("Number of workers", "option", "n", int),
)
def main(input_loc, out_loc, workers=-2):
    input_files = [str(i.absolute()) for i in input_loc.glob("**/*")]
    output_file = str(out_loc.absolute())

    p = Pool(processes=workers)
    counts = p.map(count_words, tqdm(input_files))
    df_counts = Counter()
    word_counts = Counter()
    for wc in tqdm(counts):
        df_counts.update(wc.keys())
        word_counts.update(wc)
    with codecs.open(output_file, "w", encoding="utf8") as f:
        for word, df in df_counts.items():
            f.write(u"{freq}\t{df}\t{word}\n".format(word=repr(word), df=df, freq=word_counts[word]))


if __name__ == "__main__":
    plac.call(main)
