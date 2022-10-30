from flask import Flask
from flask import request
from flask import jsonify
import query_postgres
#todo set the index to the implementation of InvertedIndex
index = None

app = Flask(__name__)

@app.route("/query")
def query():
    text = request.form['query']
    ranking = index.processQuery(text)
    return jsonify(ranking)

@app.route("/query_postgres/<query>/<k>", methods=['GET'])
def postgres_request(query, k):
    response = jsonify(query_postgres.TopK_answer(query, int(k)))
    return response