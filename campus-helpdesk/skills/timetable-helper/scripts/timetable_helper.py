
import csv
from pathlib import Path


def get_timetable(batch, day):
    # locate the mock timetable file
    project_root = Path(__file__).resolve().parents[4]
    csv_path = project_root / "campus-helpdesk" / "data" / "mock" / "timetable.csv"
    if not csv_path.exists():
        csv_path = Path(__file__).resolve().parents[3] / "data" / "mock" / "timetable.csv"

    # read timetable records
    if not csv_path.exists():
        return []

    with open(csv_path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(line for line in file if line.strip())

        records = [
            row for row in reader
            if row["batch"].strip().lower() == batch.strip().lower()
            and row["day"].strip().lower() == day.strip().lower()
        ]

    return records


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        batch = sys.argv[1].strip()
        day = sys.argv[2].strip()
    else:
        batch = input("Enter batch: ").strip()
        day = input("Enter day: ").strip()

    timetable = get_timetable(batch, day)

    if timetable:
        for entry in timetable:
            print(
                f'{entry["subject"]} | '
                f'{entry["start_time"]}-{entry["end_time"]} | '
                f'{entry["room"]} | {entry["faculty"]}'
            )
    else:
        print("No timetable entry found for the requested batch and day.")
