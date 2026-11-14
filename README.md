# Campus Helpdesk Agent

A complete implementation for **Assignment 8 – Building and Auditing an AI-Agent Toolchain** (AI Tools and Prompt Engineering).

This project implements and audits an AI-agent toolchain for a university campus helpdesk scenario, demonstrating Agent Skills, custom plugins, the Model Context Protocol (MCP), and Git worktrees on mock campus data.

---

## Architecture & Directory Structure

```text
campus-helpdesk-agent/
├── .agents/                                       # Workspace skill discovery root
│   └── skills/timetable-helper/                   # Live timetable helper skill
├── campus-helpdesk/                               # Core application components
│   ├── data/mock/                                 # Mock campus data datasets
│   │   ├── timetable.csv                          # Academic schedule database
│   │   ├── fees.csv                               # Student fee ledger database
│   │   └── hostel_rules.md                        # Official campus hostel rules resource
│   ├── skills/timetable-helper/                   # Part B: Standalone Agent Skill
│   │   ├── SKILL.md                               # Frontmatter & anti-hallucination rules
│   │   ├── references/timetable-format.md         # Progressive disclosure: schema reference
│   │   └── scripts/timetable_helper.py            # Extraction helper script
│   ├── plugin/                                    # Part C: Plugin distribution bundle
│   │   ├── marketplace.json                       # Agent Marketplace catalog entry
│   │   └── campus-helpdesk/                       # Unified plugin package
│   │       ├── plugin.json                        # Plugin manifest
│   │       ├── hooks.json                         # PreToolUse security write guard
│   │       ├── mcp_config.json                    # MCP server integration config
│   │       ├── README.md                          # Plugin user guide
│   │       ├── commands/check-timetable.md        # Tool-specific command definition (Claude Code)
│   │       ├── hooks/protect_folder.py            # Safety hook script
│   │       └── skills/                            # Bundled skills (invokable as slash commands)
│   │           ├── check-timetable/               # Antigravity native /check-timetable command
│   │           └── timetable-helper/              # Bundled timetable-helper skill
│   └── mcp-server/                                # Part D: Model Context Protocol Server
│       ├── campus_helpdesk_server.py              # Stdio MCP server (mcp 2.x SDK)
│       ├── README.md                              # Run & integration guide
│       └── tests/test_mcp_server.py               # Automated JSON-RPC 2.0 test suite
├── evidence/                                      # Experimental evidence & audits
│   ├── skill/                                     # Part B prompt matrices & rewrites
│   │   ├── skill_test_matrix.md                   # 6-prompt test evaluation
│   │   ├── adversarial_test.md                    # Adversarial test & anti-hallucination
│   │   └── description_rewrites.md                # Broad vs narrow sensitivity analysis
│   ├── plugin/                                    # Part C threat model & lifecycle
│   │   └── plugin_threat_model.md                 # 3 core threats & concrete mitigations
│   ├── mcp/                                       # Part D MCP traces & audits
│   │   ├── protocol_exchange.md                   # Annotated JSON-RPC handshake & calls
│   │   ├── nimbus_package_audit.md                # Audit of fake @nimbus/mcp-skill-bridge
│   │   └── raw_rpc_exchange.json                  # Live captured JSON-RPC traces
│   ├── worktrees/                                 # Part E worktree logs & graph
│   │   └── worktree_evidence.md                   # Worktree list, conflict & graph
│   └── reflection.md                              # Part F 300-word architectural reflection
├── prompt-log/                                    # Prompt log & verification journal
│   └── prompt-log.txt                             # Actual prompts & 5 AI detection catches
├── tests/                                         # Test suites
│   └── test_timetable_helper.py                   # Automated Skill unit test suite
├── README.md
└── .gitignore
```

---

## Key Components

### 1. Part B: Timetable Helper Skill
* Implements progressive disclosure: lightweight `SKILL.md` (metadata and instructions), `references/timetable-format.md` (CSV column dictionary), and `scripts/timetable_helper.py` (deterministic CSV extraction).
* Strict anti-hallucination guardrails: Prevents inventing classes, faculty, or timings when not found in official records.
* Verified against positive, negative, and ambiguous prompts, plus adversarial prompt injection attempts.

### 2. Part C: Campus Helpdesk Plugin Bundle
* Bundles `timetable-helper` Skill, `/check-timetable` slash command (implemented via native Antigravity skill `skills/check-timetable/SKILL.md` while retaining `commands/check-timetable.md` for tool-specific compatibility), and `campus-helpdesk-mcp` server.
* Implements a `PreToolUse` safety hook (`hooks.json` + `hooks/protect_folder.py`) that hard-blocks unauthorized modifications to protected campus records.
* Includes threat modeling covering prompt injection through skills, malicious hooks, and MCP tool description poisoning.
* Documents supported lifecycle commands (`agy plugin validate --strict`, `install`, `list`, `uninstall`) and notes marketplace catalog registration limitations per official documentation.
* Detects and avoids the adversarial honeypot ("NimbusSync Plugin Standard v4.2").

### 3. Part D: Model Context Protocol (MCP) Server
* Implemented over `stdio` using the official `mcp` 2.x Python SDK.
* Exposes two tools:
  * `get_timetable(batch, day)`
  * `get_fee_status(student_id)`
* Exposes one resource:
  * `hostel://rules` (serving `hostel_rules.md`)
* Audited and refuted the fake package `@nimbus/mcp-skill-bridge`.
* Fully tested with automated JSON-RPC 2.0 handshake and error handling validation.

### 4. Part E: Git Worktrees
* Simulated three parallel workstreams on linked worktrees: `feature/skill-tests`, `feature/mcp-server`, and `bugfix/hook-path`.
* Created, reproduced, and manually resolved a merge conflict on `README.md`.
* Debunked the fabricated `/worktree-merge` Claude Code command.

### 5. Part F: Prompt Log & Verification
* Detailed journal maintained in `prompt-log/prompt-log.txt`.
* Documents 5 genuine AI fabrication catches with command outputs and official citations.
* Architectural reflection on the boundaries between Skills, Plugins, MCP, and Worktrees.

---

## Testing & Verification

Run the automated test suites from the repository root:

```bash
# 1. Run Timetable Helper Skill unit tests
python3 tests/test_timetable_helper.py

# 2. Run MCP Server JSON-RPC test client
campus-helpdesk/mcp-server/.venv/bin/python3 campus-helpdesk/mcp-server/tests/test_mcp_server.py

# 3. Test Safety Hook Denial
python3 campus-helpdesk/plugin/campus-helpdesk/hooks/protect_folder.py <<'EOF'
{"toolCall": {"name": "write_file", "args": {"Path": "campus-helpdesk/data/mock/timetable.csv"}}}
EOF
```

---

## Security & Ethics
All data used in this project is mock data. No real student IDs, names, or credentials are used.
