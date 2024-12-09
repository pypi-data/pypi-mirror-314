import unittest
from semantic_rbac.core.user import User
from semantic_rbac.core.role import Role
from semantic_rbac.core.permission import Permission

class TestCore(unittest.TestCase):

    def test_user_role_assignment(self):
        user = User(user_id=1, name='Test User')
        role = Role(role_id=1, name='Test Role')
        user.add_role(role)
        self.assertIn(role, user.get_roles())

    def test_role_permission_assignment(self):
        role = Role(role_id=1, name='Test Role')
        permission = Permission(permission_id=1, name='Test Permission')
        role.add_permission(permission)
        self.assertIn(permission, role.get_permissions())

if __name__ == '__main__':
    unittest.main() 
    