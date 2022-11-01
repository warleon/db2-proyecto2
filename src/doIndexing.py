from invertedIndex import InvertedIndex

def doIndexing():
	dirpath = "/home/luischahua/data/index/"
	datapath = "/home/luischahua/data/arxiv/"
	index = InvertedIndex(dirpath)
	index.index(datapath)

if __name__ == "__main__":
	doIndexing()
	print("indexed arxiv directory")
