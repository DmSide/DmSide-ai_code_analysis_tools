#Similarly, to construct the dictionary without loading all texts into memory:
from gensim import corpora
from six import iteritems
# collect statistics about all tokens

# for line in open('C:/User/corpus.txt'):
 #   dictionary = corpora.Dictionary(line.lower().split())

dictionary = corpora.Dictionary(line.lower().split() for line in open('C:/User/corpus.txt'))

stoplist = set('for a of the and to in'.split())
# remove stop words and words that appear only once
stop_ids = [
     dictionary.token2id[stopword]
     for stopword in stoplist
     if stopword in dictionary.token2id
 ]
once_ids = [tokenid for tokenid, docfreq in iteritems(dictionary.dfs) if docfreq == 1]
dictionary.filter_tokens(stop_ids + once_ids)  # remove stop words and words that appear only once
dictionary.compactify()  # remove gaps in id sequence after words that were removed
print(dictionary)
#Dictionary(12 unique tokens)