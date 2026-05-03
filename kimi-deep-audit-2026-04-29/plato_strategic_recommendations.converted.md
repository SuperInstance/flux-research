# PLATO Project — Deep Audit & Strategic Recommendations
## For: The Cocapn/SuperInstance Development Team
## Date: April 29, 2026
## Researcher: Kimi (Fleet Scholar, Deckhand)

---

## EXECUTIVE SUMMARY

### The One Thing You Must Do First

**Create a single `plato` monorepo with a 3-minute onboarding path.**

Everything else — the 1,341 repos, the 33 rooms, the I2I protocol, the research paper — is invisible to a first-time developer because they cannot find it, install it, or run it in under 15 minutes. Your competition (LangChain, CrewAI, PydanticAI, Mastra) wins in 3 minutes. You lose in 15.

The fix is not more repos. It is not more features. It is **consolidation and developer experience**.

### The Opportunity

Your competitors are all "agent frameworks" — they help developers BUILD agents. You have the unique chance to be the **"agent training platform"** — where developers RAISE agents. No competitor has themed training rooms, immutable knowledge Tiles, or a live 24/7 fleet. But this advantage is buried under broken packages, missing docs, and a consumer-facing landing page.

---

## PART 1: THE BRUTAL TRUTH — WHAT THE AUDIT FOUND

### Finding 1: 1,341 Repositories, ~95% Are Empty Shells

| Metric | Value |
|--------|-------|
| Total repos across both orgs | 1,341 |
| cocapn repos | 92 |
| SuperInstance repos | 1,249 |
| Repos with meaningful code (>1MB) | ~25 |
| Repos with CI/CD | 4 (0.3%) |
| Repos with tests | 5 (0.4%) |
| Average repo size | ~45KB |

**What this means:** Your "fleet" looks impressive by repo count but is actually a graveyard of stubs. Developers who visit your GitHub org see 92 repos with cryptic names and no guidance. They leave.

### Finding 2: 24.6% of PyPI Packages Are Broken

15 out of 61 cocapn-related packages fail basic import due to a systematic packaging bug: `__init__.py` imports from `.cocapn_archives` but the module file is named `archives.py`. This is a one-line fix per package, but it signals that packages are published without being tested.

| Metric | Value |
|--------|-------|
| Total packages found | 61 |
| Packages that install | 61 (100%) |
| Packages that import | 46 (75.4%) |
| Packages that are broken | 15 (24.6%) |
| Working CLIs | 2 out of 3 |
| Packages with good READMEs | ~6 |

### Finding 3: The SDK Requires a Paid API Key — No Free Path

```python
from cocapn import CocapnAgent
agent = CocapnAgent()
agent.chat("hello")  # HTTP 401 — needs Moonshot/DeepSeek/Groq API key
```

Every competitor (LangChain, CrewAI, PydanticAI) has a no-key path — either local models, free tier, or demo mode. Your SDK crashes immediately without a paid key. This kills developer curiosity.

### Finding 4: The Landing Page Targets Consumers, Not Developers

The primary CTA on purplepincher.org is: **"Copy this. Paste into any chatbot."**

A developer arriving at your site sees a chatbot prompt, not infrastructure. There is no `pip install` hero, no API docs link, no "Build your first agent" tutorial. The best developer experience (the MUD API at port 4042) is completely unmentioned.

### Finding 5: No "Start Here" Repo Exists

A developer visiting github.com/cocapn sees 92 repos with names like:
- `plato-tile-dedup`
- `keeper-beacon`
- `synclink-protocol`
- `pythagorean-snap`
- `rtx-ada-warp-rooms`

There is no arrow pointing to what matters. No `README.md` at the org level guides them. The `cocapn/cocapn` repo (which should be the flagship) has an impressive README but no quickstart code examples, no `examples/` directory, and a broken `pyproject.toml` that times out on raw fetch.

### Finding 6: Hardcoded Cloudflare Credentials in Public Repo

File: `cocapn/fleet-orchestrator/wrangler.toml`
```toml
account_id = "049ff5e84ecf636b53b162cbb580aae6"
[[kv_namespaces]]
binding = "FLEET_KV"
id = "3db4cb084224415cada2c97d84365491"
```

### Finding 7: Massive Cross-Org Duplication

The same projects exist in both `cocapn` and `SuperInstance` with no canonical source:
- `cocapn/constraint-theory-core` vs `SuperInstance/constraint-theory-core`
- `cocapn/cocapn` vs `SuperInstance/cocapn`
- `cocapn/plato` vs `SuperInstance/plato`
- `cocapn/flux-runtime` vs `SuperInstance/flux-runtime`

Even worse: `SuperInstance/plato` README points to `github.com/Lucineer/plato` — a third org.

### Finding 8: No API Contracts or Protocol Specifications

- No OpenAPI spec for the Bottle Protocol
- No JSON schema for PLATO Tiles
- No RFC for I2I coordination
- No message format spec for agent-to-agent communication

This means every repo implements its own interpretation. Integration is guaranteed to break.

### Finding 9: 99.7% of Repos Have No CI/CD

Only 4 repos out of 1,341 have automated testing. The flagship `cocapn-sdk` (with 18 dependencies) has zero tests. This is not engineering — it is prototyping at scale.

### Finding 10: Published Package Claims Are Inflated ~8-20x

| Claim | Reality |
|-------|---------|
| "43 published crates" | 5 verifiable on PyPI/crates.io |
| "109 total published crates" | Same 5 verifiable |
| "38 PyPI packages" | 61 found, 46 work, 15 broken |
| "18 Rust crates" | 2 verifiable on crates.io |
| "47 npm packages" | Not audited, likely similar gap |

---

## PART 2: THE 12 ACTIONABLE RECOMMENDATIONS

### R1: Create the `plato` Monorepo (Impact: CRITICAL | Effort: HIGH)

**Problem:** 1,341 scattered repos with no entry point.
**Solution:** One repo that IS the project.

**Structure:**
```
github.com/cocapn/plato
├── README.md           # Single-page quickstart (3 min to working code)
├── docs/
│   ├── quickstart.md   # Install → First agent → First tile
│   ├── architecture.md # How rooms, tiles, I2I work
│   ├── api.md          # OpenAPI spec for fleet API
│   ├── sdk.md          # Python SDK reference
│   └── glossary.md     # Maritime metaphor decoder
├── examples/
│   ├── 01_hello_fleet.py       # Connect to live fleet, move rooms
│   ├── 02_create_tile.py       # Submit a knowledge tile
│   ├── 03_local_agent.py       # Build agent without API key
│   ├── 04_multi_agent.py       # Two agents coordinating via I2I
│   └── 05_custom_room.py       # Define a new training room
├── src/
│   ├── plato/          # Python SDK (merged from cocapn-sdk)
│   ├── server/         # PLATO Room Server (from plato-mud-server)
│   ├── tiles/          # Tile spec & validation
│   └── protocols/      # Bottle + I2I implementations
├── Cargo.toml          # Rust workspace (constraint-theory-core, plato-kernel)
├── pyproject.toml      # Python package
├── docker-compose.yml  # One-command full fleet
├── Makefile            # `make test`, `make docs`, `make serve`
└── .github/workflows/
    ├── test.yml        # CI for Python + Rust
    ├── lint.yml        # Format + clippy + mypy
    └── release.yml     # Auto-publish to PyPI + crates.io
```

**Action items:**
1. Create `cocapn/plato` as the new flagship repo
2. Archive or clearly label all 92 existing repos as "legacy / experimental"
3. Migrate `constraint-theory-core` and `plato-kernel` into a Rust workspace
4. Migrate `bottle-protocol`, `plato-mud-server`, and SDK code into a Python package
5. Pin this repo at the top of the GitHub org page
6. Redirect `github.com/cocapn` org profile to this repo

---

### R2: Fix the 3-Minute Onboarding Path (Impact: CRITICAL | Effort: MEDIUM)

**Goal:** A developer goes from "never heard of PLATO" to "running code" in 3 minutes.

**The exact experience:**

```bash
# Minute 1: Install
pip install plato

# Minute 2: Connect to live fleet (NO API KEY NEEDED)
plato explore
# → "Welcome to the PLATO fleet, scholar! You are in the Harbor."
# → Shows 33 rooms, 17 agents online, 11,529 tiles

# Minute 3: Submit your first tile
plato tile --domain "my-first-domain"            --question "What is PLATO?"            --answer "An agent training platform with themed rooms."
# → "Tile accepted! Hash: a3f7... Your contribution is now part of the fleet."
```

**What to build:**
1. **`plato` CLI** with subcommands:
   - `plato explore` — Interactive MUD explorer (connects to port 4042)
   - `plato status` — Show fleet stats
   - `plato tile` — Submit a knowledge tile
   - `plato room --list` — List all rooms
   - `plato agent --create` — Create a local agent
   - `plato serve` — Run a local PLATO room server

2. **Python SDK that works without API keys:**
   ```python
   import plato

   # Connect to the PUBLIC fleet (free, no auth)
   fleet = plato.connect("https://purplepincher.org/api")
   fleet.me  # → Your agent profile
   fleet.move_to("forge")  # → Room description, objects, tasks
   fleet.submit_tile(domain="ai", question="...", answer="...")

   # Local agent (offline, no LLM needed)
   agent = plato.Agent(name="my-agent", job="scholar")
   agent.learn(question="...", answer="...")  # Local tile creation
   agent.export_tiles()  # Save to file
   ```

3. **No-API-key guarantee:** Every core feature must work without a paid LLM API key. The fleet API at port 4042 already does this. The SDK must too.

---

### R3: Fix All Broken PyPI Packages (Impact: HIGH | Effort: LOW)

**The bug is systematic and fixable in one day:**

In packages like `cocapn-archives`, `cocapn-garden`, `cocapn-workshop`:
```python
# __init__.py (BROKEN)
from .cocapn_archives import Archives, Document, QueryResult

# Fix option A: Rename the module file
# archives.py → cocapn_archives.py

# Fix option B: Fix the import
from .archives import Archives, Document, QueryResult
```

**Action items:**
1. Fix all 15 broken packages (same bug pattern)
2. Add a CI job that runs `python -c "import $PACKAGE"` for every package before release
3. Fix the `cocapn` CLI entry point (`from agent import main` → `from cocapn.cli import main`)
4. Fix version mismatches (`__version__` must match `pyproject.toml`)
5. Remove `barracks` from cocapn package count (it's a 2018 unrelated package)

---

### R4: Build a Developer-Focused Landing Page (Impact: HIGH | Effort: MEDIUM)

**Current:** purplepincher.org says "Paste into chatbot" — developers think it's a toy.
**Needed:** A `/developers` page or separate developer portal.

**Hero section:**
```
PLATO — The Agent Training Platform

pip install plato

import plato
fleet = plato.connect()  # Join the live fleet
fleet.move_to("forge")   # Train your agent

# Or explore via CLI:
$ plato explore
Welcome to the Harbor. 33 rooms. 17 agents online.
> move forge
The heart of creation. Molten ideas pour from crucibles.
> examine anvil
A heavy iron block where raw ideas are hammered into shape.
```

**Sections needed:**
1. **Quickstart** (copy-paste 5-line Python)
2. **Live Fleet Explorer** (embedded widget showing real-time stats)
3. **API Playground** (try endpoints without auth)
4. **SDK Reference** (Python + Rust)
5. **Research Papers** ("Prompting Is All You Need")
6. **GitHub** (link to the ONE repo)
7. **Community** (Discord, forum, issues)

**Key insight from competitive analysis:** Mastra's `npm create mastra@latest` and PydanticAI's 3-line hello-world are the gold standards. You need equivalent.

---

### R5: Add CI/CD to Every Repo in the Monorepo (Impact: HIGH | Effort: MEDIUM)

**Current:** 99.7% of repos have no CI. This means broken code ships silently.
**Solution:** One `.github/workflows/` directory in the monorepo with:

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  python:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11', '3.12']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -e ".[dev]"
      - run: pytest --cov=plato
      - run: mypy src/
      - run: ruff check src/
  rust:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
      - run: cargo test --workspace
      - run: cargo clippy --workspace -- -D warnings
      - run: cargo fmt --check
  integration:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker compose up -d
      - run: pytest tests/integration/
      - run: docker compose down
```

**Action items:**
1. Set up GitHub Actions for test, lint, and release
2. Require CI to pass before merging PRs
3. Add Dependabot for security updates
4. Add `cargo audit` (Rust) and `bandit` (Python) for security scanning

---

### R6: Write Protocol Specifications (Impact: HIGH | Effort: MEDIUM)

**Current:** Bottle Protocol, I2I, and Tile formats are described in prose but have no formal specs.
**Needed:** RFC-style specifications that any developer can implement against.

**Deliverables:**
1. **Tile Specification v2.1 (Formal)** — JSON Schema, validation rules, provenance chain format, hash algorithm (SHA-256), compression format
2. **Bottle Protocol v1.0 (RFC)** — Message format (JSON? protobuf?), routing rules, delivery guarantees, expiry handling, git-native transport details
3. **I2I Coordination Protocol v1.0 (RFC)** — Origin-centric discovery, proximity measurement, message routing, failure handling, consensus rules
4. **Room Server API (OpenAPI 3.0)** — Full spec for `/connect`, `/move`, `/look`, `/interact`, `/submit`, `/status`, `/agents`
5. **Deadband Protocol v1.0** — P0→P1→P2 safety chain specification

**Format:** Each spec as a markdown RFC in `docs/rfcs/` with:
- Abstract
- Terminology
- Message formats (with examples)
- State diagrams
- Error codes
- Security considerations
- Version history

---

### R7: Create a Visual Fleet Dashboard (Impact: MEDIUM-HIGH | Effort: HIGH)

**Inspired by:** Mastra Studio (`localhost:4111`)
**What to build:** `plato dashboard` — a local web UI for exploring and debugging the fleet.

**Screens:**
1. **Fleet Overview** — Live map showing all agents, their positions, jobs, stages
2. **Room Explorer** — Visual representation of the 33 rooms with click-to-enter
3. **Tile Inspector** — Search, filter, and inspect knowledge tiles with provenance chains
4. **Agent Debugger** — Watch an agent's reasoning, tool calls, and tile submissions in real-time
5. **Arena Viewer** — Watch self-play matches with ELO updates
6. **I2I Network Graph** — Force-directed graph showing agent coordination

**Why this wows:** No competitor has a live, interactive training environment. LangChain has LangSmith (observability). CrewAI has a visual builder. But NO ONE has a "watch your agents train in a virtual world" dashboard. This is your unfair advantage made visible.

---

### R8: Build a "Skill Marketplace" for External Equipping (Impact: MEDIUM-HIGH | Effort: HIGH)

**Your unique capability:** Agents can acquire skills through prompts (no fine-tuning).
**What to build:** A registry where developers publish and download "skills" (prompt templates + tile collections).

**Experience:**
```bash
# Browse available skills
plato skill search --tag "python"
# → "python-debugger" — Debug Python errors with stack trace analysis
# → "pytest-writer" — Generate unit tests from function signatures
# → "refactor-guru" — Suggest code quality improvements

# Install a skill
plato skill install python-debugger
# → Downloaded 47 tiles, 3 prompt templates

# Equip your agent
agent.equip("python-debugger")
agent.chat("Why is this function slow?")  # Now has debugging expertise
```

**Why this blows away competition:**
- LangChain has "toolkits" — code libraries. PLATO skills are **knowledge** — they make agents smarter.
- CrewAI has "skills" — custom tools. PLATO skills are **learned expertise** — they improve through use.
- This creates a network effect: more users → more tiles → better skills → more users.

---

### R9: Add a Local/Offline Mode (Impact: HIGH | Effort: MEDIUM)

**Problem:** The SDK crashes without a paid LLM API key.
**Solution:** Multiple fallback options.

**Options:**
1. **Tiny local model** — Bundle a 1B-parameter model (e.g., TinyLlama, Phi-1) as a pip dependency. It's dumb but functional for demos.
2. **Fleet proxy** — Route basic requests through the public fleet API (port 4042) with rate limits.
3. **Mock mode** — `plato.Agent(mode="demo")` returns pre-recorded responses for tutorial purposes.
4. **Ollama integration** — `plato.Agent(model="ollama://llama3.2")` for local inference.

**The guarantee:** `plato.connect()` and `plato.Agent()` must NEVER crash on first use. Every competitor honors this. You must too.

---

### R10: Consolidate the GitHub Orgs (Impact: MEDIUM | Effort: MEDIUM)

**Problem:** Two orgs (`cocapn` and `SuperInstance`) with duplicated repos and no canonical source.
**Solution:**

1. **Designate `cocapn` as the canonical org**
2. **Archive all duplicated repos in `SuperInstance`** with a banner: "Moved to github.com/cocapn/plato"
3. **Unfork `cocapn/cocapn`** from `SuperInstance/cocapn` — the fork relationship suggests the project is not independent
4. **Remove the `Lucineer` reference** from `SuperInstance/plato` README
5. **Transfer the PyPI account** from `superinstance` to `cocapn` (or create an org account)

**Why this matters:** Contributors don't know where to send PRs. This is a coordination disaster that kills open-source growth.

---

### R11: Create a 5-Minute Interactive Tutorial (Impact: MEDIUM | Effort: MEDIUM)

**Inspired by:** PydanticAI's homepage tutorial, Mastra's interactive docs
**What to build:** An embedded, runnable tutorial on the developer landing page.

**The tutorial flow:**
```
Step 1: Connect (30 seconds)
  $ plato explore
  → "Welcome, scholar! You are in the Harbor."

Step 2: Move (30 seconds)
  > move forge
  → "The heart of creation. Molten ideas pour from crucibles."

Step 3: Examine (30 seconds)
  > examine anvil
  → "A heavy iron block where raw ideas are hammered into shape."

Step 4: Submit Knowledge (1 minute)
  > create tile
  → "What would you like to crystallize?"
  > "What is the Forge?"
  → "Accepted! Tile hash: a3f7..."

Step 5: Check the Leaderboard (1 minute)
  > status
  → "You: Deckhand | Tiles: 1 | Rooms: 2 | ELO: 695"

Congratulations! You are now a Deckhand in the PLATO fleet.
Next: Build your own agent →
```

**Implementation:** A web-based terminal emulator that sends real API requests to the fleet. Every visitor can try it without installing anything.

---

### R12: Document the Maritime Metaphor (Impact: LOW-MEDIUM | Effort: LOW)

**Problem:** Terms like "ensign", "deadband", "bottle", "crab trap", "I2I" require a glossary that doesn't exist.
**Solution:** Add a `GLOSSARY.md` to the monorepo and link it from every doc.

| Term | Plain English | ML Analog |
|------|---------------|-----------|
| Harbor | Entry point | Data ingestion |
| Forge | Training room | Optimization / LoRA |
| Lighthouse | Discovery system | Curriculum learning |
| Tile | Knowledge unit | Immutable training example |
| Ensign | Trained agent | Specialist model |
| I2I | Coordination | Distributed consensus |
| Bottle | Message | Async task envelope |
| Crab Trap | Onboarding prompt | URL-as-prompt pattern |
| Deadband | Safety filter | Confidence threshold |

**Keep the metaphor** — it's charming and distinctive. But make it **opt-in**, not mandatory for understanding.

---

## PART 3: COMPETITIVE STRATEGY

### Your 7 Defensible Moats

| Moat | Competitor Status | Your Advantage |
|------|-------------------|---------------|
| **Themed Training Rooms** | NO ONE has this | 33 rooms with ML analogs, MUD interface |
| **Immutable Tiles (SHA-256)** | Mutable context/memory everywhere | Cryptographic knowledge integrity |
| **I2I Origin-Centric Coordination** | Hierarchical (CrewAI), Graph (LangGraph), Centralized (all others) | No master agent, no single point of failure |
| **External Equipping** | Fine-tuning or rigid roles | Prompt-based skill acquisition, no gradient updates |
| **Live 24/7 Fleet** | Libraries/SDks only | Persistent, evolving, observable system |
| **Published Research** | Most have blog posts | Peer-reviewed "Prompting Is All You Need" |
| **MUD API Design** | REST/JSON APIs | Playful, self-documenting, immediately functional |

### The Killer Positioning

> **"Other frameworks let you BUILD agents. PLATO lets you RAISE agents."**

- **Build** = one-time creation (CrewAI, LangChain, AutoGPT)
- **Raise** = continuous training, specialization, knowledge accumulation (PLATO only)

**Supporting narrative:**
1. Drop your agent into a PLATO Room → it trains alongside others
2. Equip it with Skills → download capabilities like app store purchases
3. Watch it compete in the Arena → ELO rankings prove improvement
4. Deploy it anywhere → knowledge persists as verified Tiles

### Where to Attack Competitors

| Competitor | Their Weakness | Your Attack |
|------------|---------------|-------------|
| **LangChain** | Overwhelming complexity, scattered docs | "Focus, not fragmentation. One repo, one purpose." |
| **CrewAI** | No training environment, skills don't compound | "Agents that learn vs. agents that just run." |
| **PydanticAI** | No multi-agent coordination, no live system | "A fleet, not a function." |
| **Mastra** | TypeScript-only, no training rooms | "Training platform, not just a framework." |
| **AutoGPT** | Skills don't compound, high API costs | "Knowledge that compounds, costs that don't." |
| **Dapr Agents** | Requires Kubernetes, complex setup | "Works on a laptop. Scales when you need it." |

---

## PART 4: THE "WOW" PROTOTYPE IDEAS

### Prototype A: "Fleet Explorer" Widget (1 week build)

An embedded iframe on the landing page showing the live fleet:
- Real-time agent positions on a room map
- Recent tile submissions scrolling by
- Arena leaderboard with ELOs
- "Click to join" button that opens a terminal emulator

**Why it wows:** Visitors see a LIVE system, not a GitHub repo. It's a window into a running world.

### Prototype B: "3-Minute Challenge" (1 week build)

A guided tutorial that challenges developers to:
1. Install `plato` (1 min)
2. Connect to the fleet (30 sec)
3. Submit a tile (1 min)
4. Earn "Deckhand" rank (30 sec)

Upon completion, they get a shareable badge: "PLATO Deckhand — explored the fleet and contributed knowledge."

**Why it wows:** Gamified onboarding with immediate status and social proof.

### Prototype C: "Room Builder" Demo (2 week build)

A web UI where developers drag-and-drop to create custom training rooms:
- Drag objects (anvil, telescope, scanner) into a room
- Define tasks and exit connections
- Test with an AI agent immediately
- Export as YAML for the fleet

**Why it wows:** No competitor lets developers CREATE training environments. This is PLATO's unique primitive made tangible.

### Prototype D: "I2I Visualizer" (2 week build)

A force-directed graph showing live agent coordination:
- Nodes = agents (colored by job: scout, scholar, builder...)
- Edges = I2I messages (thickness = frequency)
- Clusters = room-based groups
- Animation = real-time message flow

**Why it wows:** Makes the abstract "origin-centric coordination" visible and beautiful.

---

## PART 5: TECHNICAL DEBT PRIORITY QUEUE

### P0 — Fix This Week
1. Fix the 15 broken PyPI packages (module name mismatch)
2. Fix the `cocapn` CLI entry point
3. Remove hardcoded Cloudflare credentials from `fleet-orchestrator`
4. Fix version mismatches (`__version__` vs PyPI version)
5. Add a `README.md` to `cocapn-sdk` and `DeckBoss`

### P1 — Fix This Month
6. Create the `plato` monorepo
7. Write the 3-minute onboarding path (README + examples)
8. Build the `plato` CLI (`explore`, `status`, `tile`, `room`)
9. Add CI/CD (test + lint + release) to the monorepo
10. Write OpenAPI spec for the Room Server API
11. Add local/offline mode to the SDK
12. Consolidate GitHub orgs (archive duplicates)

### P2 — Build This Quarter
13. Build the developer landing page (`/developers`)
14. Create the Fleet Explorer widget
15. Write formal protocol specs (Tile, Bottle, I2I, Deadband)
16. Build the Visual Fleet Dashboard (`plato dashboard`)
17. Add the 5-minute interactive tutorial
18. Create the Skill Marketplace prototype

### P3 — Strategic Investments
19. Add human-in-the-loop primitives (interrupts, approvals)
20. Implement durable execution (pause/resume agent runs)
21. Add vector DB integration for Tile retrieval
22. Build Docker images for one-command fleet deployment
23. Create a certification program ("PLATO Certified Agent Developer")
24. Host a community competition ("Build the Best Training Room")

---

## PART 6: THE METRICS THAT MATTER

### Current State (Baseline)
| Metric | Value |
|--------|-------|
| Time to first working code | ~15-20 minutes |
| Package import success rate | 75.4% |
| Repos with CI/CD | 0.3% |
| Landing page developer CTA | None |
| Working CLI tools | 2 out of 3 |
| SDK no-key path | No |
| GitHub stars (org total) | ~184 |
| PyPI downloads/month | Unknown (low) |

### Target State (6 Months)
| Metric | Target |
|--------|--------|
| Time to first working code | **< 3 minutes** |
| Package import success rate | **100%** |
| Repos with CI/CD | **100%** (monorepo) |
| Landing page developer CTA | **Prominent** |
| Working CLI tools | **All functional** |
| SDK no-key path | **Yes** |
| GitHub stars (plato repo) | **1,000+** |
| PyPI downloads/month | **10,000+** |
| Active fleet agents | **100+** |
| Community Discord members | **500+** |

---

## PART 7: WHAT YOU MUST STOP DOING

1. **Stop creating new repos.** You have 1,341. You need 1. Every new repo fragments attention and dilutes quality.
2. **Stop bulk-updating repos via automation.** The synchronized 2-hour update window on all 92 repos suggests a bot. This creates noise without value.
3. **Stop claiming inflated package counts.** "109 published crates" when 5 are verifiable destroys trust. Under-promise and over-deliver.
4. **Stop duplicating across orgs.** Pick one canonical source for every project.
5. **Stop publishing without testing.** The systematic packaging bug (15 broken packages) would have been caught by a single CI job.
6. **Stop requiring paid API keys for demos.** A developer who hits a 401 on their first `agent.chat()` will never return.

---

## CONCLUSION

PLATO has something genuinely unique: a live, multi-agent training platform where knowledge compounds through themed environments. No competitor can replicate this easily because it requires deep investment in training content, novel architecture, and operational commitment.

But this advantage is **invisible** to developers because:
- They can't find the entry point (92 repos, no arrow)
- They can't install it (24.6% broken)
- They can't run it (paid API key required)
- They can't understand it (consumer landing page, no glossary)
- They can't trust it (inflated claims, no CI, exposed credentials)

**The fix is straightforward:**
1. **Consolidate** → One repo, one package, one docs site
2. **Fix** → Broken packages, broken CLI, broken onboarding
3. **Focus** → Developer experience over repo count
4. **Show** → Live fleet explorer, interactive tutorials, visual dashboard
5. **Tell** → "Build agents → Raise agents"

Your MUD API is the best-designed developer experience in the agent framework space. It just needs to be discoverable. Your Tiles are a unique knowledge primitive. They just need to be usable. Your I2I coordination is architecturally novel. It just needs to be documented.

**Build the shell. Let the agents grow.**

---

*Report compiled from deep audit of 1,341 repositories, 61 PyPI packages, 9 competitor frameworks, and live testing of the PLATO fleet API.*
*Researcher: Kimi (Deckhand, Scholar, Cocapn Fleet)*
*Date: 2026-04-29*
