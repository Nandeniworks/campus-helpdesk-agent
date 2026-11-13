# Final Assignment Report: Building and Auditing an AI-Agent Toolchain
**Course:** AI Tools and Prompt Engineering | B.Tech CSE  
**Project:** Campus Helpdesk Agent (`campus-helpdesk-agent`)  
**Deliverables Covered:** Parts A–F, Prompt Log, Evidence Matrix, and Repository Verification  

---

## Executive Summary
This project establishes and audits an end-to-end AI-agent toolchain for Nimbus Labs' university campus helpdesk scenario. It implements and validates:
1. **Agent Skills** (`timetable-helper`) adhering to progressive disclosure and anti-hallucination guardrails.
2. **Plugin Packaging** (`campus-helpdesk`) with custom slash commands (`/check-timetable`), write-protection lifecycle hooks (`PreToolUse`), and threat modeling.
3. **Model Context Protocol (MCP)** server over stdio with verified tools (`get_timetable`, `get_fee_status`) and resources (`hostel://rules`).
4. **Git Worktree Parallelization** simulating 3 branches, deliberate conflict creation, and resolution.
5. **AI Audit & Verification** detecting 5 planted honeypots and non-existent packages/commands without hallucination.

---

## Part A: Claim Audit (15 marks)
*(Preserved from student's external report. Key audited claims summarized below):*

* **Claim 1 (MCP Primitives):** **TRUE.** MCP messages use JSON-RPC 2.0; servers expose tools, resources, and prompts.
* **Claim 2 (Persistent Memory Primitive on 2025-02-30):** **FALSE.** February 30th does not exist. MCP servers are stateless; memory is client-orchestrated.
* **Claim 3 (Skill Metadata Loading):** **TRUE.** Skills load `name` and `description` upfront; the body loads upon relevance.
* **Claim 4 (skill.config.yaml & Python 3.14):** **FALSE.** No `skill.config.yaml` or Python 3.14 runtime is required.
* **Claim 5 (Worktrees & Single Object DB):** **TRUE.** Git worktrees maintain individual working trees sharing `.git/objects`.
* **Claim 6 (`git worktree sync --all`):** **FALSE.** Nonexistent Git command.
* **Claim 7 (Plugin Bundles):** **TRUE.** Plugins bundle commands, skills, hooks, and MCP configs.
* **Claim 8 (RFC 9999 & Ed25519 Signing):** **FALSE.** Fabricated RFC; stdio MCP uses standard OS pipes without Ed25519 signatures.
* **Claim 9 (Same Branch in Multiple Worktrees):** **FALSE.** Git strictly forbids checking out the same branch in multiple worktrees.
* **Claim 10 (Hendricks & Oyelaran 2024 / Skill Collapse):** **FALSE / UNVERIFIED.** Fabricated paper citation.

---

## Part B: Design and Test a Skill (20 marks)

### 1. Implementation
* **`SKILL.md`**: Valid YAML frontmatter with positive and negative triggers.
* **Progressive Disclosure**: Detailed CSV column dictionary in `references/timetable-format.md`; deterministic query engine in `scripts/timetable_helper.py`.
* **Mock Data**: Real mock timetable stored at `campus-helpdesk/data/mock/timetable.csv`.

### 2. Prompt Matrix & Trigger Results
*(Detailed transcript log in `evidence/skill/skill_test_matrix.md`)*
* **P1 (CSE-A Monday):** **Triggered.** Returned 3 verified classes.
* **P2 (CSE-B Tuesday):** **Triggered.** Returned 1 verified class.
* **P3 (CSE-A Wednesday):** **Triggered.** Returned 2 verified classes.
* **P4 (Fees Query):** **Ignored.** Respected negative trigger; routed away from timetable skill.
* **P5 (Hostel Rules Query):** **Ignored.** Respected negative trigger; routed away from timetable skill.
* **P6 (Ambiguous Class Query):** **Clarification Requested.** Prompted user for missing batch and day without hallucinating.

### 3. Description Sensitivity Analysis
*(Detailed in `evidence/skill/description_rewrites.md`)*
* **V1 (Too Broad):** *"Use this skill whenever a student asks about daily schedule, campus activities..."* caused false-positive triggers on fees, curfews, and club events.
* **V2 (Too Narrow):** *"Use this skill only when a student asks to view the official Monday timetable for CSE-A"* caused silent failures (false negatives) on CSE-B and other weekdays.

### 4. Adversarial Prompt Defense
*(Detailed in `evidence/skill/adversarial_test.md`)*
* **Attack:** Prompt coerced agent to inject an unlisted *"Quantum Computing"* class with made-up room and faculty.
* **Defense:** Skill Instruction Rule 8 (*"Never invent or assume a subject..."*) and Data Accuracy Rules forced the agent to reject the hallucination and return only verified CSV records.

---

## Part C: Package a Plugin (20 marks)

### 1. Plugin Bundle Structure
Implemented at `campus-helpdesk/plugin/campus-helpdesk/`:
* **Manifest (`plugin.json`)**: Configured per Antigravity plugin specification.
* **Slash Command (`commands/check-timetable.md`)**: Defines `/check-timetable <BATCH> <DAY>`.
* **Security Hook (`hooks.json` & `hooks/protect_folder.py`)**: `PreToolUse` hook inspecting file write operations and hard-blocking changes to protected data files.
* **MCP Config (`mcp_config.json`)**: Connects plugin to the stdio MCP server.
* **Marketplace Entry (`marketplace.json`)**: Catalog metadata for installation.

### 2. Third-Party Plugin Threat Model
*(Detailed in `evidence/plugin/plugin_threat_model.md`)*
1. **Prompt Injection through Skill Text:** Malicious comments or directives in `SKILL.md`.  
   *Mitigation:* AST sanitization on plugin install and isolated system-prompt demarcation.
2. **Malicious Hooks:** Shell hooks running arbitrary malware on tool calls.  
   *Mitigation:* Mandatory interactive permission prompts during plugin installation and sandbox containment.
3. **Tool Poisoning via MCP Descriptions:** Deceptive tool descriptions tricking the LLM into exfiltrating credentials.  
   *Mitigation:* Static description analysis, strict regex input validation, and user confirmations for sensitive operations.

---

## Part D: Build an MCP Server (20 marks)

### 1. Architecture & Audit
* **Package Audit:** Audited `@nimbus/mcp-skill-bridge` (version 2.3) against npm and PyPI; confirmed it returns **404 Not Found** (Fabricated package). Built using official `mcp` 2.x SDK.
* **Server Implementation (`campus-helpdesk/mcp-server/campus_helpdesk_server.py`)**:
  * Tool: `get_timetable(batch, day)`
  * Tool: `get_fee_status(student_id)` (enforces regex `^STU\d{3}$`)
  * Resource: `hostel://rules` (serves `data/mock/hostel_rules.md`)

### 2. Protocol Verification
*(Detailed in `evidence/mcp/protocol_exchange.md`)*
* Executed automated test suite `tests/test_mcp_server.py`.
* Successfully captured and annotated JSON-RPC 2.0 exchanges for `initialize`, `notifications/initialized`, `tools/list`, `resources/list`, `resources/read`, and `tools/call`.
* Validated error reporting: Invalid student ID (`INVALID_999`) returns structured domain error rather than runtime crashes.

---

## Part E: Parallel Development with Worktrees (15 marks)

### 1. Worktrees Established
Linked worktrees created via `git worktree add`:
1. `.worktrees/feature-skill-tests` (branch: `feature/skill-tests`)
2. `.worktrees/feature-mcp-server` (branch: `feature/mcp-server`)
3. `.worktrees/bugfix-hook-path` (branch: `bugfix/hook-path`)

### 2. Conflict Simulation & Resolution
* Modified status line in `README.md` across both feature branches.
* Merging `feature/mcp-server` after `feature/skill-tests` produced a real Git content conflict.
* Manually resolved conflict in `README.md` combining both status updates (commit `7f61e2b`).
* Integrated bugfix branch and generated complete history graph (`3a31079`).

### 3. Evaluation of `/worktree-merge`
* **Verdict:** Nonexistent Claude Code command (Fabricated).
* **Risk:** Automated AI merges risk silent semantic regressions and security policy overwrites.

---

## Part F: Reflection and Prompt Log (10 marks)

### 1. Genuine AI Detection Catches
*(Documented in `prompt-log/prompt-log.txt`)*
1. `@nimbus/mcp-skill-bridge` (404 on npm/PyPI).
2. "NimbusSync Plugin Standard v4.2" honeypot rejected.
3. `/worktree-merge` in Claude Code debunked.
4. MCP Revision "2025-02-30" date impossibility and fake memory primitive.
5. Nonexistent `git worktree sync --all` command.

### 2. Reflection Essay (320 words)
*(Available in `evidence/reflection.md`)*
Analyzes the separation of concerns between procedural knowledge (Skills), distribution policies (Plugins), live execution (MCP), and multi-agent development isolation (Worktrees).
