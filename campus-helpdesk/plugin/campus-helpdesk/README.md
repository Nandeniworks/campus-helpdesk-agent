# Campus Helpdesk Plugin (`campus-helpdesk`)

An academic prototype AI Agent Plugin using mock campus data, developed for the Google Antigravity and Agent Toolchain ecosystem.

## Overview

The `campus-helpdesk` plugin packages academic assistance tools into a single installable unit:
1. **Agent Skill**: `timetable-helper` for natural language student schedule queries.
2. **Custom Slash Command**: `/check-timetable <BATCH> <DAY>` for direct schedule lookups, implemented via Antigravity's native skill mechanism (`skills/check-timetable/SKILL.md`). In Antigravity, bundled skills can be invoked directly as `/<skill-name>`. The repository also retains `commands/check-timetable.md` as a tool-specific definition (e.g., for Claude Code), but official Antigravity documentation confirms that Antigravity ignores `commands/`.
3. **Safety Hook**: `protected-directory-guard` (`PreToolUse`) enforcing write protection on critical campus datasets.
4. **MCP Server Integration**: Configuration for the `campus-helpdesk-mcp` stdio server.

---

## Plugin Directory Structure

```text
campus-helpdesk/
├── plugin.json                 # Plugin manifest
├── hooks.json                  # Lifecycle hooks configuration
├── mcp_config.json             # MCP server configuration
├── README.md                   # Plugin documentation
├── commands/                   # Tool-specific command folder (ignored by Antigravity)
│   └── check-timetable.md      # Slash command definition for Claude Code compatibility
├── hooks/
│   └── protect_folder.py       # PreToolUse write protection script
└── skills/
    ├── check-timetable/        # Native Antigravity slash command wrapper (invoked as /check-timetable)
    │   └── SKILL.md
    └── timetable-helper/       # Bundled timetable helper skill
        ├── SKILL.md
        ├── references/
        │   └── timetable-format.md
        └── scripts/
            └── timetable_helper.py
```

---

## Plugin Lifecycle Operations

Official Antigravity documentation specifies the standard plugin lifecycle commands via the `agy` CLI:

### 1. Validate Plugin Manifest and Structure
Validate the local plugin directory against Antigravity's schema:
```bash
agy plugin validate --strict ./campus-helpdesk/plugin/campus-helpdesk
```

### 2. Install the Plugin
Install the plugin directly from the local directory:
```bash
agy plugin install ./campus-helpdesk/plugin/campus-helpdesk
```
Alternatively, for workspace-level development, the plugin can be copied or symlinked into `.agents/plugins/campus-helpdesk/` or configured in user config directories.

### 3. Verify Installed Plugin
Inspect installed plugins and active capabilities:
```bash
agy plugin list
# Or structured JSON output:
agy plugin list --json
```

### 4. Test Slash Command & Security Hook
1. Trigger `/check-timetable CSE-A Monday` and verify schedule table output retrieved from `campus-helpdesk/data/mock/timetable.csv`.
2. Attempt an unauthorized write:
   ```bash
   python3 campus-helpdesk/plugin/campus-helpdesk/hooks/protect_folder.py <<'EOF'
   {"toolCall": {"name": "write_file", "args": {"Path": "campus-helpdesk/data/mock/timetable.csv"}}}
   EOF
   ```
   *Expected Output:* The `PreToolUse` hook returns structured JSON blocking execution:
   ```json
   {"decision": "deny", "reason": "Security Alert: Write operation to protected path 'campus-helpdesk/data/mock/timetable.csv' blocked by campus-helpdesk safety hook."}
   ```

### 5. Disable and Uninstall
* **Disable Plugin (without removing files):**
  ```bash
  agy plugin disable campus-helpdesk
  ```
* **Uninstall Plugin:**
  ```bash
  agy plugin uninstall campus-helpdesk
  ```

---

## Notes on Marketplace Registration and Environment

1. **Marketplace Catalog Scope:**
   Official Antigravity documentation (`https://antigravity.google/docs/marketplace/`) documents discovering and installing plugins from the official marketplace catalog and installing from local directories (`agy plugin install <path>`). However, official documentation does not define a CLI command such as `agy plugin marketplace add` to register arbitrary custom marketplace catalogs. The included `marketplace.json` serves as the project's marketplace-ready metadata deliverable for catalog submission, rather than an independently registerable CLI catalog.

2. **Host Environment Status:**
   In this development environment, the `agy` binary is not installed on the system PATH (`zsh: command not found: agy`). All lifecycle commands documented above reflect the standard interface defined by official Google Antigravity documentation.

---

## Authoritative References
* Google Antigravity Plugin Development: `https://antigravity.google/docs/build-plugins` (Accessed: 14 November 2026)
* Google Antigravity Marketplace: `https://antigravity.google/docs/marketplace/` (Accessed: 14 November 2026)
* Google Antigravity Plugins Specification: `https://antigravity.google/docs/plugins` (Accessed: 14 November 2026)
