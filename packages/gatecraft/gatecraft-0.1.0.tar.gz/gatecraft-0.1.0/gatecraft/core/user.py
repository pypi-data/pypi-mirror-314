from gatecraft.core.role import Role


class User(metaclass=type):
    """
    Represents a user in the RBAC system.
    """

    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.roles = set()

    def add_role(self, role):
        if not isinstance(role, Role):
            raise TypeError("Expected a Role instance.")
        self.roles.add(role)

    def remove_role(self, role):
        self.roles.discard(role)

    def get_roles(self):
        return self.roles 
    