import pinecone
import openai
import numpy as np
from gatecraft.db.vector_store_interface import VectorStoreInterface


class PineconeVectorStore(VectorStoreInterface):
    """
    Vector store implementation using Pinecone.
    """

    def __init__(self, api_key, environment, index_name):
        # Create an instance of the Pinecone client
        self.pinecone_client = pinecone.Pinecone(api_key=api_key)

        # Set the index name
        self.index_name = index_name

        # Check if the index exists
        existing_indexes = self.pinecone_client.list_indexes().names()
        if self.index_name not in existing_indexes:
            # Create a new index if it doesn't exist
            self.pinecone_client.create_index(
                name=self.index_name,
                dimension=1536,  # OpenAI's embedding dimension is 1536
                metric='cosine',
                spec=pinecone.ServerlessSpec(
                    cloud='aws',
                    region=environment
                )
            )
        self.index = self.pinecone_client.Index(self.index_name)

    def embed(self, data):
        # Generate embeddings using OpenAI
        response = openai.Embedding.create(
            input=[data],
            engine='text-embedding-ada-002'
        )
        embedding = response['data'][0]['embedding']
        return np.array(embedding)

    def upsert(self, id, vector):
        # Upsert the vector into Pinecone
        self.index.upsert(vectors=[(str(id), vector.tolist())])

    def similarity(self, vector1, vector2):
        # Compute cosine similarity between two vectors
        if np.linalg.norm(vector1) == 0 or np.linalg.norm(vector2) == 0:
            return 0.0
        dot_product = np.dot(vector1, vector2)
        norm_product = np.linalg.norm(vector1) * np.linalg.norm(vector2)
        return dot_product / norm_product

    def query(self, vector, top_k=1):
        # Query Pinecone for the most similar vectors
        response = self.index.query(
            vector=vector.tolist(),
            top_k=top_k,
            include_values=False,
            include_metadata=False
        )
        return response.matches

    def describe_index_stats(self):
        """Get statistics about the Pinecone index"""
        return self.index.describe_index_stats()
  