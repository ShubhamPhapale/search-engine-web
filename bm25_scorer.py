import math

class BM25Scorer:
    def __init__(self, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.doc_lengths = []
        self.avg_doc_length = 0
        self.inverted_index = {}

    def build_index(self, corpus):
        total_length = 0
        for doc_id, doc in enumerate(corpus):
            doc_length = len(doc)
            self.doc_lengths.append(doc_length)
            total_length += doc_length
            for term in doc:
                if term not in self.inverted_index:
                    self.inverted_index[term] = {}
                if doc_id not in self.inverted_index[term]:
                    self.inverted_index[term][doc_id] = 0
                self.inverted_index[term][doc_id] += 1
        self.avg_doc_length = total_length / len(corpus)

    def score(self, query, doc_id):
        score = 0
        for term in query:
            if term in self.inverted_index:
                n_t = len(self.inverted_index[term])
                f_t_d = self.inverted_index[term].get(doc_id, 0)
                idf = math.log((len(self.doc_lengths) - n_t + 0.5) / (n_t + 0.5) + 1)
                numerator = f_t_d * (self.k1 + 1)
                denominator = f_t_d + self.k1 * (1 - self.b + self.b * (self.doc_lengths[doc_id] / self.avg_doc_length))
                score += idf * (numerator / denominator)
        return score
