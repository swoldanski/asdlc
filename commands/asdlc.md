---
description: Bootstrap a new aSDLC project from the aSDLC template.
---

# /asdlc — bootstrap a project

Create a new aSDLC project named by `$ARGUMENTS`, using the **asdlc-bootstrap**
skill and its workflow. This command restates none of that workflow: if
`$ARGUMENTS` is empty, the skill's first step asks the user for the name and
direction.

If the skill is not installed, run:

```bash
npx skills@latest add swoldanski/asdlc -a <agent>
```
