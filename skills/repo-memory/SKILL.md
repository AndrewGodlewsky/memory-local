---
name: repo-memory
description: Set up repository-local OptMem memory when a project needs decisions recalled across chats. Use for installing or rerunning this setup in a Git repository.
---

# Repository memory

Install a local memory store and persistent project instructions so agents
capture useful project knowledge during ordinary work and recall it in later
chats. This is an evaluation of local memory; sharing knowledge with teammates
is separate work.

1. Identify the intended Git root and read its agent instructions and existing
   memory conventions. Reuse the existing setup when present; resolve conflicts
   with an existing memory workflow before installing another one.
2. Run `python <skill-directory>/scripts/setup.py --repo <absolute-git-root>`.
   Quote paths containing spaces. The script bundles a pinned OptMem version;
   setup and normal use require Python 3.9+ and no network or model API. Git is
   required for setup. It preserves existing instructions and memory on rerun,
   and refuses conflicting tool files rather than overwriting them.
3. Run `python <repo>/tools/memory/memo.py wake` and follow any requested pages or
   summaries. Save supplied or established project knowledge through `note`
   according to the installed instructions, complete requested `nap` summaries,
   then verify with `recall`.
   Leave a new store empty when no project knowledge was supplied.
4. Report the installed paths and verification result. To verify persistence,
   give a fresh chat the repository and a task requiring the saved decision;
   let it discover the decision through the installed instructions.

The installed `AGENTS.md` block is the ongoing integration; the setup skill
need not be invoked in every chat. Read-only inspection or a question about
memory does not itself request installation. Local `.optmem` history is ignored
by Git and does not travel to teammates. Use the repository's established
shared decision records for knowledge that already has an authoritative home.
