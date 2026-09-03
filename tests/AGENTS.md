# Tests Directory AGENTS.md

Purpose
- Owns the test suite and verification mechanisms for the aSDLC template
- Provides structured testing that enforces project quality standards

Ownership
- Maintained by the project core team
- Linked from root AGENTS.md as a child directory

Local Contracts
- Test scripts and configurations must not modify root-level template files directly
- All test outputs (reports, logs) remain within the /tests directory
- Test changes require aSDLC pass closeout

Work Guidance
- Verification scripts (GitHub Actions workflows) are the primary test mechanisms
- Pre-commit hooks (.git/hooks/pre-commit) enforce CHANGELOG, ROADMAP, and /docs compliance
- Test additions must align with keepachangelog.com format for CHANGELOG entries
- New test categories must be documented and cannot weaken existing aSDLC contracts

Verification
- Existing checks: pre-commit hook
- No additional verification framework exists yet; update when one is established
- Test results are reported in the aSDLC closeout pass

Child aSDLC Index
- Root-owned files: AGENTS.md, LICENSE, ROADMAP.md, CHANGELOG.md, CONTRIBUTING.md
- /docs/ holds user-facing documentation and is governed by its own child AGENTS.md
- /tests/ is owned by the root aSDLC and reports verification status on closeout