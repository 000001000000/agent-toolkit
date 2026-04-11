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

Repository URL:
- https://github.com/000001000000/agent-toolkit

## Available skills

- [skills/osint-dorking](skills/osint-dorking): OSINT dorking workflow with GHDB-backed search tooling and trigger-eval utilities.

## Development note

Each skill is self-contained so adding additional skills later does not break existing installation paths.
