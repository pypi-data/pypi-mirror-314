from gatecraft.core.permission import Permission


class Role(metaclass=type):
    """
    Represents a role assigned to users.
    """

    def __init__(self, role_id, name):
        self.role_id = role_id
        self.name = name
        self.permissions = set()

    def add_permission(self, permission):
        if not isinstance(permission, Permission):
            raise TypeError("Expected a Permission instance.")
        self.permissions.add(permission)

    def remove_permission(self, permission):
        self.permissions.discard(permission)

    def get_permissions(self):
        return self.permissions 
    