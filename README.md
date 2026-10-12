# Repository memory

An experimental skill for preserving project intent between agent chats. The
setup installs [OptMem](https://github.com/VictorTaelin/OptMem) inside one repository
with instructions to capture durable knowledge during ordinary work and retrieve
it in a fresh chat. A shared project record carries current intent through Git
to teammates. Explicit "remember this" requests are supported too. Behavioral
reliability is being evaluated before broader adoption.

See the [project language](CONTEXT.md) for what counts as project intent and
shared knowledge, and the [implementation map](https://github.com/AndrewGodlewsky/memory-local/issues/1)
for scope, dependencies, and progress.

## Set up a repository from this source

Initial support is Windows with Python 3.9+ and Git available on PATH. The target
must already be the root of a Git repository. From this source checkout:

```powershell
python skills/repo-memory/scripts/setup.py --repo 'C:\path\to\your-repository'
```

Setup uses `docs/project-memory.md` by default. If the repository already has an
authoritative decision record or index, reuse it:

```powershell
python skills/repo-memory/scripts/setup.py --repo 'C:\path\to\your-repository' --shared-memory 'docs/decisions.md'
```

The path is relative to the target repository. Setup preserves an existing
document and saves the choice in `tools/memory/config.json` for later reruns.

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

The agent records accepted intent in its shared authoritative home, saves local
history as appropriate, and supplies any summaries requested by OptMem. Then open
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

Before consequential choices, agents consult the shared record and retrieve
relevant original notes, including later additions or corrections. Summaries
help find evidence; the instructions require retaining the decision's reason
and scope rather than assuming the newest note replaces everything earlier.

OptMem stores selected notes and summaries written by the working agent. It has
no background model or automatic conversation capture. A printed summary request
needs the agent to complete the corresponding `nap` command before normal work
continues. Original notes remain available even when summaries omit details.

## Carry knowledge to a teammate

The shared record owns current agreed decisions; local notes can point to its
repository paths or anchors. The instructions, tools, configuration, and shared
documents travel through normal Git review, commit, and pull. Writing a memory
does not itself commit or publish it, and setup performs neither action.

A teammate who receives those files can read the shared knowledge immediately.
Their agent follows `AGENTS.md` to initialize a separate empty local store:

```powershell
python tools/memory/memo.py init
python tools/memory/memo.py wake
```

The `.optmem` store remains Git-ignored; contributors do not synchronize its tree.
Teammates need the repository's committed setup rather than a personal installation
of the setup skill. Broad adoption trials and general repair remain future work.

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

These automated checks exercise setup, storage mechanics, and isolated Git
handoffs. Separate behavioral observations cover [setup recall](research/setup-validation.md),
[ordinary-work capture](research/automatic-capture-validation.md),
[teammate handoff](research/teammate-validation.md), and
[deep retrieval and corrections](research/correction-evaluation.md).
Each report records its limits; these targeted checks do not decide adoption.
