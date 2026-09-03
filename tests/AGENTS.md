# Tests Directory AGENTS.md

## Tests

- **Include tests for new features and bug fixes** — but test observable behavior, not implementation.
  A test should read like a small demo of the public API: create elements, interact, assert what a user would see.
  Avoid tests that reach into internals — private attributes, call counts, monkeypatched browser or library APIs, hand-built fake objects.
  They break when the implementation changes (so they get rewritten along with it, guarding nothing) and they are hard to read for anyone who doesn't know the internals.

- **Before writing a test, read a recent one in the same file.**
  The existing suite is almost entirely behavior tests, and copying a neighbouring test's shape is faster and safer than inventing a new one.

- **A regression test must fail when the fix is reverted** — verify that once before trusting it.
  A test that has only ever been seen green proves nothing.

- **Not every change needs a test.**
  We have over a thousand tests and the browser-based ones dominate the runtime, so each new test is a permanent cost for every contributor.
  If a fix can only be covered by an elaborate test that mirrors the implementation, skipping the test can be the better choice — give the reason in the **Implementation** section of the pull request, so it reads as a deliberate decision and not as an oversight.
  A small, obviously correct fix with a clear explanation is often worth more than an unreadable regression test.

- **If you find yourself building scaffolding to observe an internal mechanism**, that is the signal to stop and either find the user-visible effect to assert on, or skip the test.