# Contributing to EMO-Core

EMO-Core is maintained by one person, Adrian N. Avramescu (independent researcher). Contributions, bug reports and questions are welcome.

## Reporting a problem or asking for help

Open an issue at https://github.com/avram3scu-art/emo-core-v1/issues. Include the command you ran, the Python version, and the full error output. Replies are on a best-effort basis; no response time is guaranteed.

## Proposing a change

1. Fork the repository and branch from `emo-2026-10` (the default branch).
2. Install as described in the README "Run it locally" section, including `git config core.hooksPath scripts/hooks`.
3. Add or update tests in `tests/` for any code change; `pytest -q` must pass.
4. The pre-push hook runs the claim-word check (`python scripts/claims_grep.py`), `ruff` and the fast tests. Do not bypass it with `--no-verify`.
5. Open a pull request describing what changed and why.

## Project rules a contribution must keep

These come from `CLAUDE.md` and apply to code, documentation and results alike:

- No statement in a README, paper or report beyond what the code does today.
- Multi-part measures (DAC, UIA) are reported as profiles of their components, never as a weighted score.
- Every result carries one evidence class (pre-registered blind, pre-registered on known history, exploratory, infrastructure).
- A test is pre-registered (protocol committed) before its data are opened.

## Governance

The maintainer decides what is merged. Decisions and their reasons are recorded in `docs/STATUS.md`.

## Licence

By contributing you agree that your contribution is licensed under the AGPL-3.0 (`LICENSE`). The project also offers a separate commercial licence (`LICENSE-COMMERCIAL`); how outside contributions relate to it has not been decided yet, so please ask in an issue before sending a large change.
