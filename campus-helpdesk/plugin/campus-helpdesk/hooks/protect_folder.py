#!/usr/bin/env python3
"""
PreToolUse lifecycle hook script for campus-helpdesk plugin.
Inspects tool calls before execution and blocks write/edit operations
targeting protected folders and critical campus datasets.
"""

import sys
import json
import re

PROTECTED_PATTERNS = [
    r"campus-helpdesk/data/mock/timetable\.csv",
    r"campus-helpdesk/data/protected/.*",
    r".*/protected/.*",
    r"\.git/.*"
]

DESTRUCTIVE_COMMAND_PATTERNS = [
    r"\brm\s+-[rf]*\s+.*protected",
    r"\brm\s+-[rf]*\s+.*timetable\.csv",
    r">\s*.*timetable\.csv"
]


def check_tool_call():
    try:
        raw_input = sys.stdin.read()
        if not raw_input.strip():
            # No input provided, allow
            print(json.dumps({"decision": "allow"}))
            return

        payload = json.loads(raw_input)
        tool_call = payload.get("toolCall", {})
        tool_name = tool_call.get("name", "")
        args = tool_call.get("args", {})

        # 1. File modification tools
        if tool_name in ["write_file", "edit_file"]:
            target_path = args.get("Path", "")
            for pattern in PROTECTED_PATTERNS:
                if re.search(pattern, target_path):
                    result = {
                        "decision": "deny",
                        "reason": f"Security Alert: Write operation to protected path '{target_path}' blocked by campus-helpdesk safety hook."
                    }
                    print(json.dumps(result))
                    return

        # 2. Command execution tools
        elif tool_name == "run_command":
            command = args.get("CommandLine", "")
            for pattern in DESTRUCTIVE_COMMAND_PATTERNS:
                if re.search(pattern, command):
                    result = {
                        "decision": "deny",
                        "reason": f"Security Alert: Destructive shell command targeting protected resources blocked by campus-helpdesk safety hook."
                    }
                    print(json.dumps(result))
                    return

        # Default: allow execution
        print(json.dumps({"decision": "allow"}))

    except Exception as e:
        # Fail-safe: if hook script encounters unexpected error, ask user
        print(json.dumps({
            "decision": "ask",
            "reason": f"Safety hook encountered validation error: {str(e)}"
        }))


if __name__ == "__main__":
    check_tool_call()
# Path normalization patch
