#!/usr/bin/env python3
"""
Fetch Avito listing statistics through SDK-native typed methods.

Pagination mode:
- streaming

Notes:
- reads stats for explicit item ids
- does not use list pagination unless the caller first resolves ids elsewhere
"""

from __future__ import annotations

import argparse

from _common import emit_json, make_client, parse_int_list


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Fetch listing stats for Avito ads.")
    parser.add_argument("--user-id", type=int, required=True, help="Avito account user id.")
    parser.add_argument(
        "--item-ids",
        required=True,
        help="Comma-separated list of listing ids.",
    )
    parser.add_argument("--date-from", help="Period start, for example 2026-04-01.")
    parser.add_argument("--date-to", help="Period end, for example 2026-04-18.")
    parser.add_argument(
        "--fields",
        help="Optional comma-separated stats fields supported by the endpoint.",
    )
    parser.add_argument(
        "--include-calls",
        action="store_true",
        help="Also fetch call statistics for the same listings.",
    )
    parser.add_argument(
        "--include-spendings",
        action="store_true",
        help="Also fetch account spendings for the same listings.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    item_ids = parse_int_list(args.item_ids)
    fields = [part.strip() for part in (args.fields or "").split(",") if part.strip()]

    with make_client() as avito:
        stats = avito.ad_stats(user_id=args.user_id).get_item_stats(
            item_ids=item_ids,
            date_from=args.date_from,
            date_to=args.date_to,
            fields=fields or None,
        )

        payload: dict[str, object] = {
            "request": {
                "user_id": args.user_id,
                "item_ids": item_ids,
                "date_from": args.date_from,
                "date_to": args.date_to,
                "fields": fields,
            },
            "item_stats": stats,
        }

        if args.include_calls:
            payload["call_stats"] = avito.ad_stats(user_id=args.user_id).get_calls_stats(
                item_ids=item_ids,
                date_from=args.date_from,
                date_to=args.date_to,
            )

        if args.include_spendings:
            payload["spendings"] = avito.ad_stats(user_id=args.user_id).get_account_spendings(
                item_ids=item_ids,
                date_from=args.date_from,
                date_to=args.date_to,
                fields=fields or None,
            )

        emit_json(payload)


if __name__ == "__main__":
    main()
