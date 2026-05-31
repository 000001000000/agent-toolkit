#!/usr/bin/env python3
"""Lightweight trigger eval checker for skills.sh style eval sets.

Reads eval definitions from evals/evals.json and compares them with model run
results to produce a trigger/non-trigger scorecard.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class EvalCase:
    eval_id: int
    prompt: str
    expected_trigger: Optional[bool]


@dataclass
class EvalResult:
    eval_id: int
    actual_trigger: Optional[bool]


class Ansi:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    CYAN = "\033[36m"


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_EVALS_PATH = SCRIPT_DIR.parent / "evals" / "evals.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check trigger/non-trigger accuracy for evals/evals.json."
    )
    parser.add_argument(
        "--evals",
        default=str(DEFAULT_EVALS_PATH),
        help="Path to eval definition JSON. Default: <skill>/evals/evals.json",
    )
    parser.add_argument(
        "--results",
        default="-",
        help=(
            "Path to model results file. Use '-' to read from stdin. "
            "Supports JSON array or JSONL."
        ),
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable ANSI colors.",
    )
    return parser.parse_args()


def read_text(path_or_dash: str) -> str:
    if path_or_dash == "-":
        return sys.stdin.read()
    return Path(path_or_dash).read_text(encoding="utf-8")


def infer_expected_trigger(expected_output: str) -> Optional[bool]:
    text = (expected_output or "").lower()
    if "should not trigger" in text:
        return False
    if "should trigger" in text:
        return True
    return None


def load_evals(path: str) -> List[EvalCase]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    raw_evals = payload.get("evals", [])

    cases: List[EvalCase] = []
    for item in raw_evals:
        eval_id = int(item["id"])
        prompt = str(item.get("prompt", ""))
        expected = item.get("expected_trigger")
        if expected is None:
            expected = infer_expected_trigger(str(item.get("expected_output", "")))
        elif not isinstance(expected, bool):
            raise ValueError(f"expected_trigger for eval {eval_id} must be boolean")

        cases.append(EvalCase(eval_id=eval_id, prompt=prompt, expected_trigger=expected))

    return cases


def truthy_bool(value: Any) -> Optional[bool]:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"true", "yes", "1", "trigger", "triggered", "on"}:
            return True
        if normalized in {"false", "no", "0", "ignore", "not-triggered", "off"}:
            return False
    return None


def normalize_result_item(item: Dict[str, Any]) -> EvalResult:
    raw_id = item.get("eval_id", item.get("id"))
    if raw_id is None:
        raise ValueError("Result item missing 'eval_id' or 'id'")

    actual_raw = item.get(
        "triggered",
        item.get(
            "actual_trigger",
            item.get("skill_triggered", item.get("use_skill")),
        ),
    )
    actual = truthy_bool(actual_raw)

    return EvalResult(eval_id=int(raw_id), actual_trigger=actual)


def load_results(path_or_dash: str) -> Dict[int, EvalResult]:
    text = read_text(path_or_dash).strip()
    if not text:
        return {}

    rows: List[Dict[str, Any]] = []
    if text.startswith("["):
        parsed = json.loads(text)
        if not isinstance(parsed, list):
            raise ValueError("JSON results must be an array of objects")
        rows = parsed
    else:
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))

    result_map: Dict[int, EvalResult] = {}
    for item in rows:
        normalized = normalize_result_item(item)
        result_map[normalized.eval_id] = normalized

    return result_map


def paint(text: str, color: str, enabled: bool) -> str:
    if not enabled:
        return text
    return f"{color}{text}{Ansi.RESET}"


def status_for(expected: Optional[bool], actual: Optional[bool]) -> str:
    if expected is None:
        return "SKIP"
    if actual is None:
        return "MISSING"
    return "PASS" if expected == actual else "FAIL"


def as_tf(value: Optional[bool]) -> str:
    if value is True:
        return "TRIGGER"
    if value is False:
        return "NO-TRIGGER"
    return "?"


def truncate(text: str, width: int) -> str:
    text = " ".join(text.split())
    if len(text) <= width:
        return text
    return text[: max(1, width - 1)] + "..."


def print_scorecard(cases: Iterable[EvalCase], results: Dict[int, EvalResult], color: bool) -> int:
    cases = list(cases)

    headers = ["ID", "Expected", "Actual", "Status", "Prompt"]
    rows: List[List[str]] = []

    counts = {"PASS": 0, "FAIL": 0, "MISSING": 0, "SKIP": 0}
    trig_total = 0
    trig_pass = 0
    no_trig_total = 0
    no_trig_pass = 0

    for case in cases:
        result = results.get(case.eval_id)
        actual = result.actual_trigger if result else None
        status = status_for(case.expected_trigger, actual)
        counts[status] += 1

        if case.expected_trigger is True:
            trig_total += 1
            if status == "PASS":
                trig_pass += 1
        elif case.expected_trigger is False:
            no_trig_total += 1
            if status == "PASS":
                no_trig_pass += 1

        rows.append(
            [
                str(case.eval_id),
                as_tf(case.expected_trigger),
                as_tf(actual),
                status,
                truncate(case.prompt, 72),
            ]
        )

    widths = [
        max(len(headers[i]), max((len(row[i]) for row in rows), default=0))
        for i in range(len(headers))
    ]

    print("\nTrigger Evaluation Scorecard\n")
    print(" | ".join(headers[i].ljust(widths[i]) for i in range(len(headers))))
    print("-+-".join("-" * w for w in widths))

    color_map = {
        "PASS": Ansi.GREEN,
        "FAIL": Ansi.RED,
        "MISSING": Ansi.YELLOW,
        "SKIP": Ansi.CYAN,
    }

    for row in rows:
        status = row[3]
        display = row.copy()
        display[3] = paint(status, color_map.get(status, Ansi.RESET), color)
        print(" | ".join(display[i].ljust(widths[i]) for i in range(len(display))))

    considered = counts["PASS"] + counts["FAIL"]
    total = len(rows)
    coverage = ((counts["PASS"] + counts["FAIL"]) / total * 100.0) if total else 0.0
    accuracy = (counts["PASS"] / considered * 100.0) if considered else 0.0

    print("\nSummary")
    print(f"- Total evals: {total}")
    print(f"- PASS: {counts['PASS']}")
    print(f"- FAIL: {counts['FAIL']}")
    print(f"- MISSING: {counts['MISSING']}")
    print(f"- SKIP (no expectation): {counts['SKIP']}")
    print(f"- Coverage: {coverage:.1f}% (results present)")
    print(f"- Accuracy: {accuracy:.1f}% (on covered evals)")

    if trig_total:
        print(f"- Trigger accuracy: {trig_pass}/{trig_total} ({(trig_pass / trig_total) * 100.0:.1f}%)")
    if no_trig_total:
        print(
            f"- Non-trigger accuracy: {no_trig_pass}/{no_trig_total} "
            f"({(no_trig_pass / no_trig_total) * 100.0:.1f}%)"
        )

    return 0 if counts["FAIL"] == 0 and counts["MISSING"] == 0 else 1


def main() -> int:
    args = parse_args()
    cases = load_evals(args.evals)
    results = load_results(args.results)
    return print_scorecard(cases, results, color=not args.no_color)


if __name__ == "__main__":
    raise SystemExit(main())