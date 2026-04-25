#!/usr/bin/env python3
"""
Inspect or execute Avito promotion operations with explicit intent.

Pagination mode:
- streaming

Notes:
- keeps execution scoped to explicit items
- supports preview-oriented reads before write actions
"""

from __future__ import annotations

import argparse

from avito.promotion.models import BbipForecastRequestItem, BbipOrderItem

from _common import emit_json, make_client, parse_int_list


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Inspect or execute Avito promotion actions.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    services = subparsers.add_parser("list-services", help="List available promotion services.")
    services.add_argument("--item-ids", required=True, help="Comma-separated listing ids.")

    orders = subparsers.add_parser("list-orders", help="List promotion orders.")
    orders.add_argument("--item-ids", help="Optional comma-separated listing ids.")
    orders.add_argument("--order-ids", help="Optional comma-separated order ids.")

    order_status = subparsers.add_parser("order-status", help="Fetch order statuses.")
    order_status.add_argument("--order-ids", required=True, help="Comma-separated order ids.")

    suggests = subparsers.add_parser("bbip-suggests", help="Get BBIP budget suggestions.")
    suggests.add_argument("--item-ids", required=True, help="Comma-separated listing ids.")

    forecast = subparsers.add_parser("bbip-forecast", help="Get BBIP forecasts.")
    forecast.add_argument("--item-id", type=int, required=True, help="Listing id.")
    forecast.add_argument("--duration", type=int, required=True, help="Promotion duration.")
    forecast.add_argument("--price", type=int, required=True, help="Current price.")
    forecast.add_argument("--old-price", type=int, required=True, help="Old price.")

    create = subparsers.add_parser("bbip-create-order", help="Create a BBIP promotion order.")
    create.add_argument("--item-id", type=int, required=True, help="Listing id.")
    create.add_argument("--duration", type=int, required=True, help="Promotion duration.")
    create.add_argument("--price", type=int, required=True, help="Current price.")
    create.add_argument("--old-price", type=int, required=True, help="Old price.")

    return parser


def main() -> None:
    args = build_parser().parse_args()

    with make_client() as avito:
        if args.command == "list-services":
            emit_json(
                avito.promotion_order().list_services(item_ids=parse_int_list(args.item_ids))
            )
            return

        if args.command == "list-orders":
            emit_json(
                avito.promotion_order().list_orders(
                    item_ids=parse_int_list(args.item_ids),
                    order_ids=[part.strip() for part in (args.order_ids or "").split(",") if part.strip()],
                )
            )
            return

        if args.command == "order-status":
            emit_json(
                avito.promotion_order().get_order_status(
                    order_ids=[part.strip() for part in args.order_ids.split(",") if part.strip()]
                )
            )
            return

        if args.command == "bbip-suggests":
            item_ids = parse_int_list(args.item_ids)
            emit_json(avito.bbip_promotion().get_suggests(item_ids=item_ids))
            return

        if args.command == "bbip-forecast":
            emit_json(
                avito.bbip_promotion(item_id=args.item_id).get_forecasts(
                    items=[
                        BbipForecastRequestItem(
                            item_id=args.item_id,
                            duration=args.duration,
                            price=args.price,
                            old_price=args.old_price,
                        )
                    ]
                )
            )
            return

        if args.command == "bbip-create-order":
            emit_json(
                avito.bbip_promotion(item_id=args.item_id).create_order(
                    items=[
                        BbipOrderItem(
                            item_id=args.item_id,
                            duration=args.duration,
                            price=args.price,
                            old_price=args.old_price,
                        )
                    ]
                )
            )
            return

        raise ValueError(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    main()
