
#Don’t forget to set
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


#From Strings to Vectors
#This time, let’s start from documents represented as strings:

documents = [
              "Human machine interface for lab abc computer applications",
              "A survey of user opinion of computer system response time",
              "The EPS user interface management system",
              "System and human system engineering testing of EPS",
              "Relation of user perceived response time to error measurement",
              "The generation of random binary unordered trees",
              "The intersection graph of paths in trees",
              "Graph minors IV Widths of trees and well quasi ordering",
              "Graph minors A survey"
             ]

#  This is a tiny corpus of nine documents,
#  each consisting of only a single sentence.

#First, let’s tokenize the documents,
#  remove common words (using a toy stoplist) as well as words that only appear once in the corpus:

from pprint import pprint  # pretty-printer
from collections import defaultdict

# remove common words and tokenize
stoplist = set('for a of the and to in'.split())
texts = [
     [word for word in document.lower().split() if word not in stoplist]
     for document in documents
 ]
# remove words that appear only once
frequency = defaultdict(int)
for text in texts:
     for token in text:
         frequency[token] += 1

texts = [
     [token for token in text if frequency[token] > 1]
     for text in texts
  ]

pprint(texts)
#[['human', 'interface', 'computer'],
#['survey', 'user', 'computer', 'system', 'response', 'time'],
# ['eps', 'user', 'interface', 'system'],
# ['system', 'human', 'system', 'eps'],
# ['user', 'response', 'time'],
# ['trees'],
# ['graph', 'trees'],
# ['graph', 'minors', 'trees'],
# ['graph', 'minors', 'survey']]



#To convert documents to vectors, we’ll use a document representation called bag-of-words.
# In this representation, each document is represented by one vector where each vector element
#  represents a question-answer pair, in the style of:

#“How many times does the word system appear in the document? Once.”
#It is advantageous to represent the questions only by their (integer) ids.
# The mapping between the questions and ids is called a dictionary:
from gensim import corpora
dictionary = corpora.Dictionary(texts)
dictionary.save('C:/User/zuzex_ai_code_analysis_tools/tmp/deerwester.dict')  # store the dictionary, for future reference
print(dictionary)
#Dictionary(12 unique tokens)


#Here we assigned a unique integer id to all words appearing in the corpus with the gensim.corpora.dictionary.Dictionary class.

print(dictionary.token2id)
#{'minors': 11, 'graph': 10, 'system': 5, 'trees': 9, 'eps': 8, 'computer': 0,
#'survey': 4, 'user': 7, 'human': 1, 'time': 6, 'interface': 2, 'response': 3}

#To actually convert tokenized documents to vectors:

new_doc = "Human computer interaction"
new_vec = dictionary.doc2bow(new_doc.lower().split())
print("New vector")
print(new_vec)  # the word "interaction" does not appear in the dictionary and is ignored
#[(0, 1), (1, 1)]

#The function doc2bow() simply counts the number of occurrences of each distinct word,
#converts the word to its integer word id and returns the result as a sparse vector.


corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('C:/User/zuzex_ai_code_analysis_tools/tmp/deerwester.mm', corpus)  # store to disk, for later use
print(corpus)
#[(0, 1), (1, 1), (2, 1)]
#[(0, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
#[(2, 1), (5, 1), (7, 1), (8, 1)]
#[(1, 1), (5, 2), (8, 1)]
#[(3, 1), (6, 1), (7, 1)]
#[(9, 1)]
#[(9, 1), (10, 1)]
#[(9, 1), (10, 1), (11, 1)]
#[(4, 1), (10, 1), (11, 1)]


#By now it should be clear that the vector feature with id=10 stands for the question “How many times does the word graph appear in the document?” and that the answer is “zero” for the first six documents and “one” for the remaining three.
#As a matter of fact, we have arrived at exactly the same corpus of vectors as in the Quick Example.