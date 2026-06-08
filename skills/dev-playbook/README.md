# Dev Playbook Skill

This skill is a default software delivery playbook that can be installed into an agent environment.

It provides opinionated baseline behavior for:
- TDD-first implementation
- Frontend reusable component architecture
- Backend reliability and contract-first delivery
- Full-stack integration verification
- Practical testing and visual checks

## Companion requirement

This skill expects the `tdd` skill to be available and uses it as the canonical workflow for TDD execution.

## Install

```bash
npx skills add 000001000000/agent-toolkit/skills/dev-playbook
```

First invocation behavior:
- On first invocation, dev-playbook runs `.agents/skills/dev-playbook/scripts/ensure-setup.sh` automatically.
- This one-time setup installs companion `tdd` (`https://github.com/mattpocock/skills --skill tdd`).
- It merges or appends the managed workspace instructions block in `.github/copilot-instructions.md`.
- It writes `.dev-playbook/.initialized`.

Ongoing invocation behavior:
- On later invocations, the same script runs in sync mode.
- If the managed template changed, it updates the managed block automatically.
- If no template change is detected, it no-ops.

Optional manual setup (non-interactive/bootstrap scripting):

```bash
bash .agents/skills/dev-playbook/scripts/setup-project.sh
```

First-run automatic setup:
- On first invocation, dev-playbook runs `.agents/skills/dev-playbook/scripts/ensure-setup.sh`.
- This one-time setup installs companion `tdd`, merges or appends the managed instructions block, and writes `.dev-playbook/.initialized`.
- Later invocations use the same script to sync managed instructions when templates are updated.

## Why use it

Use this as your main skill so you do not need to repeat the same development quality expectations in every prompt.

## Use in any project

1. Install `dev-playbook` in the target project/workspace.
2. Invoke `dev-playbook` once; it performs one-time setup automatically.
3. Continue normal usage; setup is skipped after initialization.

Template instructions for copy/paste are in `templates/copilot-instructions.md`.

## Included files

- SKILL.md: Playbook instructions and stage-based workflow.
- evals/evals.json: Starter eval prompts for validating trigger and behavior.
