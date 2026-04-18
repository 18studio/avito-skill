# SDK Integration

## Current Assumption

Use the `avito-py` package from `p141592/avito_python_api` as the primary client for Avito API access.

The public repository and package metadata are minimal, so do not assume broad endpoint coverage without checking the installed package or source tree first.

## Integration Strategy

Build the skill around a thin service layer instead of calling SDK methods directly from task scripts.

Recommended structure:

- `client.py`: construct authenticated SDK client
- `services/stats.py`: listing and account statistics
- `services/search.py`: search-position sampling logic
- `services/promotion.py`: promotion preview and execution
- `services/normalize.py`: map raw SDK responses into stable internal shapes

This prevents SKILL consumers from depending on unstable SDK response details.

## Adapter Rules

### Rule 1. Prefer SDK First

Use SDK methods first for:

- auth and token handling
- official listing data
- statistics endpoints
- promotion endpoints if exposed

### Rule 2. Centralize Raw API Fallbacks

If a required Avito API method exists but the SDK does not expose it:

1. Add one adapter in the shared client layer.
2. Keep request and response shape documented next to that adapter.
3. Reuse the normalized output everywhere else.

Do not scatter `requests` calls across multiple scripts.

### Rule 3. Normalize Early

Convert SDK objects or raw API payloads into stable dictionaries early:

```python
{
    "listing_id": "...",
    "views_total": 0,
    "contacts_total": 0,
    "favorites_total": 0,
    "promotion_spend": 0,
    "period_start": "...",
    "period_end": "...",
}
```

This makes downstream reporting and decision logic deterministic.

## Search Position Is Not a Native Fact

Search placement is usually not the same type of data as official listing statistics. Treat it as a measured observation built from a fixed search scenario.

Implement it as a separate service:

- accept explicit search inputs
- execute reproducible lookup logic
- return observed rank plus scenario metadata

Do not merge it into the official stats payload as if it came directly from the same source.

## Promotion Safety

Promotion endpoints change money exposure, so add a preview mode first.

Recommended behavior:

1. `preview` computes the decision and intended parameters
2. `execute` applies the change
3. `verify` fetches resulting state if possible

Even when the user asks to “запусти рекламу”, prepare a short intent summary before execution.

## Validation Checklist

Before writing real scripts, verify:

1. How the SDK authenticates
2. Which statistics endpoints are exposed
3. Whether promotion methods exist in the SDK
4. Whether search APIs can be used for scenario-based rank checks
5. Which fields are stable enough for normalization

If any of these are missing, document the gap and isolate the workaround in one adapter.
