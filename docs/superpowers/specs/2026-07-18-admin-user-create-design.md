# Admin user create API — design

## Purpose

Admin (a user with `role == UserRoleChoice.ADMIN`) needs an API endpoint to create a new
user account by providing first name, last name, login username, and password. There is
currently no way to create users other than Django's `createsuperuser` management command
or the Django admin site.

## Scope

Create-only. No list/retrieve/update/delete for users is part of this spec — if needed
later, it gets its own spec.

## Permission

New permission class `apps/common/permissions/is_admin_role.py::IsAdminRole`:

```python
class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == UserRoleChoice.ADMIN
        )
```

This checks the domain `role` field (`apps/common/choices/role.py::UserRoleChoice`), not
Django's `is_staff`/`is_superuser`. The two are intentionally independent: creating a
`role=ADMIN` user via this endpoint does **not** set `is_staff`, so it does not by itself
grant access to Django-admin-backed endpoints elsewhere (e.g. `IsAdminUser`-protected
Catalog/Blog admin endpoints). That's a deliberate, confirmed decision, not an oversight.

The view combines this with `IsAuthenticated` so anonymous requests get 401 rather than
403.

## Serializer

`apps/_auth/serializers/admin/user_admin_serializer.py::UserAdminCreateSerializer`
(`serializers.ModelSerializer` on `apps._auth.models.User`):

- Fields: `id` (read-only), `first_name`, `last_name`, `username`, `password`
  (write-only), `role`, `date_joined` (read-only).
- `username` gets DRF's automatic `UniqueValidator` from the model's `unique=True`.
- `password` is validated against `AUTH_PASSWORD_VALIDATORS`
  (`django.contrib.auth.password_validation.validate_password`) in a field-level
  `validate_password` method, raising a DRF `ValidationError` on failure so it surfaces
  as a normal 400 through the existing pipeline.
- `create()` pops `password` from `validated_data` and calls
  `User.objects.create_user(password=password, **validated_data)` so the password is
  hashed via `set_password` (never stored/returned raw). `validated_data` at this point
  includes `created_by` (injected by the view — see below), `first_name`, `last_name`,
  `username`, `role`.

## View

`apps/_auth/views/admin/user_admin_view.py::UserAdminCreateView`, extends
`apps.common.base_api.BaseGenericAPI` (not `AdminListCreateAPI`, since there's no list):

```python
@extend_schema(tags=["User Admin"])
class UserAdminCreateView(BaseGenericAPI):
    serializer_class = UserAdminCreateSerializer
    permission_classes = (IsAuthenticated, IsAdminRole)

    def post(self, request, *args, **kwargs):
        instance = self.serializer.save(created_by=request.user)
        return Response(self.get_serializer(instance).data, status=status.HTTP_201_CREATED)
```

`BaseGenericAPI.perform_check` (already run by `_BaseAPI.dispatch` before `post()`)
validates `request.data` against `serializer_class` and exposes it via `self.serializer`,
matching the existing pattern used by `AdminListCreateAPI.post` elsewhere in the codebase.

Response is 201 with the same serializer's output: `id`, `username`, `first_name`,
`last_name`, `role`, `date_joined`. `password` never appears in the response because it's
`write_only`.

## URLs

New `apps/_auth/urls/user_admin_urls.py`:

```python
urlpatterns = [
    path("create/", view=UserAdminCreateView.as_view(), name="user-admin-create"),
]
```

Mounted in `apps/v1.py` following the existing `admin/<app>/` convention used by catalog,
blog, etc.:

```python
path("admin/user/", include(("apps._auth.urls.user_admin_urls", "user"), namespace="user-admin")),
```

Final route: `POST /api/v1/admin/user/create/`.

## Error handling

No new error handling is introduced. Validation failures (duplicate username, weak
password, missing fields) flow through the existing
`BaseGenericAPI.perform_check` → `serializer.is_valid(raise_exception=True)` path and come
back as standard DRF 400 responses. Permission failures return 401 (anonymous) or 403
(authenticated but not `role=ADMIN`) via DRF's standard permission handling — no custom
`ExceptionResponse`/`ResponseCode` needed for this endpoint.

## Testing

New `apps/_auth/tests/test_admin_views.py` (app currently has no tests), covering:

- Authenticated `role=ADMIN` user successfully creates a user (201, correct fields,
  password hashed and not in response, `created_by` set).
- Duplicate `username` → 400.
- Password failing `AUTH_PASSWORD_VALIDATORS` → 400.
- Missing required field → 400.
- Anonymous request → 401.
- Authenticated but `role=USER` (or `role=ADMIN` with `is_staff=False`, confirming
  `is_staff` is irrelevant to this check) → 403.
