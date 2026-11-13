import csv
from pathlib import Path


def get_timetable(batch, day):
    # locate the mock timetable file across possible project directories
    current = Path(__file__).resolve()
    possible_paths = [
        current.parents[5] / "data" / "mock" / "timetable.csv",
        current.parents[5] / "campus-helpdesk" / "data" / "mock" / "timetable.csv",
        current.parents[4] / "data" / "mock" / "timetable.csv",
        current.parents[4] / "campus-helpdesk" / "data" / "mock" / "timetable.csv",
        current.parents[3] / "data" / "mock" / "timetable.csv",
        Path.cwd() / "campus-helpdesk" / "data" / "mock" / "timetable.csv",
        Path.cwd() / "data" / "mock" / "timetable.csv",
    ]

    csv_path = None
    for p in possible_paths:
        if p.exists():
            csv_path = p
            break

    if not csv_path or not csv_path.exists():
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
