#!/usr/bin/env python3
"""Audit procurement-report metadata without modifying design files.

This checks metadata completeness only. It does not approve electrical suitability,
package compatibility, availability, alternates, or fabrication readiness.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


NO_PURCHASE_STATUS = "no purchase required"


def text_value(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, dict):
        for key in ("url", "text"):
            nested = value.get(key)
            if isinstance(nested, str) and nested.strip():
                return nested.strip()
    return ""


def component_field(component: dict[str, Any], top_level: str, property_name: str) -> str:
    direct = text_value(component.get(top_level))
    if direct:
        return direct
    properties = component.get("properties")
    if not isinstance(properties, dict):
        return ""
    return text_value(properties.get(property_name))


def audit(report_path: Path) -> dict[str, Any]:
    source_bytes = report_path.read_bytes()
    report = json.loads(source_bytes)
    if not isinstance(report, dict):
        raise ValueError("report root must be an object")
    components = report.get("components")
    if not isinstance(components, list):
        raise ValueError("components must be a list")

    gaps = {
        "missing_reference": [],
        "missing_manufacturer": [],
        "missing_mpn": [],
        "missing_datasheet": [],
    }
    no_purchase = 0
    provisional = []

    for index, component in enumerate(components):
        if not isinstance(component, dict):
            raise ValueError(f"components[{index}] must be an object")

        reference = text_value(component.get("reference"))
        status = text_value(component.get("status"))
        if status.casefold() == NO_PURCHASE_STATUS:
            no_purchase += 1
            continue

        label = reference or f"<components[{index}]>"
        if not reference:
            gaps["missing_reference"].append(label)
        if not component_field(component, "manufacturer", "Manufacturer Name"):
            gaps["missing_manufacturer"].append(label)
        if not component_field(component, "mpn", "Manufacturer Part Number"):
            gaps["missing_mpn"].append(label)

        datasheet = text_value(component.get("datasheet"))
        properties = component.get("properties")
        if not datasheet and isinstance(properties, dict):
            datasheet = text_value(properties.get("Datasheet"))
            if not datasheet:
                datasheet = text_value(properties.get("Datasheet URL"))
        if not datasheet:
            gaps["missing_datasheet"].append(label)
        if "candidate" in status.casefold():
            provisional.append(label)

    gaps = {name: refs for name, refs in gaps.items() if refs}
    purchase_required = len(components) - no_purchase
    return {
        "scope": "metadata completeness only; not sourcing, electrical, footprint, or fabrication approval",
        "source_file": report_path.name,
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "total_components": len(components),
        "purchase_required_components": purchase_required,
        "no_purchase_required_components": no_purchase,
        "provisional_components": provisional,
        "gaps": gaps,
        "status": "incomplete" if gaps else "complete",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="exit 1 when purchase-required components have metadata gaps",
    )
    parser.add_argument("report", type=Path, help="procurement-audit JSON report")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        summary = audit(args.report)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"procurement audit error: {error}", file=sys.stderr)
        return 2

    print(json.dumps(summary, indent=2, sort_keys=True))
    if args.strict and summary["status"] != "complete":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
