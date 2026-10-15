# /template-tests — the template's own suite

## Purpose

Owns the behavioral suite that verifies the template itself: the bootstrap
script and the scaffold it produces. The directory is **template-only** —
`scripts/bootstrap.py` skips it by name (`TEMPLATE_ONLY_DIRS`) — so no
scaffolded project receives it.

## Ownership

Owned by this child aSDLC doc. Follows the root aSDLC contract. Any change
touching the suite goes through the aSDLC pass (Read Before Editing → edit →
Update After Editing → Closeout).

## Local Contracts

- The suite verifies the template, not a project, which is why it is not in
  `/tests/`: that directory ships into every scaffold and its child `AGENTS.md`
  governs the *project's* tests.
- The root `AGENTS.md` cannot name this directory — or any template-only one —
  because it is copied verbatim into every scaffold, where the path does not
  exist. Discovery runs through this file, as it does for `/skills/`.
- A new template-only directory needs one edit: add it to `TEMPLATE_ONLY_DIRS` in
  `scripts/bootstrap.py`. The suite reads that set instead of repeating it, so
  the exclusion cannot drift from the check.
- Tests are behavioral: they run the script in a subprocess and read the produced
  tree, its seeded files and its git state off disk — never the script's own
  report. Every test scaffolds inside a temporary directory; nothing is written
  inside the repository.

## Work Guidance

- Keep the suite standard-library only, like the script it verifies: no
  third-party package, nothing to install. `unittest` is the runner.
- Read constants from the script (`README_DESCRIPTION_PLACEHOLDER`,
  `TEMPLATE_ONLY_DIRS`, `FALLBACK_IDENTITY`) rather than restating their values,
  and resolve the ambient git identity instead of hardcoding one.
- A defect in the script or in the shipped rail earns a case here before it earns
  a fix commit, and the case must be seen to fail while the fix is reverted — a
  case that has only ever been green proves nothing.
- Prefer an assertion about the artifact ("this path exists in the scaffold") to
  one about the script's printed output; the output is a claim, the tree is the
  result.

## Verification

`python3 -m unittest discover -s template-tests -v`, or
`python3 template-tests/test_bootstrap.py` — offline and deterministic. The case
that clones the published template over the network is skipped unless
`ASDLC_TEST_NETWORK=1`.

## Child aSDLC Index

- No further child AGENTS.md files. The suite is one Python file beside this doc.
