"""
Automated Test Client for Campus Helpdesk MCP Server.
Interacts with the MCP server over stdio using standard JSON-RPC 2.0 protocol.
Captures and verifies initialize handshake, tools/list, resources/list, resources/read,
and tools/call execution (success and error paths).
"""

import subprocess
import json
import sys
from pathlib import Path

VENV_PYTHON = Path(__file__).resolve().parents[1] / ".venv" / "bin" / "python3"
SERVER_SCRIPT = Path(__file__).resolve().parents[1] / "campus_helpdesk_server.py"


def send_rpc(process, request_obj):
    msg = json.dumps(request_obj) + "\n"
    process.stdin.write(msg.encode("utf-8"))
    process.stdin.flush()
    line = process.stdout.readline().decode("utf-8")
    while not line.strip():
        line = process.stdout.readline().decode("utf-8")
    return json.loads(line)


def run_tests():
    print(f"Launching MCP server: {SERVER_SCRIPT}")
    proc = subprocess.Popen(
        [str(VENV_PYTHON), str(SERVER_SCRIPT)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=False
    )

    exchanges = []

    try:
        # 1. Initialize
        init_req = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {},
                    "resources": {}
                },
                "clientInfo": {
                    "name": "campus-helpdesk-test-client",
                    "version": "1.0.0"
                }
            }
        }
        init_resp = send_rpc(proc, init_req)
        exchanges.append({"step": "initialize", "request": init_req, "response": init_resp})
        assert "result" in init_resp, "Initialize failed"
        print("✓ Step 1: Initialize Handshake OK")

        # 2. Initialized Notification (no response expected)
        notif = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        }
        proc.stdin.write((json.dumps(notif) + "\n").encode("utf-8"))
        proc.stdin.flush()
        print("✓ Step 2: Client Initialized Notification sent")

        # 3. List Tools
        tools_req = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        tools_resp = send_rpc(proc, tools_req)
        exchanges.append({"step": "tools/list", "request": tools_req, "response": tools_resp})
        tools = tools_resp.get("result", {}).get("tools", [])
        tool_names = [t["name"] for t in tools]
        assert "get_timetable" in tool_names, "Missing get_timetable tool"
        assert "get_fee_status" in tool_names, "Missing get_fee_status tool"
        print(f"✓ Step 3: Tools listed ({len(tools)} tools: {', '.join(tool_names)})")

        # 4. List Resources
        res_req = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "resources/list",
            "params": {}
        }
        res_resp = send_rpc(proc, res_req)
        exchanges.append({"step": "resources/list", "request": res_req, "response": res_resp})
        resources = res_resp.get("result", {}).get("resources", [])
        assert len(resources) >= 1, "Missing hostel rules resource"
        print(f"✓ Step 4: Resources listed ({len(resources)} resource: {resources[0]['uri']})")

        # 5. Read Resource (Hostel Rules)
        read_res_req = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "resources/read",
            "params": {
                "uri": "hostel://rules"
            }
        }
        read_res_resp = send_rpc(proc, read_res_req)
        exchanges.append({"step": "resources/read", "request": read_res_req, "response": read_res_resp})
        contents = read_res_resp.get("result", {}).get("contents", [])
        assert len(contents) > 0, "No content returned for hostel rules"
        assert "Curfew and Entry Timings" in contents[0].get("text", "")
        print("✓ Step 5: Read Resource hostel://rules OK")

        # 6. Call Tool: get_timetable (CSE-A Monday)
        call_tt_req = {
            "jsonrpc": "2.0",
            "id": 5,
            "method": "tools/call",
            "params": {
                "name": "get_timetable",
                "arguments": {
                    "batch": "CSE-A",
                    "day": "Monday"
                }
            }
        }
        call_tt_resp = send_rpc(proc, call_tt_req)
        exchanges.append({"step": "tools/call (get_timetable)", "request": call_tt_req, "response": call_tt_resp})
        content_text = call_tt_resp.get("result", {}).get("content", [{}])[0].get("text", "")
        assert "Python Programming" in content_text
        print("✓ Step 6: Tool Call get_timetable (CSE-A, Monday) OK")

        # 7. Call Tool: get_fee_status (STU001)
        call_fee_req = {
            "jsonrpc": "2.0",
            "id": 6,
            "method": "tools/call",
            "params": {
                "name": "get_fee_status",
                "arguments": {
                    "student_id": "STU001"
                }
            }
        }
        call_fee_resp = send_rpc(proc, call_fee_req)
        exchanges.append({"step": "tools/call (get_fee_status success)", "request": call_fee_req, "response": call_fee_resp})
        fee_text = call_fee_resp.get("result", {}).get("content", [{}])[0].get("text", "")
        assert "Aarav Sharma" in fee_text
        assert "PAID" in fee_text
        print("✓ Step 7: Tool Call get_fee_status (STU001) OK")

        # 8. Call Tool Failure Case: get_fee_status (Invalid ID format)
        call_err_req = {
            "jsonrpc": "2.0",
            "id": 7,
            "method": "tools/call",
            "params": {
                "name": "get_fee_status",
                "arguments": {
                    "student_id": "INVALID_999"
                }
            }
        }
        call_err_resp = send_rpc(proc, call_err_req)
        exchanges.append({"step": "tools/call (get_fee_status error)", "request": call_err_req, "response": call_err_resp})
        err_text = call_err_resp.get("result", {}).get("content", [{}])[0].get("text", "")
        assert "Error: Invalid student ID format" in err_text
        print("✓ Step 8: Tool Call get_fee_status (Error Handling) OK")

    finally:
        proc.terminate()
        proc.wait()

    return exchanges


if __name__ == "__main__":
    exchanges = run_tests()
    print("\nAll MCP server tests passed successfully!")
    out_file = Path(__file__).resolve().parents[3] / "evidence" / "mcp" / "raw_rpc_exchange.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w") as f:
        json.dump(exchanges, f, indent=2)
    print(f"Captured raw JSON-RPC traces saved to {out_file}")
