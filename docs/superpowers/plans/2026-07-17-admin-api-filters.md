# Admin API Filtering & Search Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `django-filter`-based exact-match filtering and text search to every admin CRUD list endpoint in the project, per `docs/superpowers/specs/2026-07-17-admin-api-filters-design.md`.

**Architecture:** A new `SearchFilterSet` base in `apps/common/filters.py` generalizes the existing hand-rolled `ProductFilter` search pattern (icontains across plain fields and `ru`/`en` JSONField keys). Every app gets a `filters.py` with one `FilterSet` per admin-listed model, subclassing `SearchFilterSet`. `DEFAULT_FILTER_BACKENDS` is set globally so views only declare `filterset_class`.

**Tech Stack:** Django 5.2, DRF, `django-filter==25.1` (already a pinned dependency, not yet an installed app).

## Global Constraints

- `django-filter==25.1` is already pinned in `requirements/base.txt` — no dependency changes needed.
- Line length 120, enforced by black/flake8/isort via pre-commit (`.pre-commit-config.yaml`).
- Full suite must pass before any task is considered done: `python src/manage.py test --parallel --exclude-tag=dev-mode` (this is also the pre-commit `django-test` hook).
- Translatable JSONField locale keys are always `ru`/`en` (see `LANGUAGE_CODE`/`LANGUAGES` in `src/config/settings/locale.py`).
- Exact-match filters and search fields per model come from the approved mapping table in the spec (mirrors each model's `admin.py` `list_filter`/`search_fields`), with one approved deviation: `Lead.product` is an exact filter despite not being in `leads/admin.py`'s `list_filter`. Do not add filters beyond the spec's table.
- No model or migration changes in this plan — filtering only touches `filters.py` files, view classes, and settings.

---

### Task 1: Global settings — register `django_filters` and set the default filter backend

**Files:**
- Modify: `src/config/settings/apps.py`
- Modify: `src/config/settings/rest_framework.py`

**Interfaces:**
- Produces: `DEFAULT_FILTER_BACKENDS` containing `django_filters.rest_framework.DjangoFilterBackend`, active for every DRF view project-wide. All later tasks rely on this — they only ever set `filterset_class` on a view, never `filter_backends`.

- [ ] **Step 1: Add `django_filters` to `THIRD_PARTY_APPS`**

In `src/config/settings/apps.py`, replace:

```python
THIRD_PARTY_APPS = [
    "rest_framework_simplejwt.token_blacklist",
    "rest_framework",
    "corsheaders",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "django_json_widget",
]
```

with:

```python
THIRD_PARTY_APPS = [
    "rest_framework_simplejwt.token_blacklist",
    "rest_framework",
    "corsheaders",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "django_json_widget",
    "django_filters",
]
```

- [ ] **Step 2: Add `DEFAULT_FILTER_BACKENDS` to `REST_FRAMEWORK`**

In `src/config/settings/rest_framework.py`, replace:

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
```

with:

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
```

- [ ] **Step 3: Verify Django boots cleanly with the new app and setting**

Run: `python src/manage.py check`
Expected: `System check identified no issues (0 silenced).`

- [ ] **Step 4: Commit**

```bash
git add src/config/settings/apps.py src/config/settings/rest_framework.py
git commit -m "Register django_filters app and set it as the default DRF filter backend"
```

---

### Task 2: Shared `SearchFilterSet` base + rebase the existing `ProductFilter` onto it

**Files:**
- Modify: `src/apps/common/filters.py`
- Modify: `src/apps/catalog/filters.py`
- Modify: `src/apps/catalog/views/product_view.py`
- Test: `src/apps/catalog/tests/test_views.py` (regression only, no new tests — existing `ProductListViewTests` must keep passing unchanged)

**Interfaces:**
- Consumes: `apps.common.filters.BaseFilter` (existing: `begin_date`/`end_date` on `created_at`).
- Produces: `apps.common.filters.SearchFilterSet(BaseFilter)` — every later task's `FilterSet` subclasses this. Class attributes subclasses set: `search_fields: tuple[str, ...]` (plain `CharField`/`EmailField` names) and `locale_search_fields: tuple[str, ...]` (JSONField translatable names, matched on `ru` and `en`). Subclasses must still set `class Meta: model = ...; fields = (...)` themselves (django-filter requires it per FilterSet).

- [ ] **Step 1: Run the existing public Product filter tests to confirm current green baseline**

Run: `python src/manage.py test apps.catalog.tests.test_views`
Expected: `OK` (all `ProductListViewTests` pass, including `test_filters_by_category` and `test_search_filters_by_name`) — this is the regression baseline the rebase must not break.

- [ ] **Step 2: Add `SearchFilterSet` to `apps/common/filters.py`**

Replace the full contents of `src/apps/common/filters.py`:

```python
from django.db.models import Q
from django.utils import timezone
from django_filters.rest_framework import CharFilter, DateFilter, FilterSet


class BaseFilter(FilterSet):
    begin_date = DateFilter(field_name="created_at", lookup_expr="date__gte")
    end_date = DateFilter(field_name="created_at", lookup_expr="date__lte")


class SearchFilterSet(BaseFilter):
    """FilterSet mixin adding a `search` param that does icontains across configured fields.

    Subclasses set `search_fields` (plain CharField/EmailField names) and/or
    `locale_search_fields` (JSONField translatable names, matched on both the `ru` and `en` keys).
    """

    search = CharFilter(method="filter_search")

    search_fields = ()
    locale_search_fields = ()

    def filter_search(self, queryset, name, value):
        query = Q()
        for field in self.search_fields:
            query |= Q(**{f"{field}__icontains": value})
        for field in self.locale_search_fields:
            query |= Q(**{f"{field}__ru__icontains": value}) | Q(**{f"{field}__en__icontains": value})
        return queryset.filter(query) if query else queryset


beginning_of_the_current_month = timezone.now().replace(day=1, hour=0, minute=0, second=0)
```

- [ ] **Step 3: Rebase `ProductFilter` onto `SearchFilterSet`**

Replace the full contents of `src/apps/catalog/filters.py`:

```python
from apps.catalog.models import Product
from apps.common.filters import SearchFilterSet


class ProductFilter(SearchFilterSet):
    locale_search_fields = ("name", "description")

    class Meta:
        model = Product
        fields = ("category", "badge", "family")
```

- [ ] **Step 4: Drop the now-redundant explicit `filter_backends` from `ProductListView`**

In `src/apps/catalog/views/product_view.py`, replace:

```python
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.catalog.filters import ProductFilter
from apps.catalog.selectors import get_related_products, product_base_queryset
from apps.catalog.serializers import ProductDetailSerializer, ProductListSerializer
from apps.common.pagination import PageNumberPagination


@extend_schema(tags=["Catalog"])
class ProductListView(ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter
```

with:

```python
from drf_spectacular.utils import extend_schema
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.catalog.filters import ProductFilter
from apps.catalog.selectors import get_related_products, product_base_queryset
from apps.catalog.serializers import ProductDetailSerializer, ProductListSerializer
from apps.common.pagination import PageNumberPagination


@extend_schema(tags=["Catalog"])
class ProductListView(ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination
    filterset_class = ProductFilter
```

(leave the rest of the file — `ProductDetailView`, `ProductRelatedView` — untouched)

- [ ] **Step 5: Re-run the same tests to confirm no regression**

Run: `python src/manage.py test apps.catalog.tests.test_views`
Expected: `OK`, identical to Step 1 — `test_filters_by_category` and `test_search_filters_by_name` still pass unchanged, now via `SearchFilterSet` instead of the old hand-rolled `filter_search`.

- [ ] **Step 6: Commit**

```bash
git add src/apps/common/filters.py src/apps/catalog/filters.py src/apps/catalog/views/product_view.py
git commit -m "Extract SearchFilterSet base and rebase ProductFilter onto it"
```

---

### Task 3: Catalog admin — `CategoryAdminFilter`

**Files:**
- Modify: `src/apps/catalog/filters.py`
- Modify: `src/apps/catalog/views/admin/category_admin_view.py`
- Test: `src/apps/catalog/tests/test_admin_views.py`

**Interfaces:**
- Consumes: `apps.common.filters.SearchFilterSet` (Task 2).
- Produces: `apps.catalog.filters.CategoryAdminFilter`, wired into `CategoryAdminListCreateView`.

- [ ] **Step 1: Write the failing tests**

Append to `src/apps/catalog/tests/test_admin_views.py` (existing imports already include `reverse`, `status`, `APITestCase`, `User`, `Category` — no import changes needed):

```python


class CategoryAdminFilterTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="admin", password="pass12345", is_staff=True)
        self.client.force_authenticate(self.admin)
        self.active = Category.objects.create(
            name={"ru": "Круассаны", "en": "Croissants"}, slug="croissants", image="c.jpg", is_active=True
        )
        self.inactive = Category.objects.create(
            name={"ru": "Архив", "en": "Archive"}, slug="archive", image="a.jpg", is_active=False
        )

    def test_filters_by_is_active(self):
        response = self.client.get(reverse("catalog-admin:category-admin-list"), {"is_active": "true"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([item["slug"] for item in response.data], ["croissants"])

    def test_search_matches_locale_name(self):
        response = self.client.get(reverse("catalog-admin:category-admin-list"), {"search": "Croissants"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([item["slug"] for item in response.data], ["croissants"])

    def test_search_matches_slug(self):
        response = self.client.get(reverse("catalog-admin:category-admin-list"), {"search": "archive"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([item["slug"] for item in response.data], ["archive"])
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python src/manage.py test apps.catalog.tests.test_admin_views.CategoryAdminFilterTests`
Expected: FAIL on all three — `category-admin-list` currently ignores `is_active`/`search` query params, so both categories come back instead of one.

- [ ] **Step 3: Add `CategoryAdminFilter`**

In `src/apps/catalog/filters.py`, replace:

```python
from apps.catalog.models import Product
from apps.common.filters import SearchFilterSet


class ProductFilter(SearchFilterSet):
    locale_search_fields = ("name", "description")

    class Meta:
        model = Product
        fields = ("category", "badge", "family")
```

with:

```python
from apps.catalog.models import Category, Product
from apps.common.filters import SearchFilterSet


class ProductFilter(SearchFilterSet):
    locale_search_fields = ("name", "description")

    class Meta:
        model = Product
        fields = ("category", "badge", "family")


class CategoryAdminFilter(SearchFilterSet):
    locale_search_fields = ("name",)
    search_fields = ("slug",)

    class Meta:
        model = Category
        fields = ("is_active",)
```

- [ ] **Step 4: Wire it into the view**

In `src/apps/catalog/views/admin/category_admin_view.py`, replace:

```python
from drf_spectacular.utils import extend_schema

from apps.catalog.models import Category
from apps.catalog.serializers.admin import CategoryAdminSerializer
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI


@extend_schema(tags=["Catalog Admin"])
class CategoryAdminListCreateView(AdminListCreateAPI):
    queryset = Category.objects.all().order_by("sort_order", "id")
    serializer_class = CategoryAdminSerializer
```

with:

```python
from drf_spectacular.utils import extend_schema

from apps.catalog.filters import CategoryAdminFilter
from apps.catalog.models import Category
from apps.catalog.serializers.admin import CategoryAdminSerializer
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI


@extend_schema(tags=["Catalog Admin"])
class CategoryAdminListCreateView(AdminListCreateAPI):
    queryset = Category.objects.all().order_by("sort_order", "id")
    serializer_class = CategoryAdminSerializer
    filterset_class = CategoryAdminFilter
```

(leave `CategoryAdminDetailView` in that file untouched)

- [ ] **Step 5: Run tests to verify they pass**

Run: `python src/manage.py test apps.catalog.tests.test_admin_views`
Expected: `OK` (all catalog admin tests pass, including the new `CategoryAdminFilterTests` and the pre-existing `CategoryAdminPermissionTests`/`CategoryAdminCrudTests`).

- [ ] **Step 6: Commit**

```bash
git add src/apps/catalog/filters.py src/apps/catalog/views/admin/category_admin_view.py src/apps/catalog/tests/test_admin_views.py
git commit -m "Add is_active filter and name/slug search to the Category admin list"
```

---

### Task 4: Catalog admin — `FlavorAdminFilter`

**Files:**
- Modify: `src/apps/catalog/filters.py`
- Modify: `src/apps/catalog/views/admin/flavor_admin_view.py`
- Test: `src/apps/catalog/tests/test_admin_views.py`

**Interfaces:**
- Consumes: `apps.common.filters.SearchFilterSet` (Task 2).
- Produces: `apps.catalog.filters.FlavorAdminFilter`, wired into `FlavorAdminListCreateView`.

- [ ] **Step 1: Write the failing test**

Append to `src/apps/catalog/tests/test_admin_views.py` (add `Flavor` to the existing `from apps.catalog.models import Category` import line, making it `from apps.catalog.models import Category, Flavor`):

```python


class FlavorAdminFilterTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="admin", password="pass12345", is_staff=True)
        self.client.force_authenticate(self.admin)
        self.vanilla = Flavor.objects.create(name={"ru": "Ваниль", "en": "Vanilla"}, slug="vanilla")
        Flavor.objects.create(name={"ru": "Шоколад", "en": "Chocolate"}, slug="chocolate")

    def test_search_matches_locale_name(self):
        response = self.client.get(reverse("catalog-admin:flavor-admin-list"), {"search": "Vanilla"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([item["slug"] for item in response.data], ["vanilla"])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python src/manage.py test apps.catalog.tests.test_admin_views.FlavorAdminFilterTests`
Expected: FAIL — `flavor-admin-list` currently ignores `search`, both flavors come back.

- [ ] **Step 3: Add `FlavorAdminFilter`**

In `src/apps/catalog/filters.py`, replace the import line:

```python
from apps.catalog.models import Category, Product
```

with:

```python
from apps.catalog.models import Category, Flavor, Product
```

Then append to the end of the file:

```python


class FlavorAdminFilter(SearchFilterSet):
    locale_search_fields = ("name",)
    search_fields = ("slug",)

    class Meta:
        model = Flavor
        fields = ()
```

- [ ] **Step 4: Wire it into the view**

In `src/apps/catalog/views/admin/flavor_admin_view.py`, replace:

```python
from drf_spectacular.utils import extend_schema

from apps.catalog.models import Flavor
from apps.catalog.serializers.admin import FlavorAdminSerializer
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI


@extend_schema(tags=["Catalog Admin"])
class FlavorAdminListCreateView(AdminListCreateAPI):
    queryset = Flavor.objects.all().order_by("sort_order", "id")
    serializer_class = FlavorAdminSerializer
```

with:

```python
from drf_spectacular.utils import extend_schema

from apps.catalog.filters import FlavorAdminFilter
from apps.catalog.models import Flavor
from apps.catalog.serializers.admin import FlavorAdminSerializer
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI


@extend_schema(tags=["Catalog Admin"])
class FlavorAdminListCreateView(AdminListCreateAPI):
    queryset = Flavor.objects.all().order_by("sort_order", "id")
    serializer_class = FlavorAdminSerializer
    filterset_class = FlavorAdminFilter
```

- [ ] **Step 5: Run test to verify it passes**

Run: `python src/manage.py test apps.catalog.tests.test_admin_views`
Expected: `OK`

- [ ] **Step 6: Commit**

```bash
git add src/apps/catalog/filters.py src/apps/catalog/views/admin/flavor_admin_view.py src/apps/catalog/tests/test_admin_views.py
git commit -m "Add name/slug search to the Flavor admin list"
```

---

### Task 5: Catalog admin — `WeightAdminFilter`

**Files:**
- Modify: `src/apps/catalog/filters.py`
- Modify: `src/apps/catalog/views/admin/weight_admin_view.py`
- Test: `src/apps/catalog/tests/test_admin_views.py`

**Interfaces:**
- Consumes: `apps.common.filters.SearchFilterSet` (Task 2).
- Produces: `apps.catalog.filters.WeightAdminFilter`, wired into `WeightAdminListCreateView`.

- [ ] **Step 1: Write the failing test**

Append to `src/apps/catalog/tests/test_admin_views.py` (add `Weight` to the model import line, making it `from apps.catalog.models import Category, Flavor, Weight`):

```python


class WeightAdminFilterTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="admin", password="pass12345", is_staff=True)
        self.client.force_authenticate(self.admin)
        self.grams = Weight.objects.create(value="250.00", unit="g")
        Weight.objects.create(value="1.00", unit="kg")

    def test_filters_by_unit(self):
        response = self.client.get(reverse("catalog-admin:weight-admin-list"), {"unit": "g"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([item["id"] for item in response.data], [self.grams.id])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python src/manage.py test apps.catalog.tests.test_admin_views.WeightAdminFilterTests`
Expected: FAIL — both weights come back regardless of `unit`.

- [ ] **Step 3: Add `WeightAdminFilter`**

In `src/apps/catalog/filters.py`, replace the import line:

```python
from apps.catalog.models import Category, Flavor, Product
```

with:

```python
from apps.catalog.models import Category, Flavor, Product, Weight
```

Then append to the end of the file:

```python


class WeightAdminFilter(SearchFilterSet):
    class Meta:
        model = Weight
        fields = ("unit",)
```

- [ ] **Step 4: Wire it into the view**

In `src/apps/catalog/views/admin/weight_admin_view.py`, replace:

```python
from drf_spectacular.utils import extend_schema

from apps.catalog.models import Weight
from apps.catalog.serializers.admin import WeightAdminSerializer
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI


@extend_schema(tags=["Catalog Admin"])
class WeightAdminListCreateView(AdminListCreateAPI):
    queryset = Weight.objects.all().order_by("unit", "value")
    serializer_class = WeightAdminSerializer
```

with:

```python
from drf_spectacular.utils import extend_schema

from apps.catalog.filters import WeightAdminFilter
from apps.catalog.models import Weight
from apps.catalog.serializers.admin import WeightAdminSerializer
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI


@extend_schema(tags=["Catalog Admin"])
class WeightAdminListCreateView(AdminListCreateAPI):
    queryset = Weight.objects.all().order_by("unit", "value")
    serializer_class = WeightAdminSerializer
    filterset_class = WeightAdminFilter
```

- [ ] **Step 5: Run test to verify it passes**

Run: `python src/manage.py test apps.catalog.tests.test_admin_views`
Expected: `OK`

- [ ] **Step 6: Commit**

```bash
git add src/apps/catalog/filters.py src/apps/catalog/views/admin/weight_admin_view.py src/apps/catalog/tests/test_admin_views.py
git commit -m "Add unit filter to the Weight admin list"
```

---

### Task 6: Catalog admin — `ProductFamilyAdminFilter`

**Files:**
- Modify: `src/apps/catalog/filters.py`
- Modify: `src/apps/catalog/views/admin/product_family_admin_view.py`
- Test: `src/apps/catalog/tests/test_admin_views.py`

**Interfaces:**
- Consumes: `apps.common.filters.SearchFilterSet` (Task 2).
- Produces: `apps.catalog.filters.ProductFamilyAdminFilter`, wired into `ProductFamilyAdminListCreateView`.

- [ ] **Step 1: Write the failing test**

Append to `src/apps/catalog/tests/test_admin_views.py` (add `ProductFamily` to the model import line, making it `from apps.catalog.models import Category, Flavor, ProductFamily, Weight`):

```python


class ProductFamilyAdminFilterTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="admin", password="pass12345", is_staff=True)
        self.client.force_authenticate(self.admin)
        self.ketler = ProductFamily.objects.create(name="Ketler", slug="ketler")
        ProductFamily.objects.create(name="Taggis", slug="taggis")

    def test_search_matches_plain_name(self):
        response = self.client.get(reverse("catalog-admin:product-family-admin-list"), {"search": "Ketler"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([item["id"] for item in response.data], [self.ketler.id])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python src/manage.py test apps.catalog.tests.test_admin_views.ProductFamilyAdminFilterTests`
Expected: FAIL — both families come back regardless of `search`.

- [ ] **Step 3: Add `ProductFamilyAdminFilter`**

In `src/apps/catalog/filters.py`, replace the import line:

```python
from apps.catalog.models import Category, Flavor, Product, Weight
```

with:

```python
from apps.catalog.models import Category, Flavor, Product, ProductFamily, Weight
```

Then append to the end of the file:

```python


class ProductFamilyAdminFilter(SearchFilterSet):
    search_fields = ("name", "slug")

    class Meta:
        model = ProductFamily
        fields = ()
```

- [ ] **Step 4: Wire it into the view**

In `src/apps/catalog/views/admin/product_family_admin_view.py`, replace:

```python
from drf_spectacular.utils import extend_schema

from apps.catalog.models import ProductFamily
from apps.catalog.serializers.admin import ProductFamilyAdminSerializer
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI


@extend_schema(tags=["Catalog Admin"])
class ProductFamilyAdminListCreateView(AdminListCreateAPI):
    queryset = ProductFamily.objects.all().order_by("name")
    serializer_class = ProductFamilyAdminSerializer
```

with:

```python
from drf_spectacular.utils import extend_schema

from apps.catalog.filters import ProductFamilyAdminFilter
from apps.catalog.models import ProductFamily
from apps.catalog.serializers.admin import ProductFamilyAdminSerializer
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI


@extend_schema(tags=["Catalog Admin"])
class ProductFamilyAdminListCreateView(AdminListCreateAPI):
    queryset = ProductFamily.objects.all().order_by("name")
    serializer_class = ProductFamilyAdminSerializer
    filterset_class = ProductFamilyAdminFilter
```

- [ ] **Step 5: Run test to verify it passes**

Run: `python src/manage.py test apps.catalog.tests.test_admin_views`
Expected: `OK`

- [ ] **Step 6: Commit**

```bash
git add src/apps/catalog/filters.py src/apps/catalog/views/admin/product_family_admin_view.py src/apps/catalog/tests/test_admin_views.py
git commit -m "Add name/slug search to the ProductFamily admin list"
```

---

### Task 7: Catalog admin — `ProductAdminFilter`

**Files:**
- Modify: `src/apps/catalog/filters.py`
- Modify: `src/apps/catalog/views/admin/product_admin_view.py`
- Test: `src/apps/catalog/tests/test_admin_views.py`

**Interfaces:**
- Consumes: `apps.common.filters.SearchFilterSet` (Task 2). `Product` is already imported in `catalog/filters.py`.
- Produces: `apps.catalog.filters.ProductAdminFilter` (distinct from the public `ProductFilter` — broader field set, includes inactive products), wired into `ProductAdminListCreateView`.

- [ ] **Step 1: Write the failing tests**

Append to `src/apps/catalog/tests/test_admin_views.py` (add `Product` to the model import line, making it `from apps.catalog.models import Category, Flavor, Product, ProductFamily, Weight`):

```python


class ProductAdminFilterTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="admin", password="pass12345", is_staff=True)
        self.client.force_authenticate(self.admin)
        self.category = Category.objects.create(
            name={"ru": "Категория", "en": "Category"}, slug="cat", image="c.jpg"
        )
        self.featured = Product.objects.create(
            category=self.category,
            name={"ru": "Кетлер", "en": "Ketler"},
            slug="ketler",
            code="A1",
            box_weight="1.500",
            shelf_life_months=6,
            is_active=True,
            is_featured=True,
        )
        Product.objects.create(
            category=self.category,
            name={"ru": "Тагги", "en": "Taggis"},
            slug="taggis",
            code="B1",
            box_weight="1.500",
            shelf_life_months=6,
            is_active=False,
            is_featured=False,
        )

    def test_filters_by_is_featured(self):
        response = self.client.get(reverse("catalog-admin:product-admin-list"), {"is_featured": "true"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([item["slug"] for item in response.data], ["ketler"])

    def test_search_matches_code(self):
        response = self.client.get(reverse("catalog-admin:product-admin-list"), {"search": "B1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([item["slug"] for item in response.data], ["taggis"])
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python src/manage.py test apps.catalog.tests.test_admin_views.ProductAdminFilterTests`
Expected: FAIL on both — `product-admin-list` currently ignores `is_featured`/`search`, both products come back.

- [ ] **Step 3: Add `ProductAdminFilter`**

Append to the end of `src/apps/catalog/filters.py` (no import line change needed — `Product` is already imported):

```python


class ProductAdminFilter(SearchFilterSet):
    locale_search_fields = ("name",)
    search_fields = ("code", "slug")

    class Meta:
        model = Product
        fields = ("category", "family", "flavor", "badge", "is_featured", "is_active")
```

- [ ] **Step 4: Wire it into the view**

In `src/apps/catalog/views/admin/product_admin_view.py`, replace:

```python
from drf_spectacular.utils import extend_schema

from apps.catalog.models import Product
from apps.catalog.serializers.admin import ProductAdminSerializer
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI


@extend_schema(tags=["Catalog Admin"])
class ProductAdminListCreateView(AdminListCreateAPI):
    queryset = Product.objects.select_related("category", "family", "flavor").all().order_by("sort_order", "id")
    serializer_class = ProductAdminSerializer
```

with:

```python
from drf_spectacular.utils import extend_schema

from apps.catalog.filters import ProductAdminFilter
from apps.catalog.models import Product
from apps.catalog.serializers.admin import ProductAdminSerializer
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI


@extend_schema(tags=["Catalog Admin"])
class ProductAdminListCreateView(AdminListCreateAPI):
    queryset = Product.objects.select_related("category", "family", "flavor").all().order_by("sort_order", "id")
    serializer_class = ProductAdminSerializer
    filterset_class = ProductAdminFilter
```

(leave `ProductAdminDetailView` in that file untouched)

- [ ] **Step 5: Run tests to verify they pass**

Run: `python src/manage.py test apps.catalog.tests.test_admin_views`
Expected: `OK`

- [ ] **Step 6: Commit**

```bash
git add src/apps/catalog/filters.py src/apps/catalog/views/admin/product_admin_view.py src/apps/catalog/tests/test_admin_views.py
git commit -m "Add category/family/flavor/badge/featured/active filters and search to the Product admin list"
```

---

### Task 8: Catalog admin — `ProductImageAdminFilter`

**Files:**
- Modify: `src/apps/catalog/filters.py`
- Modify: `src/apps/catalog/views/admin/product_image_admin_view.py`
- Test: `src/apps/catalog/tests/test_admin_views.py`

**Interfaces:**
- Consumes: `apps.common.filters.SearchFilterSet` (Task 2). `Product` already imported in test file (Task 7); `Category` already imported (Task 3).
- Produces: `apps.catalog.filters.ProductImageAdminFilter`, wired into `ProductImageAdminListCreateView`.

- [ ] **Step 1: Write the failing tests**

Append to `src/apps/catalog/tests/test_admin_views.py` (add `ProductImage` to the model import line, making it `from apps.catalog.models import Category, Flavor, Product, ProductFamily, ProductImage, Weight`):

```python


class ProductImageAdminFilterTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="admin", password="pass12345", is_staff=True)
        self.client.force_authenticate(self.admin)
        category = Category.objects.create(name={"ru": "К", "en": "C"}, slug="cat", image="c.jpg")
        self.product = Product.objects.create(
            category=category,
            name={"ru": "П1", "en": "P1"},
            slug="p1",
            code="A1",
            box_weight="1.500",
            shelf_life_months=6,
        )
        other_product = Product.objects.create(
            category=category,
            name={"ru": "П2", "en": "P2"},
            slug="p2",
            code="A2",
            box_weight="1.500",
            shelf_life_months=6,
        )
        ProductImage.objects.create(product=self.product, image="main.jpg", is_main=True)
        ProductImage.objects.create(product=self.product, image="extra.jpg", is_main=False)
        ProductImage.objects.create(product=other_product, image="other.jpg", is_main=True)

    def test_filters_by_product(self):
        response = self.client.get(reverse("catalog-admin:product-image-admin-list"), {"product": self.product.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filters_by_is_main(self):
        response = self.client.get(reverse("catalog-admin:product-image-admin-list"), {"is_main": "true"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python src/manage.py test apps.catalog.tests.test_admin_views.ProductImageAdminFilterTests`
Expected: FAIL on both — `product-image-admin-list` currently ignores `product`/`is_main`, all three images come back.

- [ ] **Step 3: Add `ProductImageAdminFilter`**

In `src/apps/catalog/filters.py`, replace the import line:

```python
from apps.catalog.models import Category, Flavor, Product, ProductFamily, Weight
```

with:

```python
from apps.catalog.models import Category, Flavor, Product, ProductFamily, ProductImage, Weight
```

Then append to the end of the file:

```python


class ProductImageAdminFilter(SearchFilterSet):
    class Meta:
        model = ProductImage
        fields = ("product", "is_main")
```

- [ ] **Step 4: Wire it into the view**

In `src/apps/catalog/views/admin/product_image_admin_view.py`, replace:

```python
from drf_spectacular.utils import extend_schema

from apps.catalog.models import ProductImage
from apps.catalog.serializers.admin import ProductImageAdminSerializer
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI


@extend_schema(tags=["Catalog Admin"])
class ProductImageAdminListCreateView(AdminListCreateAPI):
    queryset = ProductImage.objects.select_related("product").all().order_by("sort_order", "id")
    serializer_class = ProductImageAdminSerializer
```

with:

```python
from drf_spectacular.utils import extend_schema

from apps.catalog.filters import ProductImageAdminFilter
from apps.catalog.models import ProductImage
from apps.catalog.serializers.admin import ProductImageAdminSerializer
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI


@extend_schema(tags=["Catalog Admin"])
class ProductImageAdminListCreateView(AdminListCreateAPI):
    queryset = ProductImage.objects.select_related("product").all().order_by("sort_order", "id")
    serializer_class = ProductImageAdminSerializer
    filterset_class = ProductImageAdminFilter
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `python src/manage.py test apps.catalog.tests.test_admin_views`
Expected: `OK`

- [ ] **Step 6: Commit**

```bash
git add src/apps/catalog/filters.py src/apps/catalog/views/admin/product_image_admin_view.py src/apps/catalog/tests/test_admin_views.py
git commit -m "Add product/is_main filters to the ProductImage admin list"
```

---

### Task 9: Blog admin — `PostAdminFilter`

**Files:**
- Create: `src/apps/blog/filters.py`
- Modify: `src/apps/blog/views/admin/post_admin_view.py`
- Test: `src/apps/blog/tests/test_admin_views.py`

**Interfaces:**
- Consumes: `apps.common.filters.SearchFilterSet` (Task 2).
- Produces: `apps.blog.filters.PostAdminFilter`, wired into `PostAdminListCreateView`. `apps.blog.filters` module now exists — Task 10 extends this same file.

- [ ] **Step 1: Write the failing tests**

Append to `src/apps/blog/tests/test_admin_views.py` (existing file already imports `json`, `reverse`, `status`, `APITestCase`, `User`, `Post`):

```python


class PostAdminFilterTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="admin", password="pass12345", is_staff=True)
        self.client.force_authenticate(self.admin)
        self.published = Post.objects.create(
            title={"ru": "Опубликован", "en": "Published"},
            slug="published-post",
            cover="c1.jpg",
            published_at="2026-01-01T00:00:00Z",
            is_published=True,
        )
        Post.objects.create(
            title={"ru": "Черновик", "en": "Draft"},
            slug="draft-post",
            cover="c2.jpg",
            published_at="2026-01-02T00:00:00Z",
            is_published=False,
        )

    def test_filters_by_is_published(self):
        response = self.client.get(reverse("blog-admin:post-admin-list"), {"is_published": "true"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([item["slug"] for item in response.data], ["published-post"])

    def test_search_matches_locale_title(self):
        response = self.client.get(reverse("blog-admin:post-admin-list"), {"search": "Draft"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([item["slug"] for item in response.data], ["draft-post"])
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python src/manage.py test apps.blog.tests.test_admin_views.PostAdminFilterTests`
Expected: FAIL on both — `post-admin-list` currently ignores `is_published`/`search`, both posts come back.

- [ ] **Step 3: Create `apps/blog/filters.py`**

```python
from apps.blog.models import Post
from apps.common.filters import SearchFilterSet


class PostAdminFilter(SearchFilterSet):
    locale_search_fields = ("title",)
    search_fields = ("slug",)

    class Meta:
        model = Post
        fields = ("is_published",)
```

- [ ] **Step 4: Wire it into the view**

In `src/apps/blog/views/admin/post_admin_view.py`, replace:

```python
from drf_spectacular.utils import extend_schema

from apps.blog.models import Post
from apps.blog.serializers.admin import PostAdminSerializer
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI


@extend_schema(tags=["Blog Admin"])
class PostAdminListCreateView(AdminListCreateAPI):
    queryset = Post.objects.all().order_by("-published_at")
    serializer_class = PostAdminSerializer
```

with:

```python
from drf_spectacular.utils import extend_schema

from apps.blog.filters import PostAdminFilter
from apps.blog.models import Post
from apps.blog.serializers.admin import PostAdminSerializer
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI


@extend_schema(tags=["Blog Admin"])
class PostAdminListCreateView(AdminListCreateAPI):
    queryset = Post.objects.all().order_by("-published_at")
    serializer_class = PostAdminSerializer
    filterset_class = PostAdminFilter
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `python src/manage.py test apps.blog.tests.test_admin_views`
Expected: `OK`

- [ ] **Step 6: Commit**

```bash
git add src/apps/blog/filters.py src/apps/blog/views/admin/post_admin_view.py src/apps/blog/tests/test_admin_views.py
git commit -m "Add is_published filter and title/slug search to the Post admin list"
```

---

### Task 10: Blog admin — `PostBlockAdminFilter`

**Files:**
- Modify: `src/apps/blog/filters.py`
- Modify: `src/apps/blog/views/admin/post_block_admin_view.py`
- Test: `src/apps/blog/tests/test_admin_views.py`

**Interfaces:**
- Consumes: `apps.common.filters.SearchFilterSet` (Task 2), `apps.blog.filters` module (Task 9).
- Produces: `apps.blog.filters.PostBlockAdminFilter`, wired into `PostBlockAdminListCreateView`.

- [ ] **Step 1: Write the failing tests**

Append to `src/apps/blog/tests/test_admin_views.py` (add `PostBlock` to the model import line, making it `from apps.blog.models import Post, PostBlock`):

```python


class PostBlockAdminFilterTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="admin", password="pass12345", is_staff=True)
        self.client.force_authenticate(self.admin)
        self.post = Post.objects.create(
            title={"ru": "Пост", "en": "Post"}, slug="post-1", cover="c1.jpg", published_at="2026-01-01T00:00:00Z"
        )
        other_post = Post.objects.create(
            title={"ru": "Другой", "en": "Other"}, slug="post-2", cover="c2.jpg", published_at="2026-01-02T00:00:00Z"
        )
        PostBlock.objects.create(post=self.post, type="heading")
        PostBlock.objects.create(post=self.post, type="text")
        PostBlock.objects.create(post=other_post, type="heading")

    def test_filters_by_post(self):
        response = self.client.get(reverse("blog-admin:post-block-admin-list"), {"post": self.post.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filters_by_type(self):
        response = self.client.get(reverse("blog-admin:post-block-admin-list"), {"type": "heading"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python src/manage.py test apps.blog.tests.test_admin_views.PostBlockAdminFilterTests`
Expected: FAIL on both — `post-block-admin-list` currently ignores `post`/`type`, all three blocks come back.

- [ ] **Step 3: Add `PostBlockAdminFilter`**

In `src/apps/blog/filters.py`, replace:

```python
from apps.blog.models import Post
from apps.common.filters import SearchFilterSet


class PostAdminFilter(SearchFilterSet):
    locale_search_fields = ("title",)
    search_fields = ("slug",)

    class Meta:
        model = Post
        fields = ("is_published",)
```

with:

```python
from apps.blog.models import Post, PostBlock
from apps.common.filters import SearchFilterSet


class PostAdminFilter(SearchFilterSet):
    locale_search_fields = ("title",)
    search_fields = ("slug",)

    class Meta:
        model = Post
        fields = ("is_published",)


class PostBlockAdminFilter(SearchFilterSet):
    class Meta:
        model = PostBlock
        fields = ("post", "type")
```

- [ ] **Step 4: Wire it into the view**

In `src/apps/blog/views/admin/post_block_admin_view.py`, replace:

```python
from drf_spectacular.utils import extend_schema

from apps.blog.models import PostBlock
from apps.blog.serializers.admin import PostBlockAdminSerializer
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI


@extend_schema(tags=["Blog Admin"])
class PostBlockAdminListCreateView(AdminListCreateAPI):
    queryset = PostBlock.objects.select_related("post").all().order_by("sort_order", "id")
    serializer_class = PostBlockAdminSerializer
```

with:

```python
from drf_spectacular.utils import extend_schema

from apps.blog.filters import PostBlockAdminFilter
from apps.blog.models import PostBlock
from apps.blog.serializers.admin import PostBlockAdminSerializer
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI


@extend_schema(tags=["Blog Admin"])
class PostBlockAdminListCreateView(AdminListCreateAPI):
    queryset = PostBlock.objects.select_related("post").all().order_by("sort_order", "id")
    serializer_class = PostBlockAdminSerializer
    filterset_class = PostBlockAdminFilter
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `python src/manage.py test apps.blog.tests.test_admin_views`
Expected: `OK`

- [ ] **Step 6: Commit**

```bash
git add src/apps/blog/filters.py src/apps/blog/views/admin/post_block_admin_view.py src/apps/blog/tests/test_admin_views.py
git commit -m "Add post/type filters to the PostBlock admin list"
```

---

### Task 11: About admin — `HomeSlideAdminFilter`, `StatAdminFilter`, `TimelineEventAdminFilter`, `ExportRegionAdminFilter`

**Files:**
- Create: `src/apps/about/filters.py`
- Modify: `src/apps/about/views/admin/home_slide_admin_view.py`
- Modify: `src/apps/about/views/admin/stat_admin_view.py`
- Modify: `src/apps/about/views/admin/timeline_event_admin_view.py`
- Modify: `src/apps/about/views/admin/export_region_admin_view.py`
- Test: `src/apps/about/tests/test_admin_views.py`

**Interfaces:**
- Consumes: `apps.common.filters.SearchFilterSet` (Task 2).
- Produces: `apps.about.filters.{HomeSlideAdminFilter, StatAdminFilter, TimelineEventAdminFilter, ExportRegionAdminFilter}`, wired into their respective views.

`HomeSlide`, `Stat`, and `ExportRegion` have no `list_filter`/`search_fields` in `about/admin.py` (small reference tables) — their `FilterSet`s exist only to give them `begin_date`/`end_date` via `SearchFilterSet`, and get no dedicated test per the spec's testing policy. Only `TimelineEvent` (`year` in `list_filter`) gets a test.

- [ ] **Step 1: Write the failing test for `TimelineEventAdminFilter`**

Append to `src/apps/about/tests/test_admin_views.py`. Replace the existing import line:

```python
from apps.about.models import Stat
```

with:

```python
from apps.about.models import Stat, TimelineEvent
```

Then append the test class:

```python


class TimelineEventAdminFilterTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="admin", password="pass12345", is_staff=True)
        self.client.force_authenticate(self.admin)
        self.event_2020 = TimelineEvent.objects.create(year=2020, title={"ru": "2020", "en": "2020"})
        TimelineEvent.objects.create(year=2021, title={"ru": "2021", "en": "2021"})

    def test_filters_by_year(self):
        response = self.client.get(reverse("about-admin:timeline-event-admin-list"), {"year": 2020})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([item["id"] for item in response.data], [self.event_2020.id])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python src/manage.py test apps.about.tests.test_admin_views.TimelineEventAdminFilterTests`
Expected: FAIL — `timeline-event-admin-list` currently ignores `year`, both events come back.

- [ ] **Step 3: Create `apps/about/filters.py`**

```python
from apps.about.models import ExportRegion, HomeSlide, Stat, TimelineEvent
from apps.common.filters import SearchFilterSet


class HomeSlideAdminFilter(SearchFilterSet):
    class Meta:
        model = HomeSlide
        fields = ()


class StatAdminFilter(SearchFilterSet):
    class Meta:
        model = Stat
        fields = ()


class TimelineEventAdminFilter(SearchFilterSet):
    class Meta:
        model = TimelineEvent
        fields = ("year",)


class ExportRegionAdminFilter(SearchFilterSet):
    class Meta:
        model = ExportRegion
        fields = ()
```

- [ ] **Step 4: Wire `HomeSlideAdminFilter` into the view**

In `src/apps/about/views/admin/home_slide_admin_view.py`, replace:

```python
from drf_spectacular.utils import extend_schema

from apps.about.models import HomeSlide
from apps.about.serializers.admin import HomeSlideAdminSerializer
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI


@extend_schema(tags=["About Admin"])
class HomeSlideAdminListCreateView(AdminListCreateAPI):
    queryset = HomeSlide.objects.all()
    serializer_class = HomeSlideAdminSerializer
```

with:

```python
from drf_spectacular.utils import extend_schema

from apps.about.filters import HomeSlideAdminFilter
from apps.about.models import HomeSlide
from apps.about.serializers.admin import HomeSlideAdminSerializer
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI


@extend_schema(tags=["About Admin"])
class HomeSlideAdminListCreateView(AdminListCreateAPI):
    queryset = HomeSlide.objects.all()
    serializer_class = HomeSlideAdminSerializer
    filterset_class = HomeSlideAdminFilter
```

- [ ] **Step 5: Wire `StatAdminFilter` into the view**

In `src/apps/about/views/admin/stat_admin_view.py`, replace:

```python
from drf_spectacular.utils import extend_schema

from apps.about.models import Stat
from apps.about.serializers.admin import StatAdminSerializer
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI


@extend_schema(tags=["About Admin"])
class StatAdminListCreateView(AdminListCreateAPI):
    queryset = Stat.objects.all()
    serializer_class = StatAdminSerializer
```

with:

```python
from drf_spectacular.utils import extend_schema

from apps.about.filters import StatAdminFilter
from apps.about.models import Stat
from apps.about.serializers.admin import StatAdminSerializer
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI


@extend_schema(tags=["About Admin"])
class StatAdminListCreateView(AdminListCreateAPI):
    queryset = Stat.objects.all()
    serializer_class = StatAdminSerializer
    filterset_class = StatAdminFilter
```

- [ ] **Step 6: Wire `TimelineEventAdminFilter` into the view**

In `src/apps/about/views/admin/timeline_event_admin_view.py`, replace:

```python
from drf_spectacular.utils import extend_schema

from apps.about.models import TimelineEvent
from apps.about.serializers.admin import TimelineEventAdminSerializer
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI


@extend_schema(tags=["About Admin"])
class TimelineEventAdminListCreateView(AdminListCreateAPI):
    queryset = TimelineEvent.objects.all()
    serializer_class = TimelineEventAdminSerializer
```

with:

```python
from drf_spectacular.utils import extend_schema

from apps.about.filters import TimelineEventAdminFilter
from apps.about.models import TimelineEvent
from apps.about.serializers.admin import TimelineEventAdminSerializer
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI


@extend_schema(tags=["About Admin"])
class TimelineEventAdminListCreateView(AdminListCreateAPI):
    queryset = TimelineEvent.objects.all()
    serializer_class = TimelineEventAdminSerializer
    filterset_class = TimelineEventAdminFilter
```

- [ ] **Step 7: Wire `ExportRegionAdminFilter` into the view**

In `src/apps/about/views/admin/export_region_admin_view.py`, replace:

```python
from drf_spectacular.utils import extend_schema

from apps.about.models import ExportRegion
from apps.about.serializers.admin import ExportRegionAdminSerializer
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI


@extend_schema(tags=["About Admin"])
class ExportRegionAdminListCreateView(AdminListCreateAPI):
    queryset = ExportRegion.objects.all()
    serializer_class = ExportRegionAdminSerializer
```

with:

```python
from drf_spectacular.utils import extend_schema

from apps.about.filters import ExportRegionAdminFilter
from apps.about.models import ExportRegion
from apps.about.serializers.admin import ExportRegionAdminSerializer
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI


@extend_schema(tags=["About Admin"])
class ExportRegionAdminListCreateView(AdminListCreateAPI):
    queryset = ExportRegion.objects.all()
    serializer_class = ExportRegionAdminSerializer
    filterset_class = ExportRegionAdminFilter
```

- [ ] **Step 8: Run tests to verify they pass**

Run: `python src/manage.py test apps.about.tests.test_admin_views`
Expected: `OK`

- [ ] **Step 9: Commit**

```bash
git add src/apps/about/filters.py src/apps/about/views/admin/home_slide_admin_view.py src/apps/about/views/admin/stat_admin_view.py src/apps/about/views/admin/timeline_event_admin_view.py src/apps/about/views/admin/export_region_admin_view.py src/apps/about/tests/test_admin_views.py
git commit -m "Add year filter to the TimelineEvent admin list; wire date-range filtering into the other About admin lists"
```

---

### Task 12: Careers admin — `CompanyAdminFilter`, `CareerValueAdminFilter`

**Files:**
- Create: `src/apps/careers/filters.py`
- Modify: `src/apps/careers/views/admin/company_admin_view.py`
- Modify: `src/apps/careers/views/admin/career_value_admin_view.py`
- Test: `src/apps/careers/tests/test_admin_views.py`

**Interfaces:**
- Consumes: `apps.common.filters.SearchFilterSet` (Task 2).
- Produces: `apps.careers.filters.{CompanyAdminFilter, CareerValueAdminFilter}`, wired into their views.

`CareerValue` has no `search_fields`/`list_filter` in `careers/admin.py` — its `FilterSet` exists only for `begin_date`/`end_date` and gets no dedicated test.

- [ ] **Step 1: Write the failing test for `CompanyAdminFilter`**

Append to `src/apps/careers/tests/test_admin_views.py`. Replace the existing import line:

```python
from apps.careers.models import CareerValue
```

with:

```python
from apps.careers.models import CareerValue, Company
```

Then append the test class:

```python


class CompanyAdminFilterTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="admin", password="pass12345", is_staff=True)
        self.client.force_authenticate(self.admin)
        self.acme = Company.objects.create(name="Acme", slug="acme", image="a.jpg")
        Company.objects.create(name="Globex", slug="globex", image="g.jpg")

    def test_search_matches_name(self):
        response = self.client.get(reverse("careers-admin:company-admin-list"), {"search": "Acme"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([item["slug"] for item in response.data], ["acme"])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python src/manage.py test apps.careers.tests.test_admin_views.CompanyAdminFilterTests`
Expected: FAIL — `company-admin-list` currently ignores `search`, both companies come back.

- [ ] **Step 3: Create `apps/careers/filters.py`**

```python
from apps.careers.models import CareerValue, Company
from apps.common.filters import SearchFilterSet


class CompanyAdminFilter(SearchFilterSet):
    search_fields = ("name", "slug")

    class Meta:
        model = Company
        fields = ()


class CareerValueAdminFilter(SearchFilterSet):
    class Meta:
        model = CareerValue
        fields = ()
```

- [ ] **Step 4: Wire `CompanyAdminFilter` into the view**

In `src/apps/careers/views/admin/company_admin_view.py`, replace:

```python
from drf_spectacular.utils import extend_schema

from apps.careers.models import Company
from apps.careers.serializers.admin import CompanyAdminSerializer
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI


@extend_schema(tags=["Careers Admin"])
class CompanyAdminListCreateView(AdminListCreateAPI):
    queryset = Company.objects.all().order_by("name")
    serializer_class = CompanyAdminSerializer
```

with:

```python
from drf_spectacular.utils import extend_schema

from apps.careers.filters import CompanyAdminFilter
from apps.careers.models import Company
from apps.careers.serializers.admin import CompanyAdminSerializer
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI


@extend_schema(tags=["Careers Admin"])
class CompanyAdminListCreateView(AdminListCreateAPI):
    queryset = Company.objects.all().order_by("name")
    serializer_class = CompanyAdminSerializer
    filterset_class = CompanyAdminFilter
```

- [ ] **Step 5: Wire `CareerValueAdminFilter` into the view**

In `src/apps/careers/views/admin/career_value_admin_view.py`, replace:

```python
from drf_spectacular.utils import extend_schema

from apps.careers.models import CareerValue
from apps.careers.serializers.admin import CareerValueAdminSerializer
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI


@extend_schema(tags=["Careers Admin"])
class CareerValueAdminListCreateView(AdminListCreateAPI):
    queryset = CareerValue.objects.all()
    serializer_class = CareerValueAdminSerializer
```

with:

```python
from drf_spectacular.utils import extend_schema

from apps.careers.filters import CareerValueAdminFilter
from apps.careers.models import CareerValue
from apps.careers.serializers.admin import CareerValueAdminSerializer
from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI


@extend_schema(tags=["Careers Admin"])
class CareerValueAdminListCreateView(AdminListCreateAPI):
    queryset = CareerValue.objects.all()
    serializer_class = CareerValueAdminSerializer
    filterset_class = CareerValueAdminFilter
```

- [ ] **Step 6: Run tests to verify they pass**

Run: `python src/manage.py test apps.careers.tests.test_admin_views`
Expected: `OK`

- [ ] **Step 7: Commit**

```bash
git add src/apps/careers/filters.py src/apps/careers/views/admin/company_admin_view.py src/apps/careers/views/admin/career_value_admin_view.py src/apps/careers/tests/test_admin_views.py
git commit -m "Add name/slug search to the Company admin list; wire date-range filtering into CareerValue"
```

---

### Task 13: Partners admin — `PartnerAdminFilter`, `CertificateAdminFilter`

**Files:**
- Create: `src/apps/partners/filters.py`
- Modify: `src/apps/partners/views/admin/partner_admin_view.py`
- Modify: `src/apps/partners/views/admin/certificate_admin_view.py`
- Test: `src/apps/partners/tests/test_admin_views.py`

**Interfaces:**
- Consumes: `apps.common.filters.SearchFilterSet` (Task 2).
- Produces: `apps.partners.filters.{PartnerAdminFilter, CertificateAdminFilter}`, wired into their views.

`Certificate` has no `search_fields`/`list_filter` in `partners/admin.py` — its `FilterSet` exists only for `begin_date`/`end_date` and gets no dedicated test.

- [ ] **Step 1: Write the failing test for `PartnerAdminFilter`**

Append to `src/apps/partners/tests/test_admin_views.py` (existing file already imports `reverse`, `status`, `APITestCase`, `User`, `Partner`):

```python


class PartnerAdminFilterTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="admin", password="pass12345", is_staff=True)
        self.client.force_authenticate(self.admin)
        self.acme = Partner.objects.create(name="Acme", logo="a.jpg")
        Partner.objects.create(name="Globex", logo="g.jpg")

    def test_search_matches_name(self):
        response = self.client.get(reverse("partners-admin:partner-admin-list"), {"search": "Acme"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([item["id"] for item in response.data], [self.acme.id])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python src/manage.py test apps.partners.tests.test_admin_views.PartnerAdminFilterTests`
Expected: FAIL — `partner-admin-list` currently ignores `search`, both partners come back.

- [ ] **Step 3: Create `apps/partners/filters.py`**

```python
from apps.common.filters import SearchFilterSet
from apps.partners.models import Certificate, Partner


class PartnerAdminFilter(SearchFilterSet):
    search_fields = ("name",)

    class Meta:
        model = Partner
        fields = ()


class CertificateAdminFilter(SearchFilterSet):
    class Meta:
        model = Certificate
        fields = ()
```

- [ ] **Step 4: Wire `PartnerAdminFilter` into the view**

In `src/apps/partners/views/admin/partner_admin_view.py`, replace:

```python
from drf_spectacular.utils import extend_schema

from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI
from apps.partners.models import Partner
from apps.partners.serializers.admin import PartnerAdminSerializer


@extend_schema(tags=["Partners Admin"])
class PartnerAdminListCreateView(AdminListCreateAPI):
    queryset = Partner.objects.all().order_by("name")
    serializer_class = PartnerAdminSerializer
```

with:

```python
from drf_spectacular.utils import extend_schema

from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI
from apps.partners.filters import PartnerAdminFilter
from apps.partners.models import Partner
from apps.partners.serializers.admin import PartnerAdminSerializer


@extend_schema(tags=["Partners Admin"])
class PartnerAdminListCreateView(AdminListCreateAPI):
    queryset = Partner.objects.all().order_by("name")
    serializer_class = PartnerAdminSerializer
    filterset_class = PartnerAdminFilter
```

- [ ] **Step 5: Wire `CertificateAdminFilter` into the view**

In `src/apps/partners/views/admin/certificate_admin_view.py`, replace:

```python
from drf_spectacular.utils import extend_schema

from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI
from apps.partners.models import Certificate
from apps.partners.serializers.admin import CertificateAdminSerializer


@extend_schema(tags=["Partners Admin"])
class CertificateAdminListCreateView(AdminListCreateAPI):
    queryset = Certificate.objects.all()
    serializer_class = CertificateAdminSerializer
```

with:

```python
from drf_spectacular.utils import extend_schema

from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI
from apps.partners.filters import CertificateAdminFilter
from apps.partners.models import Certificate
from apps.partners.serializers.admin import CertificateAdminSerializer


@extend_schema(tags=["Partners Admin"])
class CertificateAdminListCreateView(AdminListCreateAPI):
    queryset = Certificate.objects.all()
    serializer_class = CertificateAdminSerializer
    filterset_class = CertificateAdminFilter
```

- [ ] **Step 6: Run tests to verify they pass**

Run: `python src/manage.py test apps.partners.tests.test_admin_views`
Expected: `OK`

- [ ] **Step 7: Commit**

```bash
git add src/apps/partners/filters.py src/apps/partners/views/admin/partner_admin_view.py src/apps/partners/views/admin/certificate_admin_view.py src/apps/partners/tests/test_admin_views.py
git commit -m "Add name search to the Partner admin list; wire date-range filtering into Certificate"
```

---

### Task 14: Pages admin — `StaticPageAdminFilter`

**Files:**
- Create: `src/apps/pages/filters.py`
- Modify: `src/apps/pages/views/admin/static_page_admin_view.py`
- Test: `src/apps/pages/tests/test_admin_views.py`

**Interfaces:**
- Consumes: `apps.common.filters.SearchFilterSet` (Task 2).
- Produces: `apps.pages.filters.StaticPageAdminFilter`, wired into `StaticPageAdminListCreateView`.

`SiteSettings` is a singleton with no list endpoint — out of scope, untouched.

- [ ] **Step 1: Write the failing test**

Append to `src/apps/pages/tests/test_admin_views.py`. Replace the existing import line:

```python
from apps.pages.models import SiteSettings
```

with:

```python
from apps.pages.models import SiteSettings, StaticPage
```

Then append the test class:

```python


class StaticPageAdminFilterTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="admin", password="pass12345", is_staff=True)
        self.client.force_authenticate(self.admin)
        self.privacy = StaticPage.objects.create(slug="privacy-policy", title={"ru": "Приватность", "en": "Privacy"})
        StaticPage.objects.create(slug="terms", title={"ru": "Условия", "en": "Terms"})

    def test_search_matches_slug(self):
        response = self.client.get(reverse("pages-admin:static-page-admin-list"), {"search": "privacy"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([item["id"] for item in response.data], [self.privacy.id])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python src/manage.py test apps.pages.tests.test_admin_views.StaticPageAdminFilterTests`
Expected: FAIL — `static-page-admin-list` currently ignores `search`, both pages come back.

- [ ] **Step 3: Create `apps/pages/filters.py`**

```python
from apps.common.filters import SearchFilterSet
from apps.pages.models import StaticPage


class StaticPageAdminFilter(SearchFilterSet):
    search_fields = ("slug",)

    class Meta:
        model = StaticPage
        fields = ()
```

- [ ] **Step 4: Wire it into the view**

In `src/apps/pages/views/admin/static_page_admin_view.py`, replace:

```python
from drf_spectacular.utils import extend_schema

from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI
from apps.pages.models import StaticPage
from apps.pages.serializers.admin import StaticPageAdminSerializer


@extend_schema(tags=["Pages Admin"])
class StaticPageAdminListCreateView(AdminListCreateAPI):
    queryset = StaticPage.objects.all()
    serializer_class = StaticPageAdminSerializer
```

with:

```python
from drf_spectacular.utils import extend_schema

from apps.common.base_api import AdminDetailAPI, AdminListCreateAPI
from apps.pages.filters import StaticPageAdminFilter
from apps.pages.models import StaticPage
from apps.pages.serializers.admin import StaticPageAdminSerializer


@extend_schema(tags=["Pages Admin"])
class StaticPageAdminListCreateView(AdminListCreateAPI):
    queryset = StaticPage.objects.all()
    serializer_class = StaticPageAdminSerializer
    filterset_class = StaticPageAdminFilter
```

- [ ] **Step 5: Run test to verify it passes**

Run: `python src/manage.py test apps.pages.tests.test_admin_views`
Expected: `OK`

- [ ] **Step 6: Commit**

```bash
git add src/apps/pages/filters.py src/apps/pages/views/admin/static_page_admin_view.py src/apps/pages/tests/test_admin_views.py
git commit -m "Add slug search to the StaticPage admin list"
```

---

### Task 15: Leads admin — `LeadAdminFilter`, `NewsletterSubscriptionAdminFilter`

**Files:**
- Create: `src/apps/leads/filters.py`
- Modify: `src/apps/leads/views/admin/lead_admin_view.py`
- Modify: `src/apps/leads/views/admin/newsletter_subscription_admin_view.py`
- Test: `src/apps/leads/tests/test_admin_views.py`

**Interfaces:**
- Consumes: `apps.common.filters.SearchFilterSet` (Task 2).
- Produces: `apps.leads.filters.{LeadAdminFilter, NewsletterSubscriptionAdminFilter}`, wired into `LeadAdminListView` and `SubscriptionAdminListView`.
- `LeadAdminListView`/`SubscriptionAdminListView` are plain `ListAPIView`s, not `AdminListCreateAPI` — `filterset_class` works identically on both since it comes from the global `DEFAULT_FILTER_BACKENDS` (Task 1), not from `AdminListCreateAPI`.
- `LeadAdminFilter.fields` includes `product` — the one deliberate deviation from `leads/admin.py`'s `list_filter` (approved in the spec).

- [ ] **Step 1: Write the failing tests**

Append to `src/apps/leads/tests/test_admin_views.py`. Replace the existing import block:

```python
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps._auth.models import User
from apps.leads.models import Lead, NewsletterSubscription
```

with:

```python
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps._auth.models import User
from apps.catalog.models import Category, Product
from apps.leads.models import Lead, NewsletterSubscription
```

Then append to the end of the file:

```python


class LeadAdminFilterTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="admin", password="pass12345", is_staff=True)
        self.client.force_authenticate(self.admin)
        category = Category.objects.create(name={"ru": "К", "en": "C"}, slug="cat", image="c.jpg")
        self.product = Product.objects.create(
            category=category,
            name={"ru": "П", "en": "P"},
            slug="p1",
            code="A1",
            box_weight="1.500",
            shelf_life_months=6,
        )
        self.contact_lead = Lead.objects.create(
            type="contact",
            name="Ali",
            email="ali@example.com",
            phone="+998901234567",
            consent_personal_data=True,
            product=self.product,
        )
        self.done_sales_lead = Lead.objects.create(
            type="sales",
            name="Vali",
            email="vali@example.com",
            phone="+998901234568",
            consent_personal_data=True,
            status="done",
        )

    def test_filters_by_type(self):
        response = self.client.get(reverse("leads-admin:lead-admin-list"), {"type": "contact"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([item["id"] for item in response.data], [self.contact_lead.id])

    def test_filters_by_status(self):
        response = self.client.get(reverse("leads-admin:lead-admin-list"), {"status": "done"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([item["id"] for item in response.data], [self.done_sales_lead.id])

    def test_filters_by_product(self):
        response = self.client.get(reverse("leads-admin:lead-admin-list"), {"product": self.product.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([item["id"] for item in response.data], [self.contact_lead.id])

    def test_search_matches_email(self):
        response = self.client.get(reverse("leads-admin:lead-admin-list"), {"search": "vali@example.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([item["id"] for item in response.data], [self.done_sales_lead.id])


class SubscriptionAdminFilterTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="admin", password="pass12345", is_staff=True)
        self.client.force_authenticate(self.admin)
        self.active_sub = NewsletterSubscription.objects.create(email="active@example.com", is_active=True)
        NewsletterSubscription.objects.create(email="inactive@example.com", is_active=False)

    def test_filters_by_is_active(self):
        response = self.client.get(reverse("leads-admin:subscription-admin-list"), {"is_active": "true"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([item["email"] for item in response.data], ["active@example.com"])

    def test_search_matches_email(self):
        response = self.client.get(reverse("leads-admin:subscription-admin-list"), {"search": "inactive"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([item["email"] for item in response.data], ["inactive@example.com"])
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python src/manage.py test apps.leads.tests.test_admin_views.LeadAdminFilterTests apps.leads.tests.test_admin_views.SubscriptionAdminFilterTests`
Expected: FAIL on all — both `lead-admin-list` and `subscription-admin-list` currently ignore every query param, so unfiltered results come back for each assertion.

- [ ] **Step 3: Create `apps/leads/filters.py`**

```python
from apps.common.filters import SearchFilterSet
from apps.leads.models import Lead, NewsletterSubscription


class LeadAdminFilter(SearchFilterSet):
    search_fields = ("name", "email", "phone")

    class Meta:
        model = Lead
        fields = ("type", "status", "product")


class NewsletterSubscriptionAdminFilter(SearchFilterSet):
    search_fields = ("email",)

    class Meta:
        model = NewsletterSubscription
        fields = ("is_active",)
```

- [ ] **Step 4: Wire `LeadAdminFilter` into the view**

In `src/apps/leads/views/admin/lead_admin_view.py`, replace:

```python
from drf_spectacular.utils import extend_schema
from rest_framework import mixins
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from apps.common.base_api import BaseGenericUpdateAPI
from apps.leads.selectors import admin_leads
from apps.leads.serializers.admin import LeadAdminSerializer, LeadStatusUpdateSerializer


@extend_schema(tags=["Leads Admin"])
class LeadAdminListView(ListAPIView):
    serializer_class = LeadAdminSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        return admin_leads()
```

with:

```python
from drf_spectacular.utils import extend_schema
from rest_framework import mixins
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from apps.common.base_api import BaseGenericUpdateAPI
from apps.leads.filters import LeadAdminFilter
from apps.leads.selectors import admin_leads
from apps.leads.serializers.admin import LeadAdminSerializer, LeadStatusUpdateSerializer


@extend_schema(tags=["Leads Admin"])
class LeadAdminListView(ListAPIView):
    serializer_class = LeadAdminSerializer
    permission_classes = (IsAdminUser,)
    filterset_class = LeadAdminFilter

    def get_queryset(self):
        return admin_leads()
```

(leave `LeadAdminDetailView` and `LeadStatusUpdateView` in that file untouched)

- [ ] **Step 5: Wire `NewsletterSubscriptionAdminFilter` into the view**

In `src/apps/leads/views/admin/newsletter_subscription_admin_view.py`, replace:

```python
from drf_spectacular.utils import extend_schema
from rest_framework import mixins
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser

from apps.leads.selectors import admin_subscriptions
from apps.leads.serializers.admin import NewsletterSubscriptionAdminSerializer


@extend_schema(tags=["Leads Admin"])
class SubscriptionAdminListView(ListAPIView):
    serializer_class = NewsletterSubscriptionAdminSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        return admin_subscriptions()
```

with:

```python
from drf_spectacular.utils import extend_schema
from rest_framework import mixins
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser

from apps.leads.filters import NewsletterSubscriptionAdminFilter
from apps.leads.selectors import admin_subscriptions
from apps.leads.serializers.admin import NewsletterSubscriptionAdminSerializer


@extend_schema(tags=["Leads Admin"])
class SubscriptionAdminListView(ListAPIView):
    serializer_class = NewsletterSubscriptionAdminSerializer
    permission_classes = (IsAdminUser,)
    filterset_class = NewsletterSubscriptionAdminFilter

    def get_queryset(self):
        return admin_subscriptions()
```

(leave `SubscriptionAdminDetailView` in that file untouched)

- [ ] **Step 6: Run tests to verify they pass**

Run: `python src/manage.py test apps.leads.tests.test_admin_views`
Expected: `OK`

- [ ] **Step 7: Commit**

```bash
git add src/apps/leads/filters.py src/apps/leads/views/admin/lead_admin_view.py src/apps/leads/views/admin/newsletter_subscription_admin_view.py src/apps/leads/tests/test_admin_views.py
git commit -m "Add type/status/product filters and search to Lead admin list; is_active filter and email search to Subscription admin list"
```

---

### Task 16: Full suite + pre-commit verification

**Files:** none (verification only)

**Interfaces:** none — this task only confirms the sum of Tasks 1-15 is consistent project-wide.

- [ ] **Step 1: Run the full test suite exactly as the pre-commit hook does**

Run: `python src/manage.py test --parallel --exclude-tag=dev-mode`
Expected: `OK`, all apps green, including every test added in Tasks 2-15.

- [ ] **Step 2: Run drf-spectacular schema generation to confirm the new filters don't break schema introspection**

Run: `python src/manage.py spectacular --file /dev/null`
Expected: exits 0 with no errors (the schema for every `filterset_class` — including `django-filter`'s auto-generated query params — must resolve cleanly now that `django_filters` is a registered app from Task 1).

- [ ] **Step 3: Run pre-commit on everything touched**

Run: `pre-commit run --all-files`
Expected: all hooks pass (black, flake8, isort, mypy, migrations-check, django-test). If isort reorders any of the import lines from earlier tasks, accept its output — it's enforcing the project's existing import style, not a functional change.

- [ ] **Step 4: Commit any formatting fixes from Step 3, if pre-commit modified files**

```bash
git add -u
git commit -m "Apply pre-commit formatting fixes"
```

(skip this step entirely if Step 3 made no changes)
