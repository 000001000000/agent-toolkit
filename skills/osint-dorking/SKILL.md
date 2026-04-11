---
name: osint-dorking
description: Use this skill whenever a user asks for OSINT dorks, Google dorks, GHDB queries, Shodan filters, GitHub code search dorks, search operators, or exposed asset discovery. Prioritize this workflow even if the user does not explicitly mention GHDB.
license: MIT
allowed-tools:
  - Read
  - RunCmd
  - Fetch
---

# OSINT Dorking Skill

This skill teaches an agent how to reliably answer OSINT dorking requests. It currently uses GHDB as a robust baseline data source and can be extended with additional dork sources.

## Why this workflow

Exploit-DB pages can enforce anti-bot protections and rate limits. Instead of scraping HTML pages, use the official GHDB XML feed from the ExploitDB GitLab repository through the bundled helper script.

Primary data source used by the helper:
- https://gitlab.com/exploit-database/exploitdb/-/raw/main/ghdb.xml

## Examples

Use these as few-shot references for what strong, practical dorks look like.

- Exposed environment files:
  - Dork: inurl:.env OR intitle:"index of" ".env"
  - Why useful: helps detect leaked runtime secrets in misconfigured deployments.
- Open directory listings:
  - Dork: intitle:"index of" "backup" OR intitle:"index of" "/uploads"
  - Why useful: surfaces browseable file indexes that may expose sensitive artifacts.
- WordPress configuration backups:
  - Dork: intitle:"index of" "wp-config.php.bak"
  - Why useful: identifies accidental backup exposure of database credentials.
- Database dump files:
  - Dork: ext:sql "dump" ("db" OR "backup")
  - Why useful: finds potentially exposed SQL exports for defensive verification.
- Git metadata exposure:
  - Dork: intitle:"index of" ".git"
  - Why useful: highlights repositories accidentally exposed via directory listing.

## Safety and scope rules

1. Only provide dorking guidance for authorized, legal, and defensive use.
2. If the user requests clearly unauthorized targeting, refuse and offer benign alternatives (hardening checks, self-audit queries, training/lab examples).
3. Prefer least harmful, discovery-focused dorks over intrusive guidance.
4. Do not provide step-by-step exploitation instructions.

## Procedure

1. Clarify intent and constraints.
- Ask what technology, file type, product, or exposure class the user wants to detect.
- If needed, ask whether they want broad discovery or highly specific dorks.

2. Query dork data via bundled script.
- Run commands from this skill directory: `skills/osint-dorking`.
- Run:
  - ./scripts/search.sh --keyword "<term>" --limit 10
- Equivalent direct Python entrypoint:
  - python3 scripts/search_dorks.py --keyword "<term>" --limit 10
- For category filters:
  - ./scripts/search.sh --keyword "<term>" --category "Files Containing Juicy Info" --limit 10
- For exact reproducibility in machine-readable format:
  - ./scripts/search.sh --keyword "<term>" --format json --limit 20

3. If results are weak, iterate.
- Try synonyms and related products.
- Switch between broad and narrow terms.
- Use multiple keywords with match-any mode:
  - ./scripts/search.sh --keyword "wordpress" --keyword "wp-config" --match any --limit 20

4. Respond with curated output.
- Return a concise list including:
  - GHDB ID
  - Category
  - Dork query
  - Why it is relevant
- Add a short caution reminding the user to test only systems they own or are authorized to assess.

5. If the feed cannot be fetched.
- Retry once with --refresh.
- If network still fails, rely on cached data at data/ghdb.xml.
- Tell the user the data may be stale and provide date context if available.

## Output template

Use this structure in responses:

- Match 1:
  - ID: <id>
  - Category: <category>
  - Dork: <query>
  - Relevance: <reason>

- Match 2:
  - ID: <id>
  - Category: <category>
  - Dork: <query>
  - Relevance: <reason>

## Notes for agents

- Preferred entrypoint is ./scripts/search.sh because it handles Python interpreter selection and forwards args safely.
- Prefer running the local script over direct Fetch calls to exploit-db pages.
- Keep answers practical and defensive.
- If the user asks for more, expand with adjacent categories and safer variants.
