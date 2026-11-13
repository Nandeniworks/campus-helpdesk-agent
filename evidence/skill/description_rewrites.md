# Part B: Skill Description Rewrites & Trigger Sensitivity Analysis

The assignment requires:
> *"Rewrite the description twice and show how the trigger behaviour changed. Explain what makes a description too broad or too narrow."*

---

## 1. Description Variants Overview

| Variant | Frontmatter Description Text | Intended Scope | Trigger Calibration |
|---|---|---|---|
| **V0: Original (Balanced)** | `Use this skill when a user asks to view, check, search, or understand the campus timetable, including classes by batch or day, class timings, subjects, rooms, and faculty. Do not use it for fee enquiries, attendance, assignments, or general campus questions.` | Exact match for campus timetable domain | **Optimal**: High precision & high recall for schedule queries; blocks non-schedule campus topics. |
| **V1: Too Broad** | `Use this skill whenever a student asks about their daily schedule, campus activities, classes, or general college routine.` | Overly generalized catch-all | **Defective (Over-triggering)**: High false-positive rate. Triggers on fee deadlines, events, hostel curfews, and clubs. |
| **V2: Too Narrow** | `Use this skill only when a student asks to view the official Monday timetable for CSE-A.` | Over-constrained to single day/batch | **Defective (Under-triggering)**: High false-negative rate. Fails to trigger for CSE-B or any other weekday. |

---

## 2. Trigger Behavior Comparison Across Test Prompts

| Test Prompt | V0 (Balanced) | V1 (Too Broad) | V2 (Too Narrow) |
|---|:---:|:---:|:---:|
| **P1:** *"What classes does CSE-A have on Monday?"* | **Triggered** (Desired) | **Triggered** | **Triggered** |
| **P2:** *"Can you check the timetable for CSE-B on Tuesday?"* | **Triggered** (Desired) | **Triggered** | **FAILED (No Trigger)** ❌ *(Ignores CSE-B)* |
| **P3:** *"What classes do I have on Wednesday?"* | **Triggered** (Desired) | **Triggered** | **FAILED (No Trigger)** ❌ *(Ignores Wednesday)* |
| **P4:** *"How do I check if my college fees are paid?"* | **Ignored** (Desired) | **TRIGGERED (False Positive)** ❌ | **Ignored** |
| **P5:** *"What are the hostel rules and curfew timings?"* | **Ignored** (Desired) | **TRIGGERED (False Positive)** ❌ | **Ignored** |
| **P6:** *"What is happening on campus this Friday evening?"* | **Ignored** (Desired) | **TRIGGERED (False Positive)** ❌ | **Ignored** |

---

## 3. Technical Explanation: What Makes a Description Too Broad or Too Narrow?

### What Makes a Description Too Broad?
1. **Lack of Negative Boundaries (Negative Triggers):**
   * Without explicit boundary clauses (*"Do not use for fee enquiries, hostel rules, or attendance"*), language models use loose semantic associations. Since college fees and hostel curfews relate to a "college routine", an unconstrained embedding matches them all.
2. **Abstract / Ubiquitous Vocabulary:**
   * Words like *"activities"*, *"routine"*, and *"schedule"* match nearly every student question.
3. **Consequences:**
   * **Context Pollution:** Triggers unnecessary file inspection and script invocation.
   * **Tool Collapse / Confusion:** The agent queries `timetable.csv` looking for fee or hostel entries, finds nothing, and emits misleading errors instead of delegating to the appropriate handler.

### What Makes a Description Too Narrow?
1. **Hardcoding Instance Values Instead of Parameters:**
   * Constraining the trigger to specific literal values (`CSE-A`, `Monday`) turns variable entity slots into hard prerequisite conditions.
2. **Overfitting to Sample Prompts:**
   * Confusing demonstration examples with functional capability bounds.
3. **Consequences:**
   * **Under-Utilization (Silent Failure):** The agent possesses the capability (CSV data has `CSE-B` and Tuesday–Friday), but the routing layer never exposes the Skill to the model, leading to hallucinated responses or unassisted rejections.

### Principles of Optimal Description Design
1. **Domain Anchor:** Name the specific information artifact (`campus timetable`).
2. **Parametric Breadth:** List the parameters accepted (`by batch or day, class timings, subjects, rooms, faculty`).
3. **Negative Contrasts:** Explicitly name neighbor domains that the tool cannot handle (`fees`, `attendance`, `hostel rules`).
