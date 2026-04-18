---
name: avito
description: Manage Avito business workflows through the Avito API and the `avito-py` Python SDK. Use when Codex needs to analyze Avito listing performance, inspect listing statistics, estimate search placement under fixed conditions, compare ads, monitor listing health, or start and adjust paid promotion for Avito listings and accounts.
---

# Avito

## Overview

Use this skill to operate Avito listings as a business system, not as a raw API wrapper. Focus on three core jobs:

1. Read official listing and account performance data from Avito APIs through `avito-py`.
2. Measure search visibility for a listing under explicit, reproducible search conditions.
3. Launch or adjust paid promotion only after checking whether the visibility problem is caused by budget, content quality, or market competition.

Keep a strict distinction between official platform metrics and inferred diagnostics. Do not present sampled search position as a universal or exact rank for all users.

## Operating Model

Split every request into one of these modes before acting:

### 1. Reporting

Use when the user wants facts from Avito data:

- listing views, contacts, favorites, calls, chats, conversion proxies
- promotion spend and uplift
- account-level rollups by seller, category, region, or date range
- deltas versus previous period

Prefer official API responses and derived aggregates.

### 2. Diagnosis

Use when the user wants to know why a listing underperforms:

- weak traffic
- poor contact rate
- falling search visibility
- no effect from promotion

Combine official statistics with search-placement sampling and competitor context. State what is observed versus inferred.

### 3. Action

Use when the user wants to change something:

- start promotion for a listing
- change promotion mode or budget
- pause or resume promotion
- build a shortlist of ads that deserve paid support

Before any action, explain the basis for the recommendation in one short block: current metrics, expected outcome, and operational risk.

## Core Capabilities

### Capability 1. Listing Statistics

When asked for listing performance:

1. Identify the scope: one listing, a seller account, a category slice, or a date range.
2. Pull official data through the SDK client.
3. Normalize metrics into a stable internal shape.
4. Return both raw values and interpretable ratios.

Use a canonical metric layer:

- `views_total`
- `contacts_total`
- `favorites_total`
- `promotion_spend`
- `ctr_like_ratio` if Avito exposes impressions and clicks
- `contact_rate = contacts_total / views_total`
- `favorite_rate = favorites_total / views_total`
- `cpa_like = promotion_spend / contacts_total` when both are available

If the API lacks a metric, mark it unavailable instead of inventing it.

### Capability 2. Search Placement Measurement

Treat search placement as a sampled observation, not a canonical platform metric.

When asked “какое место в поиске”:

1. Fix the search scenario:
   - query text
   - category
   - region or city
   - filters
   - sort mode
   - device surface if relevant
2. Search for the listing using those exact conditions.
3. Record whether the listing is found and at what sampled position.
4. Return the result with caveats:
   - position is scenario-specific
   - ranking may vary by user context and marketplace logic
   - promoted placements and organic placements must be separated if possible

Always store the search scenario alongside the observed position. Without that context, the number is not reusable.

Use this output shape:

- `query`
- `location`
- `category`
- `filters`
- `observed_at`
- `found`
- `observed_position`
- `placement_type` such as `organic`, `promoted`, or `unknown`
- `notes`

### Capability 3. Promotion Management

Promotion actions must be recommendation-driven.

Before starting promotion:

1. Check whether the listing is active and eligible.
2. Review recent statistics and sampled visibility.
3. Classify the bottleneck:
   - no impressions or visibility problem
   - views exist but low contacts: likely content or price problem
   - good contacts already: promotion may be wasteful
4. Recommend one of:
   - do not promote
   - test light promotion
   - intensify promotion
   - stop ineffective promotion

Only then call the promotion endpoint through SDK methods or a thin raw-API fallback if the SDK does not yet expose the method.

### Capability 4. Portfolio Prioritization

Use for accounts with many listings.

Rank listings into action queues:

- `scale`: high conversion, low visibility
- `fix_before_promo`: low conversion and low content quality signals
- `watch`: stable, no immediate action
- `stop_spend`: promotion running without acceptable return

This capability is more valuable than a raw “run promotion” command because it lets the user spend budget where it can compound.

## Workflow

### Request Intake

First normalize the user request into:

- entity scope
- time window
- business question
- desired action

Examples:

- “Покажи статистику по объявлению” -> reporting, single listing
- “Почему объявление просело” -> diagnosis, single listing or cohort
- “Запусти рекламу на лучшие объявления” -> action, portfolio prioritization first

### Data Collection

Collect data in this order:

1. Credentials and account context
2. Listing metadata and current status
3. Statistics and spend
4. Search-placement observations if the task involves visibility
5. Promotion configuration and eligibility if the task involves action

### Decision Layer

Use these high-level rules:

- Low views + low sampled position -> visibility issue, promotion may help
- Good views + weak contacts -> improve listing quality before spending more
- Paid placement present + weak outcomes -> pause or change strategy
- Strong conversion + weak visibility -> best candidate for promotion

Do not jump from “traffic is bad” straight to “buy promotion”. Check whether the listing is worth amplifying.

## SDK Integration Rules

Use `avito-py` as the primary integration layer. Read [references/sdk-integration.md](references/sdk-integration.md) before implementing scripts or API calls.

If the SDK lacks a required method:

1. Confirm whether the underlying Avito API supports the operation.
2. Add a thin local adapter rather than scattering raw HTTP calls across scripts.
3. Keep response normalization in one place.

## Business Scenarios

Read [references/business-scenarios.md](references/business-scenarios.md) when the request is about account operations, KPI review, budget allocation, or rollout sequence.

## Implementation Guidance

When this skill is implemented further, prefer this layout:

- `scripts/auth_check.py`: validate credentials and list available account context
- `scripts/get_listing_stats.py`: fetch raw statistics for one listing or a batch
- `scripts/check_search_position.py`: measure sampled search placement under fixed inputs
- `scripts/manage_promotion.py`: preview, start, pause, or adjust promotion
- `scripts/portfolio_report.py`: build priority queues across many listings

Keep all API-specific field mapping in shared helpers rather than in per-task scripts.
