#!/usr/bin/env python3
"""Search OSINT dork entries using an official GHDB baseline source.

This script avoids scraping exploit-db.com pages directly.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import os
import sys
from pathlib import Path
from typing import Dict, Iterable, List
import xml.etree.ElementTree as ET

import requests

SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CACHE_FILE = SKILL_ROOT / "data" / "ghdb.xml"

DEFAULT_SOURCES = [
    "https://gitlab.com/exploit-database/exploitdb/-/raw/main/ghdb.xml",
]

FIELDS = [
    "id",
    "category",
    "short_description",
    "description",
    "query",
    "query_url",
    "link",
    "edb",
    "date",
    "author",
]


class GhdbError(Exception):
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Search dork entries from official ExploitDB GHDB XML source."
    )
    parser.add_argument(
        "terms",
        nargs="*",
        help="Optional positional keywords. Equivalent to repeated --keyword values.",
    )
    parser.add_argument(
        "-k",
        "--keyword",
        action="append",
        default=[],
        help="Keyword to search. Repeat for multiple keywords.",
    )
    parser.add_argument(
        "--match",
        choices=["all", "any"],
        default="all",
        help="How multiple keywords are matched. Default: all.",
    )
    parser.add_argument(
        "--category",
        help="Filter results by category substring (case-insensitive).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of rows to return. Default: 10.",
    )
    parser.add_argument(
        "--format",
        choices=["table", "json", "csv"],
        default="table",
        help="Output format. Default: table.",
    )
    parser.add_argument(
        "--source-url",
        action="append",
        default=[],
        help="Extra source URL(s) to try before default source.",
    )
    parser.add_argument(
        "--cache-file",
        default=str(DEFAULT_CACHE_FILE),
        help="Path for local XML cache. Default: <skill>/data/ghdb.xml.",
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Force refresh from network before reading cache.",
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Do not fetch from network. Only use local cache.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=20,
        help="Network timeout seconds. Default: 20.",
    )
    return parser.parse_args()


def unique_sources(extra_sources: Iterable[str]) -> List[str]:
    seen = set()
    ordered: List[str] = []
    for url in list(extra_sources) + DEFAULT_SOURCES:
        if url and url not in seen:
            seen.add(url)
            ordered.append(url)
    return ordered


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def fetch_xml(url: str, timeout: int) -> str:
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return response.text


def load_xml_text(args: argparse.Namespace) -> str:
    cache_path = Path(args.cache_file)
    network_errors = []

    if args.offline:
        if not cache_path.exists():
            raise GhdbError(
                f"Offline mode requested but cache file does not exist: {cache_path}"
            )
        return read_text(cache_path)

    should_try_network = args.refresh or not cache_path.exists()
    if should_try_network:
        for source in unique_sources(args.source_url):
            try:
                xml_text = fetch_xml(source, timeout=args.timeout)
                ET.fromstring(xml_text)
                write_text(cache_path, xml_text)
                return xml_text
            except Exception as exc:  # noqa: BLE001
                network_errors.append(f"{source}: {exc}")

    if cache_path.exists():
        return read_text(cache_path)

    details = "\n".join(network_errors) if network_errors else "No sources attempted."
    raise GhdbError(
        "Unable to load GHDB XML from network and no cache is available.\n"
        f"Details:\n{details}"
    )


def clean_text(value: str | None) -> str:
    if value is None:
        return ""
    return html.unescape(value).strip().replace("\n", " ")


def xml_to_records(xml_text: str) -> List[Dict[str, str]]:
    root = ET.fromstring(xml_text)
    records: List[Dict[str, str]] = []

    for entry in root.findall("entry"):
        records.append(
            {
                "id": clean_text(entry.findtext("id")),
                "category": clean_text(entry.findtext("category")),
                "short_description": clean_text(entry.findtext("shortDescription")),
                "description": clean_text(entry.findtext("textualDescription")),
                "query": clean_text(entry.findtext("query")),
                "query_url": clean_text(entry.findtext("querystring")),
                "link": clean_text(entry.findtext("link")),
                "edb": clean_text(entry.findtext("edb")),
                "date": clean_text(entry.findtext("date")),
                "author": clean_text(entry.findtext("author")),
            }
        )

    return records


def keyword_match(record: Dict[str, str], terms: List[str], mode: str) -> bool:
    if not terms:
        return True

    haystack = " ".join(
        [
            record.get("category", ""),
            record.get("short_description", ""),
            record.get("description", ""),
            record.get("query", ""),
            record.get("author", ""),
        ]
    ).lower()

    checks = [term.lower() in haystack for term in terms]
    return all(checks) if mode == "all" else any(checks)


def filter_records(records: List[Dict[str, str]], args: argparse.Namespace) -> List[Dict[str, str]]:
    all_terms = [t.strip() for t in (args.keyword + args.terms) if t.strip()]
    category_filter = (args.category or "").strip().lower()

    filtered = []
    for record in records:
        if category_filter and category_filter not in record.get("category", "").lower():
            continue
        if not keyword_match(record, all_terms, args.match):
            continue
        filtered.append(record)

    def safe_int(value: str) -> int:
        try:
            return int(value)
        except ValueError:
            return -1

    filtered.sort(key=lambda r: safe_int(r.get("id", "")), reverse=True)
    return filtered[: max(args.limit, 0)]


def print_table(records: List[Dict[str, str]]) -> None:
    if not records:
        print("No GHDB matches found.")
        return

    headers = ["id", "category", "query", "description"]
    display_rows = []

    for record in records:
        display_rows.append(
            {
                "id": record.get("id", ""),
                "category": record.get("category", "")[:40],
                "query": record.get("query", "")[:70],
                "description": record.get("description", "")[:80],
            }
        )

    widths = {
        h: max(len(h), max(len(row[h]) for row in display_rows))
        for h in headers
    }

    line = " | ".join(h.ljust(widths[h]) for h in headers)
    sep = "-+-".join("-" * widths[h] for h in headers)
    print(line)
    print(sep)
    for row in display_rows:
        print(" | ".join(row[h].ljust(widths[h]) for h in headers))


def print_json(records: List[Dict[str, str]]) -> None:
    print(json.dumps(records, indent=2, ensure_ascii=True))


def print_csv(records: List[Dict[str, str]]) -> None:
    writer = csv.DictWriter(sys.stdout, fieldnames=FIELDS)
    writer.writeheader()
    for record in records:
        writer.writerow(record)


def main() -> int:
    args = parse_args()

    try:
        xml_text = load_xml_text(args)
        records = xml_to_records(xml_text)
        filtered = filter_records(records, args)
    except GhdbError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    except requests.RequestException as exc:
        print(f"Network error: {exc}", file=sys.stderr)
        return 3
    except ET.ParseError as exc:
        print(f"Parse error: {exc}", file=sys.stderr)
        return 4

    if args.format == "json":
        print_json(filtered)
    elif args.format == "csv":
        print_csv(filtered)
    else:
        print_table(filtered)

    return 0


if __name__ == "__main__":
    os.environ.setdefault("PYTHONUTF8", "1")
    raise SystemExit(main())
