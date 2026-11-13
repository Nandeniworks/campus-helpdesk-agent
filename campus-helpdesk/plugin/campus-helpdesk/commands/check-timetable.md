---
description: Look up class schedule for a specific batch and day using campus timetable records.
---

# /check-timetable

Look up the scheduled classes for a given student batch and day.

## Usage
`/check-timetable <BATCH> <DAY>`

Example:
`/check-timetable CSE-A Monday`

## Instructions
1. Parse the `$ARGUMENTS` into `<BATCH>` and `<DAY>`.
2. If either parameter is missing, ask the user to specify it.
3. Activate the bundled `timetable-helper` Skill to retrieve matching records from the mock timetable database.
4. Output the results formatted as a table with columns: `Subject | Start Time | End Time | Room | Faculty`.
5. If no records match, output: `"No timetable entry was found for the requested batch and day in the supplied data."`
