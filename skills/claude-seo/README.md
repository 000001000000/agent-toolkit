# Claude SEO Skill

A skills.sh-compatible packaging of the upstream Claude SEO project for use with generic coding agents.

## Install

From the repository root path:

```bash
npx skills add 000001000000/agent-toolkit/skills/claude-seo
```

Repository URL:
- https://github.com/000001000000/agent-toolkit

## What is included

- Generic skill entrypoint: `SKILL.md`
- Vendored upstream core snapshot: `vendor/claude-seo/`
- Python dependencies shim: `requirements.txt`
- Trigger eval set: `evals/evals.json`
- Eval checker: `scripts/check_evals.py`

## Upstream provenance

- Source repository: https://github.com/AgriciDaniel/claude-seo
- Vendored commit: `dabfc1abb4ca9a4d7967242bf00d52593be56ed1`
- License: MIT

The vendored copy keeps the upstream workflow, specialist prompts, scripts, docs, and extension guides inside this skill so installation does not depend on the upstream repo.

## Setup

Install Python dependencies from the skill root:

```bash
cd skills/claude-seo
python3 -m pip install -r requirements.txt
```

## Usage

Use natural-language requests with any agent that supports skills. Typical prompts:

- "Run a full SEO audit for https://example.com"
- "Check this page for schema markup issues"
- "Review this site for local SEO and GBP problems"
- "Analyze AI search readiness for this article"

For script-backed workflows, run from the vendored upstream root:

```bash
cd skills/claude-seo/vendor/claude-seo
python3 scripts/fetch_page.py https://example.com
python3 scripts/pagespeed_check.py https://example.com
```

## Security note

The vendored upstream core includes defensive URL safety controls in `scripts/url_safety.py` and credential handling utilities. A quick audit during packaging found no obvious malicious behavior, remote-execution stubs, or shell-injection patterns in the core scripts.

## Testing / Evaluation

Run the lightweight trigger checker with bundled or generated results:

```bash
python3 scripts/check_evals.py --results evals/mock_results.jsonl
```

Or from stdin:

```bash
cat evals/mock_results.jsonl | python3 scripts/check_evals.py --results -
```