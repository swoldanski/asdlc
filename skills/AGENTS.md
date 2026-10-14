# /skills — Skill Packaging

## Purpose

Hold the skill packages this repository ships, together with their
slash-command entrypoints under `/commands/`. These are the template's own
distribution artifacts — they publish aSDLC tooling to agents; they are not
part of any project scaffolded from this template.

## Ownership

Owned by this child aSDLC doc. Follows the root aSDLC contract. Any change
touching `/skills` or `/commands` content goes through the aSDLC pass (Read
Before Editing → edit → Update After Editing → Closeout).

## Local Contracts

- Each skill is one directory under `/skills/` with a `SKILL.md` carrying
  `name` and `description` frontmatter; supporting files (scripts, references)
  live beside it and are shipped with it.
- A `SKILL.md` that ships executable code declares it: `allowed-tools` (the
  standard Agent Skills field, and the manifest a security scanner reads — an
  *undeclared* capability is what a least-privilege finding reports),
  `compatibility` for the runtime it needs, and `metadata` naming the script,
  its network use and the files it writes. The body must match the script: a
  capability the script has and the frontmatter omits is a defect in the
  declaration, not a finding to suppress.
- The skill package is this repository's documentation of its own tooling.
  Template-specific how-to cannot live in `/docs` or `/architecture`, because
  both are copied verbatim into every scaffold and would describe the template
  to a project that is not one.
- Slash-command entrypoints live in `/commands/<name>.md` and delegate to a
  skill rather than restating its workflow.
- `/skills/` and `/commands/` are template packaging: the bootstrap script
  excludes both, so they never appear in a scaffolded project.

## Work Guidance

- Keep each `SKILL.md` lean and self-contained: a third-person `description`
  naming its trigger phrases, an imperative workflow body, and pointers to the
  files it ships.
- Keep a skill's logic in its bundled scripts; the `SKILL.md` explains how to
  run them and how to interpret the result, not a paraphrase of the code.
- A skill that ships a script names, in one short body section, the executable,
  what it shells out to, and every file it rewrites — plus the flags and exit
  codes automation depends on.
- Prefer one command entrypoint that delegates to a skill over duplicating the
  skill's steps in the command file.

## Verification

## Child aSDLC Index

- No further child AGENTS.md files. Individual skill packages are plain
  directories and are not governed by their own AGENTS.md.
