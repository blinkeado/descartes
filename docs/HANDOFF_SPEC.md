# The handoff block

The executor ends **every** return with this block. It exists because the loop driver is effectively stateless: it does not re-read the ledgers, so the block is how it stays coherent.

```
=== LOOP HANDOFF ===
ANT: <id + one-line hypothesis>
PASS: <n> · MODE: <HUNT|VERIFY|RECONCILE>
FINDINGS this pass: <added A, re-graded B>  (ledger total: <M>)
CONFIDENCE moves: <e.g. "F3 SUSPECT→CONFIRMED; F5 → REFUTED (artefact)"  OR  "none">
STILL SUSPECT/PLAUSIBLE (need another pass): <list finding ids  OR  "none">
ARTEFACTS caught/retracted: <list  OR  "none">
RUNG: <1-5> · DRY PASSES at this rung: <k> · CLIMBED this pass: <no  OR  "N→N+1, reason">
OSCILLATING (flips ≥3): <finding ids + counts  OR  "none">
ANT STATUS: <open | closeable-positive | closeable-negative-diagnostic>
PROPOSED_DEFINITION_UPDATES.md: <N PROPOSED  OR  none>
NEXT PASS SHOULD: <one of: "VERIFY findings <ids>", "extend to <sub-analysis>", "RECONCILE + close (positive|negative-diagnostic)", "BLOCKED: need <inaccessible data> — future work", "human attention: <one-line reason>">
=== END HANDOFF ===
```

## Rules

- **Always present**, even when every field is `none` or zero. A missing block is a failed pass.
- **Counts are accurate.** The block is a contract, not a summary.
- **It goes last.** Anything after `=== END HANDOFF ===` is ignored by the parser.
- `NEXT PASS SHOULD` is the executor's own honest call for what the next heartbeat should do. The coordinator may override it, but it starts there.

## What the coordinator does with each field

See [`../COORDINATOR.md`](../COORDINATOR.md) §3 for the field-by-field decision table. In short: `ANT STATUS` decides whether to close, `STILL SUSPECT/PLAUSIBLE` blocks a positive close, `RUNG`/`DRY PASSES`/`CLIMBED` feed the next doubt audit, `OSCILLATING` goes to the human, and `NEXT PASS SHOULD` is the default instruction for the next firing.

## Why a block and not prose

A stateless driver parsing prose has to interpret, and an interpreting driver eventually promotes a SUSPECT because the sentence sounded confident. Fixed fields cannot be read optimistically.
