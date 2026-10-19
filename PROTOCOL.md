# ANT — the protocol

*A discovery engine for data reuse: take public data that already exists and produce a closed, reproducible finding that the original study left open. The value is not in the data — it is in the cycle that interrogates it.*

This document is the canonical workflow. The agents in [`agents/`](agents/) implement it; [`COORDINATOR.md`](COORDINATOR.md) is the contract that drives them. Everything here was executed end to end before it was written down — the receipts live in [`examples/mpra-eqtl-discordance`](examples/mpra-eqtl-discordance/).

---

## Premise

Without generating new data, take existing public data and produce a finding the original study named but did not resolve. A paper that reports a number and does not explain it is an open gap, and the authors' own stated gap is the most defensible place to stand.

---

## Architecture: separated roles, one director

The engine does not run in a single instance. The separation is functional, not cosmetic.

| Role | What it does | Does NOT do | Persistent store |
|---|---|---|---|
| **Orchestrator** | Reasons, mines papers, checks SOTA by search, freezes rationale and hypotheses, designs the join, decides scope. | Does not touch raw data. | frozen hypotheses + decision criteria |
| **Executor** (`data-reuse-discovery-ant`, "Descartes") | Runs against the real files, verifies joins, re-runs from zero, holds the receipts. One pass per invocation. | Does not set strategy, does not schedule itself. | `FINDINGS.md`, `ANT_REGISTRY.md`, `LOOP_LOG.md`, `CONFLICTS.md`, `OPEN_QUESTIONS.md` |
| **Doubt auditor** (`ant-doubt-auditor`) | Rules on whether each doubt the executor ran was a real doubt: `KILL` with a named defect, or `SURVIVES`. | **Cannot propose anything** — no doubts, no hypotheses, no ranking. | `DOUBT_AUDIT.md` |
| **Secretary** (`ant-status-secretary`) | Marks every ant's phase state ✅/⚠️/❌/⏳ against this document, on file evidence only. | Runs nothing, verifies no science. | `ANT_status.md` |
| **Director** (human) | Supplies domain criteria, judges rigor, decides which hypothesis is worth running. | Is not the content encyclopedia (see decision rule 9). | — |

**Why this matters, and why it is not an implementation detail:** the role separation IS what produced the self-corrections. The executor caught the orchestrator's wrong genome build *because* it was testing against the data while the other reasoned in the abstract. A single instance doing both would have shared the blind spot across both layers. The division of labour is the mechanism that generates the receipts.

**Honest scope.** A human-in-the-loop orchestration pattern and a fully autonomous engine are different things, and the difference is where the heartbeat lives. See [`COORDINATOR.md`](COORDINATOR.md) for what is automated and what is not.

---

## The cycle: pre-phase 0 + seven phases

### Phase 0 — Reconnaissance (SOTA → gap → paper → dataset → ranked hypotheses)

Before touching a single datum: map the terrain.

- Pick ONE dataset and decline the others consciously, so the work is not diluted.
- Mine the dataset's own paper, and contrast it against current SOTA **by live search, never from training memory**.
- **Output:** a ranked list of gaps. The winner is usually not the obvious one — if the obvious analysis is what the paper already did, it is not a gap.

**★ The search method: the falsificationist double loop (an engine rule, not an option).**

A single search is dangerous precisely *when it looks sufficient* — it confirms the initial hypothesis and leaves you satisfied, which is confirmation bias with an extra step. The engine searches in two passes with different roles:

1. **Pass 1 — build (verificationist):** broad, unfiltered search to map the terrain and generate the candidate answer.
2. **Pass 2 — refute (falsificationist):** assume pass 1 is incomplete or wrong, and search deliberately to kill it — queries for guidelines, consensus, gold standards, limits, criticisms. What survives the refutation attempt is what is credible.

**Honest limit:** this reduces error, it does not eliminate it. There could be a third layer. Two passes (build + attack) capture most of the error at a reasonable cost; a third is reserved for when the stakes justify it.

### Phase 1 — Rationale + hypothesis

Every hypothesis carries its explicit mechanism BEFORE any result is seen. This is the anti-HARKing pre-registration, and it is frozen in `ANT_REGISTRY.md`.

The pre-registration states: the rationale, the universe (exactly which cases are in scope), the frozen definitions, **what would falsify it**, and — where it applies — the power gate (decision rule 12). If the data later contradicts the frozen design, that is a finding, not a licence to redefine the design.

### Phase 2 — Data acquisition + verification

Download the integration datasets and verify they are what they claim to be.

**Test the join, not the filename.** Filenames lie: a file named for one genome build can carry another; a column named `target` can be the wrong entity. Probe the real join on known cases and count the matches before trusting anything downstream.

### Phase 3 — Test (integration, model-free first)

The core of the finding is built from table joins, without a model.

- If a join answers the question, train nothing. Compute is rarely the bottleneck.
- **Sanity-check traffic light:** first reproduce a number the paper itself reports. If it does not reproduce, there is a bug upstream — in the allele orientation, the key, the build — and nothing downstream can be believed yet.
- Only then run the actual cross you pre-registered.

### Phase 4 — Enhancement / corroboration with SOTA

Lift the claim from association to mechanism using the best available tool.

- Reuse existing scripts rather than writing new ones.
- **Verify SOTA against the live web, not against memory.** Tool names, versions and capabilities drift; a confident memory of a tool that does not exist is a fabrication with a citation.

### Phase 5 — Self-audit + retraction

The step that separates the engine from a pipeline that emits whatever it computed.

Ask "what is the dumbest way this could be an artefact?" and test it:

- **Saturation / max-over-many** — a metric that is high for *everything* is measuring nothing. Compare against a matched null.
- **Orientation / sign flip** — allele, strand, effect direction. Be obsessive; a case that cannot be oriented is AMBIGUOUS, not classified.
- **Wrong-key join** — build mismatch, a biased or depleted column, an ID that does not map.
- **Selection that inflates** — a target or threshold chosen to produce a result.

A broken number is **caught and retracted**, not reported. Self-correction is the signature, not the defect. When a claim survives at a weaker level than it was stated, the claim is narrowed to what the evidence supports — the gap between levels of evidence is itself the finding.

### Phase 6 — Reproducibility QC

The deliverable must run from zero for a third party.

- Every number traces to a committed script that reads a named input file. Zero inline, zero hardcode.
- **Figures read their numbers live from files.** Making a figure read live data is not cosmetic: it is a test, and it routinely exposes a wrong hardcoded value.
- Map phase → script, and re-run with all derived files deleted.

### Phase 7 — Close + translation

Freeze the scope and add the layer only the domain expert supplies.

- Inaccessible data (controlled access, paywalled, missing) is **explicit future work**, not a diluting "pending".
- A close is **positive** or **negative-diagnostic**. Both are results. A negative that says *why* the question cannot be answered with this data is a finding; a negative dressed up as a weak positive is misconduct.

---

## The decision rules (how the engine decides)

1. **Test, don't trust names.** Filenames, builds, SOTA recalled from memory → verify against reality (the join, a live search, a re-run).
2. **The authors' own gap beats an invented gap.** Standing on a number the paper reported and did not resolve is the most defensible position.
3. **Model-free first.** If a table join answers the question, train nothing.
4. **Rationale before result.** Freeze the mechanistic why before looking, or it is HARKing.
5. **Retract > inflate.** A broken number is caught and withdrawn.
6. **Freeze scope.** What is inaccessible is explicit future work, not a pending item that dilutes everything else.
7. **Sequential, not parallel.** One exhaustive end-to-end hypothesis at a time — an "ant" — never five half-done. While a heavy analysis runs, the other ant is a thinking ant (rationale, screening), not a second grinding job.
8. **Double loop on search.** Pass 1 builds, pass 2 refutes.
9. **Decision routing — the question does not go to the human first.** A decision enters the evidence cycle (SOTA + literature), NOT the human's memory. The human is the judge of rigor over what the cycle brought back, not the encyclopedia of content. Content comes from the literature; judgement comes from the human.
10. **Disagreement: fact vs judgement.** A disagreement of **fact** → independent verification against the data (open the data with your own code; do not re-read the other role's script). A disagreement of **judgement/method** → reasoning arbitration by a third role. The tie-breaker is invoked per case, not kept running.
11. **Nothing is closed forever (persistent cartesian doubt).** Every finding declared "closed" enters the re-examination queue. Reactive roles stop looking at what is closed; the proactive doubter does not. This is the antifragility layer — without it, the team's consensus is a blind spot.
12. **Power gate (mandatory before proposing).** Any hypothesis that compares groups by effect magnitude, detection, reproducibility, or abundance of connections MUST include, in its pre-registration, an explicit control for the statistical-power confounder BEFORE it runs: residualize against sampling depth and baseline level; or condition on success; or use a permutation/matched null per class; or build the signal so that it is orthogonal to power by design (sign/direction instead of magnitude). If a difference between groups does not survive conditioning on power, it is an artefact, not biology. Frozen in phase 1, verified in phase 5.
    - **Robustness hierarchy against power** (most fragile → most robust): count of detections ❌ < correlation magnitude ❌ < fraction/ratio ⚠️ < sign/direction in a within-group contrast ✅ (orthogonal to power by construction). Prefer signals from the robust end.

---

## The confidence model

Every finding carries a level and the method that set it. A finding with no confidence is not a finding.

| Level | Meaning | How it is set |
|---|---|---|
| `SUSPECT` | produced once, not independently re-checked | the HUNT-pass default |
| `PLAUSIBLE` | reproducible + survived the artefact guards + one independent check | one VERIFY check passed |
| `CONFIRMED` | an independent method agrees AND an adversarial refutation failed | full VERIFY |
| `REFUTED` | an independent method or guard disagrees | retracted from the findings; the record is kept with the reason |

**Stability (flip count).** A finding also carries how many times its confidence has *reversed direction*. A CONFIRMED that arrived once and held is not the same claim as a CONFIRMED that has flipped four times: repeated flipping is the signature of an underdetermined question, not of progress. See [`docs/CONFIDENCE_MODEL.md`](docs/CONFIDENCE_MODEL.md).

An ant cannot be closed-positive on SUSPECT or PLAUSIBLE findings.

---

## Where to aim the doubt

Doubt is expensive, so it is aimed. The targets are ordered by depth, and the ladder is **inversely priced** — the deep rungs are the cheap ones. Drought at a rung is a signal to climb, never a licence to fabricate a doubt. See [`docs/DOUBT_LADDER.md`](docs/DOUBT_LADDER.md).

---

## The proactive layer

Every role other than the proactive doubter is **reactive**: it answers a task it was given, and it shares the bias of stopping looking at what is already closed. The proactive layer exists to attack the blind spot no reactive process covers — you do not know what you do not know to re-check.

It does not have to be right. It only has to raise the correct doubt: the proactive role opens the pot, the reactive roles determine what is inside. Originating and validating in separate agents is what makes the system antifragile. Its empirical justification is a receipt, not a theory — see [`examples/mpra-eqtl-discordance`](examples/mpra-eqtl-discordance/), where the project's headline finding turned out to be a design artefact that nobody was looking for.
