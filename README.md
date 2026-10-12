# Repository memory

An experimental skill for preserving project intent between agent chats. The
setup installs [OptMem](https://github.com/VictorTaelin/OptMem) inside one repository
with instructions to capture durable knowledge during ordinary work and retrieve
it in a fresh chat. Explicit "remember this" requests are supported too. The
instructions are implemented; their behavioral reliability is still being tested
before broader adoption.

See the [project language](CONTEXT.md) for what counts as project intent and
shared knowledge, and the [implementation map](https://github.com/AndrewGodlewsky/memory-local/issues/1)
for scope, dependencies, and progress.

## Set up a repository from this source

Initial support is Windows with Python 3.9+ and Git available on PATH. The target
must already be the root of a Git repository. From this source checkout:

```powershell
python skills/repo-memory/scripts/setup.py --repo 'C:\path\to\your-repository'
```

The [repo-memory skill](skills/repo-memory/SKILL.md) describes the agent-led setup
and verification workflow. This source command creates repository-local tools
and instructions; it does not install a skill globally in your agent application.
Setup and normal use need no network access, API credentials, or third-party
Python packages. The bundled OptMem version and hash are recorded in the installed
`tools/memory/vendor/source.json`.

The target uses `tools/memory/memo.py` as its entry point and `.optmem/` for its
local history. The launcher selects that repository's store regardless of the
current directory. Read the setup output and review its changes to the repository
instructions before trying it in a fresh chat.

## Try a decision across chats

Open the target repository with your agent and ask it to read its `AGENTS.md`:

> Remember this accepted decision: the prototype uses SQLite because it must
> work without a separate database server. Production storage is undecided.

The agent saves a note and supplies any summaries requested by OptMem. Then open
a fresh chat in that same repository:

> Use the project memory to explain our prototype storage decision, its reason,
> and whether it also decides production storage.

You can also inspect the store yourself from the target repository:

```powershell
python tools/memory/memo.py wake
python tools/memory/memo.py recall 'SQLite|storage'
```

The installed instructions tell the agent to save accepted decisions, reasons,
constraints, supported findings, and corrections when they become established,
then check for unsaved context at handoff. Proposals and unresolved questions keep
their status; routine command successes do not need notes.

OptMem stores selected notes and summaries written by the working agent. It has
no background model or automatic conversation capture. A printed summary request
needs the agent to complete the corresponding `nap` command before normal work
continues. Original notes remain available even when summaries omit details.

The store is Git-ignored and persists only in that working environment. A teammate
cloning the repository does not receive those memories. Shared durable decisions,
retrieval across deep summaries and later corrections, adoption trials, and general
repair remain later issue phases.

## Demo and research

The [PocketTasks demo](optmem-demo/README.md) is an earlier local playground with
its own launcher and fictional project history. Its ignored store may already
be populated on the original machine; it does not travel with a clone. Use the
skill setup above when testing integration with another repository.

Read the [OptMem comparison](research/optmem-comparison.md) for the initial
investigation and the [trial plan](research/trial-plan.md) for proposed evaluation.
Neither smoke checks nor a successful storage round trip establish memory quality.

## Validate changes

From this source checkout:

```powershell
python -m unittest discover -s tests -v
```

These automated checks exercise the setup and storage mechanics. Fresh-agent
recall and later teammate trials provide separate evidence about agent behavior.
See the observed [setup recall](research/setup-validation.md) and
[ordinary-work capture](research/automatic-capture-validation.md) results and their limits.
