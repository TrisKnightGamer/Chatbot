from gensim.models import word2vec
from gensim.models.word2vec import Word2Vec
import pandas as pd
import numpy as np

df = pd.read_csv('../data/processed_data4.csv', usecols=[1])
df = df.values
df = np.array(df)
df = df.reshape((1,-1))[0]

model = Word2Vec.load('../models/VNCorpus7.bin')
model.build_vocab(df[0], update=True)
model.save('../models/VNCorpus7.bin')

model = Word2Vec.load('../models/VNCorpus7.bin')
model = model.wv
model.save('../models/VNCorpus7.wordvectors')


print('Done')
