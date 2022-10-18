from invertedIndex import InvertedIndex


if __name__ == '__main__':
    index = InvertedIndex("/data/index")
    index.addDocument("/data/arxiv-metadata-oai-snapshot.json")