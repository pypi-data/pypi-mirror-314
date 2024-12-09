class Entity(metaclass=type):
    """
    Represents a data entity in the system.
    """

    def __init__(self, entity_id, data, metadata=None):
        self.entity_id = entity_id
        self.data = data
        self.metadata = metadata if metadata else {} 
        