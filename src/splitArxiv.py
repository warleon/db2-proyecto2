import ijson
import os


jsonPath = "/data/arxiv-metadata-oai-snapshot.json"
dirPath = "/data/arxiv"

if not os.path.exists(dirPath):
    os.makedirs(dirPath)

file = open(jsonPath)
parser = ijson.parse(file,multiple_values=True)

inAbstract,inId = False,False
id,abstract = "",""
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
