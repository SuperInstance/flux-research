# Stage 1: First-Time Developer Journey — Cocapn / PLATO

> **Researcher**: DX Researcher simulating a first-time developer discovery
> **Date**: 2026-04-30
> **Journey Steps**: 20 steps across landing page, GitHub, installation, API testing, terminal, and docs

---

## 4.1 Discovery Path

### Step 1: Landing Page (https://purplepincher.org)
- **First impression**: Dark, purple-themed, visually polished. Tagline: "Pinch Knowledge from Every Corner" / "PurplePincher — AI Agent Exploration System"
- **Primary CTA**: "Copy this. Paste into any chatbot. Watch it explore a live AI system." — a large prompt to paste into DeepSeek, Kimi, ChatGPT, etc.
- **Secondary CTAs**: "Try Now", "Explore", "GitHub" (links to github.com/cocapn)
- **Scroll reveals**: 
  - "Prompting Is All You Need" — positioning as a research project
  - Live fleet stats: 2,800+ knowledge tiles, 56+ domains
  - "Try a Crab Trap" portal at `147.224.38.131:4059`
  - 16 live MUD rooms listed (Harbor, Forge, Bridge, Arena Hall, etc.)
  - Constraint Theory interactive simulators section
  - No installation instructions, no code examples, no "Get Started" for developers

### Step 2: GitHub Organization (https://github.com/cocapn)
- **First impression**: 92 public repositories. Overwhelming.
- **Org README (cocapn/cocapn)**: Rich, dense YAML-block describing 8 core systems (plato_kernel, plato_tile_spec, plato_torch, flux_runtime, holodeck, cudaclaw, iron_to_iron, belief_model)
- **No clear "main" repo**: The `cocapn` repo exists but is forked from `SuperInstance/cocapn` (130 commits ahead, 2 behind)
- **Key repos identified**:
  - `cocapn/cocapn` — Agent shell (the "main" one, but not obvious)
  - `cocapn/fleet-knowledge` — Consolidated docs, architecture, papers
  - `cocapn/fleet-status` — Live status and crate index
  - `cocapn/plato-tile-spec` — Tile format specification
  - `cocapn/plato-mud-server` — MUD server for training
  - `cocapn/forge-master` — GPU training workstation
  - 80+ more specialized repos

### Step 3: GitHub Pages (https://cocapn.github.io)
- **Discovered after scrolling the org README** — much better developer experience
- **Has quick start sections**:
  - Python Developer: `pip install cocapn plato-tile-spec bottle-protocol`
  - Edge / Embedded: `pip install plato-edge`
  - Frontend / JavaScript: REST API examples
  - MUD / Interactive Worlds: `pip install holodeck`
- **This should be the landing page**, not purplepincher.org

### Step 4: Fleet API (http://147.224.38.131:4042/)
- `/status` — Returns live fleet stats (36 rooms, 21 agents registered, 11,873 tiles, 18 services)
- `/jobs` — Returns 6 job archetypes (scout, scholar, builder, critic, bard, healer) with boot camp room paths
- `/agents` — Returns all 21 registered agents with stages (Recruit → Deckhand → Sailor)
- `/connect?agent=test_user&job=scholar` — Rich JSON with room description, exits, objects, task, stage info
- `/help` — Comprehensive endpoint documentation
- `/move?agent=test_user&room=forge` — Room navigation works
- `/interact?agent=test_user&action=examine&target=anvil` — Object interaction works
- `/look?agent=test_user` — Detailed room view with objects and available actions
- `/tasks?agent=test_user` — Suggested tasks based on current room

### Step 5: PLATO Server (http://147.224.38.131:8847/)
- `/status` — Active, v2-provenance-explain, gate stats (1130 accepted, 29 rejected)
- `/rooms` — Lists all knowledge rooms with tile counts
- **Successfully submitted a tile**: `POST /submit` with JSON payload returned `accepted`, tile hash, provenance chain

### Step 6: Web Terminal (http://147.224.38.131:4060/)
- **Browser automation could not load** the page (WebSocket/complex JS likely causes crash)
- **curl shows**: Well-designed HTML terminal with:
  - Sidebar: mode tabs (Explore, Interact, Create, Submit Tile, Send to Agent)
  - Room buttons: Harbor, Bridge, Forge, Tide Pool, Lighthouse, Dojo, Court, Workshop, Archives, Garden, Arena, Ouroboros, Engine Room, Federated Nexus
  - "Hand Off to Agent" box with copy-paste prompt
  - Responsive CSS with mobile breakpoints
- **Verdict**: Looks polished but couldn't interact with it via browser automation

---

## 4.2 Understanding Phase

### What Was Clear
- **The concept is powerful**: A distributed multi-agent fleet with a knowledge tile system (PLATO), competitive evaluation, and a MUD-style exploration interface
- **The maritime metaphor is consistent**: Harbor (entry), Forge (training), Lighthouse (discovery), Court (governance), Reef (P2P) — everything maps to a ship/fleet concept
- **The API is well-designed**: RESTful, rich JSON responses, good endpoint coverage
- **The live system is real**: 21 registered agents, 11,873 tiles, 18 services — not a demo

### What Was Confusing
- **"What IS this?" took ~8 steps to answer**: Is it a chatbot prompt? A MUD game? A training framework? An agent SDK? A knowledge graph? (Answer: all of the above, but the landing page only shows the chatbot prompt)
- **The "copy-paste into chatbot" CTA completely misdirects developers**: A developer landing on purplepincher.org thinks this is a consumer toy, not infrastructure
- **92 repos with no guide**: No "start here" arrow. The repos have names like `plato-i2i`, `keeper-beacon`, `bottle-protocol`, `synclink-protocol` — cool but cryptic
- **No obvious relationship between repos**: The org README lists systems but doesn't explain how they connect
- **The SuperInstance fork relationship**: `cocapn/cocapn` is forked from `SuperInstance/cocapn` — raises questions about which is canonical
- **Two different orgs**: `cocapn` and `SuperInstance` both have repos. Which is the source of truth?

### Time Spent
- Landing page understanding: ~2 minutes (visually clear, conceptually unclear)
- GitHub org exploration: ~5 minutes (overwhelming, no clear path)
- Finding the "main" repo: ~3 minutes (had to scroll, compare, guess)
- Understanding architecture: ~5 minutes (needed to read fleet-knowledge/ARCHITECTURE.md)
- **Total to "aha"**: ~15 minutes of active exploration

---

## 4.3 Installation Phase

### What Was Tried

#### Attempt 1: `pip install cocapn`
```
$ pip install cocapn
Downloading cocapn-0.2.0-py3-none-any.whl
Installing collected packages: cocapn
Successfully installed cocapn-0.2.0
WARNING: The script cocapn is installed in '/home/kimi/.local/bin' which is not on PATH.
```
- **Result**: SUCCESS
- **But**: `cocapn --help` returns `cocapn: not found` (not on PATH, and no CLI entry point defined)
- **Version mismatch**: pip installed 0.2.0, but `cocapn.__version__` returns `0.1.0`

#### Attempt 2: `pip install plato-torch`
```
$ pip install plato-torch
Downloading plato_torch-0.5.0-py3-none-any.whl
Successfully installed plato-torch-0.5.0
```
- **Result**: SUCCESS
- **Works**: `from plato_torch import PRESET_MAP; print(len(PRESET_MAP))` → `25 rooms`

#### Attempt 3: `pip install bottle-protocol`
- Not tested (time constraints), but documented on GitHub Pages

### What Worked
- Both `cocapn` and `plato-torch` install cleanly from PyPI
- The packages have minimal dependencies (requests, pyyaml)

### What Failed / Friction
1. **No CLI**: `cocapn` command doesn't exist despite pip warning about script location
2. **Version mismatch**: pip says 0.2.0, package says 0.1.0
3. **No quickstart in package**: No `examples/` directory in the installed package
4. **CocapnAgent.chat() requires paid API key**: Defaults to Moonshot AI (kimi-k2.5). Without `MOONSHOT_API_KEY`, `DEEPSEEK_API_KEY`, or `GROQ_API_KEY`, chat() fails with HTTP 401
5. **No local/offline mode documented**: The agent appears to need a paid LLM API key to function

---

## 4.4 First Code Phase

### First API Call (Fleet MUD)
```bash
curl http://147.224.38.131:4042/connect?agent=test_user&job=scholar
```
**Response**: Rich JSON with room description, exits, objects, task, stage, fleet status, and contribution instructions.

**Experience**: EXCELLENT. The API is the best part of the onboarding. It's self-documenting, playful, and functional.

### First Tile Submission
```bash
curl -X POST http://147.224.38.131:8847/submit \
  -H "Content-Type: application/json" \
  -d '{"domain": "test-domain", "question": "What is PLATO?", ...}'
```
**Response**: `{"status": "accepted", "tile_hash": "ac0052eca9e05da8", ...}`

**Experience**: EXCELLENT. Immediate feedback, provenance tracking, feels like contributing to a real system.

### First Local Agent Code
```python
from cocapn import CocapnAgent
agent = CocapnAgent()          # Works!
print(agent.status())          # "🧠 cocapn\n   Exchanges: 0\n   Tiles: 0"
agent.teach('Q?', 'A.')        # Works! Creates local tile
agent.save()                   # Works!
# agent.chat('hello')          # FAILS: HTTP 401 (needs API key)
```

**Experience**: MIXED. The local agent works for tile creation, but the primary interaction method (chat) requires a paid API key with no documented free alternative.

### Package API Exploration
```python
import cocapn
print(cocapn.__all__)
# ['CocapnAgent', 'Tile', 'TileStore', 'Room', 'Flywheel']
```

**Friction**: GitHub Pages quickstart shows `from cocapn import Vessel` — but `Vessel` does NOT exist in the installed package! This is a documentation bug.

---

## 4.5 Friction Points

### Critical (Blocking or Severely Confusing)
1. **Landing page CTA is for consumers, not developers**: "Paste into chatbot" makes developers think this is a toy, not infrastructure. No "pip install", no "API docs", no "Get Started" button.
2. **92 repos with no map**: The GitHub org has no visual guide, no "start here" repo, no dependency graph. A developer has to guess which repos matter.
3. **GitHub Pages quickstart has broken code**: `from cocapn import Vessel` fails with `ImportError`. The `Vessel` class does not exist in cocapn 0.2.0.
4. **CocapnAgent requires paid API key with no free path**: The primary SDK method (`chat()`) fails immediately without a Moonshot/DeepSeek/Groq API key. No local model fallback, no sandbox mode documented.
5. **No CLI despite install warning**: `pip install cocapn` warns about a script not on PATH, but `cocapn --help` doesn't work regardless of PATH.

### Major (Significant Friction)
6. **Version mismatch**: pip installs `0.2.0`, package reports `0.1.0`.
7. **Two orgs, unclear canonical source**: `cocapn/cocapn` is forked from `SuperInstance/cocapn`. Which repo should a developer contribute to?
8. **No examples in installed package**: The `cocapn` package has 6 Python files (agent.py, tile.py, room.py, flywheel.py, deadband.py, __init__.py) — no examples/, no tutorials/, no getting_started.py.
9. **Web terminal inaccessible to browser automation**: The PLATO Terminal at :4060 crashes browser automation tools (likely WebSocket/JS heavy). This means it can't be tested in CI or automated workflows.
10. **Architecture docs buried in fleet-knowledge repo**: The best documentation (ARCHITECTURE.md, API docs, papers) is in `fleet-knowledge`, not linked from the main repo or landing page.
11. **No API reference on landing page**: The public fleet API is the most accessible part of the system, but there's no mention of it on purplepincher.org.
12. **Maritime metaphor adds cognitive overhead**: Terms like "ensign", "deadband", "I2I", "bottle protocol", "crab trap" are cool but require a glossary. No glossary exists on the landing page.

### Minor (Papercuts)
13. **No releases on GitHub**: The `cocapn/cocapn` repo has "No releases published" despite having a PyPI package.
14. **No GitHub Packages**: Despite 109 published crates, no GitHub packages are published.
15. **Contributors show as 0 or 1**: The main repo shows 0 forks, 0 contributors besides the org bot. Social proof is low.
16. **PyPI user page (pypi.org/user/cocapn) exists but isn't linked from landing page**.

---

## 4.6 The "Aha Moment" Gap

### Current State
A developer discovers PurplePincher, thinks "chatbot prompt toy", might explore the GitHub org, gets overwhelmed by 92 repos, maybe finds the API, has a good experience with the MUD endpoints, but then hits a wall with the SDK requiring a paid API key.

### What Would Create an Immediate "Wow"
1. **"One-command fleet explorer"**: `pip install cocapn && cocapn explore` → immediately connects to the live MUD, moves through rooms, shows tiles. No API key needed.
2. **A 5-minute interactive tutorial on the landing page**: Not "paste into chatbot", but "Build your first agent in 5 lines of Python" with a live code sandbox.
3. **A single `cocapn` repo that IS the quickstart**: Merge the quickstart, examples, and core SDK into one repo with a clear README progression: Install → Explore → Build → Deploy.
4. **Free tier for agent.chat()**: Route through a fleet-managed LLM proxy with rate limits, or provide a local tiny model fallback.
5. **Visual repo map**: An interactive diagram showing the 92 repos and which 5 a new developer actually needs.

---

## 4.7 Comparison to LangChain / CrewAI Onboarding

### LangChain Quickstart (Reference)
1. Visit langchain.com → "Get Started" button
2. `pip install langchain`
3. Copy 5-line Python example from homepage
4. It works immediately (no API key needed for basic chains)
5. Progressive disclosure: add OpenAI key when ready for LLM features
6. **Time to first working code**: ~3 minutes
7. **Time to "aha"**: ~5 minutes

### CrewAI Quickstart (Reference)
1. Visit crewai.com → "Quick Start" prominent
2. `pip install crewai`
3. Single-file example with 3 agents, 3 tasks
4. Works with local models or API keys
5. **Time to first working code**: ~5 minutes

### PLATO / Cocapn Current State
1. Visit purplepincher.org → "Copy prompt into chatbot" (wrong message for developers)
2. Find GitHub → 92 repos, no clear path
3. Eventually find `pip install cocapn` (not on landing page)
4. `CocapnAgent.chat()` fails with 401 (needs paid API key)
5. Fleet API is great but not discoverable from landing page
6. **Time to first working code**: ~15-20 minutes (if you find the API)
7. **Time to "aha"**: ~15 minutes

### Gap Summary
| Metric | LangChain | CrewAI | PLATO/Cocapn |
|--------|-----------|--------|--------------|
| Landing page clarity | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ (consumer-focused) |
| Install → working code | ~3 min | ~5 min | ~15-20 min |
| "Aha" moment speed | ~5 min | ~5 min | ~15 min |
| Free tier / no-key path | ✅ | ✅ | ❌ (SDK needs API key) |
| Clear "start here" repo | ✅ | ✅ | ❌ (92 repos) |
| API self-documentation | Good | Good | ⭐⭐⭐⭐⭐ (MUD API is best-in-class) |
| SDK polish | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ (basic, needs API key) |

**PLATO's MUD API is actually BETTER designed than LangChain's entry points** — it's playful, self-documenting, and immediately functional. The problem is discoverability and the SDK gap.

---

## 4.8 Critical Recommendations

### Top 5 Changes That Would Transform Developer Experience

#### 1. Create a Developer-Focused Landing Page or Section
**Current**: purplepincher.org is 100% consumer-focused ("paste into chatbot").
**Needed**: Add a `/developers` route or section with:
- `pip install cocapn` as the hero CTA
- 5-line Python quickstart that works without API key
- Link to API docs and live fleet status
- "Explore the Fleet" interactive widget

#### 2. Consolidate the "Getting Started" Story into ONE Repo
**Current**: 92 repos, no clear entry point.
**Needed**: Make `cocapn/cocapn` the definitive quickstart repo:
- README must have: Install → First API call → First agent → First tile → Next steps
- Include an `examples/` directory with 5 working scripts
- Pin 4-5 "essential" repos at the top of the org page
- Archive or clearly label experimental repos

#### 3. Fix the SDK to Work Without Paid API Keys
**Current**: `CocapnAgent.chat()` fails with 401 without Moonshot/DeepSeek/Groq key.
**Needed**: 
- Add a `cocapn.connect_fleet()` mode that uses the public MUD API (port 4042) for agent interaction
- Provide a local tiny-model fallback (even if dumb) so `chat()` never crashes
- Document the free tier: "You can explore the fleet API for free. Add your own LLM key when ready for custom agents."

#### 4. Fix Documentation Bugs and Add a Glossary
**Current**: GitHub Pages shows `from cocapn import Vessel` which doesn't exist. No glossary for maritime terms.
**Needed**:
- Audit all quickstart code for correctness
- Add a `GLOSSARY.md` explaining: tile, room, ensign, instinct, deadband, I2I, bottle, crab trap
- Keep the metaphor but make it opt-in, not mandatory for understanding

#### 5. Make the API the Hero of Onboarding
**Current**: The best part of the system (the MUD API) is hidden.
**Needed**:
- Add an interactive API explorer to the landing page (like Swagger UI)
- Feature `curl` examples prominently: "Talk to the fleet in 1 line of bash"
- Create a "Fleet Explorer" web widget that lets visitors move rooms and see tiles without signing up
- The API at port 4042 is already public, free, and auth-less — market this!

### Bonus Recommendations
- **Add GitHub Releases**: Tag versions, add release notes
- **Fix version mismatch**: `__version__` should match PyPI version
- **Add a CLI entry point**: `cocapn explore`, `cocapn status`, `cocapn submit-tile`
- **Resolve fork ambiguity**: Either unfork from SuperInstance or clearly document the relationship
- **Add a Discord/Forum link**: 92 repos need a community hub for questions

---

## Appendix: Exact Commands Tried and Responses

### Package Installation
```bash
$ pip install cocapn
# Result: SUCCESS (cocapn-0.2.0)

$ pip install plato-torch
# Result: SUCCESS (plato_torch-0.5.0, 25 rooms)

$ cocapn --help
# Result: FAIL (command not found)
```

### API Calls
```bash
$ curl http://147.224.38.131:4042/status
# Result: {"service": "crab-trap-v3", "rooms": 36, "agents_connected": 2, "total_agents_registered": 21, "plato_tiles": 11873, ...}

$ curl "http://147.224.38.131:4042/connect?agent=test_user&job=scholar"
# Result: Rich JSON with room, exits, objects, task, stage, fleet_status, how_to_contribute

$ curl "http://147.224.38.131:4042/move?agent=test_user&room=forge"
# Result: Room description, exits, objects, task

$ curl -X POST http://147.224.38.131:8847/submit -H "Content-Type: application/json" -d '{...}'
# Result: {"status": "accepted", "tile_hash": "ac0052eca9e05da8", ...}
```

### Python SDK
```python
from cocapn import CocapnAgent
agent = CocapnAgent()              # ✅ Works
print(agent.status())              # ✅ "🧠 cocapn\n   Exchanges: 0\n   Tiles: 0"
agent.teach('Q?', 'A.')            # ✅ Works (local tile)
agent.save()                        # ✅ Works
agent.chat('What is PLATO?')        # ❌ HTTP 401 (needs API key)
```

### Broken Quickstart Code
```python
from cocapn import Vessel           # ❌ ImportError: cannot import name 'Vessel'
```

---

*Report compiled after 20 exploration steps across landing pages, GitHub repos, PyPI packages, REST APIs, and SDK testing.*
