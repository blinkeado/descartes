# The confidence model

Every finding carries a level **and the method that set it**. A finding with no confidence is not a finding; it is a rumor.

| Level | Meaning | How it is set |
|---|---|---|
| `SUSPECT` | produced once, not independently re-checked | the HUNT-pass default; also any finding a later pass has not yet re-verified |
| `PLAUSIBLE` | reproducible + survived the artefact guards + one independent check | one VERIFY check passed |
| `CONFIRMED` | an independent method agrees AND an adversarial refutation failed | full VERIFY |
| `REFUTED` | an independent method or guard disagrees | retracted from the findings; the record is kept, with the reason |

## What promotes a finding

Agreement of **two genuinely independent methods** is what promotes to CONFIRMED — a different script, a different data source, a different orientation, or a failed adversarial attempt to refute it. Re-running the same script is reproduction, not independence.

If the two methods disagree, **that disagreement is the finding**, and it goes to `CONFLICTS.md` rather than being averaged away.

## What an entry looks like

```
- <the claim, one or two lines>
  — (script.py ← named_input.tsv) — CONFIRMED[two independent methods: direct test = 0 hits AND predictor AUC 0.58, p=0.24 vs matched null] — pass 4 · flips:1
```

## Stability: the flip count

Every finding also carries how many times its confidence has **reversed direction**. CONFIRMED → REFUTED → CONFIRMED is two flips. The count is never reset.

A CONFIRMED that arrived once and held is not the same claim as a CONFIRMED that has flipped four times. **Repeated flipping is the signature of an underdetermined question, not of progress** — and the level alone hides it, which is why any finding at `flips ≥ 3` is surfaced in the handoff regardless of where it currently sits.

## The closing rule

An ant cannot be closed-positive while any of its core findings sits at SUSPECT or PLAUSIBLE. It can always be closed **negative-diagnostic**, and that is a result: a negative that says *why* the question cannot be answered with this data is a finding. A negative inflated into a weak positive is not.
