# Repository memory: proposed trial

Historical proposal from October 8, 2026. The assumptions and sequence below
predate the implementation work. Current scope and the still-pending adoption
gate are tracked in the [implementation map](https://github.com/AndrewGodlewsky/memory-local/issues/1)
and [comparison trial](https://github.com/AndrewGodlewsky/memory-local/issues/6).
The prototype skill now uses shared documents for current agreed intent and
ignored OptMem history for local context; current implementation alone does not
supersede an accepted decision. Proposed thresholds below remain unapproved.

## Working assumption

One memory store per repository, carrying decisions, failed approaches, useful findings, and their reasons across chats. Files remain local; the usual agent reads and summarizes them. Fully offline inference and cross-repository personal memory would change this design. These assumptions await the user's preference.

## Decision to make

Does OptMem help an agent resume useful repository work better than a small Markdown memory, at an acceptable reading and maintenance cost? The comparison and source links are in [optmem-comparison.md](optmem-comparison.md). The newer UniiChat gist describes a custom conversation runtime; it is a separate possible future project.

## Trial sequence

1. **Mechanical introduction — completed.** A pinned OptMem script and synthetic data live under `trials/optmem`. The 15-command smoke test passed. No skill was installed, agent instructions changed, or Git commit created. This was not a test of memory quality.
2. **Controlled recall comparison — next.** Prepare 40–60 fictional repo events and 12 questions. Include exact paths, an old important decision, a failed approach and its reason, a later correction, an unresolved task, and a fact never supplied. Compare repository only, repository plus curated Markdown, and repository plus OptMem. Both memory conditions receive the same event stream; record how they select and retain notes.
3. **Exercise compression deliberately.** Use `WAKE_LINES=8` for the stress test so older notes become summaries. Let the agent produce real summaries; do not reuse smoke-test summaries. Then repeat a smaller comparison with the default budget to distinguish forced-compression failures from normal operation.
4. **Test in fresh contexts.** A fresh evaluator receives the same repo snapshot, question, and condition-specific instructions. It must not see the answer key or event feed. Use the same model/settings, vary condition order, and repeat uncertain cases. Measure known-fact retrieval and completion of a small task without repeating an earlier failed approach.
5. **Small real-work pilot.** If the controlled comparison is promising, use one chosen repo for three normal work sessions. Record missed notes, stale facts, summary requests, duplicates, and user corrections. Choose the simplest approach that proves useful before implementing the reusable skill.

## Proposed scorecard

| Measure | What to record |
|---|---|
| Correct recall | Correct answers out of 12; original evidence references |
| Corrections | Whether the current decision supersedes the earlier one |
| Honesty | Whether an unknown fact stays unknown; no invented completion |
| Practical benefit | Repeated failed work avoided; successful task continuation |
| Cost | Tool calls, time, context bytes, and tokens when observable |
| Maintenance | Note-writing and summary calls, retries, startup interruptions |

Suggested adoption gate, to agree before the controlled test: at least 10/12 correct, all correction/unknown cases handled correctly, and a material benefit over Markdown. An example benefit is at least two additional correct answers, or comparable accuracy with substantially less context at tolerable maintenance cost. A tie favors Markdown. These are pilot decision rules, not a statistical performance claim.

## Shape of a skill if the trial succeeds

- A small instruction file teaches when to consult memory and what repository knowledge merits saving. Keep current source and tests authoritative when remembered facts conflict with them.
- A helper resolves the repo root, sets MEMORY_DIR for that invocation, and invokes the pinned tool through Python. Test nested directories and two independent repositories to prove isolation.
- Remember facts with reasons and sources, such as paths, commits, or decision references. Record corrections explicitly; retrieve original notes before relying on compressed claims.
- Decide the Git policy deliberately. Start with a local ignored store. Fixed-width log records use positional IDs, so independently appended branch histories should not be treated as ordinary mergeable Markdown. Avoid synced multi-machine writers during the first pilot.
- Choose how repo entry instructions trigger a startup read. Evaluate reliability explicitly; making a skill available alone does not establish that every new chat invokes it.
- Preserve a portable export route. Adopt UniiChat ideas individually if tests justify them. A 512-byte note size would require storage changes in upstream OptMem, not just raising its existing configuration.

## Questions remaining

Scope: repo knowledge only, task progress too, or cross-repo personal memory? Does local mean local storage or fully offline inference? Which real repo should host the pilot, and should memories eventually be shared through Git? These choices do not block the synthetic comparison.
