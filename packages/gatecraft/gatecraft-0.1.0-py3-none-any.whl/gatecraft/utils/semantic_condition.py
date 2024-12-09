from gatecraft.utils.conditions import Condition


class SemanticCondition(Condition):
    """
    Condition that evaluates based on semantic similarity.
    When inverse=False (default): Returns True if similarity >= threshold
    When inverse=True: Returns True if similarity < threshold
    """

    def __init__(self, term, threshold=0.8, inverse=False):
        self.term = term
        self.threshold = threshold
        self.inverse = inverse
        self.term_embedding = None

    def evaluate(self, user, entity, database):
        # Get or create term embedding
        if self.term_embedding is None:
            self.term_embedding = database.get_embedding(self.term)

        # Get entity embedding
        entity_embedding = database.get_embedding(entity.data)

        # Calculate similarity
        similarity = database.compute_similarity(self.term_embedding, entity_embedding)

        # For inverse conditions, return True when similarity is below threshold
        # For regular conditions, return True when similarity is above threshold
        return similarity < self.threshold if self.inverse else similarity >= self.threshold
    