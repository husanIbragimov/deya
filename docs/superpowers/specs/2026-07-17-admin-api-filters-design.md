# Admin API filtering & search (django-filter)

Date: 2026-07-17
Status: Approved

## Problem

None of the admin CRUD list endpoints (`AdminListCreateAPI` subclasses across
`catalog`, `blog`, `about`, `careers`, `partners`, `pages`, `leads`) support
filtering or search. The one exception, `ProductListView` (public), already
uses `django_filters` via a hand-rolled `ProductFilter`. Content managers
using the admin API have no way to narrow these lists other than pulling the
whole table and filtering client-side.

## Scope

Admin list endpoints only (all `AdminListCreateAPI` views, plus the two
`leads` admin `ListAPIView`s: `LeadAdminListView`, `SubscriptionAdminListView`).
Public list endpoints are out of scope except for the existing
`ProductListView`, which gets refactored (not functionally changed) to reuse
the new shared base.

## Global settings changes

- `src/config/settings/apps.py`: add `"django_filters"` to `THIRD_PARTY_APPS`.
  It's already a dependency (`requirements/base.txt`) but isn't registered as
  an installed app, which `django-filter` wants for schema/template support.
- `src/config/settings/rest_framework.py`: add
  `"DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",)`
  to `REST_FRAMEWORK`. Every view that sets `filterset_class` picks up
  filtering automatically; views without one are unaffected. Removes the need
  to repeat `filter_backends = (DjangoFilterBackend,)` on ~19 views.

## Shared filter base (`apps/common/filters.py`)

`BaseFilter` (existing) is unchanged — it contributes `begin_date`/`end_date`
range filters on `created_at`, which every model gets for free via
`BaseModel`.

Add a new `SearchFilterSet(BaseFilter)` that generalizes the manual
`Q(...) | Q(...)` search pattern currently hand-written in
`apps/catalog/filters.py::ProductFilter`:

```python
class SearchFilterSet(BaseFilter):
    search = django_filters.CharFilter(method="filter_search")
    search_fields = ()          # plain CharField/EmailField names
    locale_search_fields = ()   # JSONField translatable names (ru/en)

    def filter_search(self, queryset, name, value):
        query = Q()
        for field in self.search_fields:
            query |= Q(**{f"{field}__icontains": value})
        for field in self.locale_search_fields:
            query |= Q(**{f"{field}__ru__icontains": value}) | Q(**{f"{field}__en__icontains": value})
        return queryset.filter(query) if query else queryset
```

Each per-app `FilterSet` subclasses `SearchFilterSet`, sets `Meta.model` /
`Meta.fields` for exact-match filters, and sets `search_fields` /
`locale_search_fields` for the `search` param. A `FilterSet` with nothing to
search just omits both and gets `search`-less, date-range-only filtering.

`ProductFilter` is rebased onto `SearchFilterSet` (was `django_filters.FilterSet`
directly): its existing `category`/`badge`/`family`/`search` behavior is
unchanged, it gains `begin_date`/`end_date`, and its custom `filter_search`
method is replaced by `search_fields = ("code",)` /
`locale_search_fields = ("name", "description")`.

## Per-app field mapping

Source of truth: each model's existing `admin.py` `list_filter` (→ exact
`Meta.fields`) and `search_fields` (→ `search_fields`/`locale_search_fields`).
One deliberate deviation is called out below.

| App | New FilterSet | Wired into view | Exact filters | Search fields |
|---|---|---|---|---|
| catalog | `CategoryAdminFilter` | `CategoryAdminListCreateView` | `is_active` | `name` (locale), `slug` |
| catalog | `FlavorAdminFilter` | `FlavorAdminListCreateView` | — | `name` (locale), `slug` |
| catalog | `WeightAdminFilter` | `WeightAdminListCreateView` | `unit` | — |
| catalog | `ProductFamilyAdminFilter` | `ProductFamilyAdminListCreateView` | — | `name`, `slug` (plain) |
| catalog | `ProductAdminFilter` (rename/extend of `ProductFilter`) | `ProductAdminListCreateView` | `category`, `family`, `flavor`, `badge`, `is_featured`, `is_active` | `code` (plain), `name` (locale), `slug` |
| catalog | `ProductImageAdminFilter` | `ProductImageAdminListCreateView` | `product`, `is_main` | — |
| blog | `PostAdminFilter` | `PostAdminListCreateView` | `is_published` | `title` (locale), `slug` |
| blog | `PostBlockAdminFilter` | `PostBlockAdminListCreateView` | `post`, `type` | — |
| about | `HomeSlideAdminFilter` | `HomeSlideAdminListCreateView` | — | — (date-range only) |
| about | `StatAdminFilter` | `StatAdminListCreateView` | — | — (date-range only) |
| about | `TimelineEventAdminFilter` | `TimelineEventAdminListCreateView` | `year` | — |
| about | `ExportRegionAdminFilter` | `ExportRegionAdminListCreateView` | — | — (date-range only) |
| careers | `CompanyAdminFilter` | `CompanyAdminListCreateView` | — | `name`, `slug` (plain) |
| careers | `CareerValueAdminFilter` | `CareerValueAdminListCreateView` | — | — (date-range only) |
| partners | `PartnerAdminFilter` | `PartnerAdminListCreateView` | — | `name` (plain) |
| partners | `CertificateAdminFilter` | `CertificateAdminListCreateView` | — | — (date-range only) |
| pages | `StaticPageAdminFilter` | `StaticPageAdminListCreateView` | — | `slug` (plain) |
| leads | `LeadAdminFilter` | `LeadAdminListView` | `type`, `status`, `product` | `name`, `email`, `phone` (plain) |
| leads | `NewsletterSubscriptionAdminFilter` | `SubscriptionAdminListView` | `is_active` | `email` (plain) |

**Deviation from admin.py:** `Lead.product` is added as an exact filter even
though Django admin doesn't `list_filter` on it. It's a natural, high-value
API filter ("all leads for product X"), consistent with how
`ProductImageAdminFilter`/`PostBlockAdminFilter` already filter by their
parent FK.

Models with neither exact filters nor search (`HomeSlide`, `Stat`,
`ExportRegion`, `CareerValue`, `Certificate`) still get `begin_date`/`end_date`
via `SearchFilterSet` → `BaseFilter`. This matches their `admin.py`, which
also has no `list_filter`/`search_fields` for them — they're small reference
tables.

## File layout

New `filters.py` (flat file, matching each app's existing flat-vs-package
convention) in: `about`, `blog`, `careers`, `partners`, `pages`, `leads`.
`catalog` already has `filters.py` — extended in place with the five new
`FilterSet`s alongside the rebased `ProductFilter`/`ProductAdminFilter`.

## View wiring

Each affected view adds one line, `filterset_class = <Filter>`, and one
import. No other behavior change — `queryset`/`serializer_class`/permissions
untouched. Example (`catalog/views/admin/category_admin_view.py`):

```python
class CategoryAdminListCreateView(AdminListCreateAPI):
    queryset = Category.objects.all().order_by("sort_order", "id")
    serializer_class = CategoryAdminSerializer
    filterset_class = CategoryAdminFilter
```

`ProductListView` (public) keeps `filter_backends = (DjangoFilterBackend,)`
explicit for clarity even though it's now redundant with the global default,
since removing it isn't required — but the plan will drop it during the
`ProductFilter` rebase for consistency with every other view (no view needs
to set `filter_backends` anymore).

## Testing

Each app already has `tests/test_admin_views.py`. Add filter/search
assertions there per app, following existing test conventions (helpers in
`tests/helpers.py` for object creation). At minimum, per app with a non-empty
filter/search set: one test proving an exact-filter param narrows the list,
one proving `search` matches on a locale or plain field and excludes
non-matches. Apps with date-range-only filtering (no exact/search fields) are
not required to get a new test — `BaseFilter`'s `begin_date`/`end_date` is
already generic, shared behavior.

Run `python src/manage.py test --parallel --exclude-tag=dev-mode` (the
pre-commit `django-test` hook) before considering the work done.

## Out of scope

- Public list endpoints other than `ProductListView` (`CategoryListView`,
  `PostListView`, `TimelineListView`, `CareerValueListView`,
  `CompanyListView`, `CertificateListView`, `PartnerListView`).
- `OrderingFilter` / sort-by-field support — not requested, and django-filter
  doesn't provide it (it's a separate DRF backend).
- Pagination changes.
