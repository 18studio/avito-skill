# Avito Business Skill Plan

## SDK Constraint

Use only `avito-py` from `p141592/avito_python_api`:

- Docs: https://p141592.github.io/avito_python_api/
- GitHub: https://github.com/p141592/avito_python_api

Do not use other Avito SDKs, unofficial wrappers, scraping, or direct HTTP unless `avito-py` lacks the required operation and the user explicitly approves a fallback.

`avito-py` is a synchronous Python SDK built around `AvitoClient`. It hides transport, OAuth, and retry logic, returns typed dataclass models, and covers Avito API operations through domain objects.

## Skill Goal

Create an Avito business-logic skill, not an SDK reference skill.

The skill should translate business-user requests into `avito-py` workflows for Avito classified operations:

- Listing health and diagnostics
- Promotion ROI and paid service planning
- Lead leakage across chats, calls, and contacts
- Order, delivery, label, and stock workflows
- Review and reputation management
- Realty pricing, analytics, and bookings
- Jobs, vacancies, applications, and resumes
- Account, balance, employee, and tariff diagnostics

The skill should start from the user's business goal, collect the relevant account/listing/lead/order data, compute a business diagnosis, recommend actions, and require explicit confirmation before write, paid, or reputation-affecting operations.

## Recommended Structure

```text
avito/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── sdk-domain-map.md
│   ├── business-scenarios.md
│   ├── decision-rules.md
│   └── safety.md
└── scripts/
    ├── avito_smoke_check.py
    ├── listing_health_report.py
    └── promotion_decision_preview.py
```

Do not add extra docs such as `README.md`, `INSTALLATION_GUIDE.md`, or `QUICK_REFERENCE.md`.

## SKILL.md Content

Keep `SKILL.md` concise. It should contain:

- Frontmatter with `name: avito`.
- A trigger description covering Avito business workflows through `avito-py`.
- A core rule: use `avito-py` only.
- A business-first workflow:
  1. Identify the business goal.
  2. Identify account/user/item/order/chat scope.
  3. Read relevant data first.
  4. Compute business diagnosis.
  5. Present recommended actions.
  6. Require confirmation before paid, write, or destructive operations.
- Reference navigation:
  - Read `references/sdk-domain-map.md` when mapping a business request to SDK domains.
  - Read `references/business-scenarios.md` for workflow patterns.
  - Read `references/decision-rules.md` for business heuristics.
  - Read `references/safety.md` before write, paid, or reputation-affecting actions.

## Exact SDK Domains To Reference

Use these `avito-py` namespaces and public methods in the skill references.

### Account

- `avito.accounts.Account`
  - `get_self()`
  - `get_balance()`
  - `get_operations_history()`

- `avito.accounts.AccountHierarchy`
  - `get_status()`
  - `list_employees()`
  - `list_company_phones()`
  - `list_items_by_employee()`
  - `link_items()`

### Listings And Stats

- `avito.ads.Ad`
  - `list()`
  - `get()`
  - `update_price()`

- `avito.ads.AdStats`
  - `get_item_stats()`
  - `get_item_analytics()`
  - `get_account_spendings()`
  - `get_calls_stats()`

- `avito.ads.AdPromotion`
  - `get_vas_prices()`
  - `apply_vas()`
  - `apply_vas_direct()`
  - `apply_vas_package()`

### Promotion

- `avito.promotion.PromotionOrder`
  - `get_service_dictionary()`
  - `list_services()`
  - `list_orders()`
  - `get_order_status()`

- `avito.promotion.BbipPromotion`
  - `get_suggests()`
  - `get_forecasts()`
  - `create_order()`

- `avito.promotion.AutostrategyCampaign`
  - `create_budget()`
  - `create()`
  - `update()`
  - `get()`
  - `delete()`
  - `list()`
  - `get_stat()`

- `avito.promotion.TargetActionPricing`
  - `get_bids()`
  - `get_promotions_by_item_ids()`
  - `update_auto()`
  - `update_manual()`
  - `delete()`

- `avito.promotion.CpaAuction`
  - `get_user_bids()`
  - `create_item_bids()`

- `avito.promotion.TrxPromotion`
  - `get_commissions()`
  - `apply()`
  - `delete()`

### Leads, Chats, Calls

- `avito.messenger.Chat`
  - `list()`
  - `get()`
  - `mark_read()`
  - `blacklist()`

- `avito.messenger.ChatMessage`
  - `list()`
  - `send_message()`
  - `send_image()`
  - `delete()`

- `avito.messenger.ChatMedia`
  - `get_voice_files()`
  - `upload_images()`

- `avito.messenger.ChatWebhook`
  - `list()`
  - `subscribe()`
  - `unsubscribe()`

- `avito.messenger.SpecialOfferCampaign`
  - `get_available()`
  - `create_multi()`
  - `confirm_multi()`
  - `get_stats()`
  - `get_tariff_info()`

- `avito.cpa.CpaCall`
  - `list()`
  - `create_complaint()`

- `avito.cpa.CpaChat`
  - `get()`
  - `list()`
  - `get_phones_info_from_chats()`

- `avito.cpa.CpaLead`
  - `get_balance_info()`
  - `create_complaint_by_action_id()`

- `avito.cpa.CallTrackingCall`
  - `get()`
  - `list()`
  - `download()`

### Orders, Delivery, Stock

- `avito.orders.Order`
  - `list()`
  - `apply()`
  - `check_confirmation_code()`
  - `set_cnc_details()`
  - `get_courier_delivery_range()`
  - `set_courier_delivery_range()`
  - `update_tracking_number()`
  - `accept_return_order()`
  - `update_markings()`

- `avito.orders.OrderLabel`
  - `create()`
  - `download()`

- `avito.orders.Stock`
  - `get()`
  - `update()`

- `avito.orders.DeliveryOrder`
  - `create()`
  - `create_announcement()`
  - `delete()`
  - `create_change_parcel_result()`
  - `update_change_parcels()`

- `avito.orders.DeliveryTask`
  - `get()`

- `avito.orders.SandboxDelivery`
  - Use only for sandbox delivery workflows.

### Reviews And Ratings

- `avito.ratings.Review`
  - `list()`

- `avito.ratings.ReviewAnswer`
  - `create()`
  - `delete()`

- `avito.ratings.RatingProfile`
  - `get()`

### Realty

- `avito.realty.RealtyAnalyticsReport`
  - `get_market_price_correspondence()`
  - `get_report_for_classified()`

- `avito.realty.RealtyBooking`
  - `list_realty_bookings()`
  - `update_bookings_info()`

- `avito.realty.RealtyPricing`
  - `update_realty_prices()`

- `avito.realty.RealtyListing`
  - `get_intervals()`
  - `update_base_params()`

### Jobs

- `avito.jobs.Vacancy`
  - `list()`
  - `get()`
  - `get_by_ids()`
  - `get_statuses()`
  - `create()`
  - `update()`
  - `delete()`
  - `prolongate()`
  - `update_auto_renewal()`

- `avito.jobs.Application`
  - `list()`
  - `get_states()`
  - `apply()`
  - `update()`

- `avito.jobs.Resume`
  - `list()`
  - `get()`
  - `get_contacts()`

- `avito.jobs.JobWebhook`
  - `get()`
  - `list()`
  - `update()`
  - `delete()`

- `avito.jobs.JobDictionary`
  - `list()`
  - `get()`

### Autoload

- `avito.ads.AutoloadProfile`
  - `get()`
  - `save()`
  - `upload_by_url()`
  - `get_tree()`
  - `get_node_fields()`

- `avito.ads.AutoloadReport`
  - `list()`
  - `get()`
  - `get_last_completed()`
  - `get_items()`
  - `get_items_info()`
  - `get_fees()`
  - `get_ad_ids_by_avito_ids()`
  - `get_avito_ids_by_ad_ids()`

### Tariffs And Automotive

- `avito.tariffs.Tariff`
  - `get_tariff_info()`

- `avito.autoteka.*`
  - Use only for automotive workflows where Autoteka reports, previews, scoring, monitoring, or valuation are directly relevant.

## Business Scenarios

### Listing Health

Use:

- `Ad.list()`
- `Ad.get()`
- `AdStats.get_item_stats()`
- `AdStats.get_item_analytics()`
- `AdStats.get_calls_stats()`
- `AdStats.get_account_spendings()`

Business outputs:

- Underperforming listings
- Strong listings worth scaling
- High views with low contacts
- High contacts with weak order/sale progress
- Stale inventory
- Price-change candidates
- Listings needing content/photos/category fixes before promotion

### Promotion Decision

Use:

- `AdStats.get_item_stats()`
- `AdStats.get_account_spendings()`
- `AdPromotion.get_vas_prices()`
- `PromotionOrder.list_services()`
- `PromotionOrder.list_orders()`
- `BbipPromotion.get_suggests()`
- `BbipPromotion.get_forecasts()`
- `AutostrategyCampaign.create_budget()`
- `AutostrategyCampaign.get_stat()`
- `TargetActionPricing.get_bids()`
- `TargetActionPricing.get_promotions_by_item_ids()`

Business outputs:

- Promote
- Do not promote
- Improve listing first
- Stop or reduce spend
- Test lower budget
- Use manual/auto target-action pricing
- Use BBIP forecast/suggests before order creation

### Paid Promotion Execution

Only after explicit confirmation, use:

- `AdPromotion.apply_vas()`
- `AdPromotion.apply_vas_direct()`
- `AdPromotion.apply_vas_package()`
- `BbipPromotion.create_order()`
- `AutostrategyCampaign.create()`
- `AutostrategyCampaign.update()`
- `AutostrategyCampaign.delete()`
- `TargetActionPricing.update_auto()`
- `TargetActionPricing.update_manual()`
- `TargetActionPricing.delete()`
- `TrxPromotion.apply()`
- `TrxPromotion.delete()`
- `CpaAuction.create_item_bids()`

Before execution, show:

- Item IDs
- Service/campaign type
- Expected cost or budget
- Forecast or bid data where available
- Business reason
- Reversal/stop option if available

### Lead Leakage

Use:

- `Chat.list()`
- `Chat.get()`
- `ChatMessage.list()`
- `AdStats.get_calls_stats()`
- `CpaCall.list()`
- `CpaChat.list()`
- `CallTrackingCall.list()`

Business outputs:

- Unanswered chats
- Old unread chats
- Missed calls
- Slow-response risk
- Leads by listing
- Suggested replies
- Complaint candidates for CPA leads

### Messenger Actions

Only after explicit confirmation, use:

- `ChatMessage.send_message()`
- `ChatMessage.send_image()`
- `ChatMessage.delete()`
- `Chat.mark_read()`
- `Chat.blacklist()`
- `SpecialOfferCampaign.create_multi()`
- `SpecialOfferCampaign.confirm_multi()`

### Orders, Delivery, Labels, Stock

Use:

- `Order.list()`
- `Order.apply()`
- `Order.check_confirmation_code()`
- `Order.update_tracking_number()`
- `OrderLabel.create()`
- `OrderLabel.download()`
- `Stock.get()`
- `Stock.update()`

Business outputs:

- Orders needing seller action
- Orders missing tracking
- Return orders needing acceptance
- Label generation candidates
- Stock mismatches
- Out-of-stock ads that should not be promoted

### Reviews And Reputation

Use:

- `Review.list()`
- `RatingProfile.get()`
- `ReviewAnswer.create()`
- `ReviewAnswer.delete()`

Business outputs:

- Negative reviews without answer
- Review themes
- Rating risk
- Draft responses

Only create or delete review answers after explicit confirmation.

### Realty

Use:

- `RealtyAnalyticsReport.get_market_price_correspondence()`
- `RealtyAnalyticsReport.get_report_for_classified()`
- `RealtyBooking.list_realty_bookings()`
- `RealtyBooking.update_bookings_info()`
- `RealtyPricing.update_realty_prices()`
- `RealtyListing.get_intervals()`
- `RealtyListing.update_base_params()`

Business outputs:

- Overpriced or underpriced objects
- Booking-calendar gaps
- Seasonal price-period recommendations
- Availability issues

### Jobs

Use:

- `Vacancy.list()`
- `Vacancy.get()`
- `Vacancy.get_statuses()`
- `Application.list()`
- `Application.get_states()`
- `Resume.list()`
- `Resume.get_contacts()`

Business outputs:

- Vacancy health
- Applications needing action
- Candidate pipeline summary
- Resume search shortlist
- Webhook status

Only create, update, archive, prolong, or auto-renew vacancies after explicit confirmation.

### Account And Team Diagnostics

Use:

- `Account.get_self()`
- `Account.get_balance()`
- `Account.get_operations_history()`
- `AccountHierarchy.get_status()`
- `AccountHierarchy.list_employees()`
- `AccountHierarchy.list_company_phones()`
- `AccountHierarchy.list_items_by_employee()`
- `Tariff.get_tariff_info()`

Business outputs:

- Balance and spend visibility
- Employee ownership of listings
- Phone inventory
- Tariff constraints
- Operations-history anomalies

## Decision Rules

Use account-relative baselines instead of hardcoded universal thresholds where possible.

Examples:

- High views and low contacts usually means price, title, photos, location, or offer mismatch.
- High contacts and low order progress usually means weak response speed, seller process, delivery terms, or product fit.
- Low impressions on profitable listing makes the listing a promotion candidate.
- High spend with low contacts means pause, reduce, or rework before more promotion.
- Strong organic conversion can justify paid scaling.
- Out-of-stock or operationally risky listings should not be promoted.
- Negative reviews without answers are reputation risks.
- Old unread chats and missed calls are lead leakage.
- Realty price above market correspondence needs price correction or stronger positioning.
- Promotion should be evaluated against marginal contacts/leads, not views alone.

## Safety Rules

- Read before write.
- Never spend money without explicit confirmation.
- Never change listing price without explicit confirmation.
- Never apply, stop, or modify paid promotion without explicit confirmation.
- Never send messages, delete messages, mark chats read, blacklist users, update stock, change order status, answer reviews, or delete review answers unless the user clearly asked.
- For promotion, always show item IDs, service, forecast/cost, and business reason before applying.
- Prefer preview/report mode by default.
- Use `AvitoClient` and SDK configuration from environment.
- Never expose tokens, client secrets, refresh tokens, or authorization headers.
- Treat `401`, `403`, `429`, validation errors, and SDK mapping errors as business-blocking diagnostics.
- Do not scrape Avito public pages if official SDK/API data is enough.

## Scripts

### `scripts/avito_smoke_check.py`

Purpose:

- Check that `avito-py` imports.
- Create/configure `AvitoClient`.
- Verify authentication.
- Fetch current account with `Account.get_self()`.
- Optionally fetch balance with `Account.get_balance()`.
- Print diagnostics without secrets.

### `scripts/listing_health_report.py`

Purpose:

- Pull active listings.
- Pull stats, analytics, calls, and spend where available.
- Emit JSON/CSV rows with:
  - `item_id`
  - `title`
  - `status`
  - `price`
  - `views`
  - `contacts`
  - `calls`
  - `spend`
  - `conversion_rate`
  - `diagnosis`
  - `recommended_action`

### `scripts/promotion_decision_preview.py`

Purpose:

- Accept item IDs or filters.
- Fetch item stats.
- Fetch available promotion services/prices.
- Fetch BBIP suggests and forecasts where relevant.
- Check current promotion orders.
- Output promote/do-not-promote recommendations.
- Never buy promotion.

## Creation Steps

1. Initialize the skill:

```bash
/Users/n.baryshnikov/.codex/skills/.system/skill-creator/scripts/init_skill.py avito \
  --path /Users/n.baryshnikov/Projects/18studio/skills \
  --resources scripts,references \
  --interface display_name="Avito Business" \
  --interface short_description="Operate Avito business workflows through avito-py." \
  --interface default_prompt="Analyze my Avito business account and recommend the next actions."
```

2. Write `SKILL.md` as a concise router and workflow guide.

3. Add `references/sdk-domain-map.md` with exact `avito-py` namespaces and methods.

4. Add `references/business-scenarios.md` with seller workflow patterns.

5. Add `references/decision-rules.md` with relative business heuristics.

6. Add `references/safety.md` for paid/write/destructive operations.

7. Add scripts for repeatable reports and previews.

8. Validate:

```bash
/Users/n.baryshnikov/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  /Users/n.baryshnikov/Projects/18studio/skills/avito
```

9. Forward-test with realistic prompts:

- "Find underperforming active listings."
- "Which ads should I promote this week?"
- "Analyze unanswered leads from chats and calls."
- "Check orders needing action."
- "Prepare replies to negative reviews."
- "Check realty prices and booking gaps."

## Guiding Sentence

This skill uses `avito-py` as the only SDK layer and adds Avito classified-business reasoning on top of it: diagnose, compare, recommend, and only then execute confirmed actions.

## Acceptance Criteria

### SDK Correctness

- The skill explicitly names `p141592/avito_python_api` and links to https://p141592.github.io/avito_python_api/.
- The skill instructs agents to use `avito-py` and `AvitoClient` as the primary integration layer.
- SDK domain names and method names in references match the documented `avito-py` public contract.
- The skill does not recommend other SDKs, scraping, browser automation, or direct HTTP as the default path.
- Any fallback outside `avito-py` requires an explicit limitation and user approval.

### Business Logic Quality

- The skill starts from business goals, not API endpoints.
- Each major Avito business area has at least one workflow:
  - Listings
  - Promotion
  - Leads/chats/calls
  - Orders/delivery/stock
  - Reviews/ratings
  - Realty
  - Jobs
  - Account/team/tariff diagnostics
- Workflows produce business diagnoses and recommended actions, not raw API dumps.
- Recommendations explain the reason, expected business impact, required data, and risk.
- Decision rules prefer account-relative baselines over fixed universal thresholds.

### Safety And Control

- The skill defaults to read/report/preview mode.
- Paid actions require explicit confirmation.
- Write actions require explicit confirmation.
- Reputation-affecting actions require explicit confirmation.
- Destructive or hard-to-reverse actions require explicit confirmation.
- Promotion execution shows item IDs, service/campaign type, cost or budget, forecast where available, and business reason before applying.
- Secrets, tokens, refresh tokens, authorization headers, and client secrets are never printed.

### Progressive Disclosure

- `SKILL.md` stays concise and acts as a router.
- Detailed SDK mapping lives in `references/sdk-domain-map.md`.
- Detailed business workflows live in `references/business-scenarios.md`.
- Detailed heuristics live in `references/decision-rules.md`.
- Safety rules live in `references/safety.md`.
- No unnecessary files such as `README.md`, `INSTALLATION_GUIDE.md`, or `QUICK_REFERENCE.md` are created.

### Script Usefulness

- Scripts are small and support repeatable business tasks.
- Scripts do not replace `avito-py`; they use it.
- Scripts are safe by default and do not perform paid/write actions unless explicitly designed and confirmed.
- `avito_smoke_check.py` validates import/config/auth without exposing secrets.
- `listing_health_report.py` outputs actionable listing diagnostics.
- `promotion_decision_preview.py` previews promotion choices without buying promotion.

### Validation

- `quick_validate.py` passes for the final skill directory.
- Any scripts added are run at least in a safe/import/help mode.
- The skill can be forward-tested against realistic prompts:
  - "Find underperforming active listings."
  - "Which ads should I promote this week?"
  - "Analyze unanswered leads from chats and calls."
  - "Check orders needing action."
  - "Prepare replies to negative reviews."
  - "Check realty prices and booking gaps."

## Scoring Rubric

Score the completed job out of 100.

### 1. SDK Fidelity - 20 Points

- 20: Uses only the specified `p141592/avito_python_api` SDK, with accurate domain/method names and clear `AvitoClient` usage.
- 15: Uses the correct SDK, but some domain mapping is incomplete or slightly imprecise.
- 10: Mentions the correct SDK, but the skill still reads like generic Avito API guidance.
- 5: Mixes the correct SDK with other wrappers or direct HTTP without clear reason.
- 0: Does not center the specified SDK.

### 2. Business Scenario Coverage - 20 Points

- 20: Covers all major classified business workflows with concrete data inputs, diagnosis logic, and outputs.
- 15: Covers the main seller workflows but misses one or two important domains.
- 10: Covers listings and promotion only.
- 5: Mostly lists API capabilities without business scenarios.
- 0: No meaningful business workflow design.

### 3. Business Reasoning Quality - 20 Points

- 20: Gives useful decision rules, relative baselines, action tradeoffs, and clear recommendations.
- 15: Gives practical recommendations but some heuristics are shallow.
- 10: Gives generic advice that needs substantial interpretation by the agent.
- 5: Mostly forwards raw data to the user.
- 0: No business reasoning layer.

### 4. Safety And Risk Handling - 15 Points

- 15: Strong confirmation gates for paid, write, destructive, and reputation-affecting actions; secrets are protected.
- 10: Covers paid/write confirmations but misses some edge cases.
- 5: Mentions caution but does not define operational rules.
- 0: Allows risky actions without confirmation.

### 5. Skill Architecture - 15 Points

- 15: Clean progressive-disclosure structure; `SKILL.md` is concise; references are well separated.
- 10: Good structure with some duplication or bloated sections.
- 5: Everything is in one large file or references are unclear.
- 0: Does not follow skill-creator guidance.

### 6. Validation And Testability - 10 Points

- 10: Validation passes, scripts have safe execution modes, and realistic forward-test prompts are documented.
- 7: Validation passes but forward-testing or script checks are incomplete.
- 4: Some validation is planned but not runnable.
- 0: No validation path.

## Definition Of Done

The job is good enough when it scores at least 85/100, with no zero-score category and full marks in Safety And Risk Handling.
