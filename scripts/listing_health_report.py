#!/usr/bin/env python3
"""Report missing avito-py support for listing health reports."""

from __future__ import annotations

import argparse
import dataclasses
import json
import sys
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


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Explain why listing health needs a final avito-py method before it can be reported."
    )
    parser.add_argument("--env-file", default=".env", help="Path to .env file, or empty string to use process env only.")
    args = parser.parse_args()

    try:
        from avito import AvitoClient
    except Exception as exc:
        print(f"Failed to import avito-py: {exc.__class__.__name__}: {exc}", file=sys.stderr)
        return 1

    client = AvitoClient.from_env(env_file=args.env_file or None)
    profile = client.account().get_self()
    print(json.dumps(
        {
            "ok": False,
            "account": to_plain(profile),
            "reason": "avito-py does not provide a final listing health report method. This script will not recreate that logic locally.",
            "required_avito_py_improvements": [
                "Final read-only account/listing health summary method.",
                "Auto-resolved or consistently required user_id for account-scoped methods.",
                "Ready-to-use listing metrics with views, contacts, calls, spend, and conversion per item.",
                "Ready-to-use listing quality/status fields without raw response parsing.",
                "Structured unavailable-data and rate-limit details from Avito API errors.",
            ],
        },
        ensure_ascii=False,
        indent=2,
        default=str,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
