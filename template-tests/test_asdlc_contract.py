#!/usr/bin/env python3
"""Contract checks on the rail itself: root AGENTS.md and its child docs.

The rail is a document, so these cases read the real docs on disk instead of a
scaffold: the pass keeps its phases and their order, and no shipped doc that
enumerates the pass drops one — child docs included, and README.md included,
because both are copied into every scaffold. Standard library only, offline:

    python3 -m unittest discover -s template-tests -v
    python3 template-tests/test_asdlc_contract.py

Template-only, like the rest of the suite: ``copy_template`` skips this
directory, so a scaffolded project never receives it.
"""

from __future__ import annotations

import importlib.util
import re
import unittest
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parents[1]
RAIL = TEMPLATE / "AGENTS.md"
SCRIPT = TEMPLATE / "skills" / "asdlc-bootstrap" / "scripts" / "bootstrap.py"


def _load_script():
    """Load bootstrap.py for its constants, so this suite cannot drift from it."""
    spec = importlib.util.spec_from_file_location("asdlc_bootstrap", SCRIPT)
    assert spec is not None and spec.loader is not None, f"cannot load {SCRIPT}"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # definitions only; main() is guarded
    return module


BOOTSTRAP = _load_script()

# The phases a change passes through, in order. Propagate follows Closeout and is
# not a step of the pass, so it is checked as part of the lifecycle, not here.
PASS_PHASES = (
    "Read Before Editing",
    "Decide Before Editing",
    "Update After Editing",
    "Closeout",
)
LIFECYCLE_PHASES = PASS_PHASES + ("Propagate",)
CONTRACT_DECLARATION = "Follows the root aSDLC contract"
PASS_ENUMERATION = "aSDLC pass ("
ARROW = "→"


def heading_at(text: str, heading: str) -> int:
    """Index of a heading line, or -1. Prose mentions do not count."""
    match = re.search(rf"^{re.escape(heading)}$", text, re.MULTILINE)
    return -1 if match is None else match.start()


def section(text: str, heading: str) -> str:
    """The body of a heading, up to the next heading of the same or higher level."""
    start = heading_at(text, heading)
    if start < 0:
        return ""
    body = text[start + len(heading):]
    end = re.search(r"^#{1,2} ", body, re.MULTILINE)
    return body[: end.start()] if end else body


def flattened(path: Path) -> str:
    """Doc text with wrapped lines joined, so a phrase split across lines still matches."""
    return " ".join(path.read_text(encoding="utf-8").split())


def child_docs() -> list[Path]:
    return sorted(path for path in TEMPLATE.rglob("AGENTS.md") if path != RAIL)


def shipped_docs() -> list[Path]:
    """Markdown a scaffold receives: everything but .git and the template-only dirs."""
    skipped = BOOTSTRAP.TEMPLATE_ONLY_DIRS | BOOTSTRAP.EXCLUDE_NAMES
    return sorted(
        path
        for path in TEMPLATE.rglob("*.md")
        if not skipped & set(path.relative_to(TEMPLATE).parts)
    )


def enumeration(path: Path) -> str | None:
    """The pass list a doc spells out, or None when it spells none out.

    Two forms ship: the parenthetical the child docs use, and the arrow sentence
    README.md uses. A sentence only counts when it names a phase, so an arrow
    used for anything else is not mistaken for a pass list.
    """
    text = flattened(path)
    if PASS_ENUMERATION in text:
        return text.split(PASS_ENUMERATION, 1)[1].split(")", 1)[0]
    if ARROW not in text:
        return None
    for sentence in re.split(r"(?<=\.)\s+", text):
        if ARROW in sentence and any(phase in sentence for phase in PASS_PHASES):
            return sentence
    return None


class Phases(unittest.TestCase):
    def test_the_lifecycle_phases_exist_in_order(self):
        text = RAIL.read_text(encoding="utf-8")
        positions = {name: heading_at(text, f"## {name}") for name in LIFECYCLE_PHASES}
        missing = [name for name, at in positions.items() if at < 0]
        self.assertEqual(missing, [], f"the rail lost a phase heading: {missing}")
        self.assertEqual(
            list(positions.values()),
            sorted(positions.values()),
            "the lifecycle phases are out of order: "
            + " → ".join(name for name, _ in sorted(positions.items(), key=lambda kv: kv[1])),
        )

    def test_the_subsections_stay_under_their_phase(self):
        text = RAIL.read_text(encoding="utf-8")
        self.assertIn(
            "### Fast path",
            section(text, "## Closeout"),
            "### Fast path left ## Closeout",
        )
        self.assertIn(
            "### Decisions",
            section(text, "## Update After Editing"),
            "### Decisions left ## Update After Editing",
        )


class ShippedDocs(unittest.TestCase):
    def test_a_doc_that_enumerates_the_pass_names_every_phase_in_order(self):
        checked = 0
        for path in shipped_docs():
            enumerated = enumeration(path)
            if enumerated is None:
                continue
            checked += 1
            positions = {phase: enumerated.find(phase) for phase in PASS_PHASES}
            missing = [phase for phase, at in positions.items() if at < 0]
            self.assertEqual(
                missing,
                [],
                f"{path.relative_to(TEMPLATE)} enumerates the pass but drops {missing}",
            )
            self.assertEqual(
                list(positions.values()),
                sorted(positions.values()),
                f"{path.relative_to(TEMPLATE)} lists the pass phases out of order",
            )
            edit = enumerated[
                positions["Decide Before Editing"]
                + len("Decide Before Editing") : positions["Update After Editing"]
            ]
            self.assertIn(
                "edit",
                edit,
                f"{path.relative_to(TEMPLATE)} skips the edit between deciding and updating",
            )
        self.assertGreater(checked, 0, "no shipped doc enumerates the pass — this checks nothing")


class ChildDocs(unittest.TestCase):
    def test_every_child_doc_declares_the_rail_contract(self):
        """A proxy, not a proof.

        "No child may weaken aSDLC" cannot be machine-checked: intent has no
        syntax. This only proves every child carries the declaration that it
        follows the root contract, so a doc that never claims adherence is
        caught. A doc that claims it and then relaxes a rule still passes.
        """
        undeclared = [
            str(path.relative_to(TEMPLATE))
            for path in child_docs()
            if CONTRACT_DECLARATION not in flattened(path)
        ]
        self.assertEqual(undeclared, [], f"child docs without the declaration: {undeclared}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
