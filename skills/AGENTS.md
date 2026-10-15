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
  declaration, not a finding to suppress. Scope `allowed-tools` to the calls the
  skill makes (`Bash(python3:*) Bash(git:*)`) rather than a blanket `Bash`, which
  grants more than the script uses; the spec's own example of the field is the
  scoped form.
- The skill package is this repository's documentation of its own tooling.
  Template-specific how-to cannot live in `/docs` or `/architecture`, because
  both are copied verbatim into every scaffold and would describe the template
  to a project that is not one.
- A skill package that ships to other agents must satisfy the Agent Skills
  specification, not only this repository's conventions: `skills-ref validate
  <skill-dir>` (from `agentskills/agentskills`) is the reference check, and it
  allows exactly six frontmatter fields — `name`, `description`, `license`,
  `allowed-tools`, `metadata`, `compatibility` — written in block style, because
  its parser rejects flow-style YAML. Clients and templates add fields of their
  own (`version`, `author`, `platforms`), which the reference validator rejects,
  so a field that exists for one client only stays out of a published package.
- Slash-command entrypoints live in `/commands/<name>.md` and delegate to a
  skill rather than restating its workflow.
- `/skills/` and `/commands/` are template packaging: the bootstrap script
  excludes both, so they never appear in a scaffolded project.

## Work Guidance

- Keep each `SKILL.md` lean and self-contained: an imperative workflow body and
  pointers to the files it ships.
- The `description` opens with one sentence whose trigger survives the index
  window a client shows — a longer one is truncated to its first ~57 characters
  plus an ellipsis, so nothing routing depends on may live past that. The Agent
  Skills spec's *when to use* clause may follow as a second sentence; trigger
  *phrases* belong in `## When to Use`.
- The `name` is an invocation form, not only a label: a client that derives its
  slash command from the frontmatter registers `/` plus the slugified `name`, so
  a nicer alias exists only where the client also installs the repository's
  `commands/<name>.md` — Hermes installs neither that file nor anything outside
  the skill directory.
- Keep a skill's logic in its bundled scripts; the `SKILL.md` explains how to
  run them and how to interpret the result, not a paraphrase of the code.
- A skill that ships a script names, in one short body section, the executable,
  what it shells out to, and every file it rewrites — plus the flags and exit
  codes automation depends on.
- Prefer one command entrypoint that delegates to a skill over duplicating the
  skill's steps in the command file.

## Verification

- `skills-ref validate skills/<name>` — the Agent Skills reference check; a
  package is valid when it exits 0. Run it after any frontmatter change.
- The capability scans on the skill directory — the skills guard (`verdict:
  safe`) and SkillSpector (`risk score`, maximum issue severity) — after any
  change to a bundled script or to its declaration, because a capability the
  script has and the frontmatter omits is what these report.
- The bundled script itself, run against a throwaway target: the created tree,
  the seeded content, the git state, and the refusal paths. This one is run per
  session from the scratch directory, not tracked in the repository.

## Child aSDLC Index

- No further child AGENTS.md files. Individual skill packages are plain
  directories and are not governed by their own AGENTS.md.
