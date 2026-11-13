# Campus Helpdesk Plugin (`campus-helpdesk`)

A comprehensive, production-ready AI Agent Plugin designed for the Google Antigravity and Agent Toolchain ecosystem.

## Overview

The `campus-helpdesk` plugin packages academic assistance tools into a single installable unit:
1. **Agent Skill**: `timetable-helper` for natural language student schedule queries.
2. **Custom Slash Command**: `/check-timetable <BATCH> <DAY>` for direct schedule lookups.
3. **Safety Hook**: `protected-directory-guard` (PreToolUse) enforcing write protection on critical datasets.
4. **MCP Server Integration**: Configuration for the `campus-helpdesk-mcp` stdio server.

---

## Plugin Directory Structure

```text
campus-helpdesk/
├── plugin.json                 # Plugin manifest
├── hooks.json                  # Lifecycle hooks configuration
├── mcp_config.json             # MCP server configuration
├── README.md                   # Plugin documentation
├── commands/
│   └── check-timetable.md      # Custom slash command definition
├── hooks/
│   └── protect_folder.py       # PreToolUse write protection script
└── skills/
    └── timetable-helper/       # Bundled timetable helper skill
        ├── SKILL.md
        ├── references/
        │   └── timetable-format.md
        └── scripts/
            └── timetable_helper.py
```

---

## Installation, Verification, and Lifecycle Operations

### Step 1: Add / Register Marketplace
To add the local or remote plugin marketplace catalog in Antigravity:
```bash
# Register the marketplace catalog in your workspace configuration
agy plugin marketplace add ./campus-helpdesk/plugin/marketplace.json
```

### Step 2: Install the Plugin
```bash
# Install plugin from the registered marketplace
agy plugin install campus-helpdesk
```
Alternatively, for workspace-level development, copy or symlink the plugin folder into `.agents/plugins/campus-helpdesk/` or configure `~/.gemini/config/plugins/campus-helpdesk/`.

### Step 3: Verify the Plugin is Loaded
1. Check installed plugin status via CLI:
   ```bash
   agy plugin list
   ```
2. Verify in active conversation:
   * Ask: *"What classes does CSE-A have on Monday?"* (Verifies `timetable-helper` skill activation).
   * Run slash command: `/check-timetable CSE-A Monday`.
   * Test write gate: Attempt to write to `campus-helpdesk/data/mock/timetable.csv` and verify the `protected-directory-guard` hook blocks execution.

### Step 4: Uninstall / Disable
* **Disable Plugin (without removing files):**
  ```bash
  agy plugin disable campus-helpdesk
  ```
* **Uninstall Plugin:**
  ```bash
  agy plugin uninstall campus-helpdesk
  ```
