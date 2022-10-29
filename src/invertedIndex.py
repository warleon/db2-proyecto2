import json 
import os

import nltk
import numpy as np
from nltk.stem.snowball import SnowballStemmer


class InvertedIndex:
	def __init__(self,indexDir):
		nltk.download('punkt')
		self.indexDir = indexDir
		self.stoplist = [',', '!', '.', '?', '-', ';','"','¿',')','(','[',']',' ']
		self.stopWords = set(["the","of"])
		self.stemmer = SnowballStemmer('english')

	def processWord(self,word):
		return self.stemmer.stem(word.lower())
	
	def processText(self,text):
		res = []
		for word in text.split(self.stoplist):
			if word in self.stopWords:
				continue
			res.append(processWord(self,word))
		return res

		

	def addDocument(self,docPath):
		with open(docPath, "r") as doc:
			for line in doc:
				for pword in processText(self,line):
					wpath=os.path.join(self.indexDir,pword)
					winfo = None
					data = {}
					#check if the word was already indxed
					if os.path.exists(wpath):
						winfo = open(wpath, "rw") 
						data = json.load(winfo)
					else:
						winfo=open(wpath, "w")
						data["docfreq"] = 0
					#count the tf and df
					if docPath in data:
						data[docPath] += 1
					else:
						data[docPath] = 1
						data["docfreq"] += 1

					json.dump(data,winfo)

	def index(self,dirpath):
		for filename in os.listdir(directory):
	 		addDocument(self,filename):

	def query(self,text):
		q = processText(self,text)
		for w in q:
			wpath=os.path.join(self.indexDir,w)
			if not os.path.exists(wpath):
				continue
	
