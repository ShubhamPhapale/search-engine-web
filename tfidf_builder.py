from sklearn.feature_extraction.text import TfidfVectorizer

class TFIDFBuilder:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def fit_transform(self, corpus):
        # Transform corpus to TF-IDF matrix
        tfidf_matrix = self.vectorizer.fit_transform(corpus)
        return tfidf_matrix

    def transform(self, query):
        # Transform a single query
        return self.vectorizer.transform([query])

    def get_feature_names(self):
        # Return feature names (vocabulary)
        return self.vectorizer.get_feature_names_out()
