#!/usr/bin/env python3
"""
Build a portfolio-level Avito report across selected listings.

Pagination mode:
- default: streaming
- with --all-pages: materialize_all

Notes:
- keeps SDK lazy pagination intact by default
- full slices, negative indexes, and forced list conversion may load all pages
"""

from __future__ import annotations

import argparse

from _common import collect_items, emit_json, make_client, pagination_mode


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build a portfolio report from Avito listings.")
    parser.add_argument("--user-id", type=int, required=True, help="Avito account user id.")
    parser.add_argument("--status", help="Optional listing status filter.")
    parser.add_argument("--limit", type=int, default=100, help="Page size for SDK list calls.")
    parser.add_argument("--offset", type=int, default=0, help="Initial list offset.")
    parser.add_argument(
        "--max-items",
        type=int,
        default=100,
        help="Maximum number of listings to inspect in streaming mode.",
    )
    parser.add_argument(
        "--all-pages",
        action="store_true",
        help="Materialize all pages before building the report.",
    )
    parser.add_argument("--date-from", help="Stats period start.")
    parser.add_argument("--date-to", help="Stats period end.")
    parser.add_argument(
        "--stats-fields",
        default="",
        help="Optional comma-separated stats fields for item stats.",
    )
    return parser


def classify(ad: object, stats_by_item: dict[int, object]) -> str:
    item_id = getattr(ad, "id", None)
    stats = stats_by_item.get(item_id)
    views = getattr(stats, "views", None) if stats else None
    contacts = getattr(stats, "contacts", None) if stats else None

    if views is None or contacts is None:
        return "watch"
    if views <= 10 and contacts == 0:
        return "investigate_visibility"
    if views > 10 and contacts == 0:
        return "fix_before_promo"
    if views > 10 and contacts > 0:
        return "scale"
    return "watch"


def main() -> None:
    args = build_parser().parse_args()
    stats_fields = [part.strip() for part in args.stats_fields.split(",") if part.strip()]

    with make_client() as avito:
        listing_result = avito.ad(user_id=args.user_id).list(
            status=args.status,
            limit=args.limit,
            offset=args.offset,
        )
        selected_ads = collect_items(
            listing_result.items,
            all_pages=args.all_pages,
            max_items=args.max_items,
        )

        item_ids = [item.id for item in selected_ads if getattr(item, "id", None) is not None]
        stats_result = None
        stats_by_item: dict[int, object] = {}
        if item_ids:
            stats_result = avito.ad_stats(user_id=args.user_id).get_item_stats(
                item_ids=item_ids,
                date_from=args.date_from,
                date_to=args.date_to,
                fields=stats_fields or None,
            )
            stats_by_item = {
                record.item_id: record
                for record in stats_result.items
                if getattr(record, "item_id", None) is not None
            }

        report_items = []
        for ad in selected_ads:
            item_id = getattr(ad, "id", None)
            report_items.append(
                {
                    "ad": ad,
                    "stats": stats_by_item.get(item_id),
                    "queue": classify(ad, stats_by_item),
                }
            )

        emit_json(
            {
                "request": {
                    "user_id": args.user_id,
                    "status": args.status,
                    "limit": args.limit,
                    "offset": args.offset,
                    "max_items": args.max_items,
                    "pagination_mode": pagination_mode(all_pages=args.all_pages),
                    "date_from": args.date_from,
                    "date_to": args.date_to,
                    "stats_fields": stats_fields,
                },
                "ads_total": listing_result.total,
                "inspected_count": len(selected_ads),
                "stats_result": stats_result,
                "items": report_items,
            }
        )


if __name__ == "__main__":
    main()
