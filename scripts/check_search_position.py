#!/usr/bin/env python3
"""
Prepare a fixed Avito search-position measurement scenario.

Pagination mode:
- streaming

Notes:
- does not query Avito search yet
- emits a reproducible scenario contract for future implementation
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone

from _common import emit_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Prepare a search position scenario.")
    parser.add_argument("--item-id", type=int, required=True, help="Listing id to look for.")
    parser.add_argument("--query", required=True, help="Search query text.")
    parser.add_argument("--location", required=True, help="Region or city.")
    parser.add_argument("--category", required=True, help="Avito category.")
    parser.add_argument(
        "--filters",
        default="",
        help="Opaque filter string, for example price_from=1000,price_to=5000.",
    )
    parser.add_argument("--sort", default="default", help="Sort mode.")
    parser.add_argument("--surface", default="web", help="Search surface or device type.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    emit_json(
        {
            "status": "not_implemented",
            "message": "Search position measurement requires a dedicated search adapter.",
            "scenario": {
                "item_id": args.item_id,
                "query": args.query,
                "location": args.location,
                "category": args.category,
                "filters": args.filters,
                "sort": args.sort,
                "surface": args.surface,
                "observed_at": datetime.now(timezone.utc).isoformat(),
            },
        }
    )


if __name__ == "__main__":
    main()
