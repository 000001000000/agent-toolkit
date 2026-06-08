# BEGIN dev-playbook managed block

# Copilot Workspace Instructions

Use the dev-playbook skill as the default workflow for every software development request in this workspace.

## Default behavior

1. Treat dev-playbook as mandatory first-pass guidance for:
- Frontend work
- Backend work
- Full-stack work
- Refactoring
- Testing
- Debugging
- Code review

2. Apply TDD-first by default when feasible:
- Before executing TDD guidance, load and follow the installed tdd skill as the canonical TDD workflow.
- Red: write or update a failing test.
- Green: implement the smallest change to pass.
- Refactor: clean up while tests remain green.

3. Enforce reuse-first implementation for all code, with extra emphasis on frontend:
- First, check whether equivalent code/component already exists and reuse or extend it.
- If not, evaluate whether a library should be used.
- If neither reuse nor library is suitable, build it as a reusable component/module.

4. Apply backward compatibility conditionally:
- If a feature/module is in early dev phase and has no active consumers, do not force compatibility overhead.
- If there are active internal/external consumers, treat compatibility as required.

5. Include this decision checklist in implementation summaries:
- Reused existing component/module: yes or no, with short reason.
- Evaluated library option: yes or no, with short reason.
- Built custom component/module: yes or no, with short reason.
- Backward compatibility required: yes or no, with short reason.
- Added new abstraction/layer: yes or no, with short justification.

6. Enforce a Definition of Done in implementation summaries:
- Relevant tests passing (or clear reason not run).
- Lint/format/type checks run where available (or clear reason not run).
- Security quick-pass completed and findings reported.
- Reuse/library/custom and compatibility decisions documented.
- Docs or migration note updated when user-facing behavior changes.

7. No hidden complexity and ask-before-overengineering:
- Do not add architecture-heavy abstractions without a short justification.
- For early dev-phase features with no active consumers, ask before adding compatibility shims or speculative extension points.

8. Run a security quick-pass on every change:
- Input validation and trust boundary checks.
- Authn/authz impact checks.
- Secret handling checks.
- Dependency trust checks for new libraries.

## Exception handling

If strict TDD is not practical for a request, briefly explain why and still provide concrete verification steps.

# END dev-playbook managed block
