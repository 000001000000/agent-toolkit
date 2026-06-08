---
name: dev-playbook
description: Use this skill as the primary entry point for any software development request, including frontend, backend, full-stack, refactoring, testing, debugging, and code review. Trigger even when the user does not explicitly ask for best practices. Apply TDD-first workflow, reusable component architecture for UI work, clean code standards, practical library usage, and verification steps by default.
license: MIT
allowed-tools:
  - Read
  - RunCmd
  - Fetch
---

# Development Playbook Skill

This skill is a default operating playbook for software delivery tasks.

If a user asks for development work, this skill should be applied first to decide the delivery approach and quality gates.

## Required companion skill

For all TDD behavior, defer to the dedicated `tdd` skill as the source of truth.

- Required dependency: install the `tdd` skill in the target project/workspace.
- Requirement: when TDD is applicable, load and follow the `tdd` skill workflow instead of re-inventing TDD guidance here.
- Scope: this includes red-green-refactor sequencing, behavior-first testing, and integration-test-oriented strategy.

## Automatic setup and sync

On each invocation in a target project/workspace, run:

- `bash .agents/skills/dev-playbook/scripts/ensure-setup.sh`

Behavior:
- First run: installs companion `tdd` skill and initializes managed instructions.
- Every run: syncs the managed instructions block when the template changed.
- It tracks template version/hash in `.dev-playbook/.initialized`.
- No-op when there are no setup/template changes.

## Core operating principles

1. Prefer TDD by default.
- Use the `tdd` skill workflow as the primary TDD method.
- Start with a failing test when the task is testable.
- Implement the smallest change to pass.
- Refactor after green tests.
- If strict TDD is not practical (for example one-off infra scripts or design spikes), explain why and still add verification.

2. Build maintainable architecture, not one-off code.
- Favor clear module boundaries and composable units.
- Keep functions and components focused on a single responsibility.
- Avoid tight coupling and hidden side effects.

3. Reuse before build, especially for frontend.
- Before creating anything new, check whether an equivalent component/module already exists in the codebase.
- If it exists and meets requirements, reuse or extend it instead of duplicating.
- If it does not exist, evaluate whether a library is the better choice.
- Only build from scratch when reuse is not possible and a library is not a good fit.

4. Use libraries when they provide clear leverage.
- Prefer mature, well-documented libraries for common concerns.
- Do not reinvent commodity functionality unless the user asks.
- Keep dependency choices minimal and justified.

5. Verify, do not assume.
- Run tests and relevant checks when possible.
- For frontend, include visual verification steps.
- Report what was validated and what could not be validated.

6. Optimize for readability and explicitness.
- Prefer straightforward code over clever shortcuts.
- Use clear names and explicit contracts/types where supported.
- Keep behavior discoverable from public interfaces.

7. Preserve compatibility when it is warranted.
- First assess project maturity and dependency surface before enforcing backward compatibility.
- If the feature/module is still in active dev phase with no real consumers, prioritize delivery speed and code clarity over compatibility overhead.
- If there are real downstream consumers (other modules, external clients, released integrations), treat compatibility as a requirement.
- When compatibility is required, identify API/contract impact, prefer additive changes, and include migration notes for unavoidable breaks.

8. Build with observability in mind.
- Add actionable logs at critical boundaries and failure points.
- Include enough context in errors for fast debugging.
- Avoid noisy logging that hides signal.

9. Enforce consistency through automation.
- Run lint/format/type checks where available.
- Keep CI expectations aligned with local verification steps.
- Do not bypass failing quality gates without explicit user approval.

10. Avoid hidden complexity.
- If introducing a new abstraction, layer, or framework, provide a short justification tied to current requirements.
- Prefer the simplest design that satisfies the current scope.
- Do not add extension points for hypothetical future use unless explicitly requested.

11. Run a security quick-pass on every change.
- Check input validation and output encoding at trust boundaries.
- Check authn/authz impact for protected behavior.
- Check secret handling (no hardcoded tokens, no sensitive logging).
- Check dependency trust for newly added libraries.

## Stage-based workflow

Always classify the request into one or more stages and apply matching rules.

### Frontend stage

Use these rules whenever UI work is requested.

1. Component architecture
- Reuse-first decision order: existing component -> library -> new component.
- Search for existing components, primitives, or patterns before building anything new.
- If an existing component is close but not exact, prefer extension/composition over duplication.
- If no suitable component exists, evaluate proven UI libraries before custom implementation.
- If custom implementation is required, build it as a reusable component with a clear public API.
- Build reusable, composable components.
- Separate presentational concerns from stateful logic when useful.
- Extract shared primitives before duplicating markup.

2. UI code quality
- Keep props and public interfaces explicit and typed when the stack supports it.
- Keep styling consistent with the project design system.
- Avoid inline one-off hacks unless strictly necessary.

3. Accessibility and UX baseline
- Use semantic HTML.
- Ensure keyboard navigation and visible focus states.
- Ensure sufficient contrast and meaningful labels.

4. Visual verification
- Verify desktop and mobile states.
- Verify core interaction states (loading, empty, error, success).
- If available, use screenshots, storybook states, or visual regression checks.

### Backend stage

Use these rules whenever API, data, service, or infrastructure logic is requested.

1. Contract-first thinking
- Define or confirm interfaces (request/response, events, schemas) before implementation.
- Validate inputs at boundaries.

2. Reliability and safety
- Add robust error handling and meaningful logs.
- Make side effects explicit.
- Prefer idempotent behavior for retry-prone operations.

3. Data and performance
- Choose clear data access patterns and avoid hidden N+1 behavior.
- Measure before optimizing; optimize bottlenecks intentionally.

4. Security baseline
- Enforce authn/authz expectations.
- Avoid leaking secrets and sensitive internals.
- Sanitize and validate external input.

### Full-stack stage

When frontend and backend are both involved, apply both stage rule sets and explicitly verify integration points:
- Contract compatibility between client and server.
- Error shape consistency.
- End-to-end user flow validation.

### Testing stage

When writing or modifying tests, use this priority order:
1. Unit tests for core logic.
2. Integration tests for boundaries and data flow.
3. End-to-end tests for critical user journeys.

Testing expectations:
- Test behavior, not implementation details.
- Cover happy path plus key edge/failure paths.
- Keep fixtures minimal and readable.

## Request handling algorithm

For each request, follow this sequence:

1. Ensure setup/sync is current (run `scripts/ensure-setup.sh`).
2. Classify stage: frontend, backend, full-stack, testing, or mixed.
3. Perform reuse-first scan: existing code artifacts first, then library options.
4. Propose a concise implementation path and justify build-vs-reuse decision.
5. Apply TDD loop when feasible.
6. Implement with reusable design and clean abstractions.
7. Run verification (tests/lint/build/visual checks as applicable).
8. Run security quick-pass checklist and record findings.
9. Report outcomes, risks, and any unverified assumptions.

Complexity gate:
- Before adding new abstraction layers, justify why simpler alternatives are insufficient.
- For early dev-phase features with no active consumers, ask before adding compatibility shims, generalized extension points, or architecture-heavy patterns.

TDD rule for step 3:
- Load the installed `tdd` skill and follow it for cycle planning and execution.

## Output contract

When responding after implementation, include:
- What changed.
- Why this design was chosen.
- What was verified.
- Remaining risks or follow-ups.

Definition of Done (must be explicit):
- Relevant tests are passing, or a clear reason is provided if tests are unavailable.
- Lint/format/type checks are run when available, or a clear reason is provided.
- Security quick-pass completed with findings noted.
- Reuse/library/custom and compatibility decisions are documented.
- If behavior changed for users or consumers, docs or migration notes are updated.

Required decision checklist (always include):
- Reused existing component/module: yes or no, with short reason.
- Evaluated library option: yes or no, with short reason.
- Built custom component/module: yes or no, with short reason.
- Backward compatibility required: yes or no, based on project phase and active consumers.
- Added new abstraction/layer: yes or no, with short justification.

## Mandatory usage guidance

This skill is designed to act as the main entry playbook for development tasks.

Important limitation: skill systems typically cannot enforce absolute mandatory execution for every possible prompt by themselves.

To approximate mandatory behavior:
1. Install `dev-playbook` in every target workspace/project.
2. On invocation, run automatic setup/sync to keep companion `tdd` and managed workspace instructions current.
3. Preferred `tdd` source: `npx skills add https://github.com/mattpocock/skills --skill tdd`.
4. Keep the description broad and trigger-focused (already done here).
5. Add a workspace or user-level instruction that makes this playbook the default for development requests.

## Example triggers

- Build a settings page with reusable components and clean state handling.
- Add an API endpoint with validation and tests.
- Refactor this feature and keep behavior stable.
- Implement this full-stack flow and verify the integration.
- Add tests before changing this module.
