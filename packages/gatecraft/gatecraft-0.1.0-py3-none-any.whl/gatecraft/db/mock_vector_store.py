from gatecraft.db.vector_store_interface import VectorStoreInterface
import numpy as np


class MockVectorStore(VectorStoreInterface):
    """
    Mock vector store for demonstration purposes.
    """

    def embed(self, data):
        # Mock embedding: Convert string data to a vector of ASCII values
        return np.array([ord(char) for char in data]).astype(float)

    def similarity(self, vector1, vector2):
        # Compute cosine similarity
        if len(vector1) == 0 or len(vector2) == 0:
            return 0.0
        dot_product = np.dot(vector1, vector2)
        norm_a = np.linalg.norm(vector1)
        norm_b = np.linalg.norm(vector2)
        return dot_product / (norm_a * norm_b) 
    