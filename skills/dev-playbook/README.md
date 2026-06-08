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

## Why use it

Use this as your main skill so you do not need to repeat the same development quality expectations in every prompt.

## Included files

- SKILL.md: Playbook instructions and stage-based workflow.
- evals/evals.json: Starter eval prompts for validating trigger and behavior.
