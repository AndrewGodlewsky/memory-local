# OptMem and UniiChat: findings for a repository-local trial

Researched October 8, 2026. This is a research note, not installed agent instructions. Source investigation was read-only; a separate local mechanics trial is recorded below.

## Recommendation

Trial OptMem as a small, isolated repository memory experiment first. The newer gist contains useful ideas, but adopting it means building a chat runtime, not merely writing a skill. There is no demonstrated evidence in the linked material that it improves repository task accuracy over OptMem. Evaluate its ideas independently rather than treating “newer” as “better.” This is a recommendation inferred from the implementation and design described below.

## Sources inspected

- [OptMem repository](https://github.com/VictorTaelin/OptMem), inspected at commit `1fb164cf39028047781f72ac3bb1e5a691c1dcb0` (July 31, 2026): [README](https://github.com/VictorTaelin/OptMem/blob/1fb164cf39028047781f72ac3bb1e5a691c1dcb0/README.md), [memo source](https://github.com/VictorTaelin/OptMem/blob/1fb164cf39028047781f72ac3bb1e5a691c1dcb0/memo), [test.py](https://github.com/VictorTaelin/OptMem/blob/1fb164cf39028047781f72ac3bb1e5a691c1dcb0/test.py), [Windows notes](https://github.com/VictorTaelin/OptMem/blob/1fb164cf39028047781f72ac3bb1e5a691c1dcb0/WINDOWS.md).
- [Newer gist](https://gist.github.com/VictorTaelin/91837951a5ce5b38f341ec1ba1df6449), whose description says “OptChat” but document title says “UniiChat: one chat that never ends.” Gist API reports creation October 4, 2026, and latest revision `3c190e06f34aba0c69f49042c526093269604935` at October 8, 2026 01:58:24 UTC. It contains one Markdown file, `optchat.md`. [Pinned revision](https://gist.github.com/VictorTaelin/91837951a5ce5b38f341ec1ba1df6449/3c190e06f34aba0c69f49042c526093269604935), [API metadata](https://api.github.com/gists/91837951a5ce5b38f341ec1ba1df6449).

## What OptMem actually provides

The README describes a Python CLI that preserves selected short notes and their summaries. `MEMORY_DIR` supports a repository-specific store. `wake` supplies bounded context; `recall` searches raw notes by regex; `zoom` opens summaries; `forget` invalidates summaries rather than erasing raw notes. The default installation and identity prompt assume a machine-wide memory, so repository scope needs an explicit adaptation. [README](https://github.com/VictorTaelin/OptMem/blob/1fb164cf39028047781f72ac3bb1e5a691c1dcb0/README.md)

Source inspection confirms 280-byte UTF-8 notes, append-only fixed-width records, a binary summary cache, age-based context selection, and Windows locking support. The CLI makes no model API calls: the agent supplies each requested compression. Blocks up to 16 notes are compressed from original notes; larger blocks use child summaries. `wake` can stop if required summaries are missing. `forget` also drops subsequent cached records at affected levels, increasing rebuilding work. These are static code observations, not runtime test results. [memo source](https://github.com/VictorTaelin/OptMem/blob/1fb164cf39028047781f72ac3bb1e5a691c1dcb0/memo)

The repository contains an executable test suite, but its presence does not establish memory quality. The README's speed claim concerns storage access, not reasoning or recall accuracy. [Tests](https://github.com/VictorTaelin/OptMem/blob/1fb164cf39028047781f72ac3bb1e5a691c1dcb0/test.py), [README](https://github.com/VictorTaelin/OptMem/blob/1fb164cf39028047781f72ac3bb1e5a691c1dcb0/README.md)

## What the newer design changes

UniiChat proposes recording the conversation itself: user messages, agent replies, tool calls, clipped tool outputs, subagent reports, and imported notes. A single process owns the append-only chat log. Thoughts are excluded. A background model creates binary summaries targeting 512 bytes, with up to eight concurrent compactions; short inputs can bypass model calls. This removes reliance on an agent deciding to write every useful note, at the cost of model calls and runtime infrastructure. [Gist, sections 1–2 and 4](https://gist.github.com/VictorTaelin/91837951a5ce5b38f341ec1ba1df6449/3c190e06f34aba0c69f49042c526093269604935)

Each user turn starts a fresh model call with a persisted summary view. It grows to 128,000 bytes, then batches merges toward 64,000. Older material becomes coarser; `zoom` retrieves finer summaries and original messages, and `date` retrieves timestamps. The view is saved across restarts to preserve stable prompt prefixes. Compactions use a separate 16–32 KB contextual view. [Gist, sections 3–4 and 6](https://gist.github.com/VictorTaelin/91837951a5ce5b38f341ec1ba1df6449/3c190e06f34aba0c69f49042c526093269604935)

Its cache design is specifically described for Anthropic: stable tools/system instructions, cache marks in four-line blocks, and coordinated concurrent writes. The gist reports approximately fourfold simulated input-cost savings from batching versus frequent merges, and 98.6% turn-prefix cache reads in another simulation. These are author-reported simulations, not verified billing results, cross-provider measurements, or evidence of better answers. [Gist, section 3.3](https://gist.github.com/VictorTaelin/91837951a5ce5b38f341ec1ba1df6449/3c190e06f34aba0c69f49042c526093269604935)

## Maturity and limitations

The linked gist is a detailed specification, including prompts and one JavaScript merge-order illustration. It does not supply a complete executable chat application, setup package, test suite, or reproducible benchmark harness. Its descriptions of an existing personal setup are author claims; this investigation did not establish where that implementation is available. [Gist](https://gist.github.com/VictorTaelin/91837951a5ce5b38f341ec1ba1df6449/3c190e06f34aba0c69f49042c526093269604935)

The design also leaves decisions for an implementer:

- “Nothing is ever lost” is too broad: tool output is clipped to 30,000 characters, and its own prompt acknowledges that omitted summary clues may prevent discovery.
- Its short-message rule mentions `kind: text`, absent from its defined message kinds.
- Compaction rules prohibit placeholders, while the prompt describes an unsummarized-message placeholder; their intended scope needs clarification.
- Current-code truth and conflicting historical instructions need policy beyond its proposed “latest word” rule.
- Durable restart/retry behavior, message chunk boundaries, image storage, and recovery of an unavailable or damaged persisted view require implementation detail and tests.

The first three observations are direct inconsistencies or qualifications in the document; the latter two are design-review judgments. [Gist, sections 1–6](https://gist.github.com/VictorTaelin/91837951a5ce5b38f341ec1ba1df6449/3c190e06f34aba0c69f49042c526093269604935)

## What to test before committing

The accompanying local smoke trial reports success on Windows with Python 3.13.14, using an isolated `MEMORY_DIR`, synthetic notes, and explicitly supplied summaries. It exercised initialization, a small wake budget, compression requests, recall, zoom, summary invalidation/rebuilding, and rejection of an oversized note. This supports local CLI feasibility, not summary quality or useful recall over many sessions. [Recorded results](../trials/optmem/smoke-results.json)

Recommended comparison: no additional memory, a plain repository Markdown memory, and isolated OptMem stores using the same project facts and fresh-session questions. Assess older-fact retrieval, correction handling, source fidelity, avoided repeated work, and total reading/writing/compression effort. Include enough notes or a small enough wake budget to exercise actual compression. Do not judge success from a CLI demonstration alone.

A later experiment could test 512-byte summaries or persisted batch views separately. Full UniiChat becomes appropriate only if the desired product expands from a repository skill to a custom chat application with transcript capture and model-provider integration. This sequencing is an engineering recommendation, not an upstream requirement.
