# /docs — User Manual

## Purpose

Hold the user manual: end-user documentation for the project's user-facing
features only — how end users do things — so users get discoverable,
task-oriented guidance. The DevSecOps manual (how things work under the hood)
lives in `/architecture`.

## Ownership

Owned by this child aSDLC doc. Follows the root aSDLC contract. Any change
touching `/docs` content or the documentation index goes through the aSDLC
pass (Read Before Editing → edit → Update After Editing → Closeout).

## Local Contracts

- `/docs` holds the user manual — how end users do things — for end-user-facing
  features only.
- Documentation for contributors, internal design, DevSecOps, or any other
  non-end-user implementation detail (how things work under the hood) must be
  kept in `/architecture`, not here.
- Every user-facing feature implemented in the project must have a
  corresponding doc in this folder (root User Preferences rule).
- Docs are written for end users of the system, not contributors.
- The user-facing documentation index is maintained in `/docs/README.md`.

## Work Guidance

- Add or update a feature's doc here as part of the aSDLC closeout pass
  whenever a user-facing feature is implemented or changed.
- Before adding a doc here, confirm the content is end-user-facing; if it
  describes contributor workflow or implementation internals, place it in
  `/architecture` instead.
- **No plans, spikes, or session artifacts — ever.** A plan is a working
  document for the change that produced it, not a manual page. Plans and
  scratch work belong in the git-ignored scratch directory; a delivered change
  belongs in `CHANGELOG.md` and the docs it touched, and the durable *decisions*
  belong in the doc they govern, not in the plan that proposed them. A plan that
  ships as a manual page carries its own staleness forward, because nothing
  re-reads it. If you are writing "the plan" or "not yet implemented" into a
  `/docs` file, it is in the wrong place.
- **Generated docs stay generated.** A doc written by a generator is never
  hand-edited — its navigation (an index and back-links, where it has them) is
  part of its contract, and a missing entry or back-link is otherwise invisible,
  because the page still builds and every remaining link still resolves. Change
  the generator and re-render instead.
- Keep each doc task-oriented, concise, and operational.

## Verification

## Child aSDLC Index

- No further child AGENTS.md files. Individual docs are plain user-facing
  markdown and are not governed by their own AGENTS.md.
