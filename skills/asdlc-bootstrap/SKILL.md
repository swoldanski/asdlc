---
name: asdlc-bootstrap
description: >-
  Scaffold a new project from the aSDLC template and seed it with the project's
  vision and direction. Use when the user asks to "scaffold a new aSDLC project",
  "bootstrap a project from the aSDLC template", "start a project with aSDLC", or
  runs "/asdlc <project-name>".
license: MIT
allowed-tools: Bash Read Write
compatibility: >-
  Needs git and Python 3 (standard library only, no third-party packages). Invoke
  the script as python3 on POSIX; on Windows use py -3 or python, since python3
  is not installed by the stock installer.
metadata:
  author: Sebastian Woldanski (swoldanski)
  executable: scripts/bootstrap.py — Python 3, standard library only; run --help for every flag
  network: clones https://github.com/swoldanski/asdlc.git unless --from names a local template directory
  writes: creates the new project tree, rewrites its README.md and ROADMAP.md, runs git init/add/commit inside it
---

# aSDLC bootstrap

Create a new repository seeded from the aSDLC template, then write the project's
vision and direction into the files that govern them. The template's rules come
from the `asdlc` repository; the new project starts as a clean, standalone repo.

## When to Use

- The user asks to "scaffold a new aSDLC project", "bootstrap a project from the
  aSDLC template" or "start a project with aSDLC", or runs `/asdlc <name>`.
- **Don't use for:** adding files to an existing project, or editing the template
  itself — that repository has its own aSDLC pass.

## What this skill runs

This skill ships and runs executable code. Declared here so a scan reads the
capabilities as intended rather than as surprises:

- `scripts/bootstrap.py` — Python 3, standard library only.
- It shells out to **git**: `clone` of the template URL (unless `--from` names a
  local directory), then `init -b main`, `add -A` and `commit` inside the new
  project. No other command is invoked.
- It copies the template tree, excluding `.git`, `skills/` and `commands/`, and
  rewrites exactly two files in the new project: `README.md` (H1 title, and the
  description placeholder when one is supplied) and `ROADMAP.md` (§ *Vision* and
  the three lists). Nothing outside `<dest>/<slug>/` plus a temporary clone and
  its own staging directory is written.

## Prerequisites

- `git` on `PATH`, and network access to the template URL for the default clone.
- Python 3 — invoke as `python3` (POSIX), `py -3` or `python` (Windows).

## Workflow

1. **Collect the project name and direction.** The project name is required — if
   the user has not supplied one, ask for it. Collect the *vision* (a one-paragraph
   statement of what the project should become and the problem it solves), a
   one-line *description* if the user offers one, and any initial *direction*: what
   is already done, what is planned, and what is explicitly out of scope. Ask for
   missing vision or direction before scaffolding; do not invent them.
   *Done when:* you hold a name, and every list you will pass has either a bullet
   or an explicit "none yet".

2. **Show the plan before writing anything (`--dry-run`).** It prints the slug, the
   target path, the template source, the excluded directories, what will be seeded
   and the identity the scaffold commit will carry — and writes nothing.

   ```bash
   python3 scripts/bootstrap.py "<project-name>" --dest <parent-dir> --dry-run
   ```

3. **Scaffold.**

   ```bash
   python3 scripts/bootstrap.py "<project-name>" --dest <parent-dir> \
     --description "<one-line description>" \
     --vision "<vision paragraph>" \
     --implemented "<done item>" --backlog "<planned item>" \
     --not-in-scope "<excluded item>"
   ```

   `--description`, `--implemented`, `--backlog` and `--not-in-scope` are optional;
   the three list flags repeat once per bullet, and `--description` defaults to the
   vision's first sentence. The directory is the *slugified* project name — lowercase,
   non-alphanumeric runs collapsed to a hyphen (`Abc or Efg` → `abc-or-efg`) — while
   the README title keeps the name as given. The script clones the template from
   GitHub, or uses a local template with `--from <path>` when offline. It never copies
   a template `skills/` or `commands/`, refuses an existing `<slug>/`, and finishes
   with a fresh `git init` and initial commit — no template `.git`, tags or `origin`.
   `--no-git` skips the repository part.
   *Done when:* the script prints `Created <path>`.

4. **Finish seeding.** The script writes `--vision` verbatim as § *Vision* and each
   bullet verbatim as a list item. When `--vision` or `--description` is omitted, the
   template's placeholder stays in place as the next writer's prompt — say that,
   rather than describing the section as empty. If the user gave prose longer than one
   paragraph, tighten § *Vision* by hand; confirm the README title reads as the project
   name.
   *Done when:* § *Vision*, § *Implemented*, § *Backlog* and § *Not in scope* each read
   as the user's direction, or carry the placeholder you told them about.

5. **Report.** State where the project was created, that it is an initialised git
   repository with one commit and no remote, what direction was recorded and which
   placeholders remain. Point at `AGENTS.md` (the binding contract) and `ROADMAP.md`
   (direction) as the next things to read. Creating the remote repository and pushing
   are not part of this skill.

## Pitfalls

- **A failed scaffold leaves nothing behind, and an existing target exits 2.** The
  tree is built in a hidden staging directory and renamed into place only after the
  last step, so a failure cannot leave a half-built project that blocks its own retry.
- **`--from` with a typo fails as a path**, not as a clone error — pass an existing
  directory, or a git URL.
- **Omitting `--vision`/`--description` keeps the template placeholder.** That is the
  intended state, not a defect to fix by hand-editing the new copy.
- **A template whose README placeholder line changed loses the description silently
  otherwise** — the script warns on stderr instead of failing, so read the warning
  rather than reporting a description that was never written.
- **The scaffold commit carries your ambient git identity**; with none configured it
  falls back to `aSDLC bootstrap <asdlc@localhost>`, which is unlinked on a host.
- **`python3` is not a command on a stock Windows Python install** — use `py -3` or
  `python`.

## Verification

Run it somewhere disposable, then read the result rather than the script's report:

```bash
python3 scripts/bootstrap.py "Verify Me" --dest . --vision "One line." --implemented "seeded"
cd verify-me && git log --oneline && git remote -v && git status --short
```

Done means: the directory is the slug of the name given; `README.md`'s H1 is the name
as given and its description is the seeded line or the placeholder; the four ROADMAP
sections carry the seeded content with the template's blank-line spacing; `git log`
shows exactly one commit, `git remote -v` is empty and `git status` is clean; and no
`skills/` or `commands/` directory was copied.

## Reference

- `scripts/bootstrap.py` — the scaffolding script; `--help` lists every flag, and its
  docstring carries the exit codes (0 created, 1 failed with nothing left behind,
  2 target exists).
- The scaffolded project follows the aSDLC pass: Read Before Editing → edit →
  Update After Editing → Closeout, per its root `AGENTS.md`.
