---
description: Bootstrap a new aSDLC project from the aSDLC template.
---

# /asdlc — bootstrap a project

Given `$ARGUMENTS` as the project name, create a new aSDLC project.

Use the **asdlc-bootstrap** skill and follow its workflow:

1. Treat `$ARGUMENTS` as the project name. If it is empty, ask the user for the
   project name and the project's vision and initial direction.
2. Scaffold the project with the skill's `scripts/bootstrap.py`.
3. Seed `ROADMAP.md` § *Vision* and the three lists with the user's direction, and
   set the `README.md` title to the project name.
4. Report where the project was created and what was recorded.

If the skill is not installed, run:

```bash
npx skills@latest add swoldanski/asdlc -a <agent>
```
