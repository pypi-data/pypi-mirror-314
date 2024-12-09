class VectorStoreInterface(metaclass=type):
    """
    Interface for vector store implementations.
    """

    def embed(self, data):
        raise NotImplementedError("embed method must be implemented.")

    def similarity(self, vector1, vector2):
        raise NotImplementedError("similarity method must be implemented.") 
    