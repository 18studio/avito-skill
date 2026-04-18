# Avito Skill

Skill for operating Avito business workflows through the Avito API and the `avito-py` Python SDK.

## Purpose

The skill is designed around three jobs:

1. Read official listing and account statistics.
2. Estimate listing visibility in search under a fixed scenario.
3. Decide when to launch, change, or stop paid promotion.

## Current Status

The repository currently contains the skill definition and reference materials:

- `SKILL.md` - core operating logic of the skill
- `agents/openai.yaml` - UI metadata
- `references/business-scenarios.md` - business use cases and KPI interpretation
- `references/sdk-integration.md` - integration rules for `avito-py`

The Python implementation is not added yet. The next step is to verify actual SDK coverage and then implement the first scripts.

## Example Prompts

Examples of user requests that should trigger this skill:

- `Используй $avito и покажи статистику по объявлению 123456 за последние 14 дней`
- `Используй $avito и сравни эффективность этих 5 объявлений`
- `Используй $avito и оцени, стоит ли запускать рекламу на это объявление`
- `Используй $avito и проверь место объявления в поиске по запросу "диван", Москва, категория "Мебель"`
- `Используй $avito и найди объявления, где есть смысл усилить продвижение`
- `Используй $avito и собери еженедельный отчет по просадке трафика и контактов`

## Planned Scripts

- `scripts/auth_check.py`
- `scripts/get_listing_stats.py`
- `scripts/check_search_position.py`
- `scripts/manage_promotion.py`
- `scripts/portfolio_report.py`

## Main Principles

- Treat Avito statistics as official API data.
- Treat search position as a sampled measurement tied to a specific search scenario.
- Do not launch promotion blindly; first determine whether the bottleneck is visibility or listing quality.

## Environment and Auth

The exact auth flow must be aligned with real `avito-py` SDK behavior and Avito API requirements. Until the scripts are implemented, use a conservative configuration contract and keep auth handling centralized.

Suggested environment variables:

- `AVITO_CLIENT_ID` - Avito API client identifier
- `AVITO_CLIENT_SECRET` - Avito API client secret
- `AVITO_ACCESS_TOKEN` - optional pre-issued access token if the SDK supports direct token usage
- `AVITO_BASE_URL` - optional API base URL override for testing or environment differences
- `AVITO_ACCOUNT_ID` - optional default account or profile context

Auth rules:

- Build one shared client factory and reuse it across all scripts.
- Do not hardcode tokens or secrets in scripts or reference files.
- Prefer SDK-native token management if `avito-py` already implements it.
- If token refresh is needed, keep it in one adapter layer.
- Fail fast on missing credentials and return a clear configuration error.

Recommended implementation sequence:

1. Implement `scripts/auth_check.py`.
2. Verify what auth inputs `avito-py` actually accepts.
3. Adjust environment variable names only after that verification.
4. Reuse the same auth bootstrap in all other scripts.

## Validation

The skill structure passes `quick_validate.py`.
