#!/usr/bin/env python3
"""Scaffold a new aSDLC project from the aSDLC template.

Creates ``<dest>/<project-name>/`` from the template (remote clone, or a local
template path when offline), seeding the roadmap vision/direction and the
README title, then initialises a fresh git repository. The new repository has
no template ``.git``, tags, or ``origin`` remote, and none of the template's own
packaging directories (``skills/``, ``commands/``).

Usage:
    python3 bootstrap.py <project-name> [--dest DIR] [--from SOURCE]
                         [--vision TEXT]
                         [--implemented TEXT] [--backlog TEXT]
                         [--not-in-scope TEXT]
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import NoReturn

DEFAULT_TEMPLATE_URL = "https://github.com/swoldanski/asdlc.git"

# Template-only packaging: shipped to publish the skill, never part of a
# scaffolded project.
PACKAGING_DIRS = {"skills", "commands"}
EXCLUDE_NAMES = {".git"}


def fail(message: str, code: int = 1) -> NoReturn:
    print(f"bootstrap: error: {message}", file=sys.stderr)
    raise SystemExit(code)


def run(cmd: list[str], cwd: Path | None = None) -> None:
    subprocess.run(cmd, cwd=cwd, check=True)


def resolve_template(source: str | None, temp_roots: list[Path]) -> Path:
    """Return a directory holding the template.

    A local path is used in place; anything else is treated as a git URL and
    cloned into a temporary directory tracked for cleanup by the caller.
    """
    if source:
        local = Path(source).expanduser()
        if local.is_dir():
            return local.resolve()
    url = source or DEFAULT_TEMPLATE_URL
    tmp = Path(tempfile.mkdtemp(prefix="asdlc-template-"))
    temp_roots.append(tmp)
    dest = tmp / "template"
    try:
        run(["git", "clone", "--depth", "1", "--quiet", url, str(dest)])
    except subprocess.CalledProcessError:
        fail(
            f"could not clone template from '{url}'. If you are offline, pass "
            f"--from <local-path-to-asdlc-template>."
        )
    return dest


def copy_template(template: Path, target: Path) -> None:
    target.mkdir(parents=True)
    ignored = shutil.ignore_patterns(*EXCLUDE_NAMES)
    for entry in sorted(template.iterdir()):
        if entry.name in EXCLUDE_NAMES or entry.name in PACKAGING_DIRS:
            continue
        dest = target / entry.name
        if entry.is_dir():
            shutil.copytree(entry, dest, ignore=ignored)
        else:
            shutil.copy2(entry, dest)


def set_readme_title(readme: Path, project_name: str) -> None:
    lines = readme.read_text(encoding="utf-8").splitlines(keepends=True)
    for i, line in enumerate(lines):
        if line.startswith("# "):
            lines[i] = f"# {project_name}\n"
            break
    else:
        fail(f"no top-level heading found in {readme}")
    readme.write_text("".join(lines), encoding="utf-8")


def insert_bullets(text: str, heading: str, bullets: list[str]) -> str:
    if not bullets:
        return text
    lines = text.splitlines()
    try:
        at = lines.index(heading) + 1
    except ValueError:
        fail(f"roadmap section '{heading}' not found in template")
    lines[at:at] = [f"- {b}" for b in bullets]
    return "\n".join(lines) + "\n"


def replace_section(text: str, heading: str, body: str) -> str:
    """Replace a section's body, keeping the heading line.

    Decoupled from the template's placeholder wording: the section is found by
    its heading and everything up to the next ``## `` heading is replaced.
    """
    lines = text.splitlines()
    try:
        start = lines.index(heading)
    except ValueError:
        fail(f"roadmap section '{heading}' not found in template")
    end = start + 1
    while end < len(lines) and not lines[end].startswith("## "):
        end += 1
    lines[start + 1:end] = ["", body.strip(), ""]
    return "\n".join(lines) + "\n"


def seed_roadmap(
    roadmap: Path,
    vision: str | None,
    implemented: list[str],
    backlog: list[str],
    not_in_scope: list[str],
) -> None:
    text = roadmap.read_text(encoding="utf-8")
    if vision:
        text = replace_section(text, "## Vision", vision)
    text = insert_bullets(text, "## Implemented", implemented)
    text = insert_bullets(text, "## Backlog", backlog)
    text = insert_bullets(text, "## Not in scope", not_in_scope)
    roadmap.write_text(text, encoding="utf-8")


def init_git(target: Path) -> None:
    run(["git", "init", "-q", "-b", "main"], cwd=target)
    run(["git", "-C", str(target), "add", "-A"])
    run(
        [
            "git", "-C", str(target),
            "-c", "user.name=aSDLC bootstrap",
            "-c", "user.email=asdlc@localhost",
            "commit", "-q", "-m", "chore: scaffold from the aSDLC template",
        ]
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("project_name", help="name of the new project directory")
    parser.add_argument("--dest", default=".", help="parent directory (default: .)")
    parser.add_argument(
        "--from",
        dest="source",
        default=None,
        help=f"git URL or local template path (default: {DEFAULT_TEMPLATE_URL})",
    )
    parser.add_argument("--vision", default=None, help="roadmap vision paragraph")
    parser.add_argument("--implemented", action="append", default=[],
                        help="roadmap Implemented bullet (repeatable)")
    parser.add_argument("--backlog", action="append", default=[],
                        help="roadmap Backlog bullet (repeatable)")
    parser.add_argument("--not-in-scope", dest="not_in_scope", action="append",
                        default=[], help="roadmap Not in scope bullet (repeatable)")
    parser.add_argument("--no-git", action="store_true",
                        help="skip git init (template files only)")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    name = args.project_name
    if not name or name in {".", ".."} or "/" in name or "\\" in name:
        fail(f"invalid project name: {name!r}")

    dest_root = Path(args.dest).expanduser().resolve()
    dest_root.mkdir(parents=True, exist_ok=True)
    target = dest_root / name
    if target.exists():
        fail(f"refusing to overwrite existing path: {target}", code=2)

    temp_roots: list[Path] = []
    try:
        template = resolve_template(args.source, temp_roots)
        copy_template(template, target)
        set_readme_title(target / "README.md", name)
        seed_roadmap(
            target / "ROADMAP.md",
            args.vision,
            args.implemented,
            args.backlog,
            args.not_in_scope,
        )
        if not args.no_git:
            init_git(target)
    finally:
        for root in temp_roots:
            shutil.rmtree(root, ignore_errors=True)

    print(f"Created {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
