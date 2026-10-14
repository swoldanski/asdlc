#!/usr/bin/env python3
"""Scaffold a new aSDLC project from the aSDLC template.

Creates ``<dest>/<slug>/`` from the template (remote clone, or a local template
path when offline), seeding the README title/description and the roadmap
vision/direction, then initialises a fresh git repository. The directory name is
the slugified project name (e.g. ``Abc or Efg`` -> ``abc-or-efg``); the README
title keeps the project name as given. The new repository has no template
``.git``, tags or ``origin`` remote, and none of the template's own packaging
directories (``skills/``, ``commands/``).

Executable code: this script runs ``git clone`` (unless ``--from`` names a local
directory), copies the template tree, rewrites ``README.md`` and ``ROADMAP.md``
inside the new project, and runs ``git init``/``add``/``commit`` in it. Nothing
outside ``<dest>/<slug>/`` (plus a temporary clone and its own staging
directory) is written.

Usage:
    python3 bootstrap.py <project-name> [--dest DIR] [--from SOURCE]
                         [--description TEXT] [--vision TEXT]
                         [--implemented TEXT] [--backlog TEXT]
                         [--not-in-scope TEXT]
                         [--no-git] [--dry-run]

Exit codes:
    0  the scaffold was created, or --dry-run reported the plan
    1  the scaffold failed; the target directory was not left behind
    2  the target directory already exists
"""

from __future__ import annotations

import argparse
import os
import re
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

# The line a scaffolded project describes itself in. The template ships this
# placeholder so no template identity is copied into a new repository.
README_DESCRIPTION_PLACEHOLDER = "_One-line description of this project._"

# Author/committer used only when git cannot resolve the user's own identity.
FALLBACK_IDENTITY = ("aSDLC bootstrap", "asdlc@localhost")

_URL_RE = re.compile(r"^[a-z][a-z0-9+.-]*://", re.IGNORECASE)
_SCP_URL_RE = re.compile(r"^[^/\\@]+@[^/\\:]+:")


def fail(message: str, code: int = 1) -> NoReturn:
    print(f"bootstrap: error: {message}", file=sys.stderr)
    raise SystemExit(code)


def slugify(name: str) -> str:
    """Turn a project name into a directory-safe slug.

    ``Abc or Efg`` -> ``abc-or-efg``; any run of characters outside
    ``[a-z0-9]`` collapses to a single hyphen.
    """
    slug = re.sub(r"[^a-z0-9]+", "-", name.strip().lower()).strip("-")
    if not slug:
        fail(f"project name {name!r} has no usable characters for a directory name")
    return slug


def first_sentence(text: str) -> str:
    """The opening sentence of ``text``, for use as a one-line description."""
    stripped = " ".join(text.split())
    return re.split(r"(?<=[.!?])\s+", stripped)[0] if stripped else ""


def run(
    cmd: list[str],
    cwd: Path | None = None,
    capture: bool = False,
    check: bool = True,
) -> subprocess.CompletedProcess:
    """The only place this script shells out — git, and nothing else."""
    return subprocess.run(cmd, cwd=cwd, check=check, capture_output=capture, text=capture)


def looks_like_url(source: str) -> bool:
    """A URL or a ``git@host:path`` shorthand; anything else is read as a path."""
    return bool(_URL_RE.match(source) or _SCP_URL_RE.match(source))


def resolve_template(source: str | None, temp_roots: list[Path]) -> Path:
    """Return a directory holding the template.

    A local directory is used in place; a URL is cloned into a temporary
    directory tracked for cleanup by the caller. Anything else is a path the
    user meant literally, so it fails as a path instead of falling through to a
    clone that answers a typo with a network error.
    """
    if source:
        local = Path(source).expanduser()
        if local.is_dir():
            return local.resolve()
        if not looks_like_url(source):
            fail(
                f"--from '{source}' is not a directory: {local}\n"
                f"hint: pass an existing template directory, or a git URL "
                f"(default: {DEFAULT_TEMPLATE_URL})"
            )
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


def seed_readme(readme: Path, project_name: str, description: str | None) -> None:
    """Set the H1 to the project name and fill the description placeholder."""
    lines = readme.read_text(encoding="utf-8").splitlines(keepends=True)
    titled = False
    described = False
    for i, line in enumerate(lines):
        if not titled and line.startswith("# "):
            lines[i] = f"# {project_name}\n"
            titled = True
        elif description and line.strip() == README_DESCRIPTION_PLACEHOLDER:
            lines[i] = f"{description}\n"
            described = True
    if not titled:
        fail(f"no top-level heading found in {readme}")
    if description and not described:
        # Loud, not fatal: the template is still scaffoldable, but the caller
        # must not report a description that was never written.
        print(
            f"bootstrap: warning: README description placeholder "
            f"{README_DESCRIPTION_PLACEHOLDER!r} not found in {readme}; "
            f"--description was not written",
            file=sys.stderr,
        )
    readme.write_text("".join(lines), encoding="utf-8")


def insert_bullets(text: str, heading: str, bullets: list[str]) -> str:
    """Append bullets to a section, keeping the file's blank-line convention."""
    if not bullets:
        return text
    lines = text.splitlines()
    try:
        start = lines.index(heading)
    except ValueError:
        fail(f"roadmap section '{heading}' not found in template")
    end = start + 1
    while end < len(lines) and not lines[end].startswith("## "):
        end += 1
    body = lines[start + 1:end]
    while body and not body[-1].strip():
        body.pop()
    body += [f"- {b}" for b in bullets]
    lines[start + 1:end] = [""] + body + [""]
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


def git_config(target: Path, key: str) -> str:
    """Ambient git config value, or ``""`` when git cannot resolve one."""
    cwd = target if target.is_dir() else None
    proc = run(["git", "config", "--get", key], cwd=cwd, capture=True, check=False)
    return proc.stdout.strip() if proc.returncode == 0 else ""


def git_identity(target: Path) -> list[str]:
    """``-c`` author/committer overrides only where git resolves no identity.

    The scaffold commit is the one nobody amends, so it must not be attributed
    to a placeholder when the user has an identity configured.
    """
    name, email = FALLBACK_IDENTITY
    opts: list[str] = []
    if not git_config(target, "user.name"):
        opts += ["-c", f"user.name={name}"]
    if not git_config(target, "user.email"):
        opts += ["-c", f"user.email={email}"]
    return opts


def init_git(target: Path) -> None:
    run(["git", "init", "-q", "-b", "main"], cwd=target)
    run(["git", "-C", str(target), "add", "-A"])
    run(
        [
            "git", "-C", str(target),
            *git_identity(target),
            "commit", "-q", "-m", "chore: scaffold from the aSDLC template",
        ]
    )


def describe_template(source: str | None) -> str:
    if source and Path(source).expanduser().is_dir():
        return f"{Path(source).expanduser().resolve()} (used in place)"
    return f"{source or DEFAULT_TEMPLATE_URL} (cloned)"


def describe_identity(dest_root: Path) -> str:
    name = git_config(dest_root, "user.name")
    email = git_config(dest_root, "user.email")
    if name and email:
        return f"{name} <{email}> (ambient git config)"
    missing = ", ".join(k for k, v in (("user.name", name), ("user.email", email)) if not v)
    return f"{FALLBACK_IDENTITY[0]} <{FALLBACK_IDENTITY[1]}> (no {missing} configured)"


def print_plan(target: Path, slug: str, args: argparse.Namespace, description: str | None) -> None:
    name = args.project_name.strip()
    readme = (
        f"description -> {description!r}"
        if description
        else f"description placeholder {README_DESCRIPTION_PLACEHOLDER!r} left in place"
    )
    if args.no_git:
        git = "skipped (--no-git)"
    else:
        git = f"init -b main + one commit as {describe_identity(target.parent)}"
    print("dry run — nothing written")
    print(f"  project:  {name}")
    print(f"  slug:     {slug}")
    print(f"  target:   {target}")
    print(f"  template: {describe_template(args.source)}")
    print(f"  excludes: {', '.join(sorted(EXCLUDE_NAMES | PACKAGING_DIRS))}")
    print(f"  README:   title -> {name!r}, {readme}")
    print(
        f"  ROADMAP:  vision -> {'replaced' if args.vision else 'placeholder left in place'}"
        f"; Implemented +{len(args.implemented)}, Backlog +{len(args.backlog)},"
        f" Not in scope +{len(args.not_in_scope)}"
    )
    print(f"  git:      {git}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("project_name", help="name of the new project directory")
    parser.add_argument("--dest", default=".", help="parent directory (default: .)")
    parser.add_argument(
        "--from",
        dest="source",
        default=None,
        help=f"git URL or local template directory (default: {DEFAULT_TEMPLATE_URL})",
    )
    parser.add_argument("--description", default=None,
                        help="one-line README description (default: vision's first sentence)")
    parser.add_argument("--vision", default=None, help="roadmap vision paragraph")
    parser.add_argument("--implemented", action="append", default=[],
                        help="roadmap Implemented bullet (repeatable)")
    parser.add_argument("--backlog", action="append", default=[],
                        help="roadmap Backlog bullet (repeatable)")
    parser.add_argument("--not-in-scope", dest="not_in_scope", action="append",
                        default=[], help="roadmap Not in scope bullet (repeatable)")
    parser.add_argument("--no-git", action="store_true",
                        help="skip git init (template files only)")
    parser.add_argument("--dry-run", action="store_true",
                        help="print the plan and write nothing")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    name = args.project_name.strip()
    if not name:
        fail("project name must not be empty")
    slug = slugify(name)

    dest_root = Path(args.dest).expanduser().resolve()
    target = dest_root / slug
    if target.exists():
        fail(f"refusing to overwrite existing path: {target}", code=2)

    description = args.description or first_sentence(args.vision or "") or None
    if args.dry_run:
        print_plan(target, slug, args, description)
        return 0

    dest_root.mkdir(parents=True, exist_ok=True)
    for stale in sorted(dest_root.glob(f".{slug}.scaffold-*")):
        print(f"bootstrap: removing stale staging directory {stale}", file=sys.stderr)
        shutil.rmtree(stale, ignore_errors=True)
    staging = dest_root / f".{slug}.scaffold-{os.getpid()}"

    temp_roots: list[Path] = []
    try:
        template = resolve_template(args.source, temp_roots)
        copy_template(template, staging)
        seed_readme(staging / "README.md", name, description)
        seed_roadmap(
            staging / "ROADMAP.md",
            args.vision,
            args.implemented,
            args.backlog,
            args.not_in_scope,
        )
        if not args.no_git:
            init_git(staging)
        staging.rename(target)
    except BaseException:
        # Nothing half-built is left behind: the failed tree never becomes the
        # target, so a retry of the same command is not blocked by it.
        shutil.rmtree(staging, ignore_errors=True)
        raise
    finally:
        for root in temp_roots:
            shutil.rmtree(root, ignore_errors=True)

    print(f"Created {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
