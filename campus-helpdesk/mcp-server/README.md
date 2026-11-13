# Campus Helpdesk MCP Server

A reference implementation of a Model Context Protocol (MCP) server providing live campus data over standard input/output (`stdio`).

## Primitives Exposed

### 1. Tools
* **`get_timetable(batch: str, day: str) -> str`**:
  Queries the mock campus timetable database for classes scheduled for a specific student batch and weekday.
* **`get_fee_status(student_id: str) -> str`**:
  Retrieves financial ledger status, total tuition fees, payments made, pending dues, and due dates for a given student ID (enforcing format `STU\d{3}`).

### 2. Resources
* **`hostel://rules`**:
  Serves the official university hostel rules and conduct guidelines document (Markdown format).

---

## Installation & Setup

1. **Prerequisites**:
   * Python 3.10+ (tested with Python 3.15).
   * Virtual environment support.

2. **Setup Environment**:
   ```bash
   cd campus-helpdesk/mcp-server
   python3 -m venv .venv
   source .venv/bin/activate
   pip install mcp
   ```

---

## Running the Server

Run directly as a stdio server:
```bash
python3 campus_helpdesk_server.py
```

The server listens on `stdin` for JSON-RPC 2.0 messages and outputs responses to `stdout`.

---

## Automated Protocol Verification & Testing

An automated JSON-RPC 2.0 test client is included in `tests/test_mcp_server.py`:
```bash
python3 tests/test_mcp_server.py
```
This script exercises:
1. `initialize` capability negotiation.
2. `tools/list` schema validation.
3. `resources/list` and `resources/read`.
4. `tools/call` for `get_timetable` and `get_fee_status`.
5. Error handling on malformed student ID inputs.
Logs are saved to `evidence/mcp/raw_rpc_exchange.json`.
