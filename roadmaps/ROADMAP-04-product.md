# ROADMAP-04: Product Foundation
**Phase 4 | Priority: P2 | Timeline: This Quarter**

## What "Product" Means Here
SuperInstance is a research lab, not a SaaS startup. But "product" means "things that work well enough that someone would actually use them." Right now, most of this isn't usable by anyone except the authors.

---

## PROD-01: PyPI Package Cleanup

**Current state:** Packages exist but look abandoned — no docs URL, no classifiers, no description.
**Found by:** Startup CTO

### fleet-agent
```
python -m pip install fleet-agent
→ Shows: "UNKNOWN PACKAGE" with no description
```

**Fix:**
1. Add `description` field in pyproject.toml
2. Add `license`, `classifiers`, `urls`
3. Write `docs/` directory with README.md
4. Publish new version: `python3 -m build && twine upload`

### plato-sdk
1. Add docs URL to PyPI listing
2. Verify `import plato_sdk` works on clean install
3. Write quickstart guide in README

---

## PROD-02: flux-studio Real Features

**Current state:** Syntax highlighting only, no real IDE support
**Found by:** Startup CTO

**What "real features" means:**
- IntelliSense for GUARD DSL keywords
- Hover docs for each GUARD opcode
- FLUX-C bytecode debugger (visualize constraint satisfaction)
- "Compile and view bytecode" command

**Implementation:** Use VS Code Language Server Protocol (LSP) instead of just TextMate grammar.

---

## PROD-03: cocapn.ai Live Demo

**Current state:** Backend :5000 crashes repeatedly (healthcheck flagged)
**Found by:** Marine Safety Engineer

**Minimum viable demo:**
1. Keep :5000 running reliably (fix SIGKILL restart cycle)
2. Ensure "try it now" works for external browsers
3. Add monitoring: simple uptime badge on the page

---

## PROD-04: Documentation Overhaul

**Current state:** Inconsistent, spread across repos
**Found by:** Startup CTO (documentation = ugly)

**Priority docs to write:**
1. **"Getting Started in 10 Minutes"** — for cocapn.ai and fleet-agent
2. **GUARD DSL Specification** — complete grammar, all opcodes, examples
3. **FLUX-C Bytecode Reference** — for the VM implementers
4. **Architecture Overview** — how all the repos fit together
5. **Contribution Guide** — how to submit PRs, run tests, file issues

---

## PROD-05: Community Seed

**Current state:** 0 external contributors, 6 repos, 6 stars
**Found by:** Startup CTO

**Minimum viable community:**
1. One (1) non-SuperInstance contributor by end of quarter
2. README badges: build status, docs, Discord link
3. Open issues labeled "good first contribution"
4. Discord or GitHub Discussions active

---

## PROD-06: Community Building Tactics

- Post constraint-theory-ecosystem to Hacker News / Lobsters
- Submit GUARD DSL toprogramming language subreddits
- Write blog post: "How we replaced ML with math for safety-critical checking"
- Reach out to 3 formal methods professors about collaboration
