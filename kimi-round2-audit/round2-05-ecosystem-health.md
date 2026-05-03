# Round 2 — Ecosystem Health Audit

## 5.1 PyPI Packages

| Package | Install | Import | Version (PyPI) | Version (Code) | CLI Works | Dependencies | Notes |
|---------|---------|--------|------------------|----------------|-----------|--------------|-------|
| plato-mud-server | ✅ | ✅ | 0.2.2 | 0.1.0 | N/A | None | Version mismatch (PyPI 0.2.2 vs code 0.1.0). |
| cocapn | ✅ | ✅ | 0.2.0 | 0.1.0 | ❌ | pyyaml, requests | Version mismatch (PyPI 0.2.0 vs code 0.1.0). CLI broken (cocapn fails). |
| deadband-protocol | ✅ | ✅ | 0.3.0 | 0.3.0 | N/A | None | OK |
| bottle-protocol | ✅ | ✅ | 0.1.0 | 0.1.0 | N/A | None | No Home-page metadata. |
| flywheel-engine | ✅ | ✅ | 0.3.2 | 0.3.2 | N/A | None | OK |
| cocapn-sdk | ✅ | ✅ | 0.1.0 | 0.1.0 | N/A | bottle-protocol, cocapn, court, deadband-protocol, flywheel-engine, keeper-beacon, plato-provenance, plato-tile-spec | OK |
| plato-torch | ✅ | ✅ | 0.5.0 | 0.5.0a1 | N/A | None | Version mismatch (PyPI 0.5.0 vs code 0.5.0a1). |
| plato-tile-spec | ✅ | ✅ | 0.2.1 | NO __version__ | N/A | None | Missing `__version__`. No Home-page metadata. |
| court | ✅ | ✅ | 0.3.2 | 0.3.2 | N/A | None | OK |
| tile-refiner | ✅ | ✅ | 0.1.0 | 0.1.0 | N/A | None | No Home-page metadata. |

## 5.2 npm Packages

| Package | Install | Version | Has README | Has Code | Notes |
|---------|---------|---------|------------|----------|-------|
| @superinstance/plato-sdk | ✅ | 0.1.0 | ✅ | ✅ | OK |
| @superinstance/tile-refiner | ✅ | 0.1.1 | ❌ | ✅ | No README. |
| @superinstance/deadband | ❌ | N/A | ❌ | ❌ | Install failed: npm error code E404. |

## 5.3 crates.io Packages

| Package | Install/Build | Version | Has Binary | Notes |
|---------|---------------|---------|------------|-------|
| ct-demo | ⚠️ Library (no bin) | 0.3.0 | ❌ | Library crate — `cargo install` not applicable, but builds fine as dependency. |
| constraint-theory-core | ⚠️ Library (no bin) | 2.0.0 | ❌ | Library crate — `cargo install` not applicable, but builds fine as dependency. |
| plato-kernel | ✅ | 0.2.0 | ✅ | Binary runs but has no --help/--version. |

## 5.4 Version Consistency

| Package | Registry Version | GitHub Tag | Code Version | Consistent? |
|---------|------------------|------------|--------------|-------------|
| plato-mud-server (PyPI) | 0.2.2 | N/A | 0.1.0 | ❌ |
| cocapn (PyPI) | 0.2.0 | N/A | 0.1.0 | ❌ |
| deadband-protocol (PyPI) | 0.3.0 | N/A | 0.3.0 | ✅ |
| bottle-protocol (PyPI) | 0.1.0 | N/A | 0.1.0 | ✅ |
| flywheel-engine (PyPI) | 0.3.2 | N/A | 0.3.2 | ✅ |
| cocapn-sdk (PyPI) | 0.1.0 | N/A | 0.1.0 | ✅ |
| plato-torch (PyPI) | 0.5.0 | N/A | 0.5.0a1 | ❌ |
| plato-tile-spec (PyPI) | 0.2.1 | N/A | N/A | ⚠️ |
| court (PyPI) | 0.3.2 | N/A | 0.3.2 | ✅ |
| tile-refiner (PyPI) | 0.1.0 | N/A | 0.1.0 | ✅ |
| @superinstance/plato-sdk (npm) | 0.1.0 | N/A | N/A | ⚠️ |
| @superinstance/tile-refiner (npm) | 0.1.1 | N/A | N/A | ⚠️ |
| @superinstance/deadband (npm) | N/A | N/A | N/A | ⚠️ |
| ct-demo (crates) | 0.3.0 | N/A | N/A | ⚠️ |
| constraint-theory-core (crates) | 2.0.0 | N/A | N/A | ⚠️ |
| plato-kernel (crates) | 0.2.0 | N/A | N/A | ⚠️ |

## 5.5 Critical Issues

| Severity | Package | Issue |
|----------|---------|-------|
| High | plato-mud-server | Version mismatch: PyPI 0.2.2 vs code 0.1.0 |
| High | cocapn | Version mismatch: PyPI 0.2.0 vs code 0.1.0 |
| High | cocapn | CLI entry point 'cocapn' broken |
| Low | bottle-protocol | Missing Home-page metadata |
| High | plato-torch | Version mismatch: PyPI 0.5.0 vs code 0.5.0a1 |
| Medium | plato-tile-spec | Missing `__version__` attribute |
| Low | plato-tile-spec | Missing Home-page metadata |
| Low | tile-refiner | Missing Home-page metadata |
| Low | @superinstance/tile-refiner | Missing README |
| High | @superinstance/deadband | Package not found on npm (404) |
| Medium | ct-demo | Library only — `cargo install` not applicable, but compiles as dependency. |
| Medium | constraint-theory-core | Library only — `cargo install` not applicable, but compiles as dependency. |

## 5.6 Overall Health Score

| Registry | Packages Tested | Success Rate |
|----------|-----------------|--------------|
| PyPI | 10 | 10/10 (100%) |
| npm | 3 | 2/3 (67%) |
| crates.io | 3 | 3/3 (100%) |

## 5.7 Recommendations

| Priority | Action |
|----------|--------|
| High | Fix version mismatches in `plato-mud-server`, `cocapn`, and `plato-torch` (and add `__version__` to `plato-tile-spec`). |
| High | Fix or remove broken `cocapn` CLI entry point (`agent` module missing). |
| High | Publish missing npm package `@superinstance/deadband` or remove from registry listing. |
| Medium | Add `repository`/`Home-page` metadata to `bottle-protocol`, `plato-tile-spec`, `tile-refiner`. |
| Medium | Add README to npm package `@superinstance/tile-refiner`. |
| Low | Consider adding `--help` / `--version` flags to `plato-kernel` binary. |
| Low | Add GitHub release tags to all repositories for version traceability. |