
# Timetable CSV Reference

## File Location

`campus-helpdesk/data/mock/timetable.csv`

## Purpose

This file explains the structure of the mock timetable CSV used by the Timetable Helper Skill.

## CSV Columns

| Column | Description | Example |
|---|---|---|
| batch | Identifies the student batch | CSE-A |
| day | Day of the scheduled class | Monday |
| start_time | Class starting time | 09:00 |
| end_time | Class ending time | 10:00 |
| subject | Name of the subject | Python Programming |
| room | Classroom or laboratory | Lab 1 |
| faculty | Faculty assigned to the class | Faculty A |

## Data Format

- The file uses comma-separated values (CSV).
- Each row represents one timetable entry.
- Time values use the 24-hour HH:MM format.
- Batch and day values must match the available records.

## Lookup Rules

1. Filter records using the requested batch.
2. Filter the matching records using the requested day.
3. Return all matching timetable entries.
4. Preserve the original values from the CSV.
5. Do not create missing records or assume class schedules.

## Important

This reference describes mock data created for the assignment. It does not represent an official university timetable.
