#Gensim uses Python’s standard logging module to log various stuff at various priority levels;
# to activate logging (this is optional), run
#import logging
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

#Quick Example
#First, let’s import gensim and create a small corpus of nine documents and twelve features

from gensim import models

corpus = [ [(0, 1.0), (1, 1.0), (2, 1.0)],
           [(2, 1.0), (3, 1.0), (4, 1.0), (5, 1.0), (6, 1.0), (8, 1.0)],
           [(1, 1.0), (3, 1.0), (4, 1.0), (7, 1.0)],
           [(0, 1.0), (4, 2.0), (7, 1.0)],
           [(3, 1.0), (5, 1.0), (6, 1.0)],
           [(9, 1.0)],
           [(9, 1.0), (10, 1.0)],
           [(9, 1.0), (10, 1.0), (11, 1.0)],
           [(8, 1.0), (10, 1.0), (11, 1.0)]
         ]



#Next, let’s initialize a transformation:
tfidf = models.TfidfModel(corpus)

#A transformation is used to convert documents from one vector representation into another

vec = [(0, 1), (4, 1)]
print(tfidf[vec])

#[(0, 0.8075244), (4, 0.5898342)]

#To transform the whole corpus via TfIdf and index it, in preparation for similarity queries

from gensim import similarities

index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=12)

#and to query the similarity of our query vector vec against every document in the corpus

sims = index[tfidf[vec]]
print(list(enumerate(sims)))
#[(0, 0.4662244), (1, 0.19139354), (2, 0.24600551), (3, 0.82094586), (4, 0.0), (5, 0.0), (6, 0.0), (7, 0.0), (8, 0.0)]

#How to read this output?
# Document number zero (the first document) has a similarity score of 0.466=46.6%,
# the second document has a similarity score of 19.1% etc.