# The doubt ladder

Doubt is expensive, so it is aimed. The targets are ordered by depth, and **each rung sees a class of error the rungs below are blind to by construction.**

| Rung | Target | The question |
|---|---|---|
| 1 | the number | does it reproduce from the committed script + the named input? |
| 2 | the method | is the metric an artefact — saturation, sign flip, wrong-key join, power confound? |
| 3 | the framing | is the question circular — does the way the group was *constructed* guarantee the answer? |
| 4 | the provenance of the evidence | who built this data, why, with what incentive, and what did that construction select for? |
| 5 | your own doubt | is my method blind to a whole class of error by design — am I only catching what it can already see? |

## The gate

**Run this before spending anything on a doubt.** Every doubt pre-registers what it would move:

> *"if this test returns X, finding F moves CONFIRMED → Y."*

If no possible result could move any confidence, the doubt is decorative — do not run it. That is a dry signal, not a finding. A doubt that skipped this gate is killable on sight (`ant-doubt-auditor` §3.1), and a doubt that passed the gate but still could not lose is killable as decorative (§3.2).

## Drought is a climb signal

K consecutive dry passes at rung N ⇒ climb to rung N+1.

Exhausting the doubt at a rung means the boundary of **that rung's frame** was reached, not the truth: the drought is the shadow of the assumption, not the signal of truth. The queue never legitimately dries, because there is always a rung above — the theory that makes the evidence legible, and the incentive that made that theory dominant.

Re-doubting a rung that is already dry, instead of climbing, is killable (§3.3). Fabricating a doubt to fill the pass is the gravest defect there is (§3.4) — and the one failure this engine cannot survive.

## The ladder is inversely priced

Rungs 1–2 are expensive (re-running joins over large inputs). Rungs 4–5 are cheap (reading methods, provenance, incentives) and see deeper.

**When the budget is tight, climb — never descend.** A rung-4 catch — a fact about how the dataset was *constructed*, not about the numbers inside it — is typically worth more than a hundred rung-1 re-runs.

## Record it

The current rung, every dry pass, and every climb go in `LOOP_LOG.md` and are surfaced in the handoff. A rung that is never recorded cannot be audited, and the secretary marks it ⚠️ rather than ✅.
