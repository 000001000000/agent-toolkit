# OSINT Dorking Skill

A skills.sh-compatible skill that helps AI agents handle OSINT dorking requests across Google-style operators and related workflows (GHDB-backed baseline, extensible to Shodan/GitHub style query discovery patterns).

## Install

From the repository root path:

```bash
npx skills add <owner>/<repo>/skills/osint-dorking
```

## What is included

- SKILL instructions: [SKILL.md](SKILL.md)
- Search tool: [scripts/search_dorks.py](scripts/search_dorks.py)
- Shell wrapper: [scripts/search.sh](scripts/search.sh)
- Trigger eval set: [evals/evals.json](evals/evals.json)
- Eval checker: [scripts/check_evals.py](scripts/check_evals.py)

## Setup

Install Python dependency:

```bash
python3 -m pip install -r requirements.txt
```

## Usage

Run from this skill directory:

```bash
cd skills/osint-dorking
```

Search by keyword:

```bash
./scripts/search.sh --keyword wordpress --limit 10
```

Filter by category:

```bash
./scripts/search.sh --keyword config --category "Files Containing Juicy Info" --limit 20
```

JSON output:

```bash
./scripts/search.sh --keyword exposed --format json --limit 20
```

Direct Python entrypoint:

```bash
python3 scripts/search_dorks.py --keyword wordpress --limit 10
```

## Testing / Evaluation

Run checker with bundled mock results:

```bash
python3 scripts/check_evals.py --results evals/mock_results.jsonl
```

Read results from stdin:

```bash
cat evals/mock_results.jsonl | python3 scripts/check_evals.py --results -
```

The checker prints a PASS/FAIL scorecard and exits non-zero on FAIL or MISSING rows.

## Data source

Primary baseline source:
- https://gitlab.com/exploit-database/exploitdb/-/raw/main/ghdb.xml

The script caches data to this skill-local path:
- data/ghdb.xml
