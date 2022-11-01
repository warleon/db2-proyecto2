import time
from flask import Flask
from flask import request
from flask import jsonify
import query_postgres
from invertedIndex import InvertedIndex

dirpath = "/data/index/"
index = InvertedIndex(dirpath)

app = Flask(__name__)

@app.route("/query", methods=['POST'])
def query():
    text = request.json["text"]
    k = request.json["topk"]
    start = time.time()
    ranking = index.query(text,int(k))
    end = time.time()
    return jsonify({"items":ranking,"time":end - start})

@app.route("/query_postgres", methods=['POST'])
def postgres_request():
    text = request.json["text"]
    k = request.json["topk"]
    response = jsonify(query_postgres.TopK_answer(text, int(k)))
    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)