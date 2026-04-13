**The Skiff System** — A git-based skill rigging framework for AI agents.

---

## 1. File & Folder Structure

```bash
~/.skiff/                      # The boatyard
├── config.yaml                # Agent identity, git credentials, registries
├── manifest.yaml              # Current deck loadout (what's HOT)
├── logs/
│   └── rig-history.yaml       # Audit trail for rollbacks
├── harbor/                    # WARM state — cloned repos, ready to mount
│   ├── github.com/
│   │   ├── fleet/
│   │   │   ├── fishing/       # Skill repository
│   │   │   │   ├── .git/
│   │   │   │   ├── SKILL.md   # Skill manifest (required)
│   │   │   │   ├── rig.py     # Activation hook (required)
│   │   │   │   ├── derig.py   # Deactivation hook (optional)
│   │   │   │   ├── src/       # Skill code
│   │   │   │   ├── tools/     # Binaries/executables
│   │   │   │   └── knowledge/ # RAG documents
│   │   │   └── navigation/
│   │   └── captain-joe/
│   │       └── weather/
│   └── local/
│       └── custom-skills/
├── deck/                      # HOT state — active symlinks
│   ├── fishing -> ../harbor/github.com/fleet/fishing/
│   └── navigation -> ../harbor/github.com/fleet/navigation/
├── locker/                    # COLD state — git bundles, compressed
│   ├── fishing-v1.2.0.bundle
│   ├── fishing-v1.1.5.bundle.gz
│   └── manifest.locker        # Index of archived versions
└── cache/                     # Compiled artifacts (embeddings, .pyc)
    └── fishing/
        ├── embeddings/
        └── compiled_tools/
```

---

## 2. SKILL.md Specification

Every skill is a git repository containing a `SKILL.md` at its root.

```yaml
# SKILL.md
metadata:
  id: fleet/fishing            # Unique identifier (org/skill)
  name: fishing                # Human readable
  version: 1.2.3
  description: "Deep sea fishing operations with sonar and tackle"
  author: "captain@fleet.ai"
  license: MIT

runtime:
  engine: python3.11           # python3.11 | node20 | binary
  entry: rig.py                # Executed on RIG (equip)
  exit: derig.py               # Executed on DERIG (unequip)
  timeout: 30s                 # Max seconds for rig.py to return

dependencies:
  skills:                      # Other skills required
    - id: fleet/navigation
      version: "^2.0.0"        # Semver range
      import_as: nav           # Namespace alias
      state: hot               # Required state in deck (hot|warm)
    - id: fleet/weather
      version: ">=1.0.0"
      optional: true           # Soft dependency
  
  tools:                       # External binaries
    - name: sonar-cli
      source: 
        git: https://github.com/fleet/sonar.git
        tag: v1.0.0
  
  packages:                    # Language-specific
    python:
      - requests>=2.28.0
      - numpy

resources:
  memory_mb: 512               # Estimated RAM for hot state
  disk_mb: 100                 # Harbor storage requirement
  gpu: false

knowledge:
  - path: docs/fish-species.md
    format: markdown
    auto_embed: true           # Load into vector DB on rig
    chunk_size: 512
  - path: data/tides.json
    format: json
    embed: false               # Available as static file only

testing:
  pre_rig: tests/validate.py   # Unit tests (fast)
  post_rig: tests/e2e.py       # Integration tests (slow)
  health_check: "curl -f http://localhost:8080/health"

exports:                       # What this skill provides
  tools:
    - cast_net
    - filet_fish
  schemas:
    - FishTelemetry
```

---

## 3. Equip/Unequip Protocol

### Commands

```bash
skiff rig <skill>[@version]    # HOT: Mount and activate
skiff derig <skill>            # WARM: Deactivate but keep in harbor
skiff stow <skill>             # COLD: Archive to locker (git bundle)
skiff hoist <skill>[@version]  # WARM: Restore from locker/remote
skiff jettison <skill>         # DELETE: Remove completely
```

### The Rigging Protocol (Equip)

When an agent runs `skiff rig fishing@1.2.3`:

1. **Lock**: Create `deck/.riglock` (prevents concurrent rigging)
2. **Resolve**: Parse `SKILL.md` → build dependency DAG
3. **Fetch Dependencies**:
   - Check if `navigation^2.0.0` exists in `deck/` (hot) or `harbor/` (warm)
   - If missing: `git clone` to `harbor/github.com/fleet/navigation/`
   - Checkout tag satisfying semver
   - Recurse for sub-dependencies
4. **Conflict Check**: Ensure no tool name collisions (e.g., two skills exporting `search`)
5. **Test (Dry)**:
   - Run `python rig.py --dry-run` if supported
   - Execute `tests/validate.py` (pre-rig tests)
6. **Mount**: `ln -s harbor/github.com/fleet/fishing deck/fishing`
7. **Activate**: Execute `deck/fishing/rig.py`
   - Registers tools with agent's tool registry
   - Loads knowledge into vector store
   - Returns PID/resource handles
8. **Verify**: Run `tests/e2e.py` (post-rig tests)
9. **Commit Manifest**: Update `manifest.yaml`:

```yaml
rigged_at: "2024-01-15T14:23:00Z"
skills:
  fishing:
    id: fleet/fishing
    version: 1.2.3
    commit: a1b2c3d
    path: deck/fishing
    state: hot
    pid: 18472
    tools: [cast_net, filet_fish]
    dependencies:
      - navigation@2.1.0
  navigation:
    id: fleet/navigation
    version: 2.1.0
    state: hot
```

### The Derig Protocol (Unequip)

When an agent runs `skiff derig fishing`:

1. **Invoke Exit**: Run `deck/fishing/derig.py`
   - Unregister tools
   - Release memory
   - Kill PID 18472
2. **Unmount**: `rm deck/fishing` (symlink removed)
3. **State Transition**: Update manifest → `state: warm`
4. **GC**: Optional cleanup of cached embeddings

---

## 4. Archive & Retrieval (Cold Storage)

### Stowing (Warm → Cold)

```bash
$ skiff stow fishing --version 1.2.0
```

1. Ensure skill is derigged (warm state)
2. Create git bundle: 
   ```bash
   cd harbor/github.com/fleet/fishing
   git bundle create ../../../locker/fishing-v1.2.0.bundle --all --tags
   ```
3. Compress: `gzip locker/fishing-v1.2.0.bundle`
4. Update `locker/manifest.locker`:

```yaml
archived:
  fishing:
    - version: 1.2.0
      bundle: fishing-v1.2.0.bundle.gz
      size_mb: 12
      archived_at: "2024-01-10T09:00:00Z"
```

5. `rm -rf harbor/github.com/fleet/fishing` (reclaim space)

### Hoisting (Cold → Warm)

```bash
$ skiff hoist fishing --version 1.2.0
# or from remote only (no local bundle):
$ skiff hoist fishing --from git@github.com:fleet/fishing.git --version 1.2.0
```

1. Check `locker/manifest.locker` for bundle
2. If exists: `git bundle unbundle` into `harbor/`
3. If not: Clone from remote registry
4. Checkout specific version tag
5. State: warm (ready to rig)

---

## 5. Dependency Resolution

The resolver treats skills as a DAG with state constraints.

**Example**: Rigging `fishing` requires `navigation` to be hot.

```yaml
# In fishing/SKILL.md
dependencies:
  skills:
    - id: fleet/navigation
      version: "^2.0.0"
      state: hot              # Must be active, not just present
```

**Resolution Algorithm**:
1. Parse target skill's dependencies
2. For each dependency:
   - If in `deck/` with correct version → satisfied
   - If in `harbor/` → rig it first (recurse)
   - If in `locker/` → hoist it first
   - If missing → clone from registry
3. Check for diamond dependencies (two skills need different versions of `navigation`):
   - Abort with conflict report
   - Or use `--force` to create isolated namespace (advanced)

---

## 6. Discovery

Agents discover skills via registries configured in `~/.skiff/config.yaml`:

```yaml
registries:
  - name: fleet-official
    type: github-org
    url: https://github.com/fleet/skills
    auth: token:${GITHUB_TOKEN}
  
  - name: local-fleet
    type: filesystem
    path: /shared/skiff-skills/
  
  - name: s3-backup
    type: s3
    bucket: agent-skills
    prefix: prod/

search:
  index_url: https://skills.registry.ai/index.json
```

**Discovery Commands**:
```bash
$ skiff search fishing
fleet/fishing 1.2.3    Deep sea fishing operations
fleet/fishing 1.1.0    Legacy (LTS)
captain-joe/fishing 2.0.0  Fly fishing specialist

$ skiff inspect fleet/fishing
Shows: dependencies, resource usage, exports, versions available
```

---

## 7. Testing Before Activation

**Three-Phase Testing**:

1. **Static** (Cold → Warm transition):
   ```bash
   skiff check fishing@1.2.3
   ```
   - Validates SKILL.md schema
   - Checks dependency version solvability
   - Runs `rig.py --syntax-check` if engine supports it

2. **Pre-Rig** (Warm → Hot, before symlink):
   - Executes `tests/validate.py` in skill directory
   - Tests tool schemas without registering them
   - Validates knowledge files parse correctly

3. **Post-Rig** (Hot, after activation):
   - Runs `tests/e2e.py` with actual tool registration
   - Calls health_check endpoint if defined
   - If tests fail → auto-derig and rollback to previous version

**Rollback on Failure**:
```bash
$ skiff rig fishing --rollback-on-fail
# If post_rig tests fail, automatically:
# 1. Derig new version
# 2. Re-rig previous version from manifest history
```

---

## 8. Concrete Example: Session Log

```bash
# Agent prepares for a fishing task
$ skiff rig fishing --version 1.2.3
[RESOLVE] Checking dependencies...
[HOT]     navigation ^2.0.0 already rigged
[WARM]    Found weather >=1.0.0 in harbor
[RIG]     Rigging weather...
[TEST]    weather pre_rig... OK
[MOUNT]   Symlinking weather -> deck/
[ACTIVATE] weather rig.py... OK (pid: 4512)
[RIG]     Rigging fishing...
[TEST]    fishing pre_rig... OK
[MOUNT]   Symlinking fishing -> deck/
[ACTIVATE] fishing rig.py... OK (pid: 4513)
[TEST]    fishing post_rig... OK
[EXPORT]  Tools registered: cast_net, filet_fish, sonar_scan
[VECTOR]  Embedded 50 documents from fishing/knowledge/
[DECK]    Current loadout: navigation@2.1.0, weather@1.0.0, fishing@1.2.3

# Work happens...

# Done fishing, switching to navigation-only mode
$ skiff derig fishing
[DERIG]   Running fishing/derig.py...
[CLEANUP] Unregistered cast_net, filet_fish, sonar_scan
[RELEASE] Freed 512MB vector cache
[WARM]    fishing moved to harbor (ready for fast re-rig)

# Archive to save space
$ skiff stow fishing
[STOW]    Creating git bundle...
[STOW]    Compressed to 15MB: locker/fishing-v1.2.3.bundle.gz
[COLD]    fishing archived

# Later: rollback after bad update
$ skiff rig fishing --version 1.2.4
[ERROR]   post_rig tests failed: sonar_scan timeout
[ROLLBACK] Reverting to fishing@1.2.3...
[WARM]    Hoisting fishing-v1.2.3 from locker...
[RIG]     Rigging fishing@1.2.3... OK
```

---

## 9. Implementation Notes

**rig.py Interface**:
The activation script receives context via environment variables:

```python
# rig.py
import os
import json

SKIFF_CONTEXT = {
    "skill_id": os.environ["SKIFF_SKILL_ID"],
    "version": os.environ["SKIFF_VERSION
