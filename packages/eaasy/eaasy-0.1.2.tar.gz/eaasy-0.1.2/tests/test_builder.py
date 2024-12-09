from unittest import TestCase
from unittest.mock import MagicMock, patch
from eaasy.extensions import buil_model
from flask_restx import fields, Namespace, Model

class MockProperty:
    def __init__(self, name, type, nullable):
        self.name = name
        self.type = type
        self.nullable = nullable

@patch("builtins.print")
class TestBuilder(TestCase):
    def setUp(self, *_):
        # Create a mock BaseEntity
        self.mock_entity = MagicMock()
        self.mock_entity.__name__ = "TestEntity"
        self.mock_entity.column_list.return_value = [
            MockProperty("id", "INTEGER", False),
            MockProperty("name", "VARCHAR", True),
            MockProperty("email", "VARCHAR", False),
            MockProperty("created_at", "DATETIME", False),
            MockProperty("deleted_at", "DATETIME", True),
            MockProperty("is_active", "BOOLEAN", True),
            MockProperty("unsupported_field", "UNSUPPORTED", True)
        ]

    def test_building_model_returns_expected_namespace(self, *_):
        # Act
        namespace, _ = buil_model(self.mock_entity)

        # Assert
        self.assertIsInstance(namespace, Namespace)
        self.assertEqual(namespace.name, self.mock_entity.__name__)
        self.assertEqual(namespace.description, "TestEntity operations")
        self.assertEqual(namespace.path, "/testentity")

    def test_building_model_returns_expected_properties(self, *_):
        # Act
        _, model = buil_model(self.mock_entity)

        # Assert
        self.assertIsInstance(model, Model)
        self.assertIn("id", model)
        self.assertIn("name", model)
        self.assertIn("created_at", model)
        self.assertIn("is_active", model)

    def test_building_model_returns_expected_integer(self, *_):
        # Act
        _, model = buil_model(self.mock_entity)

        # Assert
        id_field = model["id"]
        self.assertIsInstance(id_field, fields.Integer)
        self.assertTrue(id_field.required)
        self.assertEqual(id_field.default, 0)
        self.assertEqual(id_field.example, 0)

    def test_building_model_returns_expected_nullable_string(self, *_):
        # Act
        _, model = buil_model(self.mock_entity)

        # Assert
        name_field = model["name"]
        self.assertIsInstance(name_field, fields.String)
        self.assertFalse(name_field.required)
        self.assertIsNone(name_field.default)

    def test_building_model_returns_expected_required_string(self, *_):
        # Act
        _, model = buil_model(self.mock_entity)

        # Assert
        email_field = model["email"]
        self.assertIsInstance(email_field, fields.String)
        self.assertTrue(email_field.required)
        self.assertEqual(email_field.default, "")

    def test_building_model_returns_expected_nullable_datetime(self, *_):
        # Act
        _, model = buil_model(self.mock_entity)

        # Assert
        created_at_field = model["deleted_at"]
        self.assertIsInstance(created_at_field, fields.DateTime)
        self.assertFalse(created_at_field.required)
        self.assertIsNone(created_at_field.default)

    def test_building_model_returns_expected_required_datetime(self, *_):
        # Act
        _, model = buil_model(self.mock_entity)

        # Assert
        deleted_at_field = model["created_at"]
        self.assertIsInstance(deleted_at_field, fields.DateTime)
        self.assertTrue(deleted_at_field.required)
        self.assertIsNotNone(deleted_at_field.default)

    def test_building_model_returns_expected_boolean(self, *_):
        # Act
        _, model = buil_model(self.mock_entity)

        # Assert
        is_active_field = model["is_active"]
        self.assertIsInstance(is_active_field, fields.Boolean)
        self.assertFalse(is_active_field.required)
        self.assertEqual(is_active_field.default, False)

    def test_building_model_logs_unsupported_types(self, *_):
        # Act
        _, model = buil_model(self.mock_entity)

        # Assert
        self.assertNotIn("unsupported_field", model)
