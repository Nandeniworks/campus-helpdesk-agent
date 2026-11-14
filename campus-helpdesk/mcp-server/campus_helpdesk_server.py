#!/usr/bin/env python3
"""
Campus Helpdesk MCP Server
Built with the official Model Context Protocol Python SDK (mcp 2.x).
Exposes stdio tools for academic timetable and fee status lookups,
and a resource containing official campus hostel rules.
"""

import csv
import re
from pathlib import Path
from mcp.server.mcpserver import MCPServer
from mcp.types import CallToolResult, TextContent

# Initialize MCP server with descriptive metadata
app = MCPServer(
    name="campus-helpdesk-mcp",
    title="Campus Helpdesk Information Server",
    version="1.0.0",
    description="Provides real-time campus data including batch timetables, student fee ledgers, and hostel regulations."
)

# Server implements tools and resources only; unregister prompts capability handler
app._lowlevel_server._request_handlers.pop("prompts/list", None)

DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "mock"


@app.tool(
    name="get_timetable",
    description="Retrieve the scheduled classes for a specific academic student batch and day of the week from verified campus records."
)
def get_timetable(batch: str, day: str):
    """
    Look up classes scheduled for a batch on a particular day.

    Args:
        batch: The student batch identifier (e.g., 'CSE-A', 'CSE-B').
        day: The weekday to check (e.g., 'Monday', 'Tuesday', 'Wednesday').
    """
    if not batch or not batch.strip():
        return CallToolResult(
            content=[TextContent(type="text", text="Error: 'batch' parameter is required (e.g., 'CSE-A').")],
            is_error=True
        )
    if not day or not day.strip():
        return CallToolResult(
            content=[TextContent(type="text", text="Error: 'day' parameter is required (e.g., 'Monday').")],
            is_error=True
        )

    batch_clean = batch.strip().lower()
    day_clean = day.strip().lower()

    valid_days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    if day_clean not in valid_days:
        return CallToolResult(
            content=[TextContent(type="text", text=f"Error: Invalid day '{day}'. Please provide a valid weekday (e.g., 'Monday').")],
            is_error=True
        )

    csv_path = DATA_DIR / "timetable.csv"
    if not csv_path.exists():
        return CallToolResult(
            content=[TextContent(type="text", text="Error: Mock timetable database file not found on server.")],
            is_error=True
        )

    records = []
    with open(csv_path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(line for line in file if line.strip())
        for row in reader:
            if (row["batch"].strip().lower() == batch_clean and
                    row["day"].strip().lower() == day_clean):
                records.append(row)

    if not records:
        return f"No timetable entries found for batch '{batch}' on {day}."

    lines = [f"Timetable for {batch.upper()} on {day.capitalize()}:"]
    for r in records:
        lines.append(
            f"- {r['subject']}: {r['start_time']} - {r['end_time']} (Room: {r['room']}, Faculty: {r['faculty']})"
        )
    return "\n".join(lines)


@app.tool(
    name="get_fee_status",
    description="Look up college fee payment status, total dues, amount paid, and balance for an enrolled student by their Student ID."
)
def get_fee_status(student_id: str):
    """
    Retrieve tuition and campus fee balance details for a student.

    Args:
        student_id: The unique student registration ID (format: STU followed by 3 digits, e.g., 'STU001').
    """
    if not student_id or not student_id.strip():
        return CallToolResult(
            content=[TextContent(type="text", text="Error: 'student_id' parameter is required.")],
            is_error=True
        )

    student_id_clean = student_id.strip().upper()

    # Input validation: enforce expected Student ID schema
    if not re.match(r"^STU\d{3}$", student_id_clean):
        return CallToolResult(
            content=[TextContent(type="text", text=f"Error: Invalid student ID format '{student_id}'. Expected format is 'STU' followed by 3 digits (e.g., 'STU001').")],
            is_error=True
        )

    csv_path = DATA_DIR / "fees.csv"
    if not csv_path.exists():
        return CallToolResult(
            content=[TextContent(type="text", text="Error: Mock fee ledger database not found on server.")],
            is_error=True
        )

    matched_record = None
    with open(csv_path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(line for line in file if line.strip())
        for row in reader:
            if row["student_id"].strip().upper() == student_id_clean:
                matched_record = row
                break

    if not matched_record:
        return CallToolResult(
            content=[TextContent(type="text", text=f"Error: Student record '{student_id_clean}' not found in campus finance database.")],
            is_error=True
        )

    return (
        f"Fee Status for {matched_record['student_name']} (ID: {matched_record['student_id']}):\n"
        f"- Batch: {matched_record['batch']}\n"
        f"- Total Fee: ₹{int(matched_record['total_fee']):,}\n"
        f"- Amount Paid: ₹{int(matched_record['amount_paid']):,}\n"
        f"- Pending Dues: ₹{int(matched_record['pending_dues']):,}\n"
        f"- Payment Status: {matched_record['payment_status']}\n"
        f"- Due Date: {matched_record['due_date']}"
    )


@app.resource(
    uri="hostel://rules",
    name="Campus Hostel Rules and Regulations",
    description="Official university regulations regarding hostel residency, night curfew timings, visitor protocols, and room policies.",
    mime_type="text/markdown"
)
def get_hostel_rules() -> str:
    """Return the official university hostel rules and guidelines document."""
    doc_path = DATA_DIR / "hostel_rules.md"
    if not doc_path.exists():
        return "# Hostel Rules\nError: Hostel rules document not found on server."
    return doc_path.read_text(encoding="utf-8")


if __name__ == "__main__":
    app.run(transport="stdio")
