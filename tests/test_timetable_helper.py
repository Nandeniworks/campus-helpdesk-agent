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
    subjects = [r["subject"] for r in records]
    assert "Python Programming" in subjects
    assert "Mathematics" in subjects
    assert "Database Systems" in subjects


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
    print("All timetable helper tests passed successfully.")
