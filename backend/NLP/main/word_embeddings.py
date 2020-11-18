from gensim.models import word2vec
import os
import pandas as pd
import numpy as np
from gensim.models.word2vec import Word2Vec
from sklearn.decomposition import PCA
from matplotlib import pyplot

if __name__ == '__main__':    
    model = Word2Vec.load('../models/VNCorpus7.bin')
    # fit a 2d PCA model to the vectors
    X = model[model.wv.vocab]
    pca = PCA(n_components=32)
    result = pca.fit_transform(X)

    pyplot.scatter(result[:, 0], result[:, 1])
    words = list(model.wv.vocab)
    for i, word in enumerate(words):
        pyplot.annotate(word, xy=(result[i, 0], result[i, 1]))
    pyplot.show()