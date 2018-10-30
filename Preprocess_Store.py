import os
import operator
import string
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import math
import string
from collections import deque
import pickle

tf_query = dict()
vector_product = dict()
count = 10
de = deque([])
filename = 'index'
stops = stopwords.words('english')
directory = 'C:/Users/jaish/PycharmProjects/Music Search Engine'
k = 1
no_of_docs = len(os.listdir(directory))
sum = 0

tf_dict = dict()
trans = str.maketrans('', '', string.punctuation)
bag = set()  # empty set is created
files = set()
basic_index = dict()
idf_dict = dict()
tf_idf_dict = dict()


#  this function returns stemmed and lemetized document in list form
def preprocess(filename):
    with open(filename, "r+") as f:
        data = f.read().replace("\n", " ")
        output = data.translate(trans).lower().split()
        output = [word for word in output if not word in stops]
        stemmer = PorterStemmer()
        output = [stemmer.stem(word) for word in output]
        return output


""" 
    This Function Traverses all the text Files in the directory the corpus is in
    it calls the function preprocess which

"""
# def process_files(directory):
# travese the corpus and process each document
for filename in os.listdir(directory):
    if filename.endswith(" .txt"):
        with open(filename, "r+") as f:
            data = f.read().replace("\n", " ")
            output = data.translate(trans).lower().split()
            sum = sum + len(output)
        words_list = preprocess(filename)
        basic_index[filename] = words_list
        sub = set(words_list)
        bag = bag.union(sub)

        continue
    else:
        continue

inverted_index = {bagi: set(fname for fname, wlist in basic_index.items() if bagi in wlist) for bagi in bag}

average = sum / no_of_docs

# def calculate_tf_doc():
for file, words_list in basic_index.items():
    word_freq = []
    for word in set(words_list):
        with open(file, "r+") as f:
            data = f.read().replace("\n", " ")
            output = data.translate(trans).lower().split()
            stemmer = PorterStemmer()
            output = [stemmer.stem(word) for word in output]
            tf = output.count(word) / (output.count(word) + (k * len(output) / average))
            word_freq.append((word, tf))
    tf_dict[file] = set(word_freq)

# def calculate_idf():
for word, names in inverted_index.items():
    idf_dict[word] = math.log((no_of_docs / len(names)))

# def calculate_tfidf():
for file, words in tf_dict.items():
    tf_idf_list = list()
    for word in words:
        x, y = word
        y = y * idf_dict[x]
        tf_idf_list.append((x, y))
    tf_idf_dict[file] = tf_idf_list

# serialize it and store it so that we dont have to query it again and again
print(len(tf_idf_dict))
#print(tf_idf_dict)
pickle_out = open("tf_idf_dict", "wb")
pickle.dump(tf_idf_dict, pickle_out)
pickle_out.close()

print(len(bag))
pickle_out = open("bag", "wb")
pickle.dump(bag, pickle_out)
pickle_out.close()
#   pickle bag as well since this is used in write
#you have stored the tf_idf for this dataset ..you can call this object from other file
