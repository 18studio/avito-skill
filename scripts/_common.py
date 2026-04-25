"""Shared helpers for Avito skill scripts."""

from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from itertools import islice
from typing import Any

from avito import AvitoClient


def make_client() -> AvitoClient:
    """Build the SDK client from environment configuration."""

    return AvitoClient()


def parse_int_list(raw: str | None) -> list[int]:
    """Parse a comma-separated list of integers."""

    if not raw:
        return []
    return [int(part.strip()) for part in raw.split(",") if part.strip()]


def serialize(value: Any) -> Any:
    """Convert SDK objects into JSON-serializable structures."""

    if is_dataclass(value):
        return serialize(asdict(value))
    if isinstance(value, dict):
        return {str(key): serialize(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [serialize(item) for item in value]
    return value


def emit_json(payload: Any) -> None:
    """Print a JSON payload with stable formatting."""

    print(json.dumps(serialize(payload), ensure_ascii=False, indent=2, sort_keys=True))


def collect_items(items: list[Any], *, all_pages: bool, max_items: int | None) -> list[Any]:
    """Collect items with explicit pagination mode."""

    if all_pages:
        return list(items)
    if max_items is None or max_items <= 0:
        return list(islice(items, 0))
    return list(islice(items, max_items))


def pagination_mode(*, all_pages: bool) -> str:
    """Return the normalized pagination mode label."""

    return "materialize_all" if all_pages else "streaming"
