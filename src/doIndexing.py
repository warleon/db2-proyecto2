from invertedIndex import InvertedIndex

def doIndexing():
	dirpath = "/data/index/"
	datapath = "/data/arxiv/"
	index = InvertedIndex(dirpath)
	index.index(datapath)

if __name__ == "__main__":
	doIndexing()
	print("indexed arxiv directory")
