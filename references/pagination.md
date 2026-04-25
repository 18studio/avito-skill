# Pagination

## What Changed In The SDK

The SDK now has a shared pagination layer in `avito.core`:

- `JsonPage` describes one typed page of items plus pagination metadata
- `Paginator` walks page-based or cursor-based sequences
- `PaginatedList` exposes lazy list-like access over multiple pages

This means the skill should no longer assume that every list response is an eager in-memory list.

## Core Mechanics

### `JsonPage`

`JsonPage` carries:

- `items`
- `total`
- `page`
- `per_page`
- `next_cursor`

Its `has_next` logic is:

- `True` when `next_cursor` exists
- otherwise `True` only when `total`, `page`, and `per_page` are known and `page * per_page < total`

Implication:

- page-based endpoints advance through `page` and `per_page`
- cursor-based endpoints advance through `next_cursor`
- if neither path is present, pagination stops

### `Paginator`

`Paginator.iter_pages()` calls `fetch_page(page_number, cursor)` until `page.has_next` becomes false.

Behavior:

- starts with `start_page=1` by default
- switches to cursor mode when `next_cursor` appears
- stops when there is no next page

Use `Paginator.collect()` only when the task truly needs a fully materialized list.

### `PaginatedList`

`PaginatedList` is a lazy `list` subclass.

Important behavior:

- `items[0]` reads only what is already loaded
- `items[50]` loads additional pages only until index `50` is available
- `items[:]` loads all remaining pages
- `len(items)` returns known `total` if available, otherwise loads all pages
- negative indexes force full loading
- comparing to a plain list forces full loading

Treat it as a potentially expensive list.

## Observed SDK Usage

The clearest current implementation is `avito.ads.client.AdsClient.list_items()`.

Behavior there:

1. It makes the first request with `limit` and `offset`.
2. It maps the response into typed items plus `total`.
3. If the first page already covers the dataset, it returns immediately.
4. Otherwise it wraps subsequent page fetching in `Paginator.as_list(...)`.
5. The returned `items` become a lazy `PaginatedList`.

This is important for the skill because a reporting script can accidentally fetch the whole account just by calling `len(result.items)` or slicing everything.

## How To Use Pagination In This Skill

### For reporting scripts

Use lazy traversal when possible:

- top performers
- first failing items
- first matching listings
- previews of large portfolios

Materialize all pages only when the user explicitly asks for:

- full export
- full reconciliation
- complete portfolio audit

### For analytics

Do not assume that “compute stats for all ads” requires loading all ads first.

Prefer:

1. iterate through paginated listings lazily
2. accumulate aggregates incrementally
3. stop early if the business question only needs a threshold or top slice

### For search and promotion workflows

Search-position measurement is scenario-based and usually operates on a small explicit set, so pagination is less central there.

Promotion portfolio workflows can hit large listing sets, so:

- fetch listings lazily
- classify incrementally
- materialize final queues only at the reporting boundary

## Implementation Rules

Use these rules when writing scripts around the SDK:

1. Always set `limit` intentionally on list endpoints.
2. Avoid manual pagination loops when the SDK already returns a lazy paginated result.
3. Use explicit collection only at boundaries where the full dataset is required.
4. Mention in script help or docstrings whether the command streams lazily or loads all pages.
5. When adapting a raw API endpoint into the SDK, expose pagination through `JsonPage` and `Paginator` instead of ad hoc loops.

## Script Contract

For future scripts in this skill, standardize pagination behavior.

Recommended defaults:

- default mode: `streaming`
- explicit full scan mode: `materialize_all`

Recommended CLI shape:

- `--limit 100` for page size
- `--offset 200` only where the SDK method supports an initial window
- `--all-pages` to force complete traversal

Recommended behavior:

- without `--all-pages`, keep traversal lazy and stop as soon as the task is satisfied
- with `--all-pages`, collect all pages deliberately and say so in logs or output metadata
- if a script returns only top-N or previews, do not materialize everything first unless sorting requires the full dataset

## Docstring Template

Use a short docstring block in list-oriented scripts so the behavior is obvious:

```python
"""
List Avito entities using SDK-native pagination.

Pagination mode:
- default: streaming
- with --all-pages: materialize_all

Notes:
- keeps SDK lazy pagination intact by default
- full slices, negative indexes, and forced list conversion may load all pages
"""
```

If the script must always load everything, say that directly instead:

```python
"""
Build a full account report across all available pages.

Pagination mode:
- materialize_all

Notes:
- intentionally collects all pages before aggregation
- use only for exports, audits, or full reconciliation
"""
```

## Risks To Call Out

When using the skill, mention these risks if relevant:

- “all items” may trigger many API calls
- `len()` on a lazy paginated result may be cheap if `total` is known, but not always
- full slices and negative indexes can materialize everything
- cursor-based and page-based endpoints must not be mixed carelessly in one handwritten loop
