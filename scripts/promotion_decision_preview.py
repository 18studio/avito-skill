#!/usr/bin/env python3
"""Preview Avito promotion decisions without buying promotion."""

from __future__ import annotations

import argparse
import dataclasses
import json
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
    stack = [to_plain(source)]
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


def records_list(source: Any) -> list[Any]:
    plain = to_plain(source)
    if isinstance(plain, list):
        return plain
    if isinstance(plain, dict):
        for key in ("items", "listings", "result", "data"):
            value = plain.get(key)
            if isinstance(value, list):
                return value
    return []


def get_field(source: Any, names: tuple[str, ...], default: Any = None) -> Any:
    plain = to_plain(source)
    if isinstance(plain, dict):
        for name in names:
            value = plain.get(name)
            if value not in (None, ""):
                return value
    return default


def resolve_item_ids(client: Any, explicit_ids: list[int], status: str, limit: int) -> tuple[list[int], str]:
    if explicit_ids:
        return explicit_ids, "explicit_item_ids"
    listings = records_list(client.ad().list(status=status, limit=limit, offset=0))
    item_ids = [
        int(item_id)
        for item_id in (get_field(item, ("item_id", "id", "avito_id")) for item in listings)
        if item_id
    ]
    return item_ids, f"ad_filter:status={status},limit={limit}"


def item_has_record(source: Any, item_id: int) -> bool:
    return str(item_id) in records_by_item(source)


def preview_decision(views: float, contacts: float, spend: float, has_services: bool, has_orders: bool) -> tuple[str, str, str]:
    conversion = contacts / views if views else 0.0
    if has_orders:
        return "inspect_current_promotion", "Current promotion order exists; inspect performance before adding spend.", "medium"
    if views <= 0 and has_services:
        return "test_low_budget", "Listing has low visibility and paid services are available; test only after checking content, stock, and margin.", "medium"
    if views > 0 and contacts <= 0:
        return "improve_listing_first", "Views do not convert to contacts; fix price, title, photos, delivery, or offer before promotion.", "high"
    if spend > 0 and contacts <= 0:
        return "stop_or_reduce_spend", "Spend is not producing contacts; avoid additional promotion.", "high"
    if conversion > 0 and has_services:
        return "promote_candidate", "Listing has demonstrated contact conversion; consider forecasted paid scaling.", "medium"
    return "do_not_promote_yet", "Insufficient evidence for paid promotion.", "low"


def main() -> int:
    parser = argparse.ArgumentParser(description="Preview Avito promotion recommendations. This script never applies or buys promotion.")
    parser.add_argument("item_ids", nargs="*", type=int, help="Avito item IDs to evaluate. If omitted, listings are selected by safe read-only filters.")
    parser.add_argument("--env-file", default=".env", help="Path to .env file, or empty string to use process env only.")
    parser.add_argument("--days", type=int, default=30, help="Stats lookback window.")
    parser.add_argument("--status", default="active", help="Listing status filter used when item IDs are omitted.")
    parser.add_argument("--limit", type=int, default=20, help="Maximum listings to preview when item IDs are omitted.")
    args = parser.parse_args()

    from avito import AvitoClient

    client = AvitoClient.from_env(env_file=args.env_file or None)
    item_ids, source = resolve_item_ids(client, args.item_ids, args.status, args.limit)
    if not item_ids:
        print(
            json.dumps(
                {
                    "mode": "preview_only",
                    "paid_actions_performed": False,
                    "selection": source,
                    "recommendations": [],
                    "diagnosis": "No item IDs matched the provided selection.",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    date_to = datetime.now()
    date_from = date_to - timedelta(days=args.days)

    stats = client.ad_stats().get_item_stats(item_ids=item_ids, date_from=date_from, date_to=date_to)
    spend = client.ad_stats().get_account_spendings(item_ids=item_ids, date_from=date_from, date_to=date_to)
    services = client.promotion_order().list_services(item_ids=item_ids)
    orders = client.promotion_order().list_orders(item_ids=item_ids)
    stats_by_item = records_by_item(stats)
    spend_by_item = records_by_item(spend)

    try:
        vas_prices = client.ad_promotion().get_vas_prices(item_ids=item_ids)
    except Exception as exc:
        vas_prices = {"available": False, "error": f"{exc.__class__.__name__}: {exc}"}

    try:
        suggests = client.bbip_promotion().get_suggests(item_ids=item_ids)
    except Exception as exc:
        suggests = {"available": False, "error": f"{exc.__class__.__name__}: {exc}"}

    service_records = records_list(services)
    order_records = records_list(orders)
    results = []
    for item_id in item_ids:
        item_key = str(item_id)
        item_stats = stats_by_item.get(item_key, stats)
        item_spend = spend_by_item.get(item_key, spend)
        has_services = item_has_record(service_records, item_id)
        has_orders = item_has_record(order_records, item_id)
        views = first_number(item_stats, ("views", "uniqViews", "uniq_views", "impressions"))
        contacts = first_number(item_stats, ("contacts", "contactsCount", "contacts_count"))
        amount = first_number(item_spend, ("spend", "spent", "amount", "cost"))
        decision, reason, risk = preview_decision(views, contacts, amount, has_services, has_orders)
        results.append(
            {
                "item_id": item_id,
                "decision": decision,
                "reason": reason,
                "risk": risk,
                "views": views,
                "contacts": contacts,
                "spend": amount,
                "conversion_rate": contacts / views if views else 0.0,
            }
        )

    print(
        json.dumps(
            {
                "mode": "preview_only",
                "paid_actions_performed": False,
                "selection": source,
                "recommendations": results,
                "available_services": to_plain(services),
                "current_orders": to_plain(orders),
                "vas_prices": to_plain(vas_prices),
                "bbip_suggests": to_plain(suggests),
            },
            ensure_ascii=False,
            indent=2,
            default=str,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
