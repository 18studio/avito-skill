# Business Scenarios

## Core Value

This skill should help a seller or agency answer three business questions:

1. What is happening with my listings right now?
2. Why is a listing not producing enough demand?
3. Where should I spend promotion budget next?

## Priority Scenarios

### Scenario 1. Single Listing Health Check

Use when the user asks:

- “Что с этим объявлением?”
- “Почему мало заявок?”
- “Покажи статистику и место в поиске”

Expected flow:

1. Load listing metadata and status.
2. Fetch recent official statistics.
3. Measure sampled search placement for an agreed query and region.
4. Summarize the main bottleneck.
5. Recommend either content fixes, price review, or promotion.

Success outcome:

- the user gets one operational diagnosis, not a data dump

### Scenario 2. Compare Several Listings

Use when the user asks:

- “Какое объявление просело сильнее?”
- “Сравни объявления по эффективности”
- “Какие объявления продвигать?”

Expected flow:

1. Fetch the same metric window for all listings.
2. Normalize per-listing metrics.
3. Rank by business value:
   - best conversion
   - worst visibility
   - biggest recent drop
4. Produce an action queue.

Success outcome:

- the user gets prioritization, not just a table

### Scenario 3. Promotion Readiness Check

Use when the user asks:

- “Запустить рекламу?”
- “Стоит ли продвигать это объявление?”
- “На что лучше тратить бюджет?”

Expected flow:

1. Inspect listing quality proxies from available metadata and outcomes.
2. Inspect statistics and visibility.
3. Decide whether promotion would amplify a working listing or waste money on a broken one.
4. Return a go/no-go recommendation with a reason.

Success outcome:

- promotion is treated as an investment decision

### Scenario 4. Promotion Control

Use when the user asks:

- “Запусти продвижение”
- “Останови рекламу”
- “Усиль продвижение”

Expected flow:

1. Validate account, listing state, and eligibility.
2. Preview the intended change.
3. Execute only after the intent is clear.
4. Re-fetch resulting state if the API supports it.

Success outcome:

- the action is auditable and reversible where API allows it

### Scenario 5. Daily or Weekly Portfolio Monitoring

Use when the user asks:

- “Сделай ежедневный отчет”
- “Отслеживай просадку объявлений”
- “Найди, где теряем трафик”

Expected flow:

1. Fetch batch statistics for the reporting window.
2. Compute deltas to previous comparable window.
3. Highlight anomalies:
   - traffic drop
   - contact drop
   - spend growth without result
   - visibility loss
4. Build three queues:
   - investigate
   - promote
   - leave unchanged

Success outcome:

- the skill becomes an operations assistant, not a one-off query tool

## KPI Interpretation

Use simple operational interpretations:

- High views + low contacts -> listing quality, price, trust, or offer issue
- Low views + low observed position -> discoverability issue
- High spend + weak contacts -> inefficient promotion
- Good contacts + weak visibility -> strong candidate for added promotion

Avoid pretending to know buyer intent when only top-level metrics exist.

## Search Position Policy

Never report “место в поиске” without the exact search scenario.

The minimum scenario record is:

- query
- region
- category
- filters
- sort mode
- timestamp

If the user does not specify these values, ask or choose explicit defaults and state them back.

## Action Priority

For most sellers, this is the default order of value:

1. Detect listings losing visibility
2. Find listings worth promoting
3. Stop wasteful spend
4. Produce periodic performance reports

This order should shape script development and future automation.
