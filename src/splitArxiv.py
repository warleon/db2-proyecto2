import json, os
import ijson

jsonPath = "/data/arxiv-metadata-oai-snapshot.json"
dirPath = "/data/arxiv"

if not os.path.exists(dirPath):
    os.makedirs(dirPath)

file = open(jsonPath)
parser = ijson.parse(file,multiple_values=True)

inAbstract,inId = False,False
id,abstract = "",""
count=0
for prefix, event, value in parser:
	if event=="map_key" and value == "id":
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
#chahua indexing :v
"""
import pandas as pd
import csv
jsonPath = "/home/luischahua/data/arxiv-metadata-oai-snapshot.json"
dirPath = "/home/luischahua/data/arxiv"


dirPath = "/home/luischahua/data/arxiv"
dirCSV ='/home/luischahua/papers_arxiv.csv'
field_names = ['id','abstract']
dataframe = pd.DataFrame(list())
dataframe.to_csv(dirCSV)

j = open(dirCSV,'w')
writer = csv.writer(j)
writer.writerow(field_names)
j.close()
for filename in os.listdir(dirPath):
    f = os.path.join(dirPath, filename)
    f1 = str(f)
    id1 = f1[-9:]

    f2 = open(f,'r')
    abstract1 = f2.read()
    with open(dirCSV, 'a') as csv_file:
        dict_object = csv.DictWriter(csv_file, fieldnames=field_names) 
        dict_object.writerow({'id':id1,'abstract':abstract1})
"""