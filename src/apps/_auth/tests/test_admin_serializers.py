from django.test import TestCase

from apps._auth.models import User
from apps._auth.serializers.admin import UserAdminCreateSerializer
from apps.common.choices import UserRoleChoice


class UserAdminCreateSerializerTests(TestCase):
    def valid_payload(self, **overrides):
        payload = {
            "first_name": "Aziz",
            "last_name": "Karimov",
            "username": "aziz.karimov",
            "password": "Sup3r-Secret-Pass",
        }
        payload.update(overrides)
        return payload

    def test_create_hashes_password_and_sets_created_by(self):
        creator = User.objects.create_user(username="creator", password="pass12345")
        serializer = UserAdminCreateSerializer(data=self.valid_payload())
        self.assertTrue(serializer.is_valid(), serializer.errors)

        instance = serializer.save(created_by=creator)

        self.assertEqual(instance.username, "aziz.karimov")
        self.assertEqual(instance.first_name, "Aziz")
        self.assertEqual(instance.last_name, "Karimov")
        self.assertEqual(instance.role, UserRoleChoice.USER)
        self.assertEqual(instance.created_by, creator)
        self.assertTrue(instance.check_password("Sup3r-Secret-Pass"))

    def test_password_is_write_only(self):
        serializer = UserAdminCreateSerializer(data=self.valid_payload())
        self.assertTrue(serializer.is_valid(), serializer.errors)
        instance = serializer.save()
        self.assertNotIn("password", UserAdminCreateSerializer(instance).data)

    def test_explicit_role_is_respected(self):
        serializer = UserAdminCreateSerializer(data=self.valid_payload(role=UserRoleChoice.ADMIN))
        self.assertTrue(serializer.is_valid(), serializer.errors)
        instance = serializer.save()
        self.assertEqual(instance.role, UserRoleChoice.ADMIN)
        self.assertFalse(instance.is_staff)

    def test_duplicate_username_rejected(self):
        User.objects.create_user(username="aziz.karimov", password="pass12345")
        serializer = UserAdminCreateSerializer(data=self.valid_payload())
        self.assertFalse(serializer.is_valid())
        self.assertIn("username", serializer.errors)

    def test_weak_numeric_password_rejected(self):
        serializer = UserAdminCreateSerializer(data=self.valid_payload(password="12345678"))
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)

    def test_missing_first_name_rejected(self):
        payload = self.valid_payload()
        del payload["first_name"]
        serializer = UserAdminCreateSerializer(data=payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn("first_name", serializer.errors)

    def test_missing_last_name_rejected(self):
        payload = self.valid_payload()
        del payload["last_name"]
        serializer = UserAdminCreateSerializer(data=payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn("last_name", serializer.errors)
