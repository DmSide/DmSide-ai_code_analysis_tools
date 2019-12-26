from gensim import corpora

#Gensim only requires that a corpus must be able to return one document vector at a time:
class MyCorpus(object):
     def __iter__(self):
          self.count = 0
          for line in open('C:/User/corpus.txt'):
             # assume there's one document per line, tokens separated by whitespace
             if( self.count == 0):
                 self.dictionary = corpora.Dictionary()
             else :
                 del  self.dictionary
                 self.dictionary = corpora.Dictionary()

             self.count += 1

             yield self.dictionary.doc2bow(line.lower().split(),allow_update = True)
            # yield self.dictionary.doc2bow(line.lower().split())



corpus_memory_friendly = MyCorpus()  # doesn't load the corpus into memory!

#<__main__.MyCorpus object at 0x10d5690>

for vector in corpus_memory_friendly:  # load one vector into memory at a time
     print(vector)

# [(0, 1), (1, 1), (2, 1)]
# [(0, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
# [(2, 1), (5, 1), (7, 1), (8, 1)]
# [(1, 1), (5, 2), (8, 1)]
# [(3, 1), (6, 1), (7, 1)]
# [(9, 1)]
# [(9, 1), (10, 1)]
# [(9, 1), (10, 1), (11, 1)]
# [(4, 1), (10, 1), (11, 1)]