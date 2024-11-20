from flask import Flask, render_template, request, send_from_directory
from search_engine import SearchEngine
import os

app = Flask(__name__)

# Ensure index exists (build or load)
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) + "/"
CORPUS_DIR = "corpus"
INDEX_FILE = "index.pkl"

search_engine = SearchEngine(BASE_DIR + INDEX_FILE)

# Check if index exists or if it needs to be built
if os.path.exists(BASE_DIR + INDEX_FILE):
    search_engine.load_index()
else:
    corpus, files = search_engine.load_corpus(BASE_DIR + CORPUS_DIR)
    search_engine.build_index(corpus)
    search_engine.save_index()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form["query"]
        results = search_engine.search(query)
        corpus, files = search_engine.load_corpus(BASE_DIR + CORPUS_DIR)

        # Format and enumerate results in Python
        formatted_results = [
            {
                "rank": rank,
                "doc_name": files[doc_id],
                "score": score,
            }
            for rank, (doc_id, score) in enumerate(results[:5], start=1)
        ]

        return render_template("results.html", query=query, results=formatted_results)
    return render_template("index.html")

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(BASE_DIR + CORPUS_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))  # Default to 5001 if PORT is not set
    app.run(host="0.0.0.0", port=port, debug=True)
