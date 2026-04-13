# Repo-as-State Agent Architecture (RASA)

## Core Principles
1. **GitHub repo IS the agent's brain** - No external state
2. **Resets are normal** - Each session starts from scratch
3. **Files over memory** - Everything persistent is in version control
4. **Self-correcting** - New sessions can detect and fix broken states

## File Structure

```
.github/workflows/
    agent-integrity.yml  # Automated repo validation on push
    auto-snapshot.yml    # Periodic state snapshots

agent/
    BOOT.md              # Primary startup (max 200 lines)
    STATE.yml            # Current tasks/status (YAML)
    CONTEXT.md           # Last N sessions (rolling)
    LESSONS.md           # Permanent lessons
    skills/              # All available skills
        skill_registry.yml
        python/
            skill.py
            README.md
            version.txt
        web_scrape/
        data_analysis/
    snapshots/           # Automatic recovery points
        YYYY-MM-DD-HH-MM-SS/
            STATE.yml
            CONTEXT.md
    logs/
        session_001.md
        session_002.md

work/
    current/            # Active task files
    completed/          # Archived work
    queued/             # Upcoming tasks

system/
    integrity_check.py  # Detects broken states
    recovery_guide.md   # How to restore from corruption
```

## 1. BOOT.md (The 60-Second Bootstrap)

```markdown
# AGENT BOOTSTRAP v2.1
Agent: RASA (Repo-as-State Agent)
Boot Time Target: <60s
Max Tokens: 8,000

## IMMEDIATE ACTIONS (Do in order):
1. Read STATE.yml (current tasks/status)
2. Scan STATE.yml for `emergency: true` flags
3. Run integrity check: `python system/integrity_check.py`
4. If integrity failed:
   - Read system/recovery_guide.md
   - Execute recovery protocol
5. Load skills from STATE.yml's `active_skills` list
6. Read last 3 entries from CONTEXT.md
7. Check LESSONS.md for relevant recent lessons
8. Resume work per STATE.yml instructions

## SKIP ON BOOT (For efficiency):
- Don't read entire CONTEXT.md (only last N entries)
- Don't load inactive skills
- Don't parse full work history

## INTEGRITY CHECKS:
- Verify STATE.yml syntax
- Ensure active skills exist in skills/
- Check for orphaned task files in work/current
- Validate CONTEXT.md timestamp sequence

## RECOVERY PROTOCOL:
If STATE.yml corrupted:
1. Use latest snapshot from snapshots/
2. If snapshots corrupted, rebuild from work/completed/
3. Document corruption in LESSONS.md with timestamp

## CURRENT METADATA:
Last boot: 2024-01-15T14:30:00Z
Session count: 42
Uptime efficiency: 94.7%
Common failure modes logged in LESSONS.md#boot-failures
```

## 2. STATE.yml (Machine-Readable State)

```yaml
# STATE.yml - Machine readable current state
version: "3.0"
last_updated: "2024-01-15T14:35:00Z"
session_id: "session_043"

# Active Tasks (max 3 concurrent)
active_tasks:
  - id: "task_88"
    type: "code_refactor"
    file: "work/current/feature_x.py"
    status: "in_progress"
    started: "2024-01-15T14:20:00Z"
    last_action: "extracted helper function"
    next_action: "write unit tests"
    checkpoint: "refactoring/step_2"
    priority: 1

  - id: "task_89"
    type: "research"
    file: "work/current/api_integration.md"
    status: "paused"
    reason: "waiting_on_api_key"
    priority: 2

# Loaded Skills
active_skills:
  - "python/code_analysis"
  - "web_scrape/ethical"
  - "data_analysis/stats"

# Skill Registry State
skills_state:
  python/code_analysis:
    version: "1.2"
    last_used: "2024-01-15T14:30:00Z"
    memory_usage: "low"
  
  web_scrape/ethical:
    version: "2.0"
    constraints: ["robots.txt", "rate_limit_1s"]

# Session Management
session_metrics:
  tokens_used: 42000
  api_calls: 89
  files_modified: 12
  estimated_cost: "$0.87"

# Pending Bottlenecks
bottlenecks:
  - description: "API rate limited until 14:45"
    resolution_eta: "2024-01-15T14:45:00Z"
    workaround: "batch requests"

# Sweep Status
sweep:
  enabled: true
  last_sweep: "2024-01-15T13:00:00Z"
  next_sweep: "2024-01-15T15:00:00Z"
  issues_found: 3
  issues_fixed: 2

# Emergency Flags
emergency:
  corrupted_state: false
  infinite_loop_detected: false
  resource_exhaustion: false
  last_emergency: null

# Recovery Context
recovery_mode: false
last_backup: "2024-01-15T14:00:00Z"
integrity_score: 0.98
```

## 3. CONTEXT.md (Rolling Context Window)

```markdown
# ROLLING CONTEXT
Max entries: 50  (prune oldest when exceeded)
Format: Each entry = 100 tokens max

## Entry 48 (2024-01-15T14:30-14:35)
Session: 043 | Tasks: task_88(task_89(paused))
Actions: Refactored data_processor.py, extracted validation logic
Findings: Original code had race condition in cache
Next: Write tests for validation module
Result: COMPLETED (partial)

## Entry 47 (2024-01-15T13:45-14:30)
Session: 042 | Tasks: task_87(task_88(started))
Actions: Implemented WebSocket handler, fixed connection leak
Mistake: Forgot to handle ping/pong frames initially
Lesson: Added to LESSONS.md#websocket_basics
Result: COMPLETED

## Entry 46 (2024-01-15T13:00-13:45)
Session: 041 | Tasks: task_86
Actions: Researched vector databases, wrote comparison doc
Key finding: Pinecone vs Weaviate tradeoffs documented
Result: COMPLETED
...
[Entries 1-45 pruned - see snapshots/ for archive]
```

## 4. LESSONS.md (Permanent Knowledge)

```markdown
# HARD-WON KNOWLEDGE
Never prune. Add-only. Reference in CONTEXT entries.

## BOOT FAILURES
- 2024-01-10: Circular import in skills/python/ caused infinite load
  Fix: Add dependency checking to integrity_check.py
  Prevention: Skills must declare imports in skill_registry.yml

- 2024-01-05: STATE.yml corrupted by partial write during timeout
  Fix: Write to STATE.yml.tmp then rename atomically
  Prevention: system/integrity_check.py now validates JSON schema

## PERFORMANCE PATTERNS
- Web scraping > 100 pages needs exponential backoff
- SQL queries without LIMIT cause timeouts after 30s
- OpenAI API: temperature=0.2 gives most consistent code  

## ANTI-PATTERNS
- DON'T: Modify files outside work/ directory (causes git conflicts)
- DON'T: Load >5 skills simultaneously (token overflow)
- DON'T: Start task without checkpoint in STATE.yml

## SUCCESS PATTERNS
- DO: Create checkpoint after each logical unit
- DO: Use work/current/ for active, move to work/completed/ when done
- DO: Tag difficult problems in CONTEXT.md with #challenge
```

## 5. Skill Equip/De-equip Protocol

```yaml
# skills/skill_registry.yml
skills:
  python/code_analysis:
    version: "1.2"
    description: "Analyze and refactor Python code"
    location: "skills/python/"
    dependencies: ["python/ast_parser"]
    token_cost: 1200
    max_concurrent: 2
    compatibility: ["STATE_v2+", "CONTEXT_v3+"]
    load_instructions: |
      1. Read skills/python/README.md
      2. Import skills/python/skill.py
      3. Initialize with config from STATE.yml
    unload_instructions: |
      1. Save any state to skills/python/state.json
      2. Remove from active_skills in STATE.yml
    last_updated: "2024-01-14"
    
  web_scrape/ethical:
    version: "2.0"
    constraints: ["rate_limiting", "robots_txt"]
    requires_approval: true

# Protocol for modifying skills
equip_skill:
  1. Check compatibility in skill_registry.yml
  2. Add to STATE.yml active_skills
  3. Load per skill's load_instructions
  4. Log in CONTEXT.md: "Equipped skill X vY"

deequip_skill:
  1. Run skill's unload_instructions
  2. Remove from STATE.yml active_skills  
  3. Create snapshot if skill had state
  4. Log in CONTEXT.md: "Deequipped skill X, reason R"
```

## Self-Correction Mechanism

### Detection of Broken Sessions:
```python
# system/integrity_check.py
def detect_broken_session():
    checks = [
        STATE_exists_and_valid(),
        CONTEXT_has_no_gaps(),
        active_tasks_have_files(),
        skills_exist_and_loadable(),
        no_orphaned_files_in_current(),
        git_status_clean()
    ]
    
    if sum(checks) < len(checks) * 0.8:  # 80% threshold
        return "BROKEN"
    elif STATE.yml['emergency']['infinite_loop_detected']:
        return "EMERGENCY"
    else:
        return "HEALTHY"
```

### Recovery Workflow:
1. **Detect** → Integrity check fails
2. **Diagnose** → Check which component(s) failed
3. **Restore** → Use latest valid snapshot
4. **Document** → Add failure to LESSONS.md
5. **Resume** → Continue from restored state

### Prevention Strategies:
- **Atomic writes**: Write to .tmp then rename
- **Checkpoints**: Snapshot before risky operations
- **Validation**: Schema validation for all YAML/JSON
- **Timeouts**: Auto-kill tasks exceeding time limit
- **Git hygiene**: Frequent commits with descriptive messages

## Efficiency Optimizations

### Boot-Time Token Budget:
- BOOT.md: 200 lines (800 tokens)
- STATE.yml: ~500 tokens  
- CONTEXT.md (last 3 entries): 300 tokens
- Relevant LESSONS.md: 400 tokens
- Skill loading: Variable (limit 3 skills = ~3600 tokens)
- **Total target**: <6000 tokens

### Smart Loading:
```yaml
# In BOOT.md - Priority loading
high_priority:
  - STATE.yml integrity
  - Active task files
  - Currently loaded skills
  
medium_priority:
  - Last session's CONTEXT
  - Related LESSONS
  
low_priority: (load on demand)
  - Full CONTEXT history
  - Inactive skills
  - Completed work archives
```

## Session Lifecycle

1. **Boot**: Read BOOT.md → STATE.yml → integrity check
2. **Recover if needed**: Restore from latest snapshot
3. **Load context**: Recent entries + relevant lessons
4. **Execute**: Follow STATE.yml task list
5. **Checkpoint**: Every 15 minutes auto-snapshot
6. **Cleanup**: Move completed tasks, prune CONTEXT.md
7. **Commit**: Git commit with session summary
8. **Terminate**: Update STATE.yml with session end time

This architecture ensures each reset starts from a clean but informed state, can detect and recover from corruption, and maintains efficiency through selective loading of only essential state.
