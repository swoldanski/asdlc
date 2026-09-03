# Contributing

Thank you for contributing to the aSDLC project! Please follow the guidelines below to ensure smooth collaboration and maintain project quality.

## Overview

This project uses the aSDLC framework as defined in [AGENTS.md](AGENTS.md) for structured software development. All contributions are tracked through the following core documents:

- [`AGENTS.md`](AGENTS.md) - Agent contracts and hierarchy
- [`ROADMAP.md`](ROADMAP.md) - Project direction and scope
- [`CHANGELOG.md`](CHANGELOG.md) - Change tracking

## Workflow

### 1. Pre-Work

1. Ensure you have the latest version of the framework documents:

   ```bash
   git pull origin main
   ```

2. Verify the required documents are present and current:
   - [`AGENTS.md`](AGENTS.md) - read before editing
   - [`ROADMAP.md`](ROADMAP.md) - must be kept current per user preferences
   - [`CHANGELOG.md`](CHANGELOG.md) - all notable changes documented

### 2. Branch & Development

1. Create a feature branch from `main`:

   ```bash
   git checkout -b feature/short-description
   ```

2. Make your changes following the project's purpose and scope.

3. If adding a user-facing feature:
   - Create corresponding documentation in `/docs/`
   - Update [`/docs/README.md`](/docs/README.md) if new files/directories are added

### 3. Pre-Commit Checks

Before committing, run the verification checks (see [Verification Mechanisms](#verification-mechanisms) below).

### 4. Commit Message Guidelines

Conventional commit format:

```
<type>(<scope>): <description>

<body>

<footer>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### 5. Pull Request Process

1. Push your branch and open a PR against `main`
2. Ensure all verification checks pass (see below)
3. Fill the PR template describing:
   - What changed and why
   - Which aSDLC pass this aligns with
   - Any breaking changes
   - Testing performed

### 6. Post-Merge

After PR merge:
- Branch can be deleted

## Code of Conduct

Be respectful and constructive in all interactions. Follow the project's aSDLC pass closeout procedure for any changes affecting structure, contracts, or workflows.

## Verification Mechanisms

This template currently has no verification framework. The root `AGENTS.md` rule states: "Verification must reflect an existing check; if no verification framework exists yet, leave it empty and update it when one exists." Contributors should follow the closeout procedure in the root `AGENTS.md` and the guidance in `tests/AGENTS.md` and `docs/AGENTS.md` for behavioral testing philosophy.

---
 
Questions? Open an issue or reach out to the maintainers.