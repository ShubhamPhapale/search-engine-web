import os
import pickle
from bm25_scorer import BM25Scorer
from preprocessor import Preprocessor

class SearchEngine:
    def __init__(self, index_file_path="index.pkl"):
        self.preprocessor = Preprocessor()
        self.bm25_scorer = BM25Scorer()
        self.index_file_path = index_file_path

    def load_corpus(self, folder_path):
        """
        Load a domain-specific corpus from a folder of text files.
        Each text file in the folder represents one document.
        """
        corpus = []
        try:
            # List all files in the directory
            files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
            print(files)
            # Read each file in the folder
            for file_name in files:
                file_path = os.path.join(folder_path, file_name)
                # print("path : ", file_path)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    # Read the content of the file and strip leading/trailing whitespace
                    content = file.read().strip()
                    if content:
                        corpus.append(content)
            
            print(f"Loaded {len(corpus)} documents from {folder_path}.")
            return corpus, files
        
        except FileNotFoundError:
            print(f"Error: Folder not found at {folder_path}. Please provide a valid folder path.")
            return []
        except Exception as e:
            print(f"Error loading corpus: {e}")
            return []

    def build_index(self, corpus):
        # Check if index exists
        if os.path.exists(self.index_file_path):
            print("Index file found. Loading index...")
            self.load_index()
        else:
            print("Index file not found. Generating new index...")
            preprocessed_corpus = [self.preprocessor.clean_text(doc).split() for doc in corpus]
            self.bm25_scorer.build_index(preprocessed_corpus)
            self.save_index()

    def save_index(self):
        """Save the generated index to a file using pickle."""
        with open(self.index_file_path, 'wb') as f:
            pickle.dump(self.bm25_scorer, f)
        print(f"Index saved to {self.index_file_path}.")

    def load_index(self):
        """Load the index from the file."""
        with open(self.index_file_path, 'rb') as f:
            self.bm25_scorer = pickle.load(f)
        print(f"Index loaded from {self.index_file_path}.")

    def search(self, query, top_k=10):
        preprocessed_query = self.preprocessor.clean_text(query).split()
        scores = [
            (doc_id, self.bm25_scorer.score(preprocessed_query, doc_id))
            for doc_id in range(len(self.bm25_scorer.doc_lengths))
        ]
        return sorted(scores, key=lambda x: x[1], reverse=True)[:top_k]
