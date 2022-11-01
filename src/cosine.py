import os
import math
import json
import nltk
import time
from collections import Counter
import re
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

dic_frecuency = {}


N = 10000

def processWord(word):
        return SnowballStemmer('english').stem(word.lower())
    
def processText(text):
    res = []

    stoplist = r"[\W+\d+_]"
    
    stopWords = set(["the","of"])

    for word in re.split(stoplist,text):
        subw = processWord(word)
        if not subw in stopWords and len(subw)>1:
            res.append(subw)

    for i in res:
        if not i in dic_frecuency:
            dic_frecuency[i]=1
        else:
            dic_frecuency[i]+=1
    
    return list(set(res))
    
def search(query, k):
        global dic_frecuency
        query = processText(query)
        query_length = 0
        directory = "/data/index/"
        score_doc = {}
        dic_doc_len = {}
        for term in query:
                path = directory + term
                if not os.path.isfile(path):
                    pass

                file = open(path)
                ijson = json.load(file)
                df = len(ijson["termfreq"])
                w = math.log10(1 + dic_frecuency[term]) * math.log10(1 + N /df)
                query_length += w*w
                for line in ijson["termfreq"]:
                        tf = int(ijson["termfreq"][line])

                        wd = math.log10(1 + int(tf))

                        if not line in dic_doc_len:
                           dic_doc_len[line] = 0
                        dic_doc_len[line] += wd*wd
                        if not line in score_doc:
                                score_doc[line] = 0
                        
                        score_doc[line] += wd*w
                        

        for doc in score_doc:
                score_doc[doc] = score_doc[doc]/((dic_doc_len[doc]**(1/2))*(query_length**(1/2)))
        ans = dict(sorted(score_doc.items(), key=lambda item: item[1]))
        ans_all = []
    
        for doc in list(reversed(list(ans)))[0:k]:
                docfile = open(doc,"r")
                content = docfile.read()
                ans_all.append({"title": doc, "score": ans[doc], "abstract": content})

        dic_frecuency = {}
        return ans_all
        
