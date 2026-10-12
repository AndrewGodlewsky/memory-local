---
name: repo-memory
description: Set up local OptMem history and shared project knowledge for continuity across chats and teammates. Use for installing or rerunning repository memory in a Git repository.
---

# Repository memory

Install local history, a shared project record, and persistent instructions so
agents capture durable knowledge during work and consult it in later chats.
The shared record owns current agreed intent; OptMem retains local history.

1. Identify the intended Git root and read its agent instructions and existing
   memory conventions and authoritative decision documents. Reuse their current
   home or index instead of copying decisions into a competing record. When none
   exists, use `docs/project-memory.md`. Preserve a previously configured choice
   in `tools/memory/config.json`; changing authority requires an explicit migration.
2. Run `python <skill-directory>/scripts/setup.py --repo <absolute-git-root> --shared-memory <repository-relative-document>`.
   Quote paths containing spaces. The script bundles a pinned OptMem version;
   setup and normal use require Python 3.9+ and no network or model API. Git is
   required for setup. It preserves existing instructions and memory on rerun,
   preserves an existing shared document, and refuses conflicting tool files.
   Omitting `--shared-memory` reuses the saved path or the default above.
3. Read the selected shared record, then run
   `python <repo>/tools/memory/memo.py wake` and follow requested pages or summaries.
   Save established knowledge according to the installed instructions: current
   accepted intent in its shared authoritative home, local history and source
   pointers through `note`. Complete requested `nap` work and verify with `recall`.
   Leave new records free of invented project decisions.
4. Report the installed paths, selected authority, and verification result.
   Distinguish working-tree edits from knowledge already committed and received
   by teammates. To test continuity, give a fresh agent only the repository and
   a task requiring its decisions. A fresh clone initializes its own empty store
   with `python tools/memory/memo.py init` before `wake`, as instructed in AGENTS.md.

The installed `AGENTS.md` block is the ongoing integration; the setup skill
need not be invoked in every chat. Read-only inspection or a question about
memory does not itself request installation. Share the instructions, tools,
configuration and authoritative documents through the normal Git workflow;
recording memory alone does not authorize commits or pushes. Local `.optmem`
history stays ignored and is not a synchronized tree. Teammates need the committed
repository setup, not a personal installation of this skill.
