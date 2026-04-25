#!/usr/bin/env python3
"""Generate a read-only Avito listing health report."""

from __future__ import annotations

import argparse
import csv
import dataclasses
import json
import sys
from datetime import datetime, timedelta
from typing import Any


def to_plain(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {field.name: to_plain(getattr(value, field.name)) for field in dataclasses.fields(value)}
    if isinstance(value, dict):
        return {str(key): to_plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [to_plain(item) for item in value]
    if hasattr(value, "__dict__") and not isinstance(value, type):
        return {key: to_plain(item) for key, item in vars(value).items() if not key.startswith("_")}
    return value


def first_number(source: Any, names: tuple[str, ...]) -> float:
    plain = to_plain(source)
    stack = [plain]
    while stack:
        current = stack.pop()
        if isinstance(current, dict):
            for name in names:
                value = current.get(name)
                if isinstance(value, (int, float)):
                    return float(value)
            stack.extend(current.values())
        elif isinstance(current, list):
            stack.extend(current)
    return 0.0


def records_by_item(source: Any) -> dict[str, Any]:
    records: dict[str, Any] = {}
    stack = [to_plain(source)]
    while stack:
        current = stack.pop()
        if isinstance(current, dict):
            item_id = current.get("item_id") or current.get("itemId") or current.get("id") or current.get("avito_id")
            if item_id is not None:
                records[str(item_id)] = current
            stack.extend(current.values())
        elif isinstance(current, list):
            stack.extend(current)
    return records


def get_field(source: Any, names: tuple[str, ...], default: Any = None) -> Any:
    plain = to_plain(source)
    if isinstance(plain, dict):
        for name in names:
            if name in plain and plain[name] not in (None, ""):
                return plain[name]
    return default


def unwrap_items(value: Any) -> list[Any]:
    plain = to_plain(value)
    if isinstance(plain, list):
        return plain
    if isinstance(plain, dict):
        for key in ("items", "listings", "result", "data"):
            if isinstance(plain.get(key), list):
                return plain[key]
    return []


def diagnose(views: float, contacts: float, calls: float, spend: float, median_conversion: float) -> tuple[str, str]:
    conversion = contacts / views if views else 0.0
    if views <= 0:
        return "low_visibility", "Check category, title, status, availability, and consider promotion only after listing quality is healthy."
    if contacts <= 0 and views > 0:
        return "views_without_contacts", "Review price, title, photos, location, delivery terms, and offer clarity before paid promotion."
    if median_conversion and conversion < median_conversion * 0.6:
        return "below_account_conversion", "Improve listing content or pricing before increasing spend."
    if spend > 0 and contacts <= 0:
        return "spend_without_contacts", "Pause or reduce paid services until conversion blockers are fixed."
    if calls > contacts * 1.5 and contacts > 0:
        return "call_heavy_leads", "Check missed-call handling and response process."
    return "healthy_or_needs_context", "Compare margin, stock, and fulfillment capacity before scaling."


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a read-only listing health report from avito-py data.")
    parser.add_argument("--env-file", default=".env", help="Path to .env file, or empty string to use process env only.")
    parser.add_argument("--status", default="active", help="Listing status to request from Ad.list().")
    parser.add_argument("--limit", type=int, default=50, help="Maximum listings to read.")
    parser.add_argument("--days", type=int, default=30, help="Stats lookback window.")
    parser.add_argument("--format", choices=("json", "csv"), default="json", help="Output format.")
    args = parser.parse_args()

    try:
        from avito import AvitoClient
    except Exception as exc:
        print(f"Failed to import avito-py: {exc.__class__.__name__}: {exc}", file=sys.stderr)
        return 1

    client = AvitoClient.from_env(env_file=args.env_file or None)
    date_to = datetime.now()
    date_from = date_to - timedelta(days=args.days)

    listings = unwrap_items(client.ad().list(status=args.status, limit=args.limit, offset=0))
    item_ids = [int(item_id) for item_id in (get_field(item, ("id", "item_id", "avito_id")) for item in listings) if item_id]

    stats = client.ad_stats().get_item_stats(item_ids=item_ids, date_from=date_from, date_to=date_to) if item_ids else None
    analytics = client.ad_stats().get_item_analytics(item_ids=item_ids, date_from=date_from, date_to=date_to) if item_ids else None
    calls = client.ad_stats().get_calls_stats(item_ids=item_ids, date_from=date_from, date_to=date_to) if item_ids else None
    spend = client.ad_stats().get_account_spendings(item_ids=item_ids, date_from=date_from, date_to=date_to) if item_ids else None
    stats_by_item = records_by_item(stats)
    calls_by_item = records_by_item(calls)
    spend_by_item = records_by_item(spend)

    conversions: list[float] = []
    raw_rows: list[dict[str, Any]] = []
    for item in listings:
        item_id = get_field(item, ("id", "item_id", "avito_id"))
        item_key = str(item_id)
        item_stats = stats_by_item.get(item_key, stats)
        item_calls = calls_by_item.get(item_key, calls)
        item_spend = spend_by_item.get(item_key, spend)
        views = first_number(item_stats, ("views", "uniqViews", "uniq_views", "impressions"))
        contacts = first_number(item_stats, ("contacts", "contactsCount", "contacts_count"))
        row_calls = first_number(item_calls, ("calls", "callsCount", "calls_count"))
        row_spend = first_number(item_spend, ("spend", "spent", "amount", "cost"))
        conversion = contacts / views if views else 0.0
        if conversion:
            conversions.append(conversion)
        raw_rows.append(
            {
                "item_id": item_id,
                "title": get_field(item, ("title", "name"), ""),
                "status": get_field(item, ("status",), args.status),
                "price": get_field(item, ("price",), ""),
                "views": views,
                "contacts": contacts,
                "calls": row_calls,
                "spend": row_spend,
                "conversion_rate": conversion,
                "analytics_available": analytics is not None,
            }
        )

    conversions.sort()
    median = conversions[len(conversions) // 2] if conversions else 0.0
    for row in raw_rows:
        diagnosis, action = diagnose(row["views"], row["contacts"], row["calls"], row["spend"], median)
        row["diagnosis"] = diagnosis
        row["recommended_action"] = action

    if args.format == "csv":
        writer = csv.DictWriter(sys.stdout, fieldnames=list(raw_rows[0].keys()) if raw_rows else [])
        if raw_rows:
            writer.writeheader()
            writer.writerows(raw_rows)
    else:
        print(json.dumps({"rows": raw_rows, "baseline": {"median_conversion_rate": median}}, ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
