import json 
import os


class InvertedIndex:
	def __init__(self,indexDir):
		self.indexDir = indexDir

	def processWord(self,word):
		#TODO the preprocessing 
		return word

	def indexDocument(self,docPath):
		#TODO improve this shit
		with open(docPath, "r") as doc:
			for line in doc:
        for word in line.split(" "):
					pword = processWord(word)
					wpath=os.path.join(self.indexDir,pword)
					winfo = None
					data = {}
					if os.path.exists(wpath):
						winfo = open(wpath, "rw") 
						data = json.load(winfo)
						data[pword][docPath] += 1
					else:
						winfo=open(wpath, "w")
						data[pword]={}
						data[pword][docPath] = 1

					json.dump(data,winfo)

	
