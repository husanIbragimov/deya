**Global rules for every task below:**

- All API paths end with a **trailing slash** (`/api/v1/admin/.../`). Missing slash = 400/301.
- All translatable fields are multilingual objects: `{ "en": "...", "ru": "...", "uz": "..." }`.
  Never render such an object directly in JSX — always pass it through a `tr(value, locale)` helper,
  otherwise React throws `Objects are not valid as a React child (found: object with keys {en, ru, uz})`.
- Admin forms use RU / UZ / EN tabs; each input is bound to a **scalar string**, never to the whole object.
- Images are optional everywhere. If the API returns `""` or `null`, do **not** render `<Image src="">` —
  render a placeholder instead (empty-string `src` makes the browser re-download the page).
- List endpoints return a paginated envelope `{ count, next, previous, results }` — don't assume a bare array.
- Use `PATCH` for edits (send only changed fields), `PUT` only where full replacement is required.

Standard CRUD shape used in all tasks:

```
GET    /api/v1/admin/<module>/          list
POST   /api/v1/admin/<module>/          create
GET    /api/v1/admin/<module>/{id}/     retrieve
PUT    /api/v1/admin/<module>/{id}/     full update
PATCH  /api/v1/admin/<module>/{id}/     partial update
DELETE /api/v1/admin/<module>/{id}/     delete
```

---

## 1. Home page — text blocks CRUD

**Page:** `/[locale]` (screenshot: "Создаём вкус, которому доверяют с 1994 года" + counters row)
**Status:** content is hardcoded.

Make every text unit on the home page editable from the admin.

- [ ] Backend: model for home-page text blocks with a `block_type` / `key` field so each block is addressable
      (`hero_eyebrow`, `hero_title`, `intro_left`, `intro_right`, `cta_link_text`, `cta_link_url`).
- [ ] Support **rich text** where bold fragments are needed — the intro paragraphs contain bold spans
      (`более 200 наименований продукции`, `25 стран мира`). Store as HTML, not plain text.
- [ ] Counters block is a separate repeatable model: `value` (`12+`, `25`, `60`, `90`, `77`),
      `label` (translatable), `order`, `is_active`.
      **Bug:** two counters currently show placeholder labels `as` and `ass` — real labels must come from the API.
- [ ] Admin UI: "Главная" section with the block list + edit modal (RU/UZ/EN tabs) and a sortable counters table.
- [ ] Frontend: fetch by locale, render with `tr()`, sanitize the rich-text HTML before `dangerouslySetInnerHTML`.

---

## 2. Privacy policy page — CRUD

**Page:** `/[locale]/privacy-policy` ("Политика конфиденциальности")
**Status:** static text in the codebase.

- [ ] Backend: single-record (singleton) model — `title` + `body` (rich text), per locale.
      The document has numbered sections (1., 1.1., 2.1. …), bold headings and inline links
      (`https://deya.uz` rendered in red) — the editor must preserve all of that, so a **rich-text field is required**,
      plain textarea is not enough.
- [ ] API: `GET /api/v1/pages/privacy-policy/` public, admin CRUD under `/api/v1/admin/pages/privacy-policy/`.
      If a generic "Страницы" module already exists in the admin sidebar, attach it there instead of a new module.
- [ ] Admin: WYSIWYG editor with RU/UZ/EN tabs, preview, save.
- [ ] Frontend: render sanitized HTML, keep the existing typography and the "Вернуться на главную" link.

---

## 3. Personal data consent page — CRUD

**Page:** `/[locale]/personal-data-consent` ("Согласие на обработку персональных данных")
**Status:** static text.

- [ ] Same treatment as task 2 — singleton page model, rich text, three locales.
- [ ] Content contains bulleted lists (`— имя`, `— адрес электронной почты`, …) and numbered headings —
      the editor must support lists and bold.
- [ ] **Bug in current content:** section numbering is broken — there are two sections numbered "1"
      ("1. Общие положения" and "1. Персональные данные"). Fix once the content is editable.
- [ ] Public endpoint + admin CRUD, wired into the same "Страницы" module as privacy policy.

---

## 4. About page — second block CRUD

**Page:** `/[locale]/about` (screenshot: founder photo block, "Икрамов Рустам Алиевич" + quote)
**Status:** hardcoded.

- [ ] Backend model for the block: `title` (rich text — part of the heading is styled),
      `description`, `image` (background/portrait), `person_name`, `person_quote`, all translatable except image.
- [ ] Admin: form under "О нас" with image upload + replace, RU/UZ/EN tabs.
- [ ] Frontend: render from API; guard the image (`src` may be null) and keep the dark overlay so
      white text stays readable.
- [ ] **Layout bug visible in the screenshot:** the block heading is hidden behind the fixed header
      ("…истории людей, которые" is cut off at the top). Add top padding / offset equal to the header height.

---

## 5. FIX — admin category edit is broken

**Page:** `deya-admin.netlify.app/catalog/categories` → edit modal
**Observed:** `PUT https://deya.uz/api/v1/admin/catalog/categories/4/` → **400 Bad Request**

- [ ] Read the actual 400 response body and map the field errors — do not guess.
- [ ] Most likely causes to check, in order:
  1. **Partial multilingual payload.** The modal edits one locale tab at a time (UZ shown in the screenshot),
     but `PUT` requires the *full* object. Sending `name: { uz: "ПЕРСИК uz" }` drops `ru`/`en` and fails validation.
     → Switch to `PATCH`, or merge the untouched locales back into the payload before `PUT`.
  2. **Slug.** Value is `uz` in the screenshot — this looks like the locale code leaking into the slug field.
     Slug must be unique and generated from the RU/EN name, not the tab code. Check uniqueness validation.
  3. **Image field.** When the image is unchanged, the form may be re-sending the image URL string where the
     API expects a file upload or an omitted field. Omit the key entirely if the user didn't touch it;
     send `image: null` only for explicit removal. Use `multipart/form-data` when a new file is attached,
     `application/json` otherwise.
  4. **`order` / `status`** type mismatch (string `"6"` vs int, `on/off` vs boolean).
- [ ] Surface backend field errors in the modal (including nested keys like `name.ru`) instead of a silent failure.
- [ ] Add a regression check: edit a category changing only the UZ name → saves successfully, RU/EN untouched.
- [ ] Console shows **38 errors / 84 warnings** on this page — triage them separately.

---

## 6. Partners page — first block CRUD

**Page:** `/[locale]/partners` ("Как стать партнёром?")
**Status:** hardcoded hero.

- [ ] Backend model: `photo` (background image), `title`, `description`, plus button `label` + `link`
      for "ФОРМА ДЛЯ ПАРТНЁРОВ".
- [ ] Admin: "Партнёры" section → hero block form, image upload with preview/replace, RU/UZ/EN tabs.
- [ ] Frontend: render from API. Background image must have a fallback and an overlay so the white
      heading stays legible on light photos.

---

## 7. Careers page — first block + info blocks CRUD

**Page:** `/[locale]/careers` ("Присоединяйтесь к Deya")

### 7a. Hero block
- [ ] Model: `title`, `description`, background `image`, button `label` + `link` ("ВАКАНСИИ").
- [ ] Admin form + frontend integration, same rules as above.

### 7b. Info blocks below the hero
Screenshot shows: heading "Мы каждый день стремимся сделать работу в Deya комфортной" + several
paragraphs on the left and a product image on the right.

- [ ] Model: `title` (rich text — the word "Deya" is highlighted red inside the heading),
      `description` (rich text, multiple paragraphs, first one italic), `image`, `order`, `is_active`.
- [ ] **Only two layout formats allowed** — add a `layout` choice field:
      - `text_left_image_right`
      - `image_left_text_right`
      Admin picks one of the two on create; no other variants. Frontend renders accordingly.
- [ ] Admin: repeatable block list with add / edit / delete / reorder.

---

## 8. Careers page — companies block, rich text

**Page:** `/[locale]/careers`, section "Узнайте больше о работе в Deya и найдите подходящую вам должность"
(cards: Bonu Shirinliklar, Iruskon, Sami by Deya, Вкусная булка)

- [ ] Backend: company model with `name`, `image`, and a **long-form rich-text `description`**
      (the Bonu Shirinliklar card has multiple paragraphs) — field must be `TextField`/HTML, not `CharField`.
- [ ] API must accept and return HTML safely: configure the serializer to allow the tag whitelist
      (`p, br, strong, em, ul, ol, li, a`) and strip everything else server-side.
- [ ] Frontend: rich-text editor in admin (same editor as tasks 2, 3 and 9 — pick **one** library for the whole
      project and reuse it), sanitized render on the public page.
- [ ] Overflow behaviour: long descriptions must not break the card grid — clamp with "show more" or scroll.

---

## 9. Blog — rich text editor + API format fix

**Pages:** admin "Блог" → new/edit post; public blog detail page.

- [ ] Replace the plain textarea with a **rich-text editor** (headings, bold/italic, lists, links,
      inline images, quotes).
- [ ] **Fix the API format mismatch** — decide on one canonical storage format and align both sides:
      recommended is sanitized HTML; if the backend currently stores editor-specific JSON
      (Editor.js / Tiptap doc), either serialize to HTML on save or add a converter on read.
      Document the chosen format in the API docs so both sides stop drifting.
- [ ] Content must stay per-locale: `content: { ru, uz, en }` as HTML strings.
- [ ] Sanitize on the server (never trust the client) and again on render.
- [ ] Handle inline image uploads from the editor: upload endpoint returns a URL that gets embedded in the HTML.
- [ ] Verify existing posts still render after the format change — write a migration if the stored format changes.

---

## Cross-cutting cleanup

- [ ] Add the shared `tr(value, locale)` helper and the `Translated` type; audit **all** pages for raw
      multilingual objects passed into JSX, `value=`, or template literals.
- [ ] Add the shared image guard / placeholder component; audit every `<Image>` whose `src` comes from the API.
- [ ] One rich-text editor library across the whole admin, one sanitizer config across the whole frontend.
- [ ] Loading skeletons, empty states and error states for every new list and detail fetch.
- [ ] React Query keys per module with invalidation on create/update/delete.
- [ ] Toasts on success/failure; backend field errors mapped onto the right inputs.
