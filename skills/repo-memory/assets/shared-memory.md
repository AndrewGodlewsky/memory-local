
### Shared project knowledge

At startup, read [the authoritative project record](<{shared_memory}>) before
reading local history. Consult its relevant decisions and sources before a
consequential choice. This shared record owns current agreed intent; OptMem
records local history and pointers to stable repository paths or anchors.

If this checkout has no `.optmem` directory, initialize its own empty local
store with `python tools/memory/memo.py init`, then run `wake`. Keep these
repository instructions; the upstream setup text printed by `init` describes
a different, machine-wide workflow. A teammate needs only the committed tools
and project instructions, not another contributor's personal skill installation.

Put accepted decisions, constraints, reasons, scope and durable findings in
the relevant existing authoritative section or linked decision document. Edit
the record above when no more specific authoritative home exists. Preserve
unrelated knowledge. Keep proposals and unresolved conflicts explicit rather
than presenting them as agreed decisions. Local notes can describe a change
and point to its shared source instead of maintaining a second current decision.

Shared references use repository-relative paths and stable anchors, not machine
paths or contributor-local note IDs. An edit is a working-tree change until
committed and received by teammates through normal Git review and pull; report
that distinction accurately. Recording knowledge does not authorize commits,
pushes or publication. Resolve concurrent document changes through normal Git
review/conflict resolution, surfacing contradictory intent rather than silently
overwriting it. The ignored OptMem log is never the synchronization mechanism.
