# PocketTasks: an OptMem playground

PocketTasks is a fictional Python command-line task tracker. We are planning
its first version; there is no application implementation yet. The point of
this folder is to experience project memory before building a reusable skill.

## Start here

In PowerShell:

```powershell
cd 'C:\Users\godle\OneDrive\Desktop\Claude\memory-local\optmem-demo'
python memo.py wake
```

The store starts with four fictional notes and three agent-written summaries.
The reading budget is three lines, so `wake` shows the oldest two notes as one
summary and the newest two in full. OptMem's normal budget is 96 lines; this
small setting makes compression visible immediately.

## Look behind a summary

```powershell
python memo.py zoom 0-1
python memo.py recall 'JSON|SQLite'
python memo.py recall 'export'
```

`zoom` opens the first summary into its original notes. `recall` searches the
original log using a case-insensitive regular expression. The export search
shows an initial decision and its later correction.

## Add your own decision

```powershell
python memo.py note 'User decision: completed tasks should remain visible until explicitly archived.'
python memo.py wake
```

A note may print a request to compress a pair or group of notes. The tool
does not call a model: you or the working agent writes the summary and submits
it with the printed `nap` command. Repeat until it reports no pending work.
For a simpler experience, ask the agent to record the decision and handle the
requested summaries for you.

## See the exact words again

```powershell
python memo.py recall 'archived'
```

Original notes remain available even when startup summaries omit details.
`python memo.py forget 0-1` would drop that summary and dependent cached
summaries so they can be rebuilt; it does not erase the original notes.

## Try continuity in a fresh chat

Open this folder as the working project and ask:

> Read this project's AGENTS.md, then use its memory to tell me why we chose
> the storage format and which export formats belong in version one.

Then teach it a new project decision. In another fresh chat, ask it to recall
that decision. The memory store persists between chats. The working agent
must read and update it; OptMem does not automatically capture conversations.

## Files and settings

- `memo.py`: Windows-friendly entry point; always selects this folder's store.
- `tools/memo`: unchanged upstream Python script; provenance in `tools/source.json`.
- `.optmem/LOG.txt`: original notes, managed by the tool.
- `.optmem/TREE/`: agent-written summaries.
- `AGENTS.md`: project-local integration instructions.

```powershell
python memo.py config
python memo.py config WAKE_LINES=96
python memo.py config WAKE_LINES=3
```

This demo has no API keys, model service, or background process. Your usual
AI agent sees notes when it reads them. The store is ignored by Git; this
folder is inside the parent repository, not a nested Git repository. Its
location is under OneDrive, so any configured OneDrive syncing still applies.

Upstream: https://github.com/VictorTaelin/OptMem
