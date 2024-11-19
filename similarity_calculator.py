from sklearn.metrics.pairwise import cosine_similarity

class SimilarityCalculator:
    @staticmethod
    def calculate_similarity(tfidf_matrix, query_vector):
        # Compute cosine similarity
        similarities = cosine_similarity(query_vector, tfidf_matrix)
        return similarities[0]  # Return similarity scores for the query
