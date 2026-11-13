"""
Unit test suite for campus timetable helper script.
Verifies correct CSV parsing, blank line skipping, batch/day filtering, and case insensitivity.
"""

import sys
from pathlib import Path

# Add script directory to sys.path
SCRIPT_DIR = Path(__file__).resolve().parents[1] / "campus-helpdesk" / "skills" / "timetable-helper" / "scripts"
sys.path.append(str(SCRIPT_DIR))

import timetable_helper  # noqa: E402


def test_csea_monday():
    records = timetable_helper.get_timetable("CSE-A", "Monday")
    assert len(records) == 3, f"Expected 3 records, got {len(records)}"
    
    # Assert exact authoritative fields
    assert records[0]["subject"] == "Python Programming"
    assert records[0]["room"] == "Lab 1"
    assert records[0]["faculty"] == "Faculty A"
    
    assert records[1]["subject"] == "Mathematics"
    assert records[1]["room"] == "Room 201"
    assert records[1]["faculty"] == "Faculty B"
    
    assert records[2]["subject"] == "Database Systems"
    assert records[2]["room"] == "Room 202"
    assert records[2]["faculty"] == "Faculty C"


def test_command_cli_execution():
    """Verify that timetable_helper can be invoked via CLI arguments matching /check-timetable parameters."""
    import subprocess
    script_path = SCRIPT_DIR / "timetable_helper.py"
    res = subprocess.run(
        [sys.executable, str(script_path), "CSE-A", "Monday"],
        capture_output=True,
        text=True,
        check=True
    )
    output = res.stdout.strip()
    assert "Python Programming | 09:00-10:00 | Lab 1 | Faculty A" in output
    assert "Mathematics | 10:00-11:00 | Room 201 | Faculty B" in output
    assert "Database Systems | 11:30-12:30 | Room 202 | Faculty C" in output


def test_csea_tuesday():
    records = timetable_helper.get_timetable("CSE-A", "Tuesday")
    assert len(records) == 2, f"Expected 2 records, got {len(records)}"


def test_csea_sunday_empty():
    records = timetable_helper.get_timetable("CSE-A", "Sunday")
    assert len(records) == 0, f"Expected 0 records, got {len(records)}"


def test_cseb_monday():
    records = timetable_helper.get_timetable("CSE-B", "Monday")
    assert len(records) == 1, f"Expected 1 record, got {len(records)}"
    assert records[0]["subject"] == "Computer Networks"


def test_case_insensitivity():
    records = timetable_helper.get_timetable("cse-a", "monday")
    assert len(records) == 3, f"Expected 3 records, got {len(records)}"


def test_nonexistent_batch():
    records = timetable_helper.get_timetable("NONEXISTENT", "Monday")
    assert len(records) == 0


if __name__ == "__main__":
    test_csea_monday()
    test_csea_tuesday()
    test_csea_sunday_empty()
    test_cseb_monday()
    test_case_insensitivity()
    test_nonexistent_batch()
    test_command_cli_execution()
    print("All timetable helper tests passed successfully.")
