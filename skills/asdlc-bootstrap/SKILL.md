---
name: asdlc-bootstrap
description: >-
  Scaffold a new project from the aSDLC template and seed it with the project's
  vision and direction. Use when the user asks to "scaffold a new aSDLC project",
  "bootstrap a project from the aSDLC template", "start a project with aSDLC", or
  runs "/asdlc <project-name>".
---

# aSDLC bootstrap

Create a new repository seeded from the aSDLC template, then write the project's
vision and direction into the files that govern them. The template's rules come
from the `asdlc` repository; the new project starts as a clean, standalone repo.

## Workflow

1. **Collect the project name and direction.** The project name is required — if
   the user has not supplied one, ask for it. Collect the *vision* (a one-paragraph
   statement of what the project should become and the problem it solves) and any
   initial *direction*: what is already done, what is planned, and what is
   explicitly out of scope. Ask for missing vision/direction before scaffolding;
   do not invent them. If the user gives no direction yet, scaffold with an empty
   roadmap vision and say so.

2. **Scaffold.** Run the bundled script from the skill directory:

   ```bash
   python3 scripts/bootstrap.py <project-name> --dest <parent-dir> \
     --vision "<vision paragraph>" \
     --implemented "<done item>" --backlog "<planned item>" \
     --not-in-scope "<excluded item>"
   ```

   `--implemented`, `--backlog`, and `--not-in-scope` repeat once per bullet; omit
   any that do not apply. The directory is the *slugified* project name — lowercase,
   non-alphanumeric runs collapsed to a hyphen (`Abc or Efg` → `abc-or-efg`) — while
   the README title keeps the name as given. The script clones the template from
   GitHub, or uses a local template with `--from <path>` when offline. It copies the
   template files (never a template `skills/` or `commands/`), refuses to overwrite an
   existing `<slug>/`, and finishes with a fresh `git init` and initial commit — the
   new repo has no template `.git`, tags, or `origin`.

3. **Finish seeding.** If the script did not write the whole vision (for example
   the user supplied prose rather than a single paragraph), open `ROADMAP.md` and
   complete § *Vision* and the three lists, keeping each list item to one concise
   line. Confirm `README.md`'s title reads as the project name.

4. **Report.** Tell the user where the project was created, that it is an initialised
   git repository with one commit and no remote, and what direction was recorded.
   Point them at `AGENTS.md` (the binding contract) and `ROADMAP.md` (direction) as
   the next things to read.

## Reference

- `scripts/bootstrap.py` — the scaffolding script; run `--help` for all flags.
- The scaffolded project follows the aSDLC pass: Read Before Editing → edit →
  Update After Editing → Closeout, per its root `AGENTS.md`.
