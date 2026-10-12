# Shared knowledge: teammate evaluation

Evaluated October 12, 2026, on Windows/Python 3.13.14. This is a targeted
synthetic handoff check, not the adoption comparison.

## Independent agents

A fresh writer received an installed fictional CedarBuild repository and a
normal request to explain recently agreed prototype constraints before coding.
The request contained no instruction to remember them. The writer read the
installed instructions, recorded the accepted decisions in
`docs/project-memory.md`, and saved one local note pointing to that source.
It accurately reported those changes as uncommitted and did not implement the
exporter or commit anything.

The evaluator committed the fixture's project files and cloned it. A separate
reader received only that clone and questions about the exporter, rationale,
scope and hosting. It had no original conversation or personally installed
setup skill. Its `.optmem` directory was absent on arrival. Following the
committed instructions, it initialized an empty local store; wake and a focused
recall returned no history. It answered from the shared document:

- UTF-8 JSON Lines, one job per line, supports streaming diagnostics.
- Original `job_id` values must match deployment receipts.
- These choices apply to the prototype.
- Remote hosting is undecided; no complete record schema was supplied.

The reader cited the shared source, preserved scope, and did not invent a
hosting decision or completed implementation. Its tracked working tree remained
clean. Both agents were explicitly authorized to simulate top-level contributors.

## Git and setup checks

The three shared-memory integration tests passed alongside the ten existing
setup/CLI tests. The Git test creates two independent clones and passes an
accepted decision through a normal commit and pull. Private local history and
an uncommitted observation do not transfer. Other checks show setup reuses an
existing authoritative document byte-for-byte, persists its selected path,
preserves notes on rerun, and rejects ignored or unsafe authority paths.

Installed instructions route concurrent shared-document changes through normal
Git review/conflict resolution; they do not synchronize positional OptMem logs
or authorize automatic publication. Concurrent conflicting human decisions were
not exercised in this behavioral scenario.

## Limits

One handoff demonstrates that the shared-document integration can work. It does
not establish broad reliability or an advantage for OptMem: the teammate's
answer came entirely from shared Markdown. Whether adding local OptMem is worth
its maintenance cost remains the explicit adoption trial's question. Generated
fixture stores remain ignored local artifacts.
