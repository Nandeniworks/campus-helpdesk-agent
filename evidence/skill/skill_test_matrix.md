# Part B: Skill Prompt Test Matrix

The `timetable-helper` Skill was tested across 6 representative prompts inside the Antigravity conversation environment to verify trigger behavior under progressive disclosure.

## Test Summary

| Prompt No. | Category | User Prompt | Expected Trigger | Actual Trigger | Verdict | Rationale |
|---|---|---|---|---|---|---|
| **1** | Positive | *"What classes does CSE-A have on Monday? Please provide the subject names, timings, rooms and faculty."* | YES | YES | **PASS** | Matches timetable domain, specifies batch (`CSE-A`) and day (`Monday`). |
| **2** | Positive | *"Can you check the timetable for CSE-B on Tuesday and tell me which subjects are scheduled, along with their timings and classrooms?"* | YES | YES | **PASS** | Matches timetable domain, specifies batch (`CSE-B`) and day (`Tuesday`). |
| **3** | Positive | *"I'm in CSE-A. Can you tell me what classes I have on Wednesday, including the timings, rooms and faculty?"* | YES | YES | **PASS** | Natural language student query for academic class timetable. |
| **4** | Negative | *"Can you tell me how I can check whether my college fees have been paid or are still pending?"* | NO | NO | **PASS** | Explicit negative trigger in frontmatter (*"Do not use it for fee enquiries..."*). |
| **5** | Negative | *"What are the hostel rules for students? I want to know about entry timings, visitor policies and hostel facilities."* | NO | NO | **PASS** | Explicit negative trigger in frontmatter (*"Do not use it for... general campus questions"*). |
| **6** | Ambiguous | *"Can you help me find the information for my next class?"* | Conditional | Prompted for Info | **PASS** | User requested class info but omitted batch and day. Agent asked for missing parameters per Rule 6 without guessing. |

---

## Detailed Test Logs & Actual Agent Outputs

### Test 1: Positive Trigger (CSE-A Monday)
* **User Prompt:**
  > "What classes does CSE-A have on Monday? Please provide the subject names, timings, rooms and faculty."
* **Agent Trigger Status:** Triggered `timetable-helper` Skill.
* **Actual Agent Output:**
  ```markdown
  Here is the Monday schedule for **CSE-A**:

  | Subject | Start Time | End Time | Room | Faculty |
  |---|---|---|---|---|
  | Python Programming | 09:00 | 10:00 | Lab 1 | Faculty A |
  | Mathematics | 10:00 | 11:00 | Room 201 | Faculty B |
  | Database Systems | 11:30 | 12:30 | Room 202 | Faculty C |
  ```

---

### Test 2: Positive Trigger (CSE-B Tuesday)
* **User Prompt:**
  > "Can you check the timetable for CSE-B on Tuesday and tell me which subjects are scheduled, along with their timings and classrooms?"
* **Agent Trigger Status:** Triggered `timetable-helper` Skill.
* **Actual Agent Output:**
  ```markdown
  Here is the Tuesday schedule for **CSE-B**:

  | Subject | Start Time | End Time | Room | Faculty |
  |---|---|---|---|---|
  | Mathematics | 10:00 | 11:00 | Room 201 | Faculty B |
  ```

---

### Test 3: Positive Trigger (CSE-A Wednesday)
* **User Prompt:**
  > "I'm in CSE-A. Can you tell me what classes I have on Wednesday, including the timings, rooms and faculty?"
* **Agent Trigger Status:** Triggered `timetable-helper` Skill.
* **Actual Agent Output:**
  ```markdown
  Here is the Wednesday schedule for **CSE-A**:

  | Subject | Start Time | End Time | Room | Faculty |
  |---|---|---|---|---|
  | Python Programming | 09:00 | 10:00 | Lab 1 | Faculty A |
  | Mathematics | 10:00 | 11:00 | Room 201 | Faculty B |
  ```

---

### Test 4: Negative Trigger (College Fees)
* **User Prompt:**
  > "Can you tell me how I can check whether my college fees have been paid or are still pending?"
* **Agent Trigger Status:** Did **NOT** trigger `timetable-helper`.
* **Actual Agent Output:**
  ```markdown
  I do not have access to your personal financial records or fee payment database (the current agent toolchain only covers timetable information). 

  However, to check whether your college fees have been paid or are still pending, you can typically follow these steps:
  1. Student ERP / Academic Portal...
  2. Official Payment Gateway / Receipt Portal...
  3. Campus Finance / Accounts Office...
  ```
* **Evaluation:** Respects the negative trigger condition in `SKILL.md` frontmatter: *"Do not use it for fee enquiries, attendance, assignments, or general campus questions."*

---

### Test 5: Negative Trigger (Hostel Rules)
* **User Prompt:**
  > "What are the hostel rules for students? I want to know about entry timings, visitor policies and hostel facilities."
* **Agent Trigger Status:** Did **NOT** trigger `timetable-helper`.
* **Actual Agent Output:**
  ```markdown
  Currently, the helpdesk system does not have the official campus hostel manual or policy documents loaded in its database (it is currently configured only for academic timetables).

  However, in standard university campus setups, hostel rules typically include:
  1. Entry Timings & Curfew...
  2. Visitor & Guest Policies...
  3. Hostel Facilities...
  ```
* **Evaluation:** Correctly identified that hostel regulations fall outside the timetable domain.

---

### Test 6: Ambiguous Prompt (Missing Parameters)
* **User Prompt:**
  > "Can you help me find the information for my next class?"
* **Agent Trigger Status:** Activated Skill Rule 6 (Parameter Clarification).
* **Actual Agent Output:**
  ```markdown
  To find your next class, please provide your **batch** (e.g., CSE-A or CSE-B) and the **day** of the week you'd like to check.
  ```
* **Evaluation:** Followed Instruction 6 of `SKILL.md`: *"If the user does not provide enough information, ask for the missing batch or day."* It prevented guessing an arbitrary batch or current time.
