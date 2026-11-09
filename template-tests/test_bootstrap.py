#!/usr/bin/env python3
"""Behavioral suite for the bootstrap script and the scaffold it produces.

Runs the script in a subprocess against this working tree (or a fixture copy of
it) and reads the result off disk — the produced tree, its seeded files, its git
state — not the script's own report. Standard library only:

    python3 -m unittest discover -s template-tests -v
    python3 template-tests/test_bootstrap.py
    ASDLC_TEST_NETWORK=1 python3 template-tests/test_bootstrap.py   # adds the clone case

The interpreter running the suite is the interpreter that runs the script, so
this works where ``python3`` is not a command (a stock Windows install).

Template-only: ``copy_template`` skips this directory (``TEMPLATE_ONLY_DIRS`` in
``scripts/bootstrap.py``), so a scaffolded project never receives it.
"""

from __future__ import annotations

import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parents[1]
SCRIPT = TEMPLATE / "skills" / "asdlc-bootstrap" / "scripts" / "bootstrap.py"

# Prose that describes the template rather than a project. The scaffold must not
# contain any of it; the general form of this check is the index test below.
TEMPLATE_IDENTITY_PHRASES = (
    "Blueprint for projects",
    "aSDLC framework template",
    "project template",
    "for the aSDLC template",
    "root-level template files",
)
# A note addressed to adopting projects that names the template on purpose.
PREFERENCES_NOTE = "/* These preferences govern projects adopting aSDLC"


def _load_script():
    """Load bootstrap.py for its constants, so the suite cannot drift from it."""
    spec = importlib.util.spec_from_file_location("asdlc_bootstrap", SCRIPT)
    assert spec is not None and spec.loader is not None, f"cannot load {SCRIPT}"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # definitions only; main() is guarded
    return module


BOOTSTRAP = _load_script()


def run(*args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args], capture_output=True, text=True, env=env
    )


def copyright_line(path: Path) -> str:
    """The first ``Copyright`` line of a license file — the one seeding rewrites."""
    return next(
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip().startswith("Copyright")
    )


def git(path: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=path, capture_output=True, text=True, check=True
    ).stdout


def ambient_identity() -> str:
    """The identity git resolves here, or the script's documented fallback."""
    def config(key: str) -> str:
        return subprocess.run(
            ["git", "config", "--get", key], capture_output=True, text=True
        ).stdout.strip()

    name, email = config("user.name"), config("user.email")
    if name and email:
        return f"{name} <{email}>"
    return f"{BOOTSTRAP.FALLBACK_IDENTITY[0]} <{BOOTSTRAP.FALLBACK_IDENTITY[1]}>"


class BootstrapCase(unittest.TestCase):
    """A scratch directory per test; every scaffold is built inside it."""

    def setUp(self):
        self.work = Path(tempfile.mkdtemp(prefix="asdlc-suite-"))
        self.addCleanup(shutil.rmtree, self.work, ignore_errors=True)

    def fixture_template(self, mutate=None) -> Path:
        """A copy of the template tree, for cases that need to break something."""
        dest = self.work / "template"
        shutil.copytree(
            TEMPLATE,
            dest,
            ignore=shutil.ignore_patterns(".git", *BOOTSTRAP.TEMPLATE_ONLY_DIRS),
        )
        if mutate:
            mutate(dest)
        return dest

    def scaffold(self, name="Widget Lab", *, source=None, dest=None, env=None, **flags):
        args = [name, "--dest", str(dest or self.work), "--from", str(source or TEMPLATE)]
        for flag, value in flags.items():
            flag = "--" + flag.replace("_", "-")
            if value is True:
                args.append(flag)
            elif value is not None:
                args += [flag, str(value)]
        return run(*args, env=env)


class DryRun(BootstrapCase):
    def test_writes_nothing(self):
        out = self.scaffold("Dry Run", dry_run=True, vision="One line about it.")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertFalse((self.work / "dry-run").exists(), "the dry run wrote a directory")

    def test_reports_the_plan(self):
        out = self.scaffold(
            "Dry Run", dry_run=True, vision="One line about it.", implemented="seeded"
        )
        plan = out.stdout
        self.assertIn("description -> 'One line about it.'", plan)
        self.assertIn("vision -> replaced", plan)
        self.assertIn("Implemented +1", plan)
        self.assertIn(f"LICENSE:  copyright (c) {date.today().year}", plan)
        # The identity the commit will carry, in either documented form.
        self.assertRegex(plan, r"one commit as .+ \((ambient git config|no .+ configured)\)")


class Scaffold(BootstrapCase):
    def test_tree_and_content(self):
        out = self.scaffold(
            vision="A small lab for widgets. It does X.",
            implemented="scaffold exists",
            backlog="add CI",
            not_in_scope="hosting",
        )
        self.assertEqual(out.returncode, 0, out.stderr)
        target = self.work / "widget-lab"
        self.assertTrue(target.is_dir(), "slugified directory missing")

        readme = (target / "README.md").read_text(encoding="utf-8").splitlines()
        self.assertEqual(readme[0], "# Widget Lab", "H1 is not the name as given")
        self.assertEqual(readme[2], "A small lab for widgets.", "description is not the vision's first sentence")

        roadmap = (target / "ROADMAP.md").read_text(encoding="utf-8")
        for expected in (
            "## Implemented\n\n- scaffold exists\n\n## Backlog",
            "## Backlog\n\n- add CI\n\n## Not in scope",
            "## Not in scope\n\n- hosting\n",
        ):
            self.assertIn(expected, roadmap, "seeded list spacing differs from the template")

    def test_git_state(self):
        self.assertEqual(self.scaffold().returncode, 0)
        target = self.work / "widget-lab"
        self.assertEqual(len(git(target, "log", "--oneline").splitlines()), 1, "not exactly one commit")
        self.assertEqual(
            git(target, "log", "-1", "--format=%an <%ae>").strip(),
            ambient_identity(),
            "the scaffold commit does not carry the ambient identity",
        )
        self.assertEqual(git(target, "remote", "-v").strip(), "", "a remote was created")
        self.assertEqual(git(target, "tag").strip(), "", "a tag was created")
        self.assertEqual(git(target, "status", "--porcelain").strip(), "", "the tree is not clean")

    def test_no_git(self):
        self.assertEqual(self.scaffold(no_git=True).returncode, 0)
        target = self.work / "widget-lab"
        self.assertFalse((target / ".git").exists())
        self.assertTrue((target / "README.md").is_file())

    def test_placeholders_survive_when_omitted(self):
        self.assertEqual(self.scaffold().returncode, 0)
        target = self.work / "widget-lab"
        self.assertIn("<one-paragraph statement", (target / "ROADMAP.md").read_text(encoding="utf-8"))
        self.assertIn(
            BOOTSTRAP.README_DESCRIPTION_PLACEHOLDER,
            (target / "README.md").read_text(encoding="utf-8"),
        )

    def test_changed_readme_placeholder_warns_instead_of_lying(self):
        def drop_placeholder(tpl: Path) -> None:
            readme = tpl / "README.md"
            readme.write_text(
                "\n".join(
                    line
                    for line in readme.read_text(encoding="utf-8").splitlines()
                    if line.strip() != BOOTSTRAP.README_DESCRIPTION_PLACEHOLDER
                ),
                encoding="utf-8",
            )

        out = self.scaffold(source=self.fixture_template(drop_placeholder), description="Seeded line.")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("description placeholder", out.stderr, "no warning on stderr")
        readme = (self.work / "widget-lab" / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("Seeded line.", readme, "a description was reported that was not written")
        self.assertEqual(readme.splitlines()[0], "# Widget Lab")


class Refusals(BootstrapCase):
    def test_failure_leaves_nothing_and_the_retry_works(self):
        def rename_section(tpl: Path) -> None:
            roadmap = tpl / "ROADMAP.md"
            roadmap.write_text(
                roadmap.read_text(encoding="utf-8").replace("## Vision", "## Vision statement"),
                encoding="utf-8",
            )

        tpl = self.fixture_template(rename_section)
        out = self.scaffold("Half Built", source=tpl, vision="text")
        self.assertEqual(out.returncode, 1, "a failed scaffold must exit 1")
        self.assertFalse((self.work / "half-built").exists(), "a half-built tree was left behind")
        self.assertEqual(
            list(self.work.glob(".half-built.scaffold-*")), [], "a staging directory was left behind"
        )

        roadmap = tpl / "ROADMAP.md"
        roadmap.write_text(
            roadmap.read_text(encoding="utf-8").replace("## Vision statement", "## Vision"),
            encoding="utf-8",
        )
        self.assertEqual(self.scaffold("Half Built", source=tpl, vision="text").returncode, 0)
        self.assertTrue((self.work / "half-built").is_dir(), "the retry did not work")

    def test_existing_target_exits_2(self):
        self.assertEqual(self.scaffold().returncode, 0)
        second = self.scaffold()
        self.assertEqual(second.returncode, 2, "an existing target must exit 2")

    def test_from_typo_fails_as_a_path(self):
        out = self.scaffold("Typo Path", source=self.work / "does-not-exist")
        self.assertEqual(out.returncode, 1)
        self.assertIn("is not a directory", out.stderr, "the typo was not reported as a path error")
        self.assertFalse((self.work / "typo-path").exists(), "the typo run left something behind")

    def test_stale_staging_directory_is_cleaned(self):
        stale = self.work / ".widget-lab.scaffold-999"
        stale.mkdir()
        self.assertEqual(self.scaffold().returncode, 0)
        self.assertTrue((self.work / "widget-lab").is_dir())
        self.assertFalse(stale.exists(), "a stale staging directory survived")


class TemplateIntegrity(BootstrapCase):
    """What the scaffold must NOT receive, checked against the script's own set."""

    def test_template_only_directories_are_not_copied(self):
        self.assertIn("template-tests", BOOTSTRAP.TEMPLATE_ONLY_DIRS, "this suite's own directory is unprotected")
        self.assertEqual(self.scaffold().returncode, 0)
        target = self.work / "widget-lab"
        for name in BOOTSTRAP.TEMPLATE_ONLY_DIRS:
            self.assertFalse((target / name).exists(), f"{name}/ was copied into the scaffold")

    def test_no_template_identity_prose(self):
        """Every shipped file describes the scaffold, never this repository.

        The LICENSE copyright line is the one exception: seeding rewrites it, so
        it names the template's author only when the adopter happens to be that
        same person. The license case below pins what it must say instead.
        """
        self.assertEqual(self.scaffold().returncode, 0)
        target = self.work / "widget-lab"
        template_line = copyright_line(TEMPLATE / "LICENSE")
        found = []
        for path in sorted(target.rglob("*")):
            if not path.is_file() or ".git" in path.relative_to(target).parts:
                continue
            for number, line in enumerate(
                path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1
            ):
                stripped = line.strip()
                if stripped.startswith(PREFERENCES_NOTE):
                    continue
                if path.name.lower().startswith("license") and stripped == template_line:
                    continue
                if any(phrase in line for phrase in TEMPLATE_IDENTITY_PHRASES):
                    found.append(f"{path.relative_to(target)}:{number}: {stripped[:70]}")
        self.assertEqual(found, [], "template identity prose shipped into the scaffold")

    def test_license_ships_with_the_adopters_copyright(self):
        """A scaffold needs a license, and it must name its own holder."""
        holder = "Ada Lovelace"
        out = self.scaffold(copyright_holder=holder)
        self.assertEqual(out.returncode, 0, out.stderr)
        license_file = self.work / "widget-lab" / "LICENSE"
        self.assertTrue(license_file.is_file(), "the scaffold has no LICENSE")
        self.assertEqual(
            copyright_line(license_file),
            f"Copyright (c) {date.today().year} {holder}",
            "the license does not name the adopter as copyright holder",
        )

    def test_license_holder_falls_back_to_a_visible_placeholder(self):
        """With no holder anywhere, the license must say so — never a stand-in name."""
        env = {
            **os.environ,
            "GIT_CONFIG_GLOBAL": str(self.work / "no-such-gitconfig"),
            "GIT_CONFIG_NOSYSTEM": "1",
        }
        out = self.scaffold(no_git=True, env=env)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("copyright holder", out.stderr, "no warning on stderr")
        text = (self.work / "widget-lab" / "LICENSE").read_text(encoding="utf-8")
        self.assertNotIn(BOOTSTRAP.FALLBACK_IDENTITY[0], text, "the tool's own name was used as a holder")
        self.assertEqual(
            copyright_line(self.work / "widget-lab" / "LICENSE"),
            f"Copyright (c) {date.today().year} {BOOTSTRAP.LICENSE_HOLDER_PLACEHOLDER}",
        )

    def test_license_without_a_copyright_line_fails_instead_of_shipping(self):
        def drop_copyright(tpl: Path) -> None:
            license_file = tpl / "LICENSE"
            license_file.write_text(
                "\n".join(
                    line
                    for line in license_file.read_text(encoding="utf-8").splitlines()
                    if not line.startswith("Copyright")
                ) + "\n",
                encoding="utf-8",
            )

        out = self.scaffold(source=self.fixture_template(drop_copyright))
        self.assertEqual(out.returncode, 1, "an unseeded license must not ship")
        self.assertIn("no copyright line found", out.stderr)
        self.assertFalse((self.work / "widget-lab").exists(), "a half-built tree was left behind")

    def test_index_names_only_paths_the_scaffold_has(self):
        """A shipped file that indexes a path the scaffold lacks dangles for every reader,
        and a shipped child doc the index does not name is invisible to one."""
        self.assertEqual(self.scaffold().returncode, 0)
        target = self.work / "widget-lab"
        index = (target / "AGENTS.md").read_text(encoding="utf-8").split("## Child aSDLC Index")[-1]
        named = {
            token
            for token in re.findall(r"`([^`]+)`", index)
            if "/" in token or token.endswith(".md") or token.startswith(".")
        }
        missing = sorted(token for token in named if not (target / token.strip("/")).exists())
        self.assertEqual(missing, [], "the Child aSDLC Index names paths the scaffold does not have")

        unindexed = sorted(
            f"/{doc.parent.relative_to(target)}/"
            for doc in target.rglob("AGENTS.md")
            if doc != target / "AGENTS.md"
            and f"/{doc.parent.relative_to(target)}/" not in named
        )
        self.assertEqual(unindexed, [], "a child doc ships without an entry in the Child aSDLC Index")


@unittest.skipUnless(
    __import__("os").environ.get("ASDLC_TEST_NETWORK") == "1",
    "network case: set ASDLC_TEST_NETWORK=1 to clone the published template",
)
class Network(BootstrapCase):
    def test_default_clone_path(self):
        out = run("Remote Path", "--dest", str(self.work), "--no-git")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertTrue((self.work / "remote-path" / "README.md").is_file())


if __name__ == "__main__":
    unittest.main(verbosity=2)
