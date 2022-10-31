import json 
import os
import re
import nltk
import numpy as np
from nltk.stem.snowball import SnowballStemmer


class InvertedIndex:
	def __init__(self,indexDir):
		nltk.download('punkt')
		self.indexDir = indexDir
		self.stoplist = r"[\W+\d+_]"
		self.stopWords = set(["the","of"])
		self.stemmer = SnowballStemmer('english')
		self.indexPath = os.path.join(indexDir,"index.meta")
		self.N = 0
		if not os.path.exists(self.indexDir):
			os.makedirs(self.indexDir)
		if os.path.exists(self.indexPath):
			ifile = open(self.indexPath,"r")
			ijson = json.load(ifile)
			self.N = ijson["N"]
			ifile.close()
		
	
	def __del__(self):
		ifile = open(self.indexPath,"w")
		json.dump({"N":self.N},ifile)
		ifile.close()


	def processWord(self,word):
		return self.stemmer.stem(word.lower())
	
	def processText(self,text):
		res = []
		for word in re.split(self.stoplist,text):
			if word in self.stopWords:
				continue
			res.append(self.processWord(word))
		return res

		

	def addDocument(self,docPath):
		self.N+=1
		uniqWords = set()
		with open(docPath, "r") as doc:
			for line in doc:
				for pword in self.processText(line):
					if not len(pword):
						continue
					uniqWords.add(pword)
					wpath=os.path.join(self.indexDir,pword)
					winfo = None
					data = {}
					#check if the word was already indxed
					if os.path.exists(wpath):
						winfo = open(wpath, "r") 
						data = json.load(winfo)
					else:
						winfo=open(wpath, "w")
						data["termfreq"] = {}
					#count the tf and df
					if docPath in data:
						data["termfreq"][docPath] += 1
					else:
						data["termfreq"][docPath] = 1

					winfo.close()
					winfo = open(wpath, "w") 
					json.dump(data,winfo)
					winfo.close()
			for uw in uniqWords:
				uwpath=os.path.join(self.indexDir,uw)
				uwfile = open(uwpath, "r") 
				uwjson = json.load(uwfile)
				if "docfreq" in uwjson:
					uwjson["docfreq"] += 1
				else:
					uwjson["docfreq"] = 1
				uwfile.close()
				uwfile = open(uwpath, "w") 
				json.dump(uwjson,uwfile)
				uwfile.close()

	def index(self,dirpath):
		for root, dirs, files in os.walk(dirpath):
			for filename in files:
					self.addDocument(os.path.join(root, filename))
	
	#word being a dictionary with the tf and df and doc being a document path/filename
	def tf_idf(self, word,doc):
		return np.log(1+word["termfreq"][doc])*np.log(self.N/word["docfreq"])

	#Q and doc being dictionaries of word:tfidf
	def cosine_sim(self, Q, Doc):
		words = Q.copy()
		words.update(Doc)
		qNorm=0
		docNorm=0
		s=0
		
		for w in words.keys():
			if w in Q:
				qNorm+=Q[w]*Q[w]
			if w in Doc:
				docNorm+=Doc[w]*Doc[w]
			if w in Q and w in Doc:
				s+= Q[w]*Doc[w]
		qNorm = np.sqrt(qNorm)
		docNorm = np.sqrt(docNorm)
				
		return s/(qNorm*docNorm)

	def docVector(self,doc):
		res = {}
		with open(doc,"r") as dfile:
			for line in dfile:
				for w in self.processText(line):
					if not len(w):
						continue
					wpath=os.path.join(self.indexDir,w)
					#check if the word was already indxed
					if not os.path.exists(wpath):
						continue
					wfile = open(wpath,"r")
					wjson=json.load(wfile)
					res[w]=self.tf_idf(wjson,doc)
					wfile.close()
		return res

	def query(self,text,k):
		q = self.processText(text)
		docs =set()
		for w in q:
			wpath=os.path.join(self.indexDir,w)
			if not os.path.exists(wpath):
				continue
			wfile = open(wpath, 'r')
			wjson = json.load(wfile)
		#build query tf idf
		# retrieve all relevant documents
			docs.update(wjson["termfreq"].keys())
			wfile.close()
		#build docs tf idf
		scores = []
		for doc in docs:
			curr = self.docVector(doc)
			docfile = open(doc,"r")
			content = docfile.read()
			docfile.close()
			Qtfidf = {}
			for w in q:
				Qtfidf[w]=self.tf_idf(wjson,doc)
			scores.append({"score":self.cosine_sim(Qtfidf,curr),"title":doc,"abstract":content})
		
		return sorted(scores, key=lambda k: k['score'] )[:k]


			