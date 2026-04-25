#!/usr/bin/env python3
"""Read-only Avito SDK smoke check."""

from __future__ import annotations

import argparse
import dataclasses
import json
from typing import Any


SECRET_WORDS = ("token", "secret", "authorization", "password", "cookie", "refresh")


def to_plain(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {field.name: to_plain(getattr(value, field.name)) for field in dataclasses.fields(value)}
    if isinstance(value, dict):
        return {str(key): to_plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [to_plain(item) for item in value]
    if hasattr(value, "__dict__") and not isinstance(value, type):
        return {
            key: to_plain(item)
            for key, item in vars(value).items()
            if not key.startswith("_") and not any(word in key.lower() for word in SECRET_WORDS)
        }
    return value


def redacted_error(exc: BaseException) -> str:
    text = f"{exc.__class__.__name__}: {exc}"
    for word in SECRET_WORDS:
        text = text.replace(word, f"{word[:2]}***")
        text = text.replace(word.upper(), f"{word[:2].upper()}***")
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate avito-py import, environment configuration, and account auth.")
    parser.add_argument("--env-file", default=".env", help="Path to .env file, or empty string to use process env only.")
    parser.add_argument("--balance", action="store_true", help="Also fetch account balance.")
    args = parser.parse_args()

    try:
        import avito
        from avito import AvitoClient
    except Exception as exc:  # pragma: no cover - environment diagnostic
        print(json.dumps({"ok": False, "stage": "import", "error": redacted_error(exc)}, ensure_ascii=False, indent=2))
        return 1

    result: dict[str, Any] = {
        "ok": False,
        "sdk": "avito-py",
        "module": getattr(avito, "__file__", None),
        "stages": [],
    }

    try:
        env_file = args.env_file or None
        client = AvitoClient.from_env(env_file=env_file)
        result["stages"].append({"stage": "client", "ok": True})
    except Exception as exc:
        result["stages"].append({"stage": "client", "ok": False, "error": redacted_error(exc)})
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1

    try:
        profile = client.account().get_self()
        result["account"] = to_plain(profile)
        result["stages"].append({"stage": "get_self", "ok": True})
    except Exception as exc:
        result["stages"].append({"stage": "get_self", "ok": False, "error": redacted_error(exc)})
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1

    if args.balance:
        try:
            result["balance"] = to_plain(client.account().get_balance())
            result["stages"].append({"stage": "get_balance", "ok": True})
        except Exception as exc:
            result["stages"].append({"stage": "get_balance", "ok": False, "error": redacted_error(exc)})

    result["ok"] = True
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
