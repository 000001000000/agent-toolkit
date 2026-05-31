---
name: claude-seo
description: Use this skill whenever a user asks for SEO audits, technical SEO checks, schema validation, sitemap analysis, content quality review, Core Web Vitals, AI search readiness, local SEO, hreflang, backlinks, clustering, e-commerce SEO, or SEO reporting. Trigger even when the user asks in generic terms such as analyze my site, improve search visibility, check structured data, or review page performance.
license: MIT
allowed-tools:
  - Read
  - RunCmd
  - Fetch
---

# Claude SEO Skill

This skill packages the upstream `AgriciDaniel/claude-seo` project as a self-contained skills.sh-compatible skill so any coding agent can use the workflow without relying on the upstream repository at runtime.

The upstream project is vendored under `vendor/claude-seo/`. Preserve that content and use it as the canonical source for workflow details, specialist prompts, references, and script behavior.

## Core rule

Do not improvise a generic SEO answer when the vendored workflow already covers the request. Route first, then follow the matching vendored skill instructions.

## Quick routing

Map user intent to the vendored workflow file below, then read that file before acting:

- Full website audit: `vendor/claude-seo/skills/seo-audit/SKILL.md`
- Deep single-page analysis: `vendor/claude-seo/skills/seo-page/SKILL.md`
- Technical SEO: `vendor/claude-seo/skills/seo-technical/SKILL.md`
- Content quality or E-E-A-T: `vendor/claude-seo/skills/seo-content/SKILL.md`
- Content brief generation: `vendor/claude-seo/skills/seo-content-brief/SKILL.md`
- Schema detection, validation, or generation: `vendor/claude-seo/skills/seo-schema/SKILL.md`
- Image SEO: `vendor/claude-seo/skills/seo-images/SKILL.md`
- Sitemap analysis or generation: `vendor/claude-seo/skills/seo-sitemap/SKILL.md`
- AI search, GEO, AI Overviews, citability: `vendor/claude-seo/skills/seo-geo/SKILL.md`
- Strategic SEO planning: `vendor/claude-seo/skills/seo-plan/SKILL.md`
- Programmatic SEO: `vendor/claude-seo/skills/seo-programmatic/SKILL.md`
- Competitor comparison pages: `vendor/claude-seo/skills/seo-competitor-pages/SKILL.md`
- Local SEO: `vendor/claude-seo/skills/seo-local/SKILL.md`
- Maps and GBP intelligence: `vendor/claude-seo/skills/seo-maps/SKILL.md`
- Hreflang or international SEO: `vendor/claude-seo/skills/seo-hreflang/SKILL.md`
- Google API-backed SEO analysis or reporting: `vendor/claude-seo/skills/seo-google/SKILL.md`
- Backlink analysis: `vendor/claude-seo/skills/seo-backlinks/SKILL.md`
- Semantic clustering: `vendor/claude-seo/skills/seo-cluster/SKILL.md`
- Search experience optimization: `vendor/claude-seo/skills/seo-sxo/SKILL.md`
- Drift monitoring: `vendor/claude-seo/skills/seo-drift/SKILL.md`
- E-commerce SEO: `vendor/claude-seo/skills/seo-ecommerce/SKILL.md`
- FLOW framework prompts: `vendor/claude-seo/skills/seo-flow/SKILL.md`
- Optional extension workflows: inspect the relevant file under `vendor/claude-seo/extensions/`

If the request is broad or ambiguous, start with `vendor/claude-seo/skills/seo/SKILL.md` and then load the relevant specialist workflow.

## Operating procedure

1. Clarify scope only if the user request is materially ambiguous.
2. Read the matching vendored workflow file.
3. If that workflow references additional `references/` material, read only the files needed for the current task.
4. When the task benefits from deterministic tooling, run the vendored scripts from `skills/claude-seo/vendor/claude-seo`.
5. Keep the upstream methodology intact: evidence first, falsifiable recommendations, dependency-aware prioritization, and explicit limitations.

## Script usage

Install Python dependencies from the skill root when needed:

- `cd skills/claude-seo`
- `python3 -m pip install -r requirements.txt`

Run vendored scripts from the vendored repo root so relative paths resolve correctly:

- `cd skills/claude-seo/vendor/claude-seo`
- Example fetch: `python3 scripts/fetch_page.py https://example.com`
- Example PageSpeed check: `python3 scripts/pagespeed_check.py https://example.com`
- Example schema generation: `python3 scripts/schema_generate.py --help`
- Example drift baseline: `python3 scripts/drift_baseline.py https://example.com`

Prefer the vendored script layer for tasks the upstream project already automates.

## Safety rules

1. Treat `vendor/claude-seo/scripts/url_safety.py` as the authoritative URL safety layer for script-backed fetches.
2. Do not weaken the vendored SSRF protections, private-address blocking, or credential file handling.
3. If the user asks for unauthorized, deceptive, or abusive SEO work, refuse or redirect to defensive or legitimate alternatives.
4. Do not claim API-backed findings if the required credentials are not configured.

## Output expectations

Follow the style from the vendored workflow you loaded. In general:

- State what was analyzed and any material limits.
- Separate critical findings from lower-priority improvements.
- Tie each recommendation to evidence and a check that would disconfirm it.
- Prefer actionable reports over generic SEO advice.

## What is bundled

- Vendored upstream workflows: `vendor/claude-seo/skills/`
- Vendored specialist agent prompts: `vendor/claude-seo/agents/`
- Vendored scripts: `vendor/claude-seo/scripts/`
- Vendored docs, references, schema templates, and extension guides

This wrapper is intentionally thin. The bundled upstream material carries the operational detail.