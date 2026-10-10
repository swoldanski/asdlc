# /architecture — DevSecOps Manual

## Purpose

Hold the DevSecOps manual: how things work under the hood — contributor-facing
and non-end-user implementation documentation covering internal design,
architecture decisions, and contributor workflows. Kept out of `/docs`.

## Ownership

Owned by this child aSDLC doc. Follows the root aSDLC contract. Any change
touching `/architecture` content goes through the aSDLC pass (Read Before
Editing → edit → Update After Editing → Closeout).

## Local Contracts

- `/architecture` holds the DevSecOps manual — how things work under the hood —
  for contributors and non-end-user implementation details only.
- The user manual (how end users do things) belongs in `/docs`, not here.
- Content here may describe internal design, contracts, and contributor
  workflow that users are not expected to read.
- The documentation index is maintained in `/architecture/README.md`.

## Work Guidance

- Place contributor-facing or implementation-detail docs here as part of the
  aSDLC closeout pass whenever such documentation is added or changed.

## Verification

## Child aSDLC Index

- No further child AGENTS.md files. Individual docs are plain markdown and are
  not governed by their own AGENTS.md.
