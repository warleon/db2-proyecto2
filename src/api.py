from flask import Flask
from flask import request
from flask import jsonify

#todo set the index to the implementation of InvertedIndex
index = None

app = Flask(__name__)

@app.route("/query")
def query():
    text = request.form['query']
    ranking = index.processQuery(text)
    return jsonify(ranking)
