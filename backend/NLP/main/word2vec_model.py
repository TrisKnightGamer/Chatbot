from gensim.models import word2vec
import os
import pandas as pd
import numpy as np
from gensim.models.word2vec import Word2Vec

path = os.getcwd().split("\\")
root_dir = path[:-1]
root_dir = '/'.join(root_dir)
data_path = root_dir + '/Volumes/ESD-USB/share/chatobt/backend/NLP/data'
data_path = data_path + '/processed_data4.csv'
#data_path = '/Volumes/ESD-USB/share/chatobt/backend/NLP/data/processed_data3.csv'


if __name__ == '__main__':
    sentences = []
    print("Converting to Word2Vector ... ")

    model = Word2Vec.load('../models/VNCorpus6.bin')
    model.save(root_dir + ('/models/VNCorpus7.bin'))
    print("Done")