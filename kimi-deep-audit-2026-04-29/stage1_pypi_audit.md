# Stage 1: PyPI Package Audit for Cocapn Ecosystem

> Audit Date: 2026-04-30  
> Auditor: Automated PyPI Quality Audit  
> PyPI User: [superinstance](https://pypi.org/user/superinstance/) ("casey digennaro", joined Mar 27, 2026)  
> Claimed: 38 PyPI packages + 5 Rust crates = 43 total

---

## 3.1 Package Inventory

### Verified Existing Packages: 61 found on PyPI

The superinstance user profile claims **176 projects**, but only **61 are cocapn-related** packages that we could identify and verify.

#### Core / Runtime (3)
| Package | Version | Released | Status |
|---------|---------|----------|--------|
| cocapn | 0.2.0 | 2026-04-26 | Published |
| plato-torch | 0.5.0 | 2026-04-24 | Published |
| plato-mud-server | 0.2.2 | 2026-04-27 | Published |

#### Protocols (3)
| Package | Version | Released | Status |
|---------|---------|----------|--------|
| deadband-protocol | 0.3.0 | 2026-04-27 | Published |
| bottle-protocol | 0.1.0 | 2026-04-20 | Published |
| flywheel-engine | 0.3.2 | 2026-04-28 | Published |

#### Fleet Ops (3)
| Package | Version | Released | Status |
|---------|---------|----------|--------|
| fleet-homunculus | 0.1.0 | 2026-04-20 | Published |
| barracks | 0.1.0 | 2018-08-17 | **NOT cocapn** (pre-existing package) |
| court | 0.3.2 | 2026-04-28 | Published |

#### Tile Pipeline / Data (3)
| Package | Version | Released | Status |
|---------|---------|----------|--------|
| tile-refiner | 0.1.0 | 2026-04-20 | Published |
| cocapn-archives | 0.1.0 | 2026-04-20 | Published |
| cocapn-garden | 0.1.0 | 2026-04-20 | Published |

#### Training / Ops (4)
| Package | Version | Released | Status |
|---------|---------|----------|--------|
| cocapn-workshop | 0.1.0 | 2026-04-20 | Published |
| cocapn-dry-dock | 0.1.0 | 2026-04-20 | Published |
| cocapn-observatory | 0.1.0 | 2026-04-20 | Published |
| cocapn-horizon | 0.1.0 | 2026-04-20 | Published |

#### Research / Creative (8)
| Package | Version | Released | Status |
|---------|---------|----------|--------|
| cocapn-oneiros | 0.3.1 | 2026-04-28 | Published |
| cocapn-colora | 0.2.2 | 2026-04-28 | Published |
| cocapn-curriculum-forest | 0.1.0 | 2026-04-20 | Published |
| cocapn-abyss | 0.1.0 | 2026-04-20 | Published |
| cocapn-meta-lab | 0.1.0 | 2026-04-20 | Published |
| cocapn-fleetmind | 0.1.0 | 2026-04-20 | Published |
| cocapn-platonic-dial | 0.1.0 | 2026-04-20 | Published |
| cocapn-coliseum | 0.1.0 | 2026-04-20 | Published |

#### PLATO Framework Components (33)
| Package | Version | Released | Importable |
|---------|---------|----------|------------|
| plato-mcp-client | 0.1.3 | 2026-04-28 | Yes |
| plato-i2i | 0.1.2 | 2026-04-28 | Yes |
| plato-edge | 0.1.1 | 2026-04-28 | Yes |
| plato-dcs | 0.2.0 | 2026-04-28 | Yes |
| plato-unified-belief | 0.1.0 | 2026-04-20 | Yes |
| plato-deadband | 0.1.0 | 2026-04-20 | Yes |
| plato-tile-dedup | 0.1.0 | 2026-04-20 | Yes |
| plato-tile-scorer | 0.1.0 | 2026-04-20 | Yes |
| plato-achievement | 0.1.0 | 2026-04-20 | Yes |
| plato-adapter-store | 0.1.0 | 2026-04-20 | Yes |
| plato-address | 0.1.0 | 2026-04-20 | Yes |
| plato-afterlife-reef | 0.1.0 | 2026-04-20 | Yes |
| plato-deploy-policy | 0.1.0 | 2026-04-20 | Yes |
| plato-dynamic-locks | 0.1.0 | 2026-04-20 | Yes |
| plato-e2e-pipeline | 0.1.0 | 2026-04-20 | Yes |
| plato-forge-listener | 0.1.0 | 2026-04-20 | Yes |
| plato-ghostable | 0.1.0 | 2026-04-20 | Yes |
| plato-live-data | 0.1.0 | 2026-04-20 | Yes |
| plato-mcp-bridge | 0.1.0 | 2026-04-20 | Yes |
| plato-query-parser | 0.1.0 | 2026-04-20 | Yes |
| plato-room-persist | 0.1.0 | 2026-04-20 | Yes |
| plato-room-search | 0.1.0 | 2026-04-20 | Yes |
| plato-room-server | 0.1.0 | 2026-04-20 | Yes |
| plato-tile-bridge | 0.1.0 | 2026-04-20 | Yes |

#### Fleet / Infrastructure (4)
| Package | Version | Released | Notes |
|---------|---------|----------|-------|
| cocapn-lighthouse | 1.0.1 | 2026-04-28 | CLI-only (`lighthouse` script), import as `lighthouse` |
| cocapn-hermitcrab | 0.1.0 | 2026-04-28 | CLI-only (`cocapn-git-agent` script) |
| cocapn-sdk | 0.1.0 | 2026-04-28 | Published |

### Missing Packages: 1
| Package | Expected | Status |
|---------|----------|--------|
| plato-forge-trainer | Listed in README | **NOT FOUND on PyPI** |

### Not Cocapn-Related: 1
| Package | Status |
|---------|--------|
| barracks | Pre-existing package (2018), not part of cocapn ecosystem. Likely name-squatting or unrelated. |

---

## 3.2 Installation Test Results

### Packages That Install Successfully via `pip install`

**All 61 verified packages install successfully** via `pip install`. The packages are small (1-90 KB wheels, mostly <10 KB), pure Python, and have no external build dependencies.

### Packages That Fail to Import After Installation

**10 packages are completely broken** - they install but cannot be imported due to internal module naming mismatches:

| Package | Error | Root Cause |
|---------|-------|------------|
| cocapn-archives | `ModuleNotFoundError: No module named 'cocapn_archives.cocapn_archives'` | `__init__.py` imports from `.cocapn_archives` but module file is `archives.py` |
| cocapn-garden | `ModuleNotFoundError: No module named 'cocapn_garden.cocapn_garden'` | `__init__.py` imports from `.cocapn_garden` but module file is `garden.py` |
| cocapn-workshop | `ModuleNotFoundError: No module named 'cocapn_workshop.cocapn_workshop'` | `__init__.py` imports from `.cocapn_workshop` but module file is `workshop.py` |
| cocapn-dry-dock | `ModuleNotFoundError: No module named 'cocapn_dry_dock.cocapn_dry_dock'` | `__init__.py` imports from `.cocapn_dry_dock` but module file is `dry_dock.py` |
| cocapn-observatory | `ModuleNotFoundError: No module named 'cocapn_observatory.cocapn_observatory'` | `__init__.py` imports from `.cocapn_observatory` but module file is `observatory.py` |
| cocapn-horizon | `ModuleNotFoundError: No module named 'cocapn_horizon.cocapn_horizon'` | `__init__.py` imports from `.cocapn_horizon` but module file is `horizon.py` |
| plato-address-bridge | `ModuleNotFoundError: No module named 'plato_address_bridge'` | **No package directory at all** - only `.dist-info` installed |
| plato-forge-daemon | `ModuleNotFoundError: No module named 'plato_forge_daemon'` | **No package directory at all** |
| plato-forge-pipeline | `ModuleNotFoundError: No module named 'plato_forge_pipeline'` | **No package directory at all** |
| plato-instinct | `ModuleNotFoundError: No module named 'plato_instinct'` | **No package directory at all** |
| plato-relay-tidepool | `ModuleNotFoundError: No module named 'plato_relay_tidepool'` | **No package directory at all** |
| plato-room-scheduler | `ModuleNotFoundError: No module named 'plato_room_scheduler'` | **No package directory at all** |
| plato-sim-channel | `ModuleNotFoundError: No module named 'plato_sim_channel'` | **No package directory at all** |
| plato-tile-current | `ModuleNotFoundError: No module named 'plato_tile_current'` | **No package directory at all** |
| plato-tile-room-bridge | `ModuleNotFoundError: No module named 'plato_tile_room_bridge'` | **No package directory at all** |

**15 total broken packages** out of 61 = **24.6% failure rate** for basic importability.

### CLI Entry Points

| Package | CLI Script | Status | Notes |
|---------|-----------|--------|-------|
| cocapn | `cocapn` | **BROKEN** | `ModuleNotFoundError: No module named 'agent'` |
| cocapn-lighthouse | `lighthouse` | **WORKS** | Full CLI with `scan`, `beachcomb`, `infer`, `status`, `bottle`, `onboard`, `config` commands |
| cocapn-hermitcrab | `cocapn-git-agent` | **WORKS** | Full CLI with `run`, `observe`, `plan`, `bootstrap` commands |

---

## 3.3 Package Quality Assessment

### Version Number Mismatches (Code vs Package)

| Package | PyPI Version | `__version__` in Code | Severity |
|---------|-------------|----------------------|----------|
| cocapn | 0.2.0 | 0.1.0 | Medium |
| plato-torch | 0.5.0 | 0.5.0a1 | Low |
| plato-mud-server | 0.2.2 | 0.1.0 | Medium |
| plato-mcp-client | 0.1.3 | 0.1.0 | Low |
| cocapn-lighthouse | 1.0.1 | 1.0.0 | Low |
| lighthouse | n/a | 1.0.0 | n/a |

### Missing `__version__` Attribute

| Package | Has `__version__`? |
|---------|-------------------|
| barracks | **NO** |
| plato-adapter-store | **NO** |

### README / Documentation Quality

| Package | Has README on PyPI? | Quality Assessment |
|---------|-------------------|-------------------|
| cocapn | Yes | Excellent - comprehensive with ASCII art, architecture diagrams, room tables |
| plato-torch | Yes | Excellent - detailed with preset tables, architecture diagram, code examples |
| flywheel-engine | Yes | Good - API reference table, quick start code, class documentation |
| deadband-protocol | Yes | Minimal - one paragraph + install instructions |
| bottle-protocol | Yes | Minimal - one sentence description |
| court | Yes | Good - governance concepts, usage examples |
| plato-mud-server | Yes | Good - MUD server description, installation instructions |
| Most others (40+) | No / Minimal | "PLATO framework component" placeholder or 1-2 sentences |

**Pattern:** The 6 "core" packages have decent READMEs. The remaining ~40+ packages have essentially no documentation.

### Dependencies

| Package | Dependencies | Assessment |
|---------|-------------|------------|
| cocapn | requests>=2.28.0, pyyaml>=6.0 | Reasonable |
| cocapn-hermitcrab | pyyaml, requests | Reasonable |
| cocapn-sdk | 18 dependencies | Heavy for a "SDK" - pulls in many transitive deps |
| barracks | lz4>=2.1.0 | Reasonable |
| plato-edge | 1 dependency | Reasonable |
| Most others | **ZERO dependencies** | Suspicious - these packages claim complex AI functionality but have no dependencies on ML/DL libraries |

### API Design / Documentation Mismatches

| Package | Documented API | Actual API | Issue |
|---------|---------------|-----------|-------|
| cocapn.Tile | `model`, `agent`, `hash`, `parents` | `question`, `answer`, `domain`, `confidence`, `source`, `tags`, `id`, `timestamp`, `usage_count`, `success_count`, `version` | Completely different signature |
| deadband_protocol.Deadband | `.filter()` method | `epsilon()`, `snap_check()`, `within()` | Wrong method names |
| bottle_protocol.Bottle | No docs for constructor | Requires `sender`, `recipient`, `message`, `bottle_id`, `timestamp`, `metadata` | Undocumented required args |
| fleet_homunculus.FleetBody | No docs for constructor | Requires `fleet_id` | Undocumented required arg |

---

## 3.4 Critical Issues

### 1. **Systematic Packaging Bug: Module Name Mismatch (15 packages)**
**Severity: CRITICAL**

The `__init__.py` files in many packages use the pattern:
```python
from .cocapn_archives import Archives, Document, QueryResult
```

But the actual module file is named `archives.py`, not `cocapn_archives.py`. This makes the packages completely unusable as Python imports. This is a build/packaging automation bug that affects 15 packages (10 with naming mismatch, 5 with no module at all).

**Affected packages:**
- cocapn-archives, cocapn-garden, cocapn-workshop, cocapn-dry-dock, cocapn-observatory, cocapn-horizon (6 with wrong import)
- plato-address-bridge, plato-forge-daemon, plato-forge-pipeline, plato-instinct, plato-relay-tidepool, plato-room-scheduler, plato-sim-channel, plato-tile-current, plato-tile-room-bridge (9 with no module directory)

### 2. **CLI Entry Point Broken (cocapn main package)**
**Severity: HIGH**

The `cocapn` package installs a `cocapn` CLI script that fails immediately:
```
File "/home/kimi/.local/bin/cocapn", line 5, in <module>
    from agent import main
ModuleNotFoundError: No module named 'agent'
```

This suggests the CLI was copied from a different project or the module structure changed without updating the entry point.

### 3. **Version Numbers Don't Match (3+ packages)**
**Severity: MEDIUM**

Installed 0.2.0 but code reports 0.1.0. This indicates packages were version-bumped in metadata without updating the code, suggesting hasty or automated releases without verification.

### 4. **"Barracks" is Not a Cocapn Package**
**Severity: MEDIUM**

The `barracks` package (v0.1.0, released 2018) is a pre-existing utility for "reading & writing series of data for data mining". It is NOT part of the cocapn ecosystem and has a completely different purpose. It should not be counted as a cocapn package.

### 5. **Claimed 38 Packages, Found 60+ but Quality is Very Low**
**Severity: MEDIUM**

While there ARE many packages (60+ cocapn-related), most are:
- Tiny (<5 KB)
- Have no real dependencies
- Have no meaningful README
- Have placeholder descriptions ("PLATO framework component")
- Appear to be generated from templates

### 6. **No PyPI User Profile for "cocapn"**
**Severity: LOW**

The URL `https://pypi.org/user/cocapn/` returns 404. All packages are published under the `superinstance` user account, not a `cocapn` organization.

---

## 3.5 Recommendations

### Immediate Fixes (Priority 1)

1. **Fix the 15 broken packages** - Either:
   - Rename the module files to match the `__init__.py` imports (e.g., `archives.py` -> `cocapn_archives.py`), OR
   - Fix the `__init__.py` imports to use the actual module names (e.g., `from .archives import ...`)
   
2. **Fix the `cocapn` CLI entry point** - Update the script to import from the correct module path

3. **Fix version number mismatches** - Update `__version__` in code to match package metadata

### Medium Priority

4. **Add `__version__` to barracks and plato-adapter-store**

5. **Remove barracks from the cocapn package count** - It's not a cocapn package

6. **Add actual dependencies to packages that claim ML/AI functionality** - e.g. `plato-torch` should probably depend on `torch`, `numpy`, etc. Currently it has zero dependencies which is suspicious for a "training room" library.

### Documentation Priority

7. **Write READMEs for the 40+ placeholder packages** - "PLATO framework component" is not a sufficient description

8. **Document the actual API signatures** - The documented Tile API and actual Tile API are completely different

### Strategic Recommendation

9. **Consolidate the micro-packages** - Having 60+ tiny packages (many <5 KB) creates maintenance burden and confusion. Consider consolidating related functionality into fewer, well-documented packages.

---

## Summary Statistics

| Metric | Count |
|--------|-------|
| Total cocapn-related packages found | 61 |
| Packages that install successfully | 61 (100%) |
| Packages that import successfully | 46 (75.4%) |
| Packages that are completely broken (can't import) | 15 (24.6%) |
| Packages with CLI entry points | 3 |
| Working CLI entry points | 2 |
| Broken CLI entry points | 1 |
| Packages with good README | ~6 |
| Packages with placeholder README | ~40+ |
| Version mismatches (code vs package) | 3+ |
| Packages with zero dependencies | ~50+ |
| Missing packages (claimed but not found) | 1 (plato-forge-trainer) |
| Non-cocapn packages incorrectly counted | 1 (barracks) |

---

*End of Stage 1 PyPI Audit Report*
