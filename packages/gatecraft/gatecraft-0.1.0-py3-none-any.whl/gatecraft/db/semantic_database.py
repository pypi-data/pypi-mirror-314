class SemanticDatabase(metaclass=type):
    """
    Manages semantic operations using the vector store.
    """

    def __init__(self, vector_store, similarity_threshold=0.85):
        self.vector_store = vector_store
        self.similarity_threshold = similarity_threshold

    def get_embedding(self, data):
        return self.vector_store.embed(data)

    def compute_similarity(self, embedding1, embedding2):
        return self.vector_store.similarity(embedding1, embedding2)

    def store_embedding(self, id, embedding):
        return self.vector_store.upsert(id, embedding)

    def query_similar(self, embedding, top_k=1):
        matches = self.vector_store.query(embedding, top_k)
        # Filter matches based on similarity threshold
        filtered_matches = [
            {'id': match.id, 'score': match.score}
            for match in matches if match.score >= self.similarity_threshold
        ]
        return filtered_matches
    