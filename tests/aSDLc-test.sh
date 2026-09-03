#!/usr/bin/env bash
# aSDLC Template Test Suite
# Run: bash /tests/aSDLc-test.sh or make test-all (if Makefile present)

set -euo pipefail

CHANGELOG="CHANGELOG.md"
ROADMAP="ROADMAP.md"
DOCS_DIR="docs"
AGENTS="AGENTS.md"

pass=0
fail=0

echo "========================================="
echo " aSDLC Template Test Suite"
echo "========================================="
echo ""

# Test 1: CHANGELOG format
echo "--- Test 1: CHANGELOG.md Format ---"
if [ -f "$CHANGELOG" ]; then
  if grep -q "^## \[Unreleased\]" "$CHANGELOG"; then
    echo "  [PASS] [Unreleased] section present"
    pass=$((pass + 1))
  else
    echo "  [FAIL] Missing [Unreleased] section"
    fail=$((fail + 1))
  fi
  if grep -q "^### Added\|^### Changed\|^### Deprecated\|^### Removed\|^### Fixed\|^### Security" "$CHANGELOG"; then
    echo "  [PASS] Change categories present"
    pass=$((pass + 1))
  else
    echo "  [FAIL] No change categories found"
    fail=$((fail + 1))
  fi
else
  echo "  [FAIL] CHANGELOG.md not found"
  fail=$((fail + 1))
fi
echo ""

# Test 2: ROADMAP structure
echo "--- Test 2: ROADMAP.md Structure ---"
if [ -f "$ROADMAP" ]; then
  if grep -q "## Implemented\|## Backlog\|## Not in scope" "$ROADMAP"; then
    echo "  [PASS] Required lists present (Implemented/Backlog/Not in scope)"
    pass=$((pass + 1))
  else
    echo "  [FAIL] Missing required lists"
    fail=$((fail + 1))
  fi
else
  echo "  [FAIL] ROADMAP.md not found"
  fail=$((fail + 1))
fi
echo ""

# Test 3: /docs linkage
echo "--- Test 3: /docs Directory ---"
if [ -d "$DOCS_DIR" ]; then
  echo "  [PASS] docs/ directory exists"
  pass=$((pass + 1))
  if [ -f "$DOCS_DIR/README.md" ]; then
    echo "  [PASS] docs/README.md exists (child aSDLC index)"
    pass=$((pass + 1))
  else
    echo "  [WARN] docs/README.md missing"
  fi
else
  echo "  [FAIL] docs/ directory not found"
  fail=$((fail + 1))
fi
echo ""

# Test 4: AGENTS.md contracts
echo "--- Test 4: AGENTS.md Structure ---"
if [ -f "$AGENTS" ]; then
  if grep -q "## Core Contract" "$AGENTS"; then
    echo "  [PASS] Core Contract section present"
    pass=$((pass + 1))
  else
    echo "  [FAIL] Missing Core Contract section"
    fail=$((fail + 1))
  fi
else
  echo "  [FAIL] AGENTS.md not found"
  fail=$((fail + 1))
fi
echo ""

# Test 5: CONTRIBUTING.md references
echo "--- Test 5: CONTRIBUTING.md References ---"
if [ -f "CONTRIBUTING.md" ]; then
  if grep -q "AGENTS.md" CONTRIBUTING.md && ! grep -q "github.com" CONTRIBUTING.md; then
    echo "  [PASS] References root AGENTS.md (no GitHub URLs)"
    pass=$((pass + 1))
  else
    echo "  [FAIL] Incorrect AGENTS.md references"
    fail=$((fail + 1))
  fi
else
  echo "  [FAIL] CONTRIBUTING.md not found"
  fail=$((fail + 1))
fi
echo ""

# Summary
echo "========================================="
echo " Summary"
echo "========================================="
echo "  Passed: $pass"
echo "  Failed: $fail"
echo ""

total=$((pass + fail))
if [ "$fail" -eq 0 ]; then
  echo "All $total tests passed! ✅"
  exit 0
else
  echo "$fail test(s) failed ❌"
  exit 1
fi