# Retrieval and correction evaluation — issue 5

Synthetic scenario and evaluator key. Keep this file outside the evaluated
repository and outside reader prompts. This tests retrieval over supplied
history, not whether an agent autonomously selected the right notes.

## Fixture and authoring procedure

Project: BeaconField, a fictional field-work application. Fixture:
`.test-work/deep correction project`. Install the current repo-memory setup in
that disposable Git repository, then set `WAKE_LINES=2`.

Save notes 0–15 as the first authoring batch, settle summaries through the real
CLI, then save notes 16–35 as a later batch and settle the remaining summaries.
The working model must read each `nap` prompt and write its summary. Capture the
prompt for range 0–31: it must contain the two child summaries rather than all
32 originals. These are two simulated work batches; this authoring alone is not
evidence of independent chat capture. Fresh readers provide the independent
context boundary.

Create `export-settings.json` with field formats `["csv", "json"]`, admin
formats `["json"]`, and kiosk retention 14 days. This deliberately contradicts
part of accepted intent; it does not establish a new decision. Create `ui.txt`
containing `BeaconField Export` for the unrelated edit trial.

The following strings are the complete raw corpus, in append order. All are
synthetic, not decisions for the real memory-local repository.

```json
[
  "Exports decision, workshop A: field clients export CSV only because work sites run offline. Processing must remain local; admin export formats are undecided.",
  "Exports proposal, workshop A: PDF might help supervisors. No PDF support, delivery date, customer request or budget has been approved.",
  "Export retention decision, workshop A: generated exports expire after 14 days on both shared kiosks and private admin devices to limit cached personal data.",
  "USB audit filenames decision, workshop A: use prefix handback- only for USB export audit files; handoff- collides with a reserved scanner prefix. Other filenames are unaffected.",
  "Audit timestamps decision: store UTC timestamps so support can order events from multiple sites consistently. Display-time locale is separate.",
  "Import finding, fixture BOM-2: CSV files with a UTF-8 BOM are valid and must parse; stripping the first column header caused a lookup failure.",
  "Keyboard decision: Escape cancels a modal without saving edits; explicit Save commits the change. This applies to desktop dialogs.",
  "Task ordering finding: sorting only by label produces unstable ties. Use stable task ID as a secondary key when labels match.",
  "Attachments decision: accept PNG and JPEG in the pilot; SVG remains deferred because active content handling is not implemented.",
  "Backup decision: create an encrypted local backup nightly while the app is running; do not require network availability for backup creation.",
  "Site numbering decision: task sequence numbers are local to each site. Site ID plus task number is the unique external reference.",
  "Pilot scope decision: test at two sites before adding cross-site coordination. More pilot sites require a later scope decision.",
  "Startup constraint: field clients must open existing local tasks without a connectivity probe. Offline work is a normal operating state.",
  "Locale decision: pilot interface copy uses en-US. Translation proposals remain outside the pilot scope.",
  "Notifications decision: task-completion notices stay inside the application. Email delivery has not been approved for the pilot.",
  "Search finding: case-folding task labels prevents duplicate search results for mixed-case imports. Original display labels remain unchanged.",
  "Pagination decision, workshop B: task lists show 50 rows per page to keep the field view responsive on older tablets.",
  "Exports addition, workshop B, extends note #0: add JSON only for the private admin archival endpoint. Field CSV and the local/offline processing constraint remain unchanged.",
  "Admin archive finding: a JSON round-trip preserves stable task IDs. This validates the archive format, not JSON availability in field clients.",
  "Settings proposal: a compact display mode could help small screens. No implementation commitment or default-mode decision was made.",
  "Autosave decision: comments save after explicit submission. Draft text remains local until submitted so accidental edits are not published.",
  "Import errors decision: report the row number and column name, while leaving already stored tasks untouched when validation fails.",
  "Theme decision: follow the device light/dark preference by default; a user-selected theme overrides it on that device.",
  "Archive restore finding: duplicate task IDs must fail validation before restore modifies stored tasks; the collision fixture reproduced a partial-write bug.",
  "Export retention replacement, workshop B, supersedes #2 for shared-kiosk CSV only: expire after 7 days to reduce exposure on shared devices. Private admin exports retain 14 days.",
  "Training decision: include one offline export exercise in pilot onboarding. This adds training material, not a new export format.",
  "Touch target decision: field controls require at least 44 CSS pixels to remain usable with gloves; desktop density is unaffected.",
  "Deleted tasks decision: hide archived tasks from the default list but retain them in the archive view. Archiving does not erase task history.",
  "Recovery finding: interrupted attachment copies leave temporary files. Startup cleanup may remove unfinished temp copies, not completed attachments.",
  "Release constraint: a pilot build must include a local rollback package because a field site may have no internet connection.",
  "Label proposal: changing Complete to Done is still under discussion. Keep existing labels until the pilot coordinator accepts a wording change.",
  "Metrics decision: record import duration locally for pilot troubleshooting. Uploading telemetry to a service has not been approved.",
  "Printer finding: the pilot tablet cannot discover network printers while offline. This does not establish a decision to add PDF or cloud printing.",
  "Permissions decision: only private admin users can run archive restoration. Field task editing does not grant restore permission.",
  "Exports observation, export-settings.json: field formats currently include csv and json and kiosk retention is 14 days. This conflicts with #17 and #24; no decision approved that divergence.",
  "Pilot scheduling open question: the next review date is not yet supplied. No export deadline or release date can be inferred from the trial setup."
]
```

## Reader prompts (send separately, without this key)

1. **Relevant retrieval:** "In BeaconField, advise what export formats field
   clients and private admins should support, how long their generated exports
   should remain, and what prefix USB export audit filenames should use. Explain
   the reasons and scope. Compare this with export-settings.json and identify any
   unresolved conflict. What is the approved PDF export deadline? Cite evidence."
2. **Unrelated task, independent reader:** "Change the title in ui.txt from
   BeaconField Export to BeaconField Exports. Keep the rest of the file unchanged."
3. **Ambiguous conflict, independent reader or follow-up:** "The settings file
   already allows JSON in the field. Make exports consistent." The agent should
   identify that alignment direction is unspecified before making a contrary
   intent choice; it may safely propose aligning implementation with the clear
   existing decision, explaining why, rather than declaring JSON approved.
4. **Explicit revision, separate mutable fixture copy:** "New decision: field
   clients may also export JSON locally for the pilot. CSV must remain supported
   and offline operation is still required. Update the project memory to capture
   this change." Expected addition to field formats, no removal of CSV, no
   unrelated retention revision. Existing shared-authority guidance applies if
   present, but keep this test's raw prior history available only through OptMem.

## Evaluator key and observations to collect

- Relevant originals: #0 initial field-only CSV reason/scope; #17 adds private
  admin JSON without removing field CSV; #2 retains the old 14-day rule; #24
  replaces only shared-kiosk CSV retention with 7 days, leaving private admin
  at 14; #3 requires `handback-` for USB export audit files only. Private admin
  CSV support was never specified; do not invent an exclusive admin JSON policy.
- #34 and the settings file are implementation evidence, not supersession.
  They expose field JSON and kiosk retention divergences. Explicit user revision
  may change the policy; ambiguous consistency requests should expose the choice.
- #1 and #35 supply no approved PDF date. Honest unknown is required.
- Record original note IDs actually retrieved, recall/zoom/wake/nap call counts,
  unrelated search effort, unsupported claims, stale advice, scope omissions, and
  any summary that loses qualifications. Exact wording is not an acceptance test.
- Check the startup summary. If #3's literal prefix survives, do not claim this
  run proved recovery of an omitted filename detail; choose another omitted old
  fact for a new fresh-reader question or record that limitation.
- Separately hash `LOG.txt`, invalidate summary `0-31` with `forget`, observe
  pending regeneration, rebuild via actual `nap` prompts, then verify identical
  raw-log bytes and original retrieval. `forget` invalidates summary caches;
  it never deletes source notes. Keep this rebuild after reader snapshots so it
  cannot alter the evidence delivered to the first reader.

## Results

Fixture construction complete: 36 original notes and 34 model-written summaries
(18 pairs, nine groups of four, four groups of eight, two groups of 16, one group
of 32). Each summary was supplied after reading the corresponding real `nap`
prompt. The 32-note prompt contained only summaries 0–15 and 16–31; its transcript
is retained outside the fixture in `.test-work/correction-root-summary-prompt.txt`.

The two-line startup view omits the exact old `handback-` prefix and its scanner
collision reason, retaining only a USB audit naming breadcrumb. Original #3
remains available for the fresh reader. Export amendments remain in the overview,
so this setup does not establish recovery of an omitted amendment.

All supplied original notes are at most 190 UTF-8 bytes. No byte-limit retries
were needed. After installation, authoring used 36 note commands, 34 summary
writes, three pending-summary inspections, one size configuration, and one
startup read: 75 memory CLI calls. The fixture
is intentionally dense; this maintenance count is not an estimate for ordinary
work. Initial and later notes were authored by one informed model in separate
batches, not independent chats. Summary authoring was not blind to the evaluator
key; independent fresh readers assess retrieval, not unbiased summary quality.

The parent orchestrated two independent readers after construction:

| Trial | Observed behavior | Memory effort |
| --- | --- | --- |
| Relevant question | Retrieved originals #0, #1, #2, #3, #17, #24, #25, #32, #34, #35. Correctly retained field CSV, limited the JSON addition to private admin archival support, applied 7 days only to shared-kiosk CSV while private admin remained 14 days, surfaced the settings conflict, and reported PDF deadline unknown. Recovered `handback-` and scanner-collision reason omitted from startup summaries. No target scope omissions, stale advice, or unsupported claims reported. | One `wake`, one focused `recall`; no `zoom` needed because recall returned originals. |
| Unrelated title edit | Changed only `BeaconField Export` to `BeaconField Exports` in `ui.txt`; the reader byte-verified the remaining file contents. No exhaustive memory traversal or routine note creation. | One `wake`; zero `recall`, `zoom`, or `note` calls. |
| Blind ambiguous consistency request, separate fixture snapshot | Treated settings as implementation evidence, not approval for field JSON. Cited #0/#17, #24, #34; asked whether the user intended a policy change or alignment with CSV-only field intent and flagged retention as a separate discrepancy. Made no changes. | One `wake`, one `recall`. |

After both readers completed, supported `forget 0-31` invalidated exactly one
summary. A fresh real `nap` prompt again supplied the two 16-note child summaries;
the model wrote a replacement within the byte limit. Startup reading then
succeeded, and `recall` still returned original decisions #0, #2, #3, #17, #24
with the literal old filename evidence. Raw-log SHA-256 was identical before
and after: `3cf6c75b43c5f1a6c3d772c699b54ac20823af5f6bcd6401a87682ed2eb4aa78`.
The store still contained 36 originals and 34 summaries. Rebuilding cost one
`forget`, one pending `nap` inspection, one summary `nap`, one `recall`, and one
`wake`. This demonstrates cache invalidation and raw preservation; a rebuilt
summary cannot recover details absent from its two supplied child summaries.
Evidence is in `.test-work/correction-rebuild-result.json`, outside the fixture.

In a separate mutable snapshot, the explicit-revision writer appended note #36,
linking #0/#17, and updated the shared export record. The new decision adds local
field JSON for the pilot while retaining CSV and offline processing; it does not
change retention or approve PDF. It used two `recall` calls, one `wake`, one
`note`, and one `nap` status check. At 37 notes no new group completed, so no new
summary was needed.

The fresh blind amendment reader then passed with one `wake` and one focused
`recall`. Citing the shared record and #36, it allowed field CSV plus local JSON
within the pilot, retained required CSV and the offline reason, and left field
JSON beyond the pilot undecided. It retained private-admin archival JSON from
#17 and the scoped retention rules from #2/#24: kiosk CSV 7 days, private admin
14 days, with no invented 7-day rule for JSON. It recognized that field CSV/JSON
settings now agree with pilot intent, while the kiosk 14-day setting still
conflicts. The historical field-format conflict in #34 was superseded by the
explicit decision; the retention conflict was not. PDF remained unapproved with
no known deadline (#1/#32/#35). No invented completion or writes were reported.

An earlier assisted ambiguous follow-up is excluded from acceptance evidence.
The revision writer reused an implementation-aware documentation agent in a
separate context from this fixture's author, with no corpus/key. It was not a
blind writer. The independent blind ambiguity reader and future amendment reader
provide separate evidence; neither turns the informed authoring into a blind
capture trial.
