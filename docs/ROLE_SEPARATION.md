# Role separation

The separation of roles is not an implementation detail. **It is the mechanism that produces the self-corrections.**

An executor that tests against the data catches an orchestrator that reasons in the abstract, because the two make different mistakes. A single instance doing both shares its blind spot across both layers and has no way to see it. The division of labour is what generates the receipts.

## The asymmetric auditor

The doubt auditor can issue exactly two verdicts: `KILL` with a named, checkable defect, or `SURVIVES`. **It cannot propose anything**: not a doubt, not a hypothesis, not a ranking, not "a better version of this doubt would be...". Not even when it is obviously right.

The reason is structural:

- A perpetual doubter eventually runs out of honest doubt. At that point the temptation is to **fabricate a doubt to justify the pass**, and whoever fabricated it is the worst possible judge of whether they did.
- A self-auditor shares the bias. Two doubters watching each other share the *failure mode*, so they validate each other. That is theatre.
- An agent that **can only delete** never needs to invent in order to justify its own existence.
- Its failure mode, over-pruning, is the **opposite** of the executor's, which is fabricating. Opposite failure modes contain each other.

The moment the auditor is allowed to propose, its incentive becomes the executor's and the check is gone. That the auditor is right about what ought to be doubted is exactly why it cannot say so. If it sees a gap, its silence is part of the design: the gap is the executor's work.

`SURVIVES` is not an endorsement. It means "I found no defect".

## Fact vs judgement routing

Not every disagreement is resolved the same way:

| Disagreement | How it resolves |
|---|---|
| **Fact** ("the number is X" vs "the number is Y") | Independent verification against the data. The verifier opens the data with its **own** code, and it does not re-read the other role's script, because re-reading inherits the other's framing. |
| **Judgement / method** ("this metric is the right one") | Reasoning arbitration by a third role. |

The tie-breaker is invoked **per case**, not kept running, because a standing arbiter becomes a participant.

## The proactive layer

Every role except one is **reactive**: it answers a task it was given, and it shares the bias of stopping looking at whatever is already closed.

The proactive doubter exists to attack the blind spot no reactive process covers: *you do not know what you do not know to re-check*. It does not have to be right. It only has to raise the correct doubt: the proactive role opens the pot, the reactive roles determine what is inside. Originating a doubt and validating it in separate agents is what makes the system antifragile.

Its justification is a receipt, not a theory. See [`../examples/mpra-eqtl-discordance`](../examples/mpra-eqtl-discordance/): the project's headline finding was a design artefact, and nobody was looking for it.
