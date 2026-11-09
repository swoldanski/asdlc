# Contributing

Thank you for contributing to this project!

## Where the rules live

The root [`AGENTS.md`](AGENTS.md) is the binding contract. The aSDLC pass, the
rule for what belongs under `/docs` versus `/architecture`, the AI-attribution
trailer, and the closeout procedure all live there; this file does not restate
them. Read the rail first, then come back here for the mechanics it leaves open.

The documents it indexes are [`AGENTS.md`](AGENTS.md), [`ROADMAP.md`](ROADMAP.md)
for direction, and the project's release record — [`CHANGELOG.md`](CHANGELOG.md)
unless the project keeps its release history in git tags, in which case the tags
are the record and the changelog stays as the template left it.

## Workflow

1. Update `main` and create a feature branch:

   ```bash
   git pull origin main
   git checkout -b feature/short-description
   ```

2. Make your changes following the project's purpose and scope.

3. Run the checks the repository defines before committing — its test command,
   linter, or build, whichever `AGENTS.md` or the project's own docs name. If it
   defines none, say so in the closeout rather than claiming a check that does
   not exist.

## Commit Messages

Conventional commit format:

```
<type>(<scope>): <description>

<body>

<footer>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## Pull Request Process

1. Push your branch and open a pull request against `main`.
2. Ensure the repository's checks pass.
3. Describe in the pull request:
   - What changed and why
   - Which aSDLC pass this aligns with
   - Any breaking changes
   - Testing performed

After merge, the branch can be deleted.

## Code of Conduct

Be respectful and constructive in all interactions.

---

Questions? Open an issue or reach out to the maintainers.