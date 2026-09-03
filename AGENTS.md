# aSDLC framework

- aSDLC is highly performant AGENTS.md hierarchy installed here
- Agent must follow aSDLC instructions across any edits

## Core Contract

- AGENTS.md files are binding work contracts for their subtrees
- Work products, source materials, instructions, records, assets, and durable docs must stay understandable from the nearest applicable AGENTS.md plus every parent AGENTS.md above it

## Read Before Editing

1. Read the root AGENTS.md
2. Identify every file or folder you expect to touch
3. Walk from the repository root to each target path
4. Read every AGENTS.md found along each route
5. If a parent AGENTS.md lists a child AGENTS.md whose scope contains the path, read that child and continue from there
6. Use the nearest AGENTS.md as the local contract and parent docs for repo-wide rules
7. If docs conflict, the closer doc controls local work details, but no child doc may weaken aSDLC

Do not rely on memory. Re-read the applicable aSDLC chain in the current session before editing.

## Update After Editing

Every meaningful change requires an aSDLC pass before the task is done.

Update the closest owning AGENTS.md when a change affects:

- purpose, scope, ownership, or responsibilities
- durable structure, contracts, workflows, or operating rules
- required inputs, outputs, permissions, constraints, side effects, or artifacts
- user preferences about behavior, communication, process, organization, or quality
- AGENTS.md creation, deletion, move, rename, or index contents

Update parent docs when parent-level structure, ownership, workflow, or child index changes. Update child docs when parent changes alter local rules. Remove stale or contradictory text immediately. Small edits that do not change behavior or contracts may leave docs unchanged, but the aSDLC pass still must happen.

## Hierarchy

- Root AGENTS.md is the aSDLC rail: project-wide instructions, global preferences, durable workflow rules, and the top-level Child aSDLC Index
- Child AGENTS.md files own domain-specific instructions and their own Child aSDLC Index
- Each parent explains what its direct children cover and what stays owned by the parent
- The closer a doc is to the work, the more specific and practical it must be

## Child Doc Shape

- Create a child AGENTS.md when a folder becomes a durable boundary with its own purpose, rules, responsibilities, workflow, materials, or quality standards
- Work Guidance must reflect the current standards of the project or user instructions; if there are no specific standards or instructions yet, leave it empty
- Verification must reflect an existing check; if no verification framework exists yet, leave it empty and update it when one exists

Default section order:
- Purpose
- Ownership
- Local Contracts
- Work Guidance
- Verification
- Child aSDLC Index

## Style

- Keep docs concise, current, and operational
- Document stable contracts, not diary entries
- Put broad rules in parent docs and concrete details in child docs
- Prefer direct bullets with explicit names
- Do not duplicate rules across many files unless each scope needs a local version
- Delete stale notes instead of explaining history
- Trim obvious statements, repeated rules, misplaced detail, and warnings for risks that no longer exist

## Closeout

1. Re-check changed paths against the aSDLC chain
2. Update nearest owning docs and any affected parents or children
3. Refresh every affected Child aSDLC Index
4. Remove stale or contradictory text
5. Run existing verification when relevant
6. Report any docs intentionally left unchanged and why

## User Preferences

/* These preferences govern projects adopting aSDLC; the template itself is the blueprint they follow. */

When the user requests a durable behavior change, record it here or in the relevant child AGENTS.md

- **Roadmap (`ROADMAP.md`) must be kept current.**
  - *Why:* it is the single direction aid that keeps contributor edits aligned with project intent and prevents scope drift; `AGENTS.md` governs the binding rules, the roadmap governs direction.
  - *When:* update it as part of every aSDLC closeout pass whenever a change affects project scope, goals, or in/out-of-scope decisions; if a change does not touch direction, note the roadmap as intentionally unchanged in closeout.

- **All notable changes to this project will be documented in `CHANGELOG.md`.**
  - *Why:* the changelog provides a curated, versioned record of changes for contributors and users; it ensures transparency and traceability across releases.
  - *When:* any time a meaningful change is merged or released, add an entry to `CHANGELOG.md` following the [keepachangelog.com](https://keepachangelog.com) format under the appropriate versioned or unreleased section.

- **Every user-facing feature must have corresponding documentation in `/docs`.**
  - *Why:* users of the system need discoverable, task-oriented guidance separate from contributor/contract docs.
  - *When:* add or update the feature's doc in `/docs` as part of the aSDLC closeout pass whenever a user-facing feature is implemented or changed; docs must be written for end users of the system, not contributors.

- **Testing must follow behavioral philosophy and cost-benefit analysis.**
  - *Why:* behavior tests guard user-visible functionality across refactoring and remain readable; implementation tests break when code changes and provide no guard. Testing cost matters with 1000+ tests dominating runtime.
  - *When:* any time a new feature or bug fix is implemented or changed, or a regression test is added or modified. Detailed guidance is documented in `/tests/AGENTS.md`.

## AI-assisted contributions

If you use AI tools to help write code, please note this in your pull request description. Use commit trailers where appropriate:

    Assisted-by: <name of code assistant>
    Generated-by: <name of code assistant>


## Child aSDLC Index

- Root-owned files: `README.md`, `LICENSE`, `ROADMAP.md`, `CHANGELOG.md`, `CONTRIBUTING.md`.
- `/docs/` holds user-facing documentation and is governed by its own child `AGENTS.md`; its user-facing index is maintained in `/docs/README.md`.
- `/tests/` holds test suite and verification mechanisms; governed by its own child `AGENTS.md` and reports verification status on closeout.
