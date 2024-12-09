class Condition(metaclass=type):
    """
    Abstract base class for conditions.
    """

    def evaluate(self, user, entity, database):
        raise NotImplementedError("evaluate method must be implemented.") 
    