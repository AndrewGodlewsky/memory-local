# First setup slice: validation evidence

Evaluated October 12, 2026, on Windows with Python 3.13.14. This records the initial explicit-capture slice, not an adoption decision.

## Scope

The repo-memory skill installs a pinned local OptMem tool, a repository-isolated launcher, persistent instructions, and an ignored store. The install is repeatable and preserves existing unrelated instructions and notes.

## Fresh-context observation

An independent writer agent received only the skill, a disposable fictional Harbor repository, and a request to remember two accepted decisions. It ran setup, recorded two notes, supplied its own requested summary, and checked recall. It added no answer-bearing project documents.

A separate reader agent with no inherited conversation received only the installed project and questions about storage, imports, prototype versus production, and the production hosting region. It read the installed instructions, used wake, recall, and zoom, and reported:

- Prototype storage uses SQLite because field technicians need deployment without a separate database service.
- That choice applies only to the prototype; production storage remains undecided.
- Imports preserve original external task IDs so retries can be recognized.
- No production hosting region was recorded, so no region could be named.

The reader cited original note IDs, preserved the reason and scope, and did not invent an answer to the unknown question. The writer and reader were explicitly authorized to simulate top-level project agents so the installed restriction on ordinary delegated agents would not invalidate the experiment.

## Mechanical checks

Run `python -m unittest discover -s tests -v`. The suite checks real CLI behavior, summary completion and original-note preservation, source provenance, isolated stores across directories and repositories, repeat setup with existing CRLF documents, and clear failures for absent stores, invalid notes, wrong roots, and conflicting tool files. Vendor attributes preserve source bytes when Git line-ending conversion is enabled.

The skill passed the bundled quick_validate validator. No additional model API key, service, or global installation was used.

## Limits

This is one synthetic explicit-remembering scenario. It does not establish automatic note selection, recall after deep compression, teammate handoff, statistical reliability, or acceptable maintenance cost. Those remain separate map slices. The generated store is an ignored local evaluation artifact; reproducible mechanics and the observations above are retained in source.
