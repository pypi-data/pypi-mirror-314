import unittest
from semantic_rbac.core.user import User
from semantic_rbac.core.role import Role
from semantic_rbac.core.permission import Permission
from semantic_rbac.core.entity import Entity
from semantic_rbac.core.policy import AccessControlPolicy
from semantic_rbac.utils.semantic_condition import SemanticCondition
from semantic_rbac.db.semantic_database import SemanticDatabase
from semantic_rbac.db.mock_vector_store import MockVectorStore

class TestPolicy(unittest.TestCase):

    def setUp(self):
        vector_store = MockVectorStore()
        self.semantic_db = SemanticDatabase(vector_store)
        self.policy = AccessControlPolicy(database=self.semantic_db)

        # Users
        self.user = User(user_id=1, name='Test User')

        # Roles
        self.role = Role(role_id=1, name='Test Role')

        # Permissions
        self.permission = Permission(permission_id=1, name='Test Permission')
        condition = SemanticCondition(term='test', threshold=0.5)
        self.permission.add_condition(condition)

        # Assign permissions and roles
        self.role.add_permission(self.permission)
        self.user.add_role(self.role)

        # Entities
        self.entity = Entity(entity_id=1, data='This is a test entity.')

    def test_access_allowed(self):
        allowed = self.policy.is_access_allowed(self.user, self.entity)
        self.assertTrue(allowed)

    def test_regular_condition(self):
        # Setup
        user = User(1, "test_user")
        role = Role(1, "test_role")
        permission = Permission(1, "test_permission")
        
        # Add regular condition - allow cat-related content
        condition = SemanticCondition("cat", threshold=0.7, inverse=False)
        permission.add_condition(condition)
        role.add_permission(permission)
        user.add_role(role)

        # Test
        cat_entity = Entity(1, "A cute cat playing with yarn")
        dog_entity = Entity(2, "A dog chasing a ball")
        
        self.assertTrue(self.policy.is_access_allowed(user, cat_entity))
        self.assertFalse(self.policy.is_access_allowed(user, dog_entity))

    def test_inverse_condition(self):
        # Setup
        user = User(1, "test_user")
        role = Role(1, "test_role")
        permission = Permission(1, "test_permission")
        
        # Add inverse condition - block violent content
        condition = SemanticCondition("violent", threshold=0.7, inverse=True)
        permission.add_condition(condition)
        role.add_permission(permission)
        user.add_role(role)

        # Test
        safe_entity = Entity(1, "A peaceful day in the park")
        violent_entity = Entity(2, "A violent fight broke out")
        
        self.assertTrue(self.policy.is_access_allowed(user, safe_entity))
        self.assertFalse(self.policy.is_access_allowed(user, violent_entity))

    def test_multiple_inverse_conditions(self):
        # Setup
        user = User(1, "test_user")
        role = Role(1, "test_role")
        permission = Permission(1, "test_permission")
        
        # Block both violent and adult content
        permission.add_condition(SemanticCondition("violent", threshold=0.7, inverse=True))
        permission.add_condition(SemanticCondition("adult", threshold=0.7, inverse=True))
        role.add_permission(permission)
        user.add_role(role)

        # Test
        safe_entity = Entity(1, "A children's book about friendship")
        violent_entity = Entity(2, "A violent action movie")
        adult_entity = Entity(3, "Adult content warning")
        
        self.assertTrue(self.policy.is_access_allowed(user, safe_entity))
        self.assertFalse(self.policy.is_access_allowed(user, violent_entity))
        self.assertFalse(self.policy.is_access_allowed(user, adult_entity))

    def test_inverse_cat_access(self):
        # Setup user with access to everything except cats
        user = User(user_id=2, name='Bob')
        role = Role(role_id=2, name='Everything Except Cats')
        permission = Permission(permission_id=2, name='Access All Except Cats')
        
        # Create inverse condition for cats
        condition = SemanticCondition(term='cat', threshold=0.7, inverse=True)
        permission.add_condition(condition)
        role.add_permission(permission)
        user.add_role(role)
        
        # Test with cat content
        cat_entity = Entity(entity_id=2, data='A cute cat playing with yarn')
        allowed = self.policy.is_access_allowed(user, cat_entity)
        self.assertFalse(allowed)
        
        # Test with non-cat content
        dog_entity = Entity(entity_id=3, data='A dog playing in the park')
        allowed = self.policy.is_access_allowed(user, dog_entity)
        self.assertTrue(allowed)

if __name__ == '__main__':
    unittest.main() 
    