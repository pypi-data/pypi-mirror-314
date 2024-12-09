class Permission(metaclass=type):
    """
    Represents a permission with associated conditions.
    """

    def __init__(self, permission_id, name, conditions=None):
        self.permission_id = permission_id
        self.name = name
        self.conditions = conditions if conditions else []

    def add_condition(self, condition):
        self.conditions.append(condition)

    def get_conditions(self):
        return self.conditions 
    