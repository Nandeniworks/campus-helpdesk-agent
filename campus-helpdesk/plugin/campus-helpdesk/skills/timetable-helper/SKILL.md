---
name: timetable-helper
description: Use this skill when a user asks to view, check, search, or understand the campus timetable, including classes by batch or day, class timings, subjects, rooms, and faculty. Do not use it for fee enquiries, attendance, assignments, or general campus questions.
---

# Timetable Helper

## Purpose

Help students find timetable information using the supplied mock timetable CSV file.

## Instructions

1. Read the timetable data from `campus-helpdesk/data/mock/timetable.csv`.
2. Identify the requested batch and day.
3. Search only the records available in the CSV.
4. Present matching classes in a clear, organised format.
5. Include the subject, start time, end time, room, and faculty.
6. If the user does not provide enough information, ask for the missing batch or day.
7. If no matching timetable entry exists, clearly say that the information is unavailable.
8. Never invent or assume a subject, class time, room, faculty member, or timetable entry.
9. Never modify the original CSV file.

## Data Accuracy Rules

- The supplied CSV is the only source of timetable information.
- Do not use general knowledge to fill missing timetable entries.
- Do not assume that a class exists because it normally might be taught on a particular day.
- Clearly distinguish between unavailable information and an empty timetable.
- If the CSV cannot be accessed or read, report the problem instead of generating an answer.

## Response Format

When timetable records are found, use a table with these columns:

| Subject | Start Time | End Time | Room | Faculty |
|---|---|---|---|---|

If no matching record is found, respond:

"No timetable entry was found for the requested batch and day in the supplied data."

## Additional Resources

Read `references/timetable-format.md` when you need information about the CSV structure or its fields.

Use the helper script in `scripts/` when available to retrieve timetable records.
