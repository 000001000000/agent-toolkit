# Multi-Skill Repository For AI Agent Skills

This repository is structured as a multi-skill package for the skills.sh ecosystem.

## Repository layout

```text
.
├── skills-lock.json
└── skills
    └── osint-dorking
        ├── SKILL.md
        ├── README.md
        ├── requirements.txt
        ├── data
        ├── evals
        └── scripts
```

## Install a specific skill

Install the OSINT dorking skill directly via subpath:

```bash
npx skills add 000001000000/agent-toolkit/skills/osint-dorking
```

Install the Claude SEO skill directly via subpath:

```bash
npx skills add 000001000000/agent-toolkit/skills/claude-seo
```

Install the Dev Playbook skill directly via subpath:

```bash
npx skills add 000001000000/agent-toolkit/skills/dev-playbook
```

Repository URL:
- https://github.com/000001000000/agent-toolkit

## Available skills

- [skills/osint-dorking](skills/osint-dorking): OSINT dorking workflow with GHDB-backed search tooling and trigger-eval utilities.
- [skills/claude-seo](skills/claude-seo): Generic-agent packaging of the Claude SEO workflow with vendored upstream scripts, prompts, and reference material.
- [skills/dev-playbook](skills/dev-playbook): Default software development playbook with TDD-first flow, frontend/backend/full-stack rules, and verification gates.

## Use In Any Project

For projects where you want this behavior by default:

1. Install playbook skill:

```bash
npx skills add 000001000000/agent-toolkit/skills/dev-playbook
```

2. Invoke `dev-playbook` once in that project.
- On first invocation, the skill runs one-time setup automatically.
- It installs companion `tdd` from Matt Pocock's skills repository.
- It merges or appends the managed workspace instructions block.
- It writes `.dev-playbook/.initialized` so later invocations skip setup.

3. Continue using `dev-playbook` normally.
- On every invocation, setup sync checks for template updates and refreshes the managed instructions block automatically when needed.

Optional manual setup (for non-interactive/bootstrap scripting):

```bash
bash .agents/skills/dev-playbook/scripts/setup-project.sh
```

First-run behavior:
- On first use of dev-playbook in a target project, it runs one-time setup via `.agents/skills/dev-playbook/scripts/ensure-setup.sh`.
- This installs companion `tdd`, merges or appends the managed workspace instructions block, and writes `.dev-playbook/.initialized`.

Update behavior:
- On later invocations, the same script runs in sync mode and updates the managed instructions block only if the template changed.

## Development note

Each skill is self-contained so adding additional skills later does not break existing installation paths.
