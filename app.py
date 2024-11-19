# Main application starts here
from flask import Flask, request, render_template
from search_engine import SearchEngine
import os

app = Flask(__name__)
# search_engine = SearchEngine()

# Ensure index exists (build or load)
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) + "/"
CORPUS_DIR = "corpus"
INDEX_FILE = "index.pkl"

search_engine = SearchEngine(BASE_DIR + INDEX_FILE)

if os.path.exists(BASE_DIR + INDEX_FILE):
    # search_engine.load_index(BASE_DIR + INDEX_FILE)
    search_engine.load_index()
else:
    corpus = search_engine.load_corpus(BASE_DIR + CORPUS_DIR)
    search_engine.build_index(corpus)
    search_engine.save_index(BASE_DIR + INDEX_FILE)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form.get("query", "").strip()
        if query:
            results = search_engine.search(query, top_k=5)
            return render_template("results.html", query=query, results=results)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
