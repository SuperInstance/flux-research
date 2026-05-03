# Round 2 - Developer Experience Audit

## Audit Information
- **Auditor:** DX Research Bot (test_auditor)
- **Date:** 2025-04-30
- **Test Agent:** test_auditor / hello_auditor
- **Platform:** PLATO / COCAPN
- **Website:** https://cocapn.github.io
- **API Base (Documented):** http://cocapn.ai:4042 (BROKEN)
- **API Base (Actual):** http://147.224.38.131:4042 (WORKING)

---

## Timeline (Step-by-Step)

| Step | Action | Time | Result | Notes |
|------|--------|------|--------|-------|
| 1a | Visit https://cocapn.github.io | ~2s | SUCCESS | Beautiful landing page. Stats: 92 repos, 61 PyPI packages, 48 npm, 18 Rust crates, 11,500+ tiles, 1,257 rooms |
| 1b | Visit https://cocapn.github.io/developers.html | ~1s | SUCCESS | Clean dev page. 3-step quickstart (connect, explore, submit). Architecture diagram. "Install Anywhere" section shows pip/npm/cargo commands |
| 1c | Read quickstart | ~1min | CLEAR | Well-written. But uses `cocapn.ai:4042` URLs which are broken |
| 2a | `pip install cocapn` | ~5s | SUCCESS | Installed 0.2.0. Warning: script not on PATH |
| 2b | `pip install plato-mud-server` | ~3s | SUCCESS | 0.2.2 installed |
| 2c | `pip install deadband-protocol` | ~3s | SUCCESS | 0.3.0 installed |
| 2d | `pip install bottle-protocol` | ~3s | SUCCESS | 0.1.0 installed |
| 2e | `pip install flywheel-engine` | ~3s | SUCCESS | 0.3.2 installed |
| 2f | `pip install cocapn-sdk` | ~5s | SUCCESS | 0.1.0 + dependencies (keeper-beacon, court, plato-tile-spec, plato-provenance) |
| 2g | `pip install plato` | ~10s | CRITICAL FAILURE | Installed WRONG package (plato-0.2.1 with Faker). Dependency conflict: downgraded typing-extensions to 3.10.0.2, breaking pydantic, fastapi, torch, rich-toolkit |
| 2h | `cocapn --help` | ~1s | FAILURE | `ModuleNotFoundError: No module named 'agent'` - CLI entry point broken |
| 2i | `plato --help` | ~1s | FAILURE | `plato: not found` - No CLI exists |
| 2j | `python -c "import cocapn; print(cocapn.__version__)"` | ~1s | PARTIAL | Returns 0.1.0 but pip installed 0.2.0 - version mismatch |
| 3a | `curl http://cocapn.ai:4042/help` | 15s | TIMEOUT | Connection timeout on all documented endpoints |
| 3b | `curl http://cocapn.ai:4042/status` | 15s | TIMEOUT | Same issue |
| 3c | `curl http://cocapn.ai:4042/connect?...` | 15s | TIMEOUT | Same issue |
| 3d | Discover direct IP in HTML comment | ~2min | DISCOVERY | Found `147.224.38.131` in cocapn.ai homepage HTML comment |
| 3e | `curl http://147.224.38.131:4042/help` | 0.38s | SUCCESS | JSON response with endpoint documentation |
| 3f | `curl http://147.224.38.131:4042/status` | 0.40s | SUCCESS | crab-trap-v3, 39 rooms, 24 agents, 12151 tiles |
| 3g | `curl http://147.224.38.131:4042/connect?...` | 1.16s | SUCCESS | Rich harbor description, 23 exits, 3 objects, scholar job assigned |
| 3h | `curl http://147.224.38.131:4042/look?...` | 0.36s | SUCCESS | Full room state with objects and agents |
| 3i | `curl http://147.224.38.131:4042/move?...` | 0.37s | SUCCESS | Moved to forge, task assigned, submit hint provided |
| 4 | `curl -X POST http://147.224.38.131:8847/submit` | ~1s | SUCCESS | Accepted, tile_hash returned, provenance chain signed, trace_id generated |
| 5a | `curl http://147.224.38.131:8847/status` | ~1s | SUCCESS | Active v2-provenance-explain, gate stats, room list with tile counts |
| 5b | `curl http://147.224.38.131:8847/rooms` | ~1s | SUCCESS | 100+ rooms with tile counts and creation dates |
| 6 | `curl http://147.224.38.131:4044/leaderboard` | ~1s | SUCCESS | 10+ agents with ELO ratings (mu/sigma/rating), wins/losses/draws |
| 7a | `python -c "from cocapn import CocapnAgent; agent=CocapnAgent(); print(agent.status())"` | ~1s | SUCCESS | Offline status: 1 tile, sentiment 0.5 |
| 7b | `python -c "import cocapn; print(dir(cocapn))"` | ~1s | SUCCESS | 14 exports: CocapnAgent, Flywheel, Room, Tile, TileStore, agent, deadband, flywheel, room, tile |
| 7c | Test `agent.teach(q, a)` | ~1s | SUCCESS | "Learned. 2 tiles total." |
| 7d | Test `agent.chat('hello')` | ~1s | FAILURE | HTTP 401 Unauthorized - requires API key |
| 7e | Test `agent.conversation('hello')` | ~1s | FAILURE | `'list' object is not callable` - naming bug |
| 7f | Test `Flywheel().stats()` | ~1s | SUCCESS | Returns total_tiles, rooms, exchanges |
| 8a | Visit https://github.com/cocapn/plato | ~2s | PARTIAL | Monorepo exists. 2 commits. 0 stars/forks/watchers. 1 contributor. No CI. No tests. No releases. |
| 8b | Check examples/ | ~1s | MINIMAL | Only 1 example: 01_hello_fleet.py |
| 8c | Check docs/ | ~1s | GOOD | openapi.yaml + 3 RFCs (tile, bottle, i2i protocols) |
| 8d | Check src/plato/ | ~1s | MINIMAL | Only __init__.py and cli.py. No test directory. |

---

## Errors & Friction Points

| Severity | Issue | Location | Details |
|----------|-------|----------|---------|
| CRITICAL | All documented API URLs are broken | developers.html, README.md, GitHub | `cocapn.ai:4042`, `:8847`, `:4044` all timeout. Cloudflare doesn't proxy non-standard ports. The actual endpoint requires direct IP `147.224.38.131`. No user can follow the quickstart as written. |
| CRITICAL | `pip install plato` installs wrong package | developers.html "Install Anywhere" | Installs `plato-0.2.1` (Faker-based data generation library), NOT the PLATO framework. Downgrades typing-extensions, breaking pydantic, fastapi, torch, and 10+ other packages. |
| HIGH | `cocapn` CLI is completely broken | `cocapn` entry point script | Script does `from agent import main` but no `agent` module exists at top level. Entry point is misconfigured. Every CLI invocation crashes. |
| HIGH | `cocapn.__version__` mismatch | `cocapn` Python package | pip says 0.2.0, module says 0.1.0. Indicates stale __init__.py or release/tag mismatch. |
| MEDIUM | No `plato` CLI exists | developers page | Page says `pip install plato` but there's no `plato` CLI. The monorepo source only has 2 files (__init__.py and cli.py). |
| MEDIUM | `conversation` is a list, not a method | `cocapn.agent.CocapnAgent` | `agent.conversation(...)` raises `'list' object is not callable`. Should be `agent.conversation` as attribute, or renamed to avoid confusion. |
| MEDIUM | `agent.chat()` requires API key without documentation | `cocapn.agent.CocapnAgent` | Returns HTTP 401. No mention of needing an API key in docs. Offline methods work but online methods fail silently. |
| MEDIUM | PATH warning on pip install | All pip installs | Scripts installed to `/home/kimi/.local/bin` which is not on PATH. New users won't find the CLI even if it worked. |
| LOW | Example file imports wrong module | `examples/01_hello_fleet.py` | Does `import plato` but `plato` package is unrelated. Also uses `sys.path.insert(0, "../src")` - won't work when installed. |
| LOW | No tests in monorepo | `cocapn/plato` GitHub repo | No test/ directory, no CI, no pytest configuration. Cannot verify anything works. |
| LOW | README uses localhost URLs in architecture diagram | `cocapn/plato` README.md | Architecture diagram shows `localhost:8847` and `localhost:4042` - these are local dev URLs, not the live fleet. |
| LOW | No GitHub releases or packages | `cocapn/plato` GitHub repo | No releases published, no packages. Makes it hard to track versions or install from source. |
| LOW | Single contributor, 0 community | `cocapn/plato` GitHub repo | 0 stars, 0 forks, 0 watchers, 1 contributor. No community validation. |

---

## API Response Quality

| Endpoint | Latency | Response Quality | Issues |
|----------|---------|-------------------|--------|
| `GET /help` | 0.38s | Excellent | Full JSON documentation of all endpoints and jobs |
| `GET /status` | 0.40s | Excellent | Service name, architecture, room count, agent count, tile count, jobs list, fleet services count |
| `GET /connect` | 1.16s | Excellent | Rich room description, exits, objects, job, boot_camp, task, stage, fleet_status, how_to_contribute guide |
| `GET /look` | 0.36s | Excellent | Room state with object details (name, description, available_actions, dynamic flag), agents_here list, exits mapping |
| `GET /move` | 0.37s | Excellent | New room with task, stage info, submit_hint with exact curl command |
| `GET /examine` | ~0.5s | Good | Simple but clear object description |
| `GET /tasks` | ~0.5s | Good | 3 contextual tasks based on room and job |
| `POST /submit` | ~1s | Excellent | Accepted status, tile_hash, room_tile_count, provenance chain info, trace_id |
| `GET /rooms` | ~1s | Excellent | 100+ rooms with tile counts and creation timestamps |
| `GET /leaderboard` | ~1s | Excellent | Full ELO ratings with mu/sigma/rating, wins/losses/draws/games |

**API Verdict:** The API itself is fast, well-designed, and richly documented. The only problem is that the documented URLs don't work.

---

## SDK/CLI Assessment

| Component | Status | Version | Issues |
|-----------|--------|---------|--------|
| `cocapn` package | Installs OK | 0.2.0 (pip) / 0.1.0 (module) | Version mismatch. CLI broken. |
| `cocapn-sdk` package | Installs OK | 0.1.0 | Re-exports cocapn + adds TileSpec, ProvenanceChain, Judge, Bottle |
| `plato-mud-server` | Installs OK | 0.2.2 | No CLI tested |
| `deadband-protocol` | Installs OK | 0.3.0 | Standalone |
| `bottle-protocol` | Installs OK | 0.1.0 | Standalone |
| `flywheel-engine` | Installs OK | 0.3.2 | Standalone |
| `plato` (PyPI) | WRONG PACKAGE | 0.2.1 | Installs unrelated Faker-based library |
| `cocapn` CLI | BROKEN | - | `ModuleNotFoundError: No module named 'agent'` |
| `plato` CLI | MISSING | - | No entry point exists |
| `CocapnAgent` class | Partial | 0.1.0 | `status()`, `teach()`, `save()` work offline. `chat()` needs API key. `conversation` is broken. |
| `Tile` class | Works | - | Creates tiles with auto ID, timestamp, confidence. Has `to_dict()`. |
| `Room` class | Works | - | Basic room model |
| `TileStore` class | Works | - | Basic tile storage |
| `Flywheel` class | Works | - | `stats()`, `record_exchange()`, `ensure_room()`, `get_context()` |

---

## Overall Score

| Metric | Score (1-10) | Benchmark |
|--------|-------------|-----------|
| First impression (landing page) | 9 | LangChain: 8, CrewAI: 7 |
| Quickstart clarity (text) | 8 | LangChain: 7, CrewAI: 6 |
| Quickstart accuracy (does it work?) | 2 | LangChain: 9, CrewAI: 8 |
| Installation experience | 4 | LangChain: 9, CrewAI: 8 |
| Time to first successful API call | 2 | LangChain: 9, CrewAI: 8 |
| API design & response quality | 9 | LangChain: 8, CrewAI: 7 |
| SDK quality | 5 | LangChain: 9, CrewAI: 7 |
| CLI quality | 1 | LangChain: 8, CrewAI: 6 |
| Documentation completeness | 6 | LangChain: 9, CrewAI: 7 |
| GitHub repo quality | 3 | LangChain: 9, CrewAI: 8 |
| Error handling & debugging | 3 | LangChain: 8, CrewAI: 7 |
| **OVERALL** | **5/10** | LangChain: ~8.5, CrewAI: ~7.5 |

---

## The "Aha Moment"

**When it happens:** Step 3e - after discovering the direct IP and running the first successful API call.

**What it is:** The `connect` endpoint returns a rich, immersive description of the Harbor room with 23 exits, 3 interactive objects, and a personalized task. The world feels alive.

**Problem:** The aha moment is DELAYED by ~15 minutes of confusion because the documented URLs don't work. Most developers would have given up before reaching it.

---

## What Breaks, What Confuses, What's Missing

### What Breaks
1. **Every documented API URL** - `cocapn.ai:4042`, `:8847`, `:4044` all timeout. This is the #1 blocker.
2. **`cocapn` CLI** - Entry point references non-existent `agent` module.
3. **`pip install plato`** - Installs completely wrong package with dependency conflicts.
4. **`agent.conversation()`** - Naming collision with list attribute.
5. **`agent.chat()`** - Requires undocumented API key.

### What Confuses
1. **Which package to install?** Website says `pip install plato`, but that's wrong. Should be `pip install cocapn` or `pip install cocapn-sdk`.
2. **Why does the quickstart not work?** A developer copies the curl command exactly as shown and gets silence/timeout.
3. **Version mismatch** - pip says 0.2.0, code says 0.1.0. Which is real?
4. **No connection between SDK and API** - The SDK works offline, but it's unclear how to connect to the live fleet via the SDK.
5. **PATH warning** - Scripts installed to a path not on $PATH. Novice users won't understand.

### What's Missing
1. **Working quickstart URLs** - Must fix Cloudflare proxying or document direct IP.
2. **`pip install plato` ownership** - Need to either claim the PyPI name or stop advertising it.
3. **Tests** - No tests in monorepo = no confidence.
4. **CI/CD** - No GitHub Actions for automated testing.
5. **More examples** - Only 1 example file, and it imports the wrong module.
6. **CLI that works** - Need `cocapn` CLI that actually starts.
7. **API key documentation** - If `agent.chat()` needs a key, document how to get one.
8. **SDK-to-live-fleet bridge** - Show how to use `CocapnAgent` with the real API.
9. **Version consistency** - `__version__` must match package version.
10. **Community signals** - 0 stars/forks makes the project look abandoned.

---

## Recommendations

| Priority | Action | Impact |
|----------|--------|--------|
| P0 | Fix quickstart URLs. Either use a subdomain with standard ports (e.g., `api.cocapn.ai/help` proxied to `147.224.38.131:4042`), or document the direct IP clearly. | Unblocks 100% of new users |
| P0 | Fix `pip install plato` - either claim the PyPI name, or remove it from docs and replace with `pip install cocapn-sdk` | Prevents dependency disasters |
| P0 | Fix `cocapn` CLI entry point in pyproject.toml/console_scripts | Makes CLI usable |
| P1 | Add tests to monorepo and set up GitHub Actions CI | Builds confidence, prevents regressions |
| P1 | Fix `cocapn.__version__` to match pip version | Reduces confusion |
| P1 | Document how to use SDK with live API (API keys, base_url config) | Connects SDK to real fleet |
| P1 | Fix or rename `conversation` attribute on CocapnAgent | Removes naming collision |
| P2 | Add more examples (at least 3-5 covering SDK, CLI, and raw API) | Helps different learning styles |
| P2 | Add GitHub release tags and publish packages from monorepo | Enables version tracking |
| P2 | Add a CONTRIBUTING.md and issue templates | Grows community |
| P2 | Add a `plato` CLI that wraps the fleet API | Consistent with `pip install plato` promise |
| P3 | Add star/fork badges and CI status badge to README | Social proof |
| P3 | Document the `typing-extensions` conflict workaround for `pip install plato` | Damage control for wrong package installs |

---

## Summary

**PLATO's API is genuinely impressive** - fast, rich, well-structured, and the live fleet has real data (12,000+ tiles, 39 rooms, 24 agents). The concept of "raising agents" in a MUD-like world is compelling and unique.

**But the developer experience is broken at the front door.** A first-time developer following the official quickstart will:
1. Try the curl command and wait 15 seconds for nothing
2. Try `pip install plato` and break their Python environment
3. Try `cocapn --help` and get a traceback
4. Give up before ever experiencing the "aha moment" of the Harbor room

**The gap between the vision and the onboarding reality is massive.** With 3-4 critical fixes (URLs, CLI, package name, version), this could jump from a 5/10 to an 8/10 experience overnight. The underlying platform is solid - it just needs the front door to open.
