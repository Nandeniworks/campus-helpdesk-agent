# Part C: Lifecycle Hook Evidence & Verification Log

**Component:** `campus-helpdesk` Plugin Lifecycle Hook (`PreToolUse`)  
**Hook Configuration:** `campus-helpdesk/plugin/campus-helpdesk/hooks.json`  
**Hook Implementation:** `campus-helpdesk/plugin/campus-helpdesk/hooks/protect_folder.py`  
**Execution Environment:** Python 3 (stdio JSON-RPC payload interface)  
**Verification Date:** November 2026  

---

## 1. Test Overview and Objective

The `protected-directory-guard` is a `PreToolUse` lifecycle hook designed to intercept tool calls before execution. Its primary objective is to enforce hard write-protection on critical academic datasets (e.g., `campus-helpdesk/data/mock/timetable.csv`, `.git/`, and protected directories) while allowing benign file writes and non-destructive operations.

To verify the hook without performing destructive modifications on disk, three simulated tool-call payloads were piped directly to `protect_folder.py` via `sys.stdin`, and the resulting JSON decisions (`allow` vs. `deny`) were evaluated.

---

## 2. Test Execution Matrix

| Test ID | Test Scenario | Target Operation / Payload | Expected Decision | Actual Decision | Status |
|:---:|---|---|:---:|:---:|:---:|
| **HK-01** | **Safe File Write** | `write_file` to unconstrained path (`sandbox/student_notes.txt`) | `allow` | `allow` | **PASS** |
| **HK-02** | **Protected File Write Block** | `write_file` to protected timetable (`campus-helpdesk/data/mock/timetable.csv`) | `deny` | `deny` | **PASS** |
| **HK-03** | **Destructive Command Block** | `run_command` executing `rm -rf campus-helpdesk/data/protected` | `deny` | `deny` | **PASS** |

---

## 3. Detailed Test Exchanges

### Test 1: Safe File Write (HK-01)
* **Objective:** Confirm that the hook allows standard, unconstrained file writing outside protected paths.
* **Input Payload (`sys.stdin`):**
  ```json
  {
    "toolCall": {
      "name": "write_file",
      "args": {
        "Path": "sandbox/student_notes.txt"
      }
    }
  }
  ```
* **Actual Output (`sys.stdout`):**
  ```json
  {"decision": "allow"}
  ```
* **Evaluation:** **PASS**. The target path does not match any pattern in `PROTECTED_PATTERNS`, so the hook permits normal execution.

---

### Test 2: Protected File Write Block (HK-02)
* **Objective:** Verify that the hook intercepts and denies write operations targeting the official mock timetable dataset.
* **Input Payload (`sys.stdin`):**
  ```json
  {
    "toolCall": {
      "name": "write_file",
      "args": {
        "Path": "campus-helpdesk/data/mock/timetable.csv"
      }
    }
  }
  ```
* **Actual Output (`sys.stdout`):**
  ```json
  {
    "decision": "deny",
    "reason": "Security Alert: Write operation to protected path 'campus-helpdesk/data/mock/timetable.csv' blocked by campus-helpdesk safety hook."
  }
  ```
* **Evaluation:** **PASS**. The hook matched `r"campus-helpdesk/data/mock/timetable\.csv"` in `PROTECTED_PATTERNS`, rejected the tool call, and returned a structured security alert without altering the file.

---

### Test 3: Destructive Shell Command Block (HK-03)
* **Objective:** Verify that the hook inspects `run_command` arguments and intercepts destructive shell patterns targeting protected resources.
* **Input Payload (`sys.stdin`):**
  ```json
  {
    "toolCall": {
      "name": "run_command",
      "args": {
        "CommandLine": "rm -rf campus-helpdesk/data/protected"
      }
    }
  }
  ```
* **Actual Output (`sys.stdout`):**
  ```json
  {
    "decision": "deny",
    "reason": "Security Alert: Destructive shell command targeting protected resources blocked by campus-helpdesk safety hook."
  }
  ```
* **Evaluation:** **PASS**. The hook matched `r"\brm\s+-[rf]*\s+.*protected"` in `DESTRUCTIVE_COMMAND_PATTERNS` and blocked the shell invocation.

---

## 4. Summary & Verification Conclusion

All 3 simulated test cases passed with exit code 0 and deterministic JSON responses. The hook logic effectively separates safe workspace modifications from restricted dataset modifications, establishing an automated pre-execution defense against accidental data overwrites and unauthorized tool execution.

