import json, os
import csv

import ijson

jsonPath = "/data/arxiv-metadata-oai-snapshot.json"
dirPath = "/data/arxiv"
dirCSV ='/data/papers_arxiv.csv'


def separateArxiv():
	file = open(jsonPath)
	parser = ijson.parse(file,multiple_values=True)

	inAbstract,inId = False,False
	id,abstract = "",""
	count=0
	for prefix, event, value in parser:
		if event=="map_key" and value == "title":
			p,e,v = next(parser)
			id = v
		elif (event=="map_key" and value == "abstract"):
			p,e,v = next(parser)
			abstract = v
		
		if len(id) and len(abstract):
			path = os.path.join(dirPath,id)
			with open(path,"w") as f:
				f.write(abstract)
			id,abstract = "",""
			count+=1
		if count >=100:
			break
def  createCSV():
	field_names = ['id','abstract']

	j = open(dirCSV,'w')
	writer = csv.writer(j)
	writer.writerow(field_names)
	j.close()
	for filename in os.listdir(dirPath):
			f = os.path.join(dirPath, filename)
			id1 = filename

			f2 = open(f,'r')
			abstract1 = f2.read()
			with open(dirCSV, 'a') as csv_file:
					dict_object = csv.DictWriter(csv_file, fieldnames=field_names) 
					dict_object.writerow({'id':id1,'abstract':abstract1})

if __name__=="__main__":
	if not os.path.exists(dirPath):
			os.makedirs(dirPath)
			separateArxiv()
	if not os.path.exists(dirCSV):
		createCSV()