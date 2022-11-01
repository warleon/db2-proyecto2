import os
import math

import nltk

from collections import Counter

from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer('english')

def process(texto):
    #re.sub('[^A-Za-z0-9]+', ' ', texto )
  # tokenizar
    palabras = nltk.word_tokenize(texto.lower())
  # crear el stoplis
    stoplist = []
    stoplist = stopwords.words('english')
    stoplist += [',', '!', '.', '?', '-', ';','"','¿',')','(','[',']']
    
    palabras_limpias = []
    for token in palabras:
       if token not in stoplist:
           palabras_limpias.append(token)

    stemmer = SnowballStemmer('english')
    for i in range(len(palabras_limpias)):
        palabras_limpias[i] = stemmer.stem(palabras_limpias[i])
    
    return Counter(palabras_limpias)

N = 50_000

def search(Q, k):
        query = process(Q)

        query_length = 0
        directory = "../indexes/"
        score_doc = {}
        dic_doc_len = {}
        for term in query:
                
                path = directory + term + ".txt"
                ##print(path)
                #print("estaaaaaa")
                if not os.path.isfile(path):
                        pass

                file = open(path)
                df = len(open(path).readlines())
                w = math.log10(1 + query[term]) * math.log10(1 + N /df)
                query_length += w*w
                cnt=0
                score_doc_1 = {}
                
                i=0
                for line in file.readlines():
                        cnt+=1
                        line = line.split(",")

                        document = line[0]
                        tf = line[1]
                        title = line[2:]
                        title = ''.join(title).rstrip()
                        wd = math.log10(1 + int(tf))

                        if not title in dic_doc_len:
                           dic_doc_len[title] = 0
                        dic_doc_len[title] += wd*wd
                        if not title in score_doc:
                                score_doc[title] = 0
                        
                        score_doc[title] += wd*w
                        

        for doc in score_doc:

                score_doc[doc] = score_doc[doc]/((dic_doc_len[doc]**(1/2))*(query_length**(1/2)))
        ans = dict(sorted(score_doc.items(), key=lambda item: item[1]))

        v = []
        for doc in list(reversed(list(ans)))[0:k]:
                v.append({"title": doc, "score": ans[doc]})

        
        return {"data": v}