import plac
import gensim


@plac.annotations(
    in_dir=("Location of input directory"),
    out_loc=("Location of output file"),
    n_workers=("Number of workers", "option", "n", int),
    size=("Dimension of the word vectors", "option", "d", int),
    window=("Context window size", "option", "w", int),
    min_count=("Min count", "option", "m", int),
    negative=("Number of negative samples", "option", "g", int),
    nr_iter=("Number of iterations", "option", "i", int),
)
def main(in_dir, out_loc, negative=5, n_workers=4, window=5, size=128, min_count=10, nr_iter=2):
    sentences = gensim.models.word2vec.PathLineSentences(in_dir)
    model = gensim.models.word2vec.Word2Vec(
        sentences=sentences,
        size=size,
        window=window,
        min_count=min_count,
        workers=n_workers,
        sample=1e-5,
        negative=negative,
        iter=nr_iter
    )
    model.wv.save_word2vec_format(out_loc, binary=False)


if __name__ == '__main__':
    plac.call(main)
