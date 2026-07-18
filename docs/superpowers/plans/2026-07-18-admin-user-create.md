# Admin User Create API Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `POST /api/v1/admin/user/create/` endpoint that lets an admin (`role == UserRoleChoice.ADMIN`) create a new user by submitting first name, last name, username, and password.

**Architecture:** Follows the existing admin-CRUD pattern in this codebase (`apps/common/base_api.py` + per-app `views/admin/` + `serializers/admin/` + `admin/<app>/` URL namespace, as used by `catalog`, `blog`, etc.), but built on plain `BaseGenericAPI` instead of `AdminListCreateAPI` since this is create-only. A new `IsAdminRole` permission checks the domain `role` field rather than Django's `is_staff`, deliberately independent of `is_staff`-gated admin endpoints elsewhere.

**Tech Stack:** Django 5.2, Django REST Framework, `djangorestframework_simplejwt` (existing auth), drf-spectacular (`@extend_schema`), Django's `AUTH_PASSWORD_VALIDATORS`.

## Global Constraints

- All Django code lives under `src/`; every command below is run with `python src/manage.py ...` from the repo root, or `python manage.py ...` from inside `src/`.
- No new model fields or migrations — this plan only adds a serializer, a permission, a view, and URL wiring. Do not run `makemigrations`.
- Line length 120, follow `black`/`isort`/`flake8` conventions already enforced by `.pre-commit-config.yaml`.
- Password is hashed via `User.objects.create_user(...)` (never store/return it raw) and validated against `AUTH_PASSWORD_VALIDATORS` (`src/config/settings/middleware.py:13-26`).
- New `role=ADMIN` users created via this endpoint must NOT have `is_staff` auto-set — `role` and `is_staff` stay independent (confirmed design decision, see `docs/superpowers/specs/2026-07-18-admin-user-create-design.md`).
- Test command: `python src/manage.py test <label> --exclude-tag=dev-mode` (this is also the pre-commit `django-test` hook — it must pass before any commit succeeds).

---

## File Structure

- **Create** `src/apps/_auth/serializers/admin/__init__.py` — exports `UserAdminCreateSerializer`.
- **Create** `src/apps/_auth/serializers/admin/user_admin_serializer.py` — `UserAdminCreateSerializer`, validates input and hashes the password on create.
- **Create** `src/apps/_auth/tests/__init__.py` — `_auth` has no `tests/` package yet.
- **Create** `src/apps/_auth/tests/test_admin_serializers.py` — direct (non-HTTP) tests for `UserAdminCreateSerializer`.
- **Create** `src/apps/common/permissions/is_admin_role.py` — `IsAdminRole` permission class.
- **Modify** `src/apps/common/permissions/__init__.py` — export `IsAdminRole`.
- **Create** `src/apps/_auth/tests/test_permissions.py` — direct (non-HTTP, no DB) tests for `IsAdminRole`.
- **Create** `src/apps/_auth/views/admin/__init__.py` — exports `UserAdminCreateView`.
- **Create** `src/apps/_auth/views/admin/user_admin_view.py` — `UserAdminCreateView`.
- **Create** `src/apps/_auth/urls/user_admin_urls.py` — mounts `UserAdminCreateView` at `create/`.
- **Modify** `src/apps/v1.py` — add the `admin/user/` include, namespaced `user-admin`.
- **Create** `src/apps/_auth/tests/test_admin_views.py` — end-to-end HTTP tests (permission + creation + validation) via `APITestCase`.

---

### Task 1: `UserAdminCreateSerializer`

**Files:**
- Create: `src/apps/_auth/serializers/admin/user_admin_serializer.py`
- Create: `src/apps/_auth/serializers/admin/__init__.py`
- Test: `src/apps/_auth/tests/test_admin_serializers.py`
- Create: `src/apps/_auth/tests/__init__.py`

**Interfaces:**
- Consumes: `apps._auth.models.User` (existing — fields `username`, `first_name`, `last_name`, `password`, `role`, `date_joined`, plus `BaseModel`'s `created_by`); `apps._auth.managers.user_manager.UserManager.create_user(username, password=None, **extra_fields)` (existing).
- Produces: `apps._auth.serializers.admin.UserAdminCreateSerializer` — a `ModelSerializer` with fields `id, username, first_name, last_name, password (write_only), role, date_joined`. `.save(created_by=<User>)` returns a `User` instance with a hashed password. Task 3's view imports this as `from apps._auth.serializers.admin import UserAdminCreateSerializer`.

- [ ] **Step 1: Write the failing tests**

Create `src/apps/_auth/tests/__init__.py` (empty file).

Create `src/apps/_auth/tests/test_admin_serializers.py`:

```python
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
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python src/manage.py test apps._auth.tests.test_admin_serializers --exclude-tag=dev-mode -v 2`
Expected: FAIL/ERROR — `ModuleNotFoundError: No module named 'apps._auth.serializers.admin'`.

- [ ] **Step 3: Implement the serializer**

Create `src/apps/_auth/serializers/admin/__init__.py`:

```python
from .user_admin_serializer import UserAdminCreateSerializer

__all__ = ["UserAdminCreateSerializer"]
```

Create `src/apps/_auth/serializers/admin/user_admin_serializer.py`:

```python
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps._auth.models import User


class UserAdminCreateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True, allow_blank=False, max_length=150)
    last_name = serializers.CharField(required=True, allow_blank=False, max_length=150)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "password", "role", "date_joined"]
        read_only_fields = ["id", "date_joined"]

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        return User.objects.create_user(password=password, **validated_data)
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python src/manage.py test apps._auth.tests.test_admin_serializers --exclude-tag=dev-mode -v 2`
Expected: PASS (7 tests).

- [ ] **Step 5: Commit**

```bash
git add src/apps/_auth/serializers/admin/__init__.py src/apps/_auth/serializers/admin/user_admin_serializer.py src/apps/_auth/tests/__init__.py src/apps/_auth/tests/test_admin_serializers.py
git commit -m "feat(_auth): add UserAdminCreateSerializer for admin user creation"
```

---

### Task 2: `IsAdminRole` permission

**Files:**
- Create: `src/apps/common/permissions/is_admin_role.py`
- Modify: `src/apps/common/permissions/__init__.py`
- Test: `src/apps/_auth/tests/test_permissions.py`

**Interfaces:**
- Consumes: `apps.common.choices.UserRoleChoice` (existing — `ADMIN = 0`, `USER = 1`); `apps._auth.models.User.role` (existing field).
- Produces: `apps.common.permissions.IsAdminRole` — a DRF `BasePermission` subclass with `has_permission(self, request, view) -> bool`, `True` only when `request.user` is authenticated and `request.user.role == UserRoleChoice.ADMIN`. Task 3's view imports this as `from apps.common.permissions import IsAdminRole`.

- [ ] **Step 1: Write the failing test**

Create `src/apps/_auth/tests/test_permissions.py`:

```python
from types import SimpleNamespace

from django.contrib.auth.models import AnonymousUser
from django.test import SimpleTestCase

from apps._auth.models import User
from apps.common.choices import UserRoleChoice
from apps.common.permissions import IsAdminRole


class IsAdminRoleTests(SimpleTestCase):
    def setUp(self):
        self.permission = IsAdminRole()

    def _request_for(self, user):
        return SimpleNamespace(user=user)

    def test_admin_role_user_has_permission(self):
        user = User(username="admin", role=UserRoleChoice.ADMIN)
        self.assertTrue(self.permission.has_permission(self._request_for(user), None))

    def test_regular_role_user_denied(self):
        user = User(username="regular", role=UserRoleChoice.USER)
        self.assertFalse(self.permission.has_permission(self._request_for(user), None))

    def test_anonymous_user_denied(self):
        self.assertFalse(self.permission.has_permission(self._request_for(AnonymousUser()), None))
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python src/manage.py test apps._auth.tests.test_permissions --exclude-tag=dev-mode -v 2`
Expected: FAIL/ERROR — `ImportError: cannot import name 'IsAdminRole' from 'apps.common.permissions'`.

- [ ] **Step 3: Implement the permission**

Create `src/apps/common/permissions/is_admin_role.py`:

```python
from rest_framework.permissions import BasePermission

from apps.common.choices import UserRoleChoice


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.role == UserRoleChoice.ADMIN)
```

Modify `src/apps/common/permissions/__init__.py` (current content is `from .admin_model_permission import *`):

```python
from .admin_model_permission import *
from .is_admin_role import IsAdminRole
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `python src/manage.py test apps._auth.tests.test_permissions --exclude-tag=dev-mode -v 2`
Expected: PASS (3 tests).

- [ ] **Step 5: Commit**

```bash
git add src/apps/common/permissions/is_admin_role.py src/apps/common/permissions/__init__.py src/apps/_auth/tests/test_permissions.py
git commit -m "feat(common): add IsAdminRole permission for role-based admin checks"
```

---

### Task 3: `UserAdminCreateView` + URL wiring

**Files:**
- Create: `src/apps/_auth/views/admin/user_admin_view.py`
- Create: `src/apps/_auth/views/admin/__init__.py`
- Create: `src/apps/_auth/urls/user_admin_urls.py`
- Modify: `src/apps/v1.py`
- Test: `src/apps/_auth/tests/test_admin_views.py`

**Interfaces:**
- Consumes: `apps._auth.serializers.admin.UserAdminCreateSerializer` (Task 1), `apps.common.permissions.IsAdminRole` (Task 2), `apps.common.base_api.BaseGenericAPI` (existing — `perform_check` validates `request.data` against `serializer_class` before the handler runs and exposes it via `self.serializer`).
- Produces: route `POST /api/v1/admin/user/create/`, URL name `user-admin:user-admin-create`.

- [ ] **Step 1: Write the failing tests**

Create `src/apps/_auth/tests/test_admin_views.py`:

```python
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps._auth.models import User
from apps.common.choices import UserRoleChoice


class UserAdminCreateViewTests(APITestCase):
    def setUp(self):
        self.url = reverse("user-admin:user-admin-create")
        self.valid_payload = {
            "first_name": "Aziz",
            "last_name": "Karimov",
            "username": "aziz.karimov",
            "password": "Sup3r-Secret-Pass",
        }

    def test_anonymous_cannot_create(self):
        response = self.client.post(self.url, data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_regular_role_user_forbidden(self):
        user = User.objects.create_user(username="regular", password="pass12345", role=UserRoleChoice.USER)
        self.client.force_authenticate(user)
        response = self.client.post(self.url, data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_role_without_is_staff_can_create(self):
        admin = User.objects.create_user(
            username="root-admin", password="pass12345", role=UserRoleChoice.ADMIN, is_staff=False
        )
        self.client.force_authenticate(admin)
        response = self.client.post(self.url, data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

    def test_create_user_success(self):
        admin = User.objects.create_user(username="root-admin", password="pass12345", role=UserRoleChoice.ADMIN)
        self.client.force_authenticate(admin)

        response = self.client.post(self.url, data=self.valid_payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(response.data["username"], "aziz.karimov")
        self.assertEqual(response.data["first_name"], "Aziz")
        self.assertEqual(response.data["last_name"], "Karimov")
        self.assertEqual(response.data["role"], UserRoleChoice.USER)
        self.assertNotIn("password", response.data)

        created = User.objects.get(username="aziz.karimov")
        self.assertTrue(created.check_password("Sup3r-Secret-Pass"))
        self.assertEqual(created.created_by, admin)
        self.assertFalse(created.is_staff)

    def test_duplicate_username_rejected(self):
        admin = User.objects.create_user(username="root-admin", password="pass12345", role=UserRoleChoice.ADMIN)
        self.client.force_authenticate(admin)
        User.objects.create_user(username="aziz.karimov", password="pass12345")

        response = self.client.post(self.url, data=self.valid_payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)

    def test_missing_first_name_rejected(self):
        admin = User.objects.create_user(username="root-admin", password="pass12345", role=UserRoleChoice.ADMIN)
        self.client.force_authenticate(admin)
        payload = {**self.valid_payload}
        del payload["first_name"]

        response = self.client.post(self.url, data=payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("first_name", response.data)
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python src/manage.py test apps._auth.tests.test_admin_views --exclude-tag=dev-mode -v 2`
Expected: FAIL/ERROR — `django.urls.exceptions.NoReverseMatch: 'user-admin' is not a registered namespace`.

- [ ] **Step 3: Implement the view**

Create `src/apps/_auth/views/admin/__init__.py`:

```python
from .user_admin_view import UserAdminCreateView

__all__ = ["UserAdminCreateView"]
```

Create `src/apps/_auth/views/admin/user_admin_view.py`:

```python
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps._auth.serializers.admin import UserAdminCreateSerializer
from apps.common.base_api import BaseGenericAPI
from apps.common.permissions import IsAdminRole


@extend_schema(tags=["User Admin"])
class UserAdminCreateView(BaseGenericAPI):
    serializer_class = UserAdminCreateSerializer
    permission_classes = (IsAuthenticated, IsAdminRole)

    def post(self, request, *args, **kwargs):
        instance = self.serializer.save(created_by=request.user)
        return Response(self.get_serializer(instance).data, status=status.HTTP_201_CREATED)
```

- [ ] **Step 4: Wire up the URLs**

Create `src/apps/_auth/urls/user_admin_urls.py`:

```python
from django.urls import path

from apps._auth.views.admin import UserAdminCreateView

urlpatterns = [
    path("create/", view=UserAdminCreateView.as_view(), name="user-admin-create"),
]
```

Modify `src/apps/v1.py` — current full content is:

```python
from django.urls import include, path

urlpatterns = [
    path(
        "auth/",
        include(("apps._auth.urls.auth_urls", "auth"), namespace="auth"),
    ),
    path(
        "user/",
        include(("apps._auth.urls.user_urls", "user"), namespace="user"),
    ),
    path("upload/", include(("apps.upload.urls", "upload"), namespace="upload")),
    path("", include(("apps.catalog.urls.urls", "catalog"), namespace="catalog")),
    path("admin/catalog/", include(("apps.catalog.urls.admin_urls", "catalog"), namespace="catalog-admin")),
    path("", include(("apps.blog.urls.urls", "blog"), namespace="blog")),
    path("admin/blog/", include(("apps.blog.urls.admin_urls", "blog"), namespace="blog-admin")),
    path("", include(("apps.about.urls.urls", "about"), namespace="about")),
    path("admin/about/", include(("apps.about.urls.admin_urls", "about"), namespace="about-admin")),
    path("", include(("apps.careers.urls.urls", "careers"), namespace="careers")),
    path("admin/careers/", include(("apps.careers.urls.admin_urls", "careers"), namespace="careers-admin")),
    path("", include(("apps.partners.urls.urls", "partners"), namespace="partners")),
    path("admin/partners/", include(("apps.partners.urls.admin_urls", "partners"), namespace="partners-admin")),
    path("", include(("apps.pages.urls.urls", "pages"), namespace="pages")),
    path("admin/pages/", include(("apps.pages.urls.admin_urls", "pages"), namespace="pages-admin")),
    path("", include(("apps.leads.urls.urls", "leads"), namespace="leads")),
    path("admin/leads/", include(("apps.leads.urls.admin_urls", "leads"), namespace="leads-admin")),
]
```

Replace it with (only the new `admin/user/` block is added, directly after the `"user/"` block — every other line is unchanged):

```python
from django.urls import include, path

urlpatterns = [
    path(
        "auth/",
        include(("apps._auth.urls.auth_urls", "auth"), namespace="auth"),
    ),
    path(
        "user/",
        include(("apps._auth.urls.user_urls", "user"), namespace="user"),
    ),
    path(
        "admin/user/",
        include(("apps._auth.urls.user_admin_urls", "user"), namespace="user-admin"),
    ),
    path("upload/", include(("apps.upload.urls", "upload"), namespace="upload")),
    path("", include(("apps.catalog.urls.urls", "catalog"), namespace="catalog")),
    path("admin/catalog/", include(("apps.catalog.urls.admin_urls", "catalog"), namespace="catalog-admin")),
    path("", include(("apps.blog.urls.urls", "blog"), namespace="blog")),
    path("admin/blog/", include(("apps.blog.urls.admin_urls", "blog"), namespace="blog-admin")),
    path("", include(("apps.about.urls.urls", "about"), namespace="about")),
    path("admin/about/", include(("apps.about.urls.admin_urls", "about"), namespace="about-admin")),
    path("", include(("apps.careers.urls.urls", "careers"), namespace="careers")),
    path("admin/careers/", include(("apps.careers.urls.admin_urls", "careers"), namespace="careers-admin")),
    path("", include(("apps.partners.urls.urls", "partners"), namespace="partners")),
    path("admin/partners/", include(("apps.partners.urls.admin_urls", "partners"), namespace="partners-admin")),
    path("", include(("apps.pages.urls.urls", "pages"), namespace="pages")),
    path("admin/pages/", include(("apps.pages.urls.admin_urls", "pages"), namespace="pages-admin")),
    path("", include(("apps.leads.urls.urls", "leads"), namespace="leads")),
    path("admin/leads/", include(("apps.leads.urls.admin_urls", "leads"), namespace="leads-admin")),
]
```

- [ ] **Step 5: Run the tests to verify they pass**

Run: `python src/manage.py test apps._auth.tests.test_admin_views --exclude-tag=dev-mode -v 2`
Expected: PASS (6 tests).

- [ ] **Step 6: Run the full `_auth` app test suite**

Run: `python src/manage.py test apps._auth --exclude-tag=dev-mode -v 2`
Expected: PASS (all tests from Task 1, Task 2, and Task 3 — 16 tests total).

- [ ] **Step 7: Commit**

```bash
git add src/apps/_auth/views/admin/__init__.py src/apps/_auth/views/admin/user_admin_view.py src/apps/_auth/urls/user_admin_urls.py src/apps/v1.py src/apps/_auth/tests/test_admin_views.py
git commit -m "feat(_auth): add admin user-create endpoint at POST /api/v1/admin/user/create/"
```

---

## Manual verification (optional, after Task 3)

Not required for tests to pass, but useful to sanity-check against a running stack:

```bash
# inside docker (make up), or against a local runserver
curl -X POST http://localhost:8000/api/v1/admin/user/create/ \
  -H "Authorization: Bearer <admin-role-user-access-token>" \
  -H "Content-Type: application/json" \
  -d '{"first_name": "Aziz", "last_name": "Karimov", "username": "aziz.karimov", "password": "Sup3r-Secret-Pass"}'
```

Expected: `201` with `{"id": ..., "username": "aziz.karimov", "first_name": "Aziz", "last_name": "Karimov", "role": 1, "date_joined": "..."}`.
