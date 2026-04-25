#!/usr/bin/env python3
"""
Validate Avito SDK auth and show integration-safe debug info.

Pagination mode:
- streaming

Notes:
- does not traverse paginated resources
- intended as a smoke test for environment and credentials
"""

from __future__ import annotations

import argparse

from _common import emit_json, make_client


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate Avito auth configuration.")
    parser.add_argument(
        "--skip-profile",
        action="store_true",
        help="Only print transport debug info without calling account().get_self().",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()

    with make_client() as avito:
        payload: dict[str, object] = {
            "status": "ok",
            "debug_info": avito.debug_info(),
        }
        if not args.skip_profile:
            payload["profile"] = avito.account().get_self()
        emit_json(payload)


if __name__ == "__main__":
    main()
