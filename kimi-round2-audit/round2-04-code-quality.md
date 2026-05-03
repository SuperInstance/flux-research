# Round 2 — Code Quality Spot Check

**Repository:** https://github.com/cocapn/plato  
**Date:** 2026-04-30  
**Reviewer:** Senior Software Engineer Review  

---

## 4.1 Repository Structure

```
plato/
├── .gitignore              # Standard Python gitignore
├── LICENSE                 # MIT License
├── README.md               # Extensive project docs
├── pyproject.toml          # Package config (setuptools)
├── src/
│   └── plato/
│       ├── __init__.py     # SDK: FleetConnection + connect() + main()
│       └── cli.py          # CLI: 7 subcommands
├── examples/
│   └── 01_hello_fleet.py   # Single example script
└── docs/
    ├── openapi.yaml        # OpenAPI 3.1 spec
    ├── rfc-001-tile-protocol.md
    ├── rfc-002-bottle-protocol.md
    └── rfc-003-i2i-protocol.md
```

**What's Present:**
- Clean src-layout (`src/plato/`)
- `pyproject.toml` with dev dependencies (pytest, mypy, ruff)
- OpenAPI specification with schemas
- 3 well-structured RFC documents
- 1 runnable example
- MIT license

**What's Missing (Critical Gaps):**
- **No test directory or test files** — pytest finds zero tests
- **No `.github/workflows/`** — zero CI/CD automation
- **No `tests/` folder** — no unit, integration, or regression tests
- **No `Makefile`** or task runner for lint/test/format
- **No `tox.ini`** or matrix testing
- **No Rust code** despite README advertising 5 crates.io packages — this repo is Python-only
- **No CHANGELOG.md** or version history
- **No CONTRIBUTING.md** or developer guide
- **No type stubs** (`py.typed` marker missing)

---

## 4.2 Python SDK Review

### File: `src/plato/__init__.py` (158 lines)

#### Architecture
- Single class `FleetConnection` encapsulating all HTTP calls
- `connect()` factory function returns a connected instance
- Uses `urllib.request` (stdlib) instead of `requests` — lightweight but limited

#### Type Safety: Score 3/5
**Positives:**
- Most method signatures have type hints (`host: str`, `confidence: float`, etc.)
- Return types annotated: `-> Dict[str, Any]`
- `Optional[List[str]]` used for nullable fields

**Negatives:**
- `self._stage = {}` and `self._room = None` lack annotations (lines 37–38)
- `self._boot_camp = []` lacks type annotation (line 37)
- `main()` function has no return type annotation (line 154)
- Missing `py.typed` marker means downstream consumers can't use mypy effectively

#### Error Handling: Score 2/5
**Critical Issue — No Exception Handling at All:**
- Lines 40–55 (`_get`, `_post`): Zero `try/except` blocks. Any network error (timeout, DNS failure, 500 response) propagates raw to the caller.
- `urllib.error.HTTPError` is imported (line 17) but **never caught**.
- `urllib.error.URLError` is never caught.
- `json.loads()` can raise `json.JSONDecodeError` on bad server responses — uncaught.
- `timeout=10` hardcoded with no configurability.

**Recommended fix:**
```python
from urllib.error import HTTPError, URLError

def _get(self, url: str) -> Dict[str, Any]:
    try:
        req = urllib.request.Request(url, headers={...})
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            return json.loads(resp.read())
    except HTTPError as e:
        raise PlatoAPIError(f"HTTP {e.code}: {e.reason}") from e
    except URLError as e:
        raise PlatoConnectionError(f"Connection failed: {e.reason}") from e
    except json.JSONDecodeError as e:
        raise PlatoAPIError(f"Invalid JSON from server: {e}") from e
```

#### Security: Score 2/5
**CRITICAL: URL Parameter Injection Vulnerability**

Lines 59, 68, 75, 79 construct URLs via f-string interpolation:
```python
self._get(f"{self._mud_base}/connect?agent={self.agent}&job={self.job}")
```

If `agent="evil&job=admin"` or `agent="test agent"`, the query string is malformed:
- `agent=test agent` → space is sent raw (should be `%20`)
- `agent=evil&job=admin` → injects extra `job` parameter

**Fix:** Use `urllib.parse.urlencode` or `urllib.parse.quote`:
```python
from urllib.parse import urlencode

query = urlencode({"agent": self.agent, "job": self.job})
self._get(f"{self._mud_base}/connect?{query}")
```

**Other Security Issues:**
- No input validation on `agent` parameter (should restrict to alphanumeric + hyphens per OpenAPI spec)
- No input validation on `domain`, `question`, `answer` lengths (per RFC-001 gates)
- No rate limiting or retry logic
- HTTP (not HTTPS) used on port 4042 (`http://cocapn.ai:4042`) — plaintext MUD API

#### Documentation: Score 3/5
- Module docstring is good with usage example (lines 1–11)
- `connect()` has detailed docstring with Args/Returns/Example (lines 128–151)
- Most methods have one-line docstrings
- Missing: docstrings on `_get`, `_post`, `main()`
- Missing: docstring on class properties (`room_name`, `boot_camp`, `stage`)

---

## 4.3 CLI Review

### File: `src/plato/cli.py` (314 lines)

#### Command Structure
7 subcommands: `explore`, `status`, `rooms`, `room`, `tile`, `map`, `agents`

**Positives:**
- Subparser pattern with `argparse` — clean, standard approach
- Good help text per subcommand (lines 256–290)
- `choices=["scholar", ...]` for job parameter (line 265)
- Interactive explorer handles `EOFError` and `KeyboardInterrupt` gracefully (lines 183–187)
- `--agent`, `--confidence`, `--tags` flags on `tile` command

**Negatives:**
- No `--host` override flag — hardcoded to `cocapn.ai` (line 20)
- No `--timeout` flag
- No `--version` flag
- No verbose/quiet logging levels
- No `--format json` output option for scripting
- `cmd_explore` has deeply nested logic (90+ lines) — could be broken into smaller functions

#### Error Handling: Score 3/5
Better than the SDK but still weak:
- Each command wraps in `try/except Exception` (lines 48–62, 67–83, etc.)
- Catches all exceptions but prints only `str(e)` — loses traceback, no structured error codes
- No specific handling for HTTP 404 vs 500 vs timeout
- `sys.exit(1)` on all errors — acceptable but could use different exit codes

#### UX Issues:
- Hardcoded emojis in output may fail on some terminals (e.g., Windows CMD)
- `cmd_room` truncates answers at 120 chars with `...` — no `--full` flag
- `cmd_rooms` limits to 30 rooms with no `--all` flag
- No shell completion support

---

## 4.4 Rust Code Review

**N/A — No Rust code in this repository.**

The README advertises 5 crates.io packages (`cargo install ct-demo plato-afterlife plato-instinct plato-relay plato-lab-guard`) but this repository is **Python-only**. The monorepo claim is misleading — this appears to be just the Python SDK wrapper, not the actual monorepo containing all language implementations.

---

## 4.5 Test Suite

**Score: 1/5 — No tests exist.**

- `find . -name "*test*"` returns nothing
- `python -m pytest` exits with "no module named pytest" (not even in environment)
- Zero unit tests for `FleetConnection`
- Zero integration tests for CLI commands
- Zero mock tests for HTTP layer
- Edge cases untested:
  - Network timeout
  - HTTP 500 response
  - Malformed JSON response
  - Empty response body
  - Invalid `confidence` values (< 0 or > 1)
  - Unicode in `question`/`answer`
  - Very long `question` (> 500 chars)

**Recommended test coverage:**
```python
# tests/test_connection.py
import pytest
from unittest.mock import patch, MagicMock
from plato import FleetConnection

def test_connect_success():
    ...

def test_connect_http_error():
    ...

def test_connect_timeout():
    ...

def test_submit_tile_validates_confidence():
    ...

def test_move_to_url_encoding():
    ...
```

---

## 4.6 Examples

### File: `examples/01_hello_fleet.py`

**Positives:**
- Clear docstring with usage instructions (lines 1–7)
- Demonstrates full SDK workflow: connect → look → move → examine → submit_tile
- Uses `sys.path.insert` to import from `../src` — works without pip install

**Negatives:**
- Only **one example** for a project of this scope
- No error handling — if server is down, script crashes with unhelpful traceback
- No `--dry-run` mode
- Example uses live production server by default — risky for beginners
- Missing examples for:
  - CLI usage
  - Custom host configuration
  - Batch tile submission
  - Bottle protocol usage
  - Reading room data

**Does it run?**
- Syntax is valid (`python -m py_compile` passes)
- Would execute against live server — no offline/mock mode
- `sys.path.insert(0, "../src")` assumes CWD is `examples/` directory

---

## 4.7 CI/CD

**Score: 1/5 — No CI/CD exists.**

- No `.github/workflows/` directory
- No automated testing on PR/push
- No automated linting (ruff, mypy)
- No automated package publishing
- No dependency vulnerability scanning
- No code coverage reporting

**Recommended minimal workflow:**
```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.8', '3.10', '3.12']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -e ".[dev]"
      - run: ruff check src tests
      - run: mypy src
      - run: pytest --cov=plato --cov-report=xml
```

---

## 4.8 Production Readiness Scorecard

| Area | Score | Notes |
|------|-------|-------|
| Code readability and style | 3/5 | Clean PEP 8 style, ruff configured, but inconsistent docstring depth |
| Type safety | 3/5 | Most signatures typed, but missing `py.typed`, internal attrs untyped |
| Error handling | 2/5 | SDK has zero exception handling; CLI catches generically with no granularity |
| Documentation | 3/5 | Good README and RFCs, good `connect()` docstring, but many gaps |
| Test coverage | 1/5 | Zero tests. Absolutely none. |
| Security | 2/5 | URL parameter injection, no input validation, HTTP plaintext for MUD |
| Architecture | 3/5 | Simple and modular, but single-responsibility violations in CLI explorer |
| CI/CD | 1/5 | No automation whatsoever |
| Examples | 2/5 | One example only, no CLI examples, no error-handling patterns |
| Package config | 3/5 | pyproject.toml present but `main = "plato:main"` script entry is fragile |

**Overall Production Readiness: 2.3/5 — Not production-ready.**

---

## 4.9 Critical Issues

| Severity | Issue | Location | Fix |
|----------|-------|----------|-----|
| **CRITICAL** | URL query parameter injection — `agent`/`room`/`target` not URL-encoded | `src/plato/__init__.py` lines 59, 68, 75, 79; `src/plato/cli.py` lines 115, 147, 159, 169 | Use `urllib.parse.urlencode()` for all query strings |
| **CRITICAL** | Zero exception handling in SDK HTTP layer | `src/plato/__init__.py` lines 40–55 | Wrap `_get`/`_post` in try/except for `HTTPError`, `URLError`, `JSONDecodeError`; raise custom exceptions |
| **HIGH** | No tests exist | Entire repo | Create `tests/` with pytest, add unit + integration tests, target 80%+ coverage |
| **HIGH** | No CI/CD | Entire repo | Add `.github/workflows/ci.yml` with pytest, ruff, mypy across Python 3.8–3.12 |
| **HIGH** | `pyproject.toml` script entry `plato = "plato:main"` may conflict with package namespace | `pyproject.toml` line 38 | Verify entry point resolution; consider `plato = "plato.cli:main"` instead |
| **MEDIUM** | No input validation on `agent` name format | `src/plato/__init__.py` line 29 | Validate against `^[a-zA-Z0-9_-]+$` per OpenAPI spec |
| **MEDIUM** | No input validation on `confidence` range | `src/plato/__init__.py` line 86 | Add `assert 0.0 <= confidence <= 1.0` or raise `ValueError` |
| **MEDIUM** | No `py.typed` marker — downstream mypy can't use types | Root package | Add empty `py.typed` file in `src/plato/` |
| **MEDIUM** | HTTP (not HTTPS) for MUD API on port 4042 | `src/plato/cli.py` line 26; `src/plato/__init__.py` line 22 | Document security implications; add TLS if possible |
| **MEDIUM** | Hardcoded timeouts with no configurability | `src/plato/__init__.py` lines 43, 54 | Add `timeout` parameter to `FleetConnection.__init__` |
| **LOW** | `connect()` factory calls `.connect()` automatically — side effect in constructor | `src/plato/__init__.py` lines 149–151 | Consider separating construction from connection; document behavior |
| **LOW** | `cmd_explore` is 84 lines — violates single-responsibility | `src/plato/cli.py` lines 108–191 | Extract input parsing, action dispatch, and room display into helper functions |

---

## 4.10 Recommendations

| Priority | Action |
|----------|--------|
| **P0** | Fix URL parameter injection vulnerability immediately — use `urllib.parse.urlencode` |
| **P0** | Add exception handling in `FleetConnection._get` and `_post` with custom exception classes |
| **P0** | Create `tests/` directory with comprehensive pytest suite (minimum 80% coverage) |
| **P0** | Add `.github/workflows/ci.yml` for automated testing, linting, and type-checking |
| **P1** | Add `py.typed` marker and run `mypy --strict` to fix all type errors |
| **P1** | Add input validation: agent name regex, confidence range, question/answer length limits |
| **P1** | Add `--host`, `--timeout`, `--format json`, and `--version` flags to CLI |
| **P1** | Create `tests/test_cli.py` with `unittest.mock` to test CLI commands without network |
| **P2** | Add retry logic with exponential backoff for transient network failures |
| **P2** | Add logging (std `logging` module) with configurable verbosity |
| **P2** | Add 3–5 more examples: CLI usage, custom host, batch tile submission |
| **P2** | Add `CHANGELOG.md` and `CONTRIBUTING.md` |
| **P3** | Consider migrating from `urllib.request` to `httpx` or `requests` for better ergonomics |
| **P3** | Add pre-commit hooks for ruff and mypy |
| **P3** | Add Dependabot or similar for dependency security scanning |

---

## Summary

The `cocapn/plato` repository is a **small, well-intentioned Python SDK** for an agent training platform. The code is readable and the architecture is simple, but it is **not production-ready** by a significant margin. The most critical gaps are:

1. **Security vulnerability:** URL parameter injection via unescaped query strings
2. **Zero error handling:** SDK crashes on any network failure
3. **Zero tests:** No automated verification of any code path
4. **Zero CI/CD:** No quality gates prevent bad code from merging

With approximately 2–3 days of focused effort (tests + error handling + CI + URL encoding), this could reach a 4/5 production readiness score. As it stands, it is suitable for prototyping and demos only.
