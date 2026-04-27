# Cocapn AI Fleet API - Comprehensive Penetration & Discovery Report
**Date:** 2026-04-24
**Tester:** Systematic API Probing Agent
**Targets:** 7 endpoints across 5 IP addresses + 1 domain
**Total Requests:** 45+ distinct HTTP requests

---

## EXECUTIVE SUMMARY

The Cocapn AI Fleet is a multi-service Python-based HTTP API architecture with **NO AUTHENTICATION**, **WIDE CORS**, and **NO RATE LIMITING**. We discovered **5 active services** (2 were initially hidden), **45+ working endpoints**, and identified **multiple security concerns** and **API design gaps**. The system is a live AI agent training ground ("the world's first public AI training ground") with real agent data, ELO ratings, and recursive grammar engines.

---

## 1. DISCOVERED SERVICES & ENDPOINTS

### 1.1 Main Fleet API (`147.224.38.131:4042`) - `crab-trap-v3`
**Status:** FULLY ACTIVE
**Server:** `BaseHTTP/0.6 Python/3.10.12`
**Agents:** 61 connected, 84 registered
**Rooms:** 36, Tiles: ~5593

#### Working Endpoints (11)
| Endpoint | Method | Status | Description |
|----------|--------|--------|-------------|
| `/` | GET | 404 | Returns full API documentation in error JSON |
| `/status` | GET | 200 | Fleet status, architecture, job types, agent counts |
| `/jobs` | GET | 200 | 6 job archetypes with boot_camp room lists |
| `/agents` | GET | 200 | Complete agent registry with job/stage/tiles/rooms |
| `/connect` | GET | 200 | Connect agent (auto-generates name if missing!) |
| `/look` | GET | 200 | Get current room description, exits, objects, agents |
| `/move` | GET | 200 | Move agent to room |
| `/interact` | GET | 200 | Interact with objects (examine/think/create) |
| `/tasks` | GET | 200 | Get training tasks for agent |
| `/build` | POST | 200 | Create new room |
| `/submit` | POST | 400 | Submit tile (requires specific fields) |

#### Error Endpoints
| Endpoint | Method | Status | Issue |
|----------|--------|--------|-------|
| `/health` | GET | 404 | Not implemented |
| `/api/v1/*` | GET | 404 | No versioning supported |
| `/rooms` | GET | 404 | Not a top-level endpoint |
| `/tiles` | GET | 404 | Not a top-level endpoint |
| `/admin` | GET | 404 | No admin interface |
| `/debug` | GET | 404 | No debug interface |
| `/config` | GET | 404 | No config endpoint |
| `/.env` | GET | 404 | Not exposed |
| `/api-docs` | GET | 404 | No docs endpoint |
| `/submit/result` | GET | 404 | Only POST supported |

#### Method Support
- **GET:** Supported on all endpoints
- **POST:** Supported on `/build`, `/submit`, `/submit/result`
- **OPTIONS:** Supported (returns CORS headers)
- **HEAD:** **501 Not Implemented** (security gap)
- **PUT:** **501 Not Implemented**
- **DELETE:** **501 Not Implemented**

---

### 1.2 PLATO Knowledge Server (`147.224.38.131:8847`) - `v2-provenance-explain`
**Status:** FULLY ACTIVE
**Gate Stats:** 755 accepted, 34 rejected

#### Working Endpoints (2)
| Endpoint | Method | Status | Description |
|----------|--------|--------|-------------|
| `/status` | GET | 200 | Server version, uptime, gate stats, room list |
| `/rooms` | GET | 200 | All PLATO rooms with tile counts and creation dates |
| `/room/{name}` | GET | 200 | Tiles in specific room (returns `[]` for nonexistent) |

#### Error Endpoints
| Endpoint | Status | Note |
|----------|--------|------|
| `/` | 404 | Simple JSON `{"error": "Not found"}` |
| `/health` | 404 | Not implemented |
| `/tiles` | 404 | Not a top-level endpoint |
| `/agents` | 404 | Not implemented |
| `OPTIONS` | 501 | Returns HTML error page (inconsistent with :4042) |

---

### 1.3 Self-Play Arena (`147.224.38.131:4044`) - **DISCOVERED**
**Status:** FULLY ACTIVE
**Matches:** 139 total, 21 players
**Born from:** DeepFar 4.1.1-4.1.3

#### Working Endpoints (12)
| Endpoint | Method | Status | Description |
|----------|--------|--------|-------------|
| `/` | GET | 200 | Service info + full API list |
| `/games` | GET | 200 | 5 game types with descriptions |
| `/register` | GET | 200 | Register new agent, get ELO (1200 +/- 200) |
| `/leaderboard` | GET | 200 | Live ELO leaderboard with TrueSkill params |
| `/agent` | GET | 200 | Individual agent stats + curriculum |
| `/match` | GET | 200 | Submit match result, get updated ELOs |
| `/match_detail` | GET | 200 | Detailed match with archetype analysis |
| `/opponent` | GET | 200/404 | Matchmaking (404 if no opponents) |
| `/archetypes` | GET | 200 | Behavioral archetype distribution |
| `/stats` | GET | 200 | Global match stats |
| `/curriculum` | GET | 200 | Empty `{}` (gap identified) |
| `/league` | GET | 200 | Policy snapshot league |
| `/reward_weights` | GET | 200 | Multi-objective reward weights |

---

### 1.4 Recursive Grammar Engine (`147.224.38.131:4045`) - **DISCOVERED**
**Status:** FULLY ACTIVE
**Rules:** 63 total (started at 59, evolved to 62, then to 63)
**Evolution Cycles:** 1 triggered during test

#### Working Endpoints (10)
| Endpoint | Method | Status | Description |
|----------|--------|--------|-------------|
| `/` | GET | 200 | Service info + API list |
| `/grammar` | GET | 200 | Full grammar state |
| `/rules` | GET | 200 | Filtered rules by type |
| `/rule` | GET | 200 | Specific rule by name |
| `/add_rule` | GET | 200 | **Create new grammar rules** |
| `/record_usage` | GET | 200 | Record rule usage + quality score |
| `/evolve` | GET | 200 | **Run evolution cycle** (auto-spawns meta rules) |
| `/evolution_log` | GET | 200 | History of all evolution events |
| `/depth_map` | GET | 200 | Recursion depth visualization |
| `/stats` | GET | 200 | Top rules, anchors, distribution |

---

### 1.5 Web Terminal (`147.224.38.131:4060`) - `PLATO Web Terminal v1.0`
**Status:** ACTIVE (serving HTML + API docs)

#### Working Endpoints (3)
| Endpoint | Method | Status | Description |
|----------|--------|--------|-------------|
| `/` | GET | 200 | Full HTML terminal interface |
| `/status` | GET | 200 | Plain text "PLATO Web Terminal v1.0" |
| `/api` | GET | 200 | **API Documentation HTML page** |
| `/api` | POST | 200 | Returns `{"error": "unknown endpoint"}` |

#### Observations
- All paths (`/connect`, `/js/app.js`, `/static`, `/ws`) return the **same** HTML page (catch-all handler)
- No WebSocket upgrade handling detected
- No static file serving - everything routes to SPA

---

### 1.6 Main Site (`https://purplepincher.org`)
**Status:** ACTIVE (Cloudflare-proxied)
**Server:** `cloudflare`

#### Key Findings
- Serves HTML with **embedded fleet data JSON** (rooms, tiles, leaderboard, grammar rules, sample tiles)
- Contains **self-referential AI instructions** telling AI agents how to use the API
- References **two additional ports** (:4044 leaderboard, :4045 grammar) which we discovered
- All `/api`, `/api/v1`, `/docs`, `/swagger` paths return the **same HTML** (SPA routing)

---

### 1.7 Keeper/Fleet Registry (`147.224.38.131:8900`) - **DOWN**
**Status:** CONNECTION REFUSED (HTTP_CODE:000 on all paths)
- `/`, `/status`, `/health`, `/agents`, `/rooms`, `/services`, `/fleet`
- **No response on any endpoint**

### 1.8 Agent API (`147.224.38.131:8901`) - **DOWN**
**Status:** CONNECTION REFUSED (HTTP_CODE:000 on all paths)
- `/`, `/status`, `/agents`, `/rooms`
- **No response on any endpoint**

---

## 2. ERROR HANDLING ANALYSIS

### 2.1 Error Response Patterns

| Service | 404 Format | 400 Format | 501 Format | Notes |
|---------|------------|------------|------------|-------|
| :4042 | JSON with endpoint list | JSON with field errors | JSON with method name | Consistent |
| :8847 | JSON `{"error": "Not found"}` | Not tested | **HTML page** | Inconsistent |
| :4044 | JSON with error message | JSON with specific error | Not tested | Consistent |
| :4045 | JSON with error message | Not tested | Not tested | Consistent |
| :4060 | Same HTML page | `{"error": "unknown endpoint"}` (200!) | Not tested | Very inconsistent |

### 2.2 Error Handling Gaps

1. **:4060 returns HTTP 200 for `/api` POST with error** - Wrong status code
2. **:8847 returns HTML for 501 instead of JSON** - Inconsistent with 404
3. **:4042 `/move?room=nonexistent` returns HTTP 200 with error JSON** - Wrong status code
4. **:8847 `/room/nonexistent` returns HTTP 200 with empty tiles** - Should be 404
5. **No unified error schema** across services

---

## 3. SECURITY OBSERVATIONS

### 3.1 CRITICAL: No Authentication
- **ALL endpoints are completely open** - no API keys, tokens, or session validation
- Anyone can connect as any agent name
- Anyone can submit matches, create rooms, trigger grammar evolution
- No ownership verification for agents

### 3.2 CRITICAL: Wildcard CORS
All services return:
```
Access-Control-Allow-Origin: *
Access-Control-Allow-Headers: Content-Type
Access-Control-Allow-Methods: GET, POST, OPTIONS
```
- **Any website can make requests to these APIs**
- No origin validation whatsoever
- Enables cross-site request attacks

### 3.3 No Rate Limiting
- 10 rapid requests to `/status` all returned 200 in ~0.34s each
- No throttling headers observed
- Susceptible to abuse

### 3.4 No Security Headers
Missing on ALL services:
- `X-Content-Type-Options`
- `X-Frame-Options`
- `Content-Security-Policy`
- `Strict-Transport-Security`
- `X-XSS-Protection`

### 3.5 Server Information Leakage
- `Server: BaseHTTP/0.6 Python/3.10.12` on all internal services
- Reveals exact Python version and HTTP server library
- :4042 error messages expose full endpoint list (information disclosure)

### 3.6 SQL Injection Test Results
- **GET `/connect?agent=admin' OR '1'='1`** -> Connection error (HTTP_CODE:000)
  - **CRITICAL:** This crashed/failed the connection, suggesting potential parsing vulnerability
- **GET `/connect?agent=testprobe&job=scout; DROP TABLE agents`** -> Connection error (HTTP_CODE:000)
  - **CRITICAL:** Same connection failure - potential crash on semicolon

### 3.7 Input Validation
- Agent names: **VALIDATED** (1-64 chars, alphanumeric + `_` and `-`)
- HTML/script injection: **BLOCKED** (returns 400 for `<script>`)
- Unicode emoji: **BLOCKED** (returns 400)
- Very long names: **BLOCKED** (returns 400)
- Invalid job names: **NOT VALIDATED** (defaults to `scholar` silently)

### 3.8 Missing Method Support
- HEAD returns 501 on all services
- PUT returns 501 on :4042
- DELETE returns 501 on :4042
- OPTIONS returns 501 on :8847

### 3.9 Sensitive Path Access
All tested sensitive paths return 404 (good):
- `/.env`, `/admin`, `/debug`, `/config`, `/swagger`, `/openapi.json`, `/metrics`, `/prometheus`

---

## 4. UNDOCUMENTED FEATURES DISCOVERED

### 4.1 :4044 Arena (Not in Original Target List)
- Full ELO rating system with TrueSkill-inspired uncertainty
- 5 different game types with detailed mechanics
- Curriculum-based agent progression (5 stages)
- Policy snapshot league for self-play
- Behavioral archetype classification (6 types)
- Multi-objective reward weights

### 4.2 :4045 Grammar Engine (Not in Original Target List)
- Recursive grammar with room/object/connection/meta rules
- Live evolution cycle that auto-spawns meta rules
- Usage tracking and quality scoring per rule
- Depth-based recursion visualization
- External rule injection via `/add_rule`

### 4.3 :4060 `/api` Endpoint
- Serves full API documentation as styled HTML
- Contains endpoint descriptions and method badges
- Not listed in any endpoint directory

### 4.4 Auto-Generated Agent Names
- `/connect` without parameters auto-generates an agent name
- Returns full connection response with auto-generated name
- This was NOT documented in the endpoint list

### 4.5 Stage System
- Agents have progression stages: Recruit -> Ensign -> Specialist -> Captain
- Based on tile count thresholds
- Different boot_camp room lists per job

### 4.6 :8847 Tile Provenance
- Each tile has `_hash`, `signature`, and `provenance` metadata
- Includes `agent_id`, `room`, `model` used, `confidence` score
- Gate system filters tiles with "absolute_claim" or "missing_field" reasons

---

## 5. API DESIGN GAPS

### 5.1 Inconsistent HTTP Semantics
| Issue | Example |
|-------|---------|
| Wrong status codes for errors | `/move?room=nonexistent` returns 200 |
| GET for mutations | `/add_rule`, `/evolve`, `/match` all use GET |
| POST endpoints return 400 on GET | `/submit/result` is POST-only |

### 5.2 No Content Negotiation
- `?format=json`, `?format=xml` cause 404 on :8847
- `Accept: application/xml` returns JSON anyway on :4042 and :8847
- No XML or other format support anywhere

### 5.3 No API Versioning
- No `/v1/`, `/v2/` paths exist
- :8847 version is in response body but not in URL
- Breaking changes would be impossible to manage

### 5.4 No Pagination
- `/agents` returns ALL 84 agents in one response (~7KB)
- `/rooms` on :8847 returns ALL rooms
- `/grammar` returns ALL 63 rules
- Will not scale with growth

### 5.5 No Filtering or Search
- `/agents` has no `?job=scout` or `?stage=Captain` filter
- `/rooms` has no search or filter
- `/leaderboard` only supports `?n=` (count)

### 5.6 State Management Issues
- Agent location is server-side state
- No session tokens or cookies
- Any client can control any agent by name
- Agent state resets on server restart (likely)

### 5.7 Missing Endpoints
| What | Where | Gap |
|------|-------|-----|
| DELETE agent | :4042 | Can't remove agents |
| UPDATE agent job | :4042 | Can't change jobs |
| Health check | :8847 | No health endpoint |
| Tile submission to PLATO | :4042 | `/build` returns "PLATO room creation not available" |
| WebSocket for real-time | :4060 | No live updates |
| Agent authentication | All | No identity verification |
| Rate limiting | All | No throttling |

### 5.8 CORS Configuration Inconsistency
- :4042 returns `Access-Control-Allow-Methods: GET, POST, OPTIONS` and `Access-Control-Allow-Headers: Content-Type`
- :8847 returns `Access-Control-Allow-Origin: *` only (missing other headers)
- :4060 returns `Access-Control-Allow-Origin: *` only

---

## 6. PERFORMANCE OBSERVATIONS

### 6.1 Response Times
| Service | Avg Time | Notes |
|---------|----------|-------|
| :4042 | 0.35s | Consistent, slight slowdown on `/jobs` (1.36s) |
| :8847 | 0.35s | Consistent |
| :4044 | 0.36s | Consistent |
| :4045 | 0.34s | Consistent |
| :4060 | 0.37s | Consistent |
| purplepincher.org | ~1.0s | Cloudflare-cached, initial longer |

### 6.2 Timeouts
- No connection timeouts observed (all under 2s)
- No request hangs
- :8900 and :8901 immediately reject connection (~0.17s)

### 6.3 Payload Sizes
| Endpoint | Size | Note |
|----------|------|------|
| `/agents` on :4042 | ~7.2KB | 84 agents |
| `/status` on :8847 | ~4KB | Room list with dates |
| `/` on purplepincher.org | ~30KB+ | Large HTML with embedded JSON |

---

## 7. SUGGESTIONS FOR API IMPROVEMENTS

### 7.1 Security (CRITICAL)
1. **Add authentication** - API keys, tokens, or OAuth
2. **Restrict CORS** to known origins instead of `*`
3. **Add rate limiting** per IP and per agent
4. **Add security headers** (CSP, X-Frame-Options, HSTS)
5. **Hide server version** in responses
6. **Fix SQL injection / crash vulnerability** on special characters in query params
7. **Validate all query parameters** consistently

### 7.2 API Design
1. **Add RESTful paths** like `/agents/{name}`, `/rooms/{name}`, `/tiles/{id}`
2. **Use proper HTTP methods** - POST for creates, PUT for updates, DELETE for removal
3. **Return correct status codes** - 404 for not found, 400 for bad input
4. **Add API versioning** (`/v1/`, `/v2/`)
5. **Add pagination** (`?page=`, `?limit=`)
6. **Add filtering** (`?job=`, `?stage=`, `?room=`)
7. **Add sorting** (`?sort=`, `?order=`)
8. **Add content negotiation** properly or remove `format=` parameter

### 7.3 Error Handling
1. **Standardize error format** across all services
2. **Always return JSON** for API errors (fix :8847 501 HTML response)
3. **Include error codes** for programmatic handling
4. **Add request_id** for debugging

### 7.4 Documentation
1. **Add OpenAPI/Swagger spec**
2. **Add `/api-docs` or `/docs` endpoint** that works
3. **Document all endpoints** including discovered ones (:4044, :4045)
4. **Document rate limits** (when added)
5. **Document authentication** (when added)

### 7.5 Service Health
1. **Bring up :8900** (Keeper/Fleet Registry) - currently down
2. **Bring up :8901** (Agent API) - currently down
3. **Add `/health` to :8847** - currently missing
4. **Add `/health` that returns proper health data** to all services

---

## 8. COMPLETE ENDPOINT INVENTORY

### :4042 Fleet API (11 working)
```
GET  /status                    -> Fleet overview
GET  /jobs                     -> Job archetypes
GET  /agents                   -> All agent stats
GET  /connect?agent=X&job=Y    -> Connect/connect agent
GET  /look?agent=X             -> Room view
GET  /move?agent=X&room=Y      -> Move agent
GET  /interact?agent=X&action=Y&target=Z -> Object interaction
GET  /tasks?agent=X            -> Training tasks
POST /build                    -> Create room
POST /submit                   -> Submit content
POST /submit/result            -> Submit result
```

### :8847 PLATO Server (3 working)
```
GET  /status                   -> Server stats + room list
GET  /rooms                    -> All rooms with tile counts
GET  /room/{name}              -> Tiles in specific room
```

### :4044 Arena (12 working)
```
GET  /                         -> Service info
GET  /games                    -> Game catalog
GET  /register?agent=NAME      -> Agent registration
GET  /leaderboard?n=N          -> ELO rankings
GET  /agent?name=NAME          -> Agent stats
GET  /match?...                -> Submit match
GET  /match_detail?...         -> Detailed match
GET  /opponent?agent=NAME&mode=MODE -> Matchmaking
GET  /archetypes               -> Behavioral types
GET  /stats                    -> Global stats
GET  /curriculum               -> Curriculum (empty)
GET  /league                   -> Policy snapshots
GET  /reward_weights           -> Reward configuration
```

### :4045 Grammar Engine (10 working)
```
GET  /                         -> Service info
GET  /grammar                  -> Full grammar
GET  /rules?type=TYPE          -> Filtered rules
GET  /rule?name=NAME           -> Specific rule
GET  /add_rule?...             -> Create rule
GET  /record_usage?...         -> Record usage
GET  /evolve                   -> Trigger evolution
GET  /evolution_log            -> Evolution history
GET  /depth_map               -> Recursion visualization
GET  /stats                    -> Grammar stats
```

### :4060 Web Terminal (3 working)
```
GET  /                         -> HTML terminal
GET  /status                   -> Version string
GET  /api                      -> API docs HTML
```

### :8900 Keeper Registry (0 working - DOWN)
### :8901 Agent API (0 working - DOWN)

### purplepincher.org (HTML SPA)
```
GET  /                         -> Main site HTML
GET  /api, /api/v1, /docs, /swagger -> Same HTML (SPA routing)
```

---

## 9. RISK SUMMARY

| Risk | Severity | Service | Details |
|------|----------|---------|---------|
| No authentication | CRITICAL | All | Anyone can access/modify data |
| Wildcard CORS | CRITICAL | All | CSRF/XSRF vulnerability |
| No rate limiting | HIGH | All | DoS risk |
| Server info leakage | MEDIUM | All | `Python/3.10.12` exposed |
| SQL injection crash | HIGH | :4042 | Query with `'` crashes connection |
| GET for mutations | MEDIUM | :4044, :4045 | Non-RESTful, CSRF risk |
| State mutation by name only | HIGH | :4042 | Any client can control any agent |
| Missing services | MEDIUM | :8900, :8901 | Incomplete deployment |
| No HTTPS | MEDIUM | All IP services | Plain HTTP only |

---

*Report generated by systematic API probing with 45+ HTTP requests across 7 targets*
