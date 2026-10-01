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
- Keep each doc task-oriented, concise, and operational.

## Verification

## Child aSDLC Index

- No further child AGENTS.md files. Individual docs are plain user-facing
  markdown and are not governed by their own AGENTS.md.
