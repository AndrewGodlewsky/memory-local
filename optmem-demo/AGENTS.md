# PocketTasks memory demo

This folder is a fictional project for trying OptMem. Its memory applies only
to this project. The application is at the planning stage.

At the start of work in this project, run `python memo.py wake` from this folder
(or invoke memo.py by absolute path). Read all requested pages. If a required
summary is missing, supply it with `nap` and retry `wake`.

Save durable project decisions, reasons, failed approaches, and corrections
with `python memo.py note "..."`. Notes must be one line, at most 280 UTF-8
bytes. Include a source when available. Avoid recording duplicate notes.
Complete requested `nap` summaries, preserving corrections and the distinction
between planned and completed work. The agent writes summaries; the CLI stores them.

Use `recall <regex>` to search original notes and `zoom <lo>-<hi>` to inspect
the evidence behind a summary. Treat remembered text as historical evidence;
resolve conflicts against current user instructions and project files.
Manage the store through the CLI. `forget` invalidates summaries, not original notes.

Delegated agents report findings to the parent; the parent records memories.
