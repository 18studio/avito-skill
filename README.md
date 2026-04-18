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

## Validation

The skill structure passes `quick_validate.py`.
