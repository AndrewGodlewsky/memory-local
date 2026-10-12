# Ordinary-work capture: observed behavior

Evaluated October 12, 2026, in a disposable EventDesk repository. This is a targeted synthetic check of automatic capture, not the later adoption comparison.

## Writer scenario

A fresh agent received installed project instructions and a normal coding request to implement and test CSV row normalization. The request supplied a pilot input decision and reason, an earlier failed identifier approach, a current identifier requirement, and a JSON-import idea explicitly not approved. It contained no request to remember or write memory.

The agent read startup memory, recorded three focused notes before completing the implementation, implemented the requested function, passed three unittests, and recorded verified completion in a fourth note. It wrote all three requested summaries with the working model and left no compression pending.

The notes retained:

- CSV-only pilot input because existing field tools export CSV; JSON remains an unapproved future idea.
- Original task IDs and first-occurrence handling, with the user-reported prior failure of regenerated IDs causing retry duplicates.
- Validation requirements with implementation/testing initially marked pending.
- Verified implementation and three passing tests, explicitly superseding the pending status.

## Fresh reader

A separate agent with no inherited conversation received the project and questions, and was restricted to installed instructions and memory rather than application source/test answers. It retrieved the input decision and rationale, the earlier ID failure and current requirement, the unapproved status of JSON, and the superseding completion evidence. It correctly stated that a production hosting region was not recorded.

The reader needed one wake and one focused recall. The resulting store held four distinct original notes and three summaries: seven memory writes in this small task. There were no repeated unchanged notes or standalone routine-command-success notes. Recording verified completion consumed one note and is reported as maintenance cost, not assumed free.

## Checks and limits

The skill validator and ten setup/CLI integration tests passed after the instruction change. A wording review identified and fixed ambiguity around splitting long notes: each note retains enough topic/status/scope to remain interpretable on its own.

This single scenario shows the desired behavior can occur without reminder prompts. It does not establish reliability across models or tasks, acceptable maintenance cost, deep-compression recall, or teammate handoff. Both agents were explicitly authorized to act as simulated top-level agents in the fixture. Ordinary delegated agents still report findings to their parent rather than writing duplicate memory.
