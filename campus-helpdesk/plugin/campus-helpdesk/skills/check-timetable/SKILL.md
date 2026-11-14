---
name: check-timetable
description: Look up the scheduled classes for a given student batch and day. Can be invoked directly as /check-timetable <BATCH> <DAY> or via natural language schedule queries.
---

# Check Timetable Slash Command

Look up the scheduled classes for a given student batch and day using official campus timetable records.

## Usage

`/check-timetable <BATCH> <DAY>`

Example:
`/check-timetable CSE-A Monday`

## Instructions

1. Parse the input arguments into `<BATCH>` (e.g., `CSE-A`, `CSE-B`) and `<DAY>` (e.g., `Monday`, `Tuesday`, `Wednesday`, `Thursday`, `Friday`).
2. If either parameter is missing, ask the user to specify the missing batch or day without assuming values.
3. Retrieve matching records from `campus-helpdesk/data/mock/timetable.csv` using the bundled `timetable-helper` extraction script:
   `python3 campus-helpdesk/plugin/campus-helpdesk/skills/timetable-helper/scripts/timetable_helper.py <BATCH> <DAY>`
4. Output the results formatted as a table with columns:
   `Subject | Start Time | End Time | Room | Faculty`
5. If no records match, output:
   `"No timetable entry was found for the requested batch and day in the supplied data."`
6. Adhere strictly to the anti-hallucination rules: never invent or assume subjects, timings, rooms, or faculty details.

