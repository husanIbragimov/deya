from django.test import TestCase
from drf_spectacular.generators import SchemaGenerator


class CustomAutoSchemaChoicesDescriptionTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.schema = SchemaGenerator().get_schema(request=None, public=True)

    def test_create_endpoint_lists_choice_field_options_in_description(self):
        operation = self.schema["paths"]["/api/v1/admin/user/create/"]["post"]

        self.assertIn("role", operation["description"])
        self.assertIn("0 -", operation["description"])
        self.assertIn("1 -", operation["description"])

    def test_list_endpoint_does_not_repeat_choices_in_description(self):
        list_create_path = self.schema["paths"].get("/api/v1/admin/catalog/weights/")
        if list_create_path is None or "get" not in list_create_path:
            self.skipTest("weight admin list endpoint not present in schema")

        description = list_create_path["get"].get("description") or ""
        self.assertNotIn("Available choices", description)
