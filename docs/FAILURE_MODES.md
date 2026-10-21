# Failure modes

The engine is built around specific, named ways that data reuse goes wrong. Each one has a guard.

## Of the method

| Failure | What it looks like | Guard |
|---|---|---|
| **Saturation / max-over-many** | A metric that is high for *everything* is measuring nothing. | Compare against a matched null before believing any rate. |
| **Orientation / sign flip** | Allele, strand, or effect direction silently inverted. | Be obsessive about orientation. A case that cannot be oriented is AMBIGUOUS, not classified. |
| **Wrong-key join** | Build mismatch, a biased or depleted column, an ID that does not map. | Test the join on known cases and count matches. Filenames lie. |
| **Selection that inflates** | The target or the threshold was chosen to produce the result. | Freeze definitions before looking; report what the frozen choice yields. |
| **Circularity (collider)** | The group was *constructed* on the very layer being tested, so the overlap is guaranteed. | Ask what the group's construction selected for, and compare against the ambient floor, not against zero. |
| **Power confound** | A difference between groups that is really a difference in detection, depth, or efficiency. | The power gate: residualize, condition, matched null, or build the signal orthogonal to power by design. |

The circularity and power failures are the subtle ones, because the number is computed correctly. **A correct number can still be a meaningless one.**

## Of the engine

| Failure | Why it happens | Guard |
|---|---|---|
| **Fabricated doubt** | A perpetual doubter under pressure to produce invents a doubt to justify the pass. | The §5c gate (pre-register what would move) + the asymmetric auditor + the rule that a dry pass declared honestly is a result. |
| **Over-pruning** | The auditor kills legitimate doubts because the defect is plausible but not demonstrable. | The burden of proof is the auditor's; when in doubt, SURVIVES. A KILL ratio over 50% is flagged as self-suspicion. |
| **HARKing** | A frozen hypothesis is quietly redefined after the result is seen. | Pre-registration in `ANT_REGISTRY.md` before data is touched. If the data contradicts the design, that is the finding. |
| **HARKing at the meta level** | Judging a doubt by whether it found something. | Judge the *design* of the doubt, not its outcome. A dry doubt may have been a perfect one. |
| **Believing pass 1** | One pass always has errors, and a fresh result is persuasive. | Nothing is CONFIRMED on the pass that produced it. |
| **Consensus blindness** | Everyone stops looking at what is closed. | The proactive layer, whose only job is to doubt the closed. |
| **Un-regenerable numbers** | A number that lives only in a chat message. | Every number traces to a committed script and a named input, or it is not a finding. |
| **Lost in-flight state** | The parent process dies and the subagent loses everything it had not written. | Persist as you go, never at the close. On resume, write to disk first. |

## The one that is fatal

Every failure above is recoverable, and most of them produce a receipt that makes the engine more trustworthy afterwards. **Fabricating a doubt is the exception.** An engine whose doubt cannot be trusted has nothing left to offer, because its only product is doubt that survived.
