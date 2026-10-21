# The coordinator

The loop is not inside any agent. The executor's definition forbids it from scheduling itself, so **the coordinator is the only piece that sees the clock**. It fires one pass, reads the handoff that pass returns, and decides what to fire next. It holds no findings of its own.

This document is the contract. Everything in it is either a rule written into an agent's definition (cited by section) or an operational lesson with a receipt.

---

## 1. What the coordinator is

| It is | It is not |
|---|---|
| The heartbeat: it decides *when* the next pass runs | A doubter: it never proposes a doubt or a hypothesis |
| The parser of the `=== LOOP HANDOFF ===` block | A verifier: it never re-grades a finding's confidence |
| The dispatcher that keeps the three roles from invading each other | A reader of the ledgers: the handoff exists so the driver stays coherent *without* re-reading files (executor §4) |
| The only role that applies changes to an agent's own definition (executor §14) | An editor of `FINDINGS.md`, `ANT_REGISTRY.md`, `LOOP_LOG.md`, `DOUBT_AUDIT.md` or `ANT_status.md`, which belong to their owners |

The coordinator can be a human firing passes by hand, or a parent agent session on a timer. The contract is the same either way.

---

## 2. One iteration

```
                    ┌─────────────────────────────────────────┐
                    │  fire executor: one pass                │
                    │  (HUNT | VERIFY | RECONCILE)            │
                    └──────────────────┬──────────────────────┘
                                       │ returns === LOOP HANDOFF ===
                    ┌──────────────────▼──────────────────────┐
                    │  parse the handoff (§3)                 │
                    └──────────────────┬──────────────────────┘
                                       │
            ┌──────────────────────────┼──────────────────────────┐
            │                          │                          │
   every pass:                every N passes:            on ANT STATUS:
   fire secretary            fire doubt auditor          closeable-*
   (re-mark phases)          (KILL / SURVIVES)          → close, then open
            │                          │                 the next ant from
            └──────────────────────────┴───────► loop ◄── OPEN_QUESTIONS.md
```

1. **Fire the executor for exactly one pass.** Tell it the current date (it has no clock) and instruct it to **persist as it goes** (§6).
2. **Parse the handoff.** Nothing else in the return is a contract; anything after the block is ignorable.
3. **Fire the secretary** to re-mark that ant's phases against `PROTOCOL.md` on file evidence.
4. **Every N passes, fire the doubt auditor** over the passes since its last audit. N is the project's choice; 3 is the value this engine was run with.
5. **Act on `ANT STATUS`.** If it is `closeable-*`, close the ant and open exactly one new ant from `OPEN_QUESTIONS.md`. If it is `open`, fire the next pass as `NEXT PASS SHOULD` says.
6. **Repeat.** Do not stop to report intermediate findings or to ask whether to continue (§5).

---

## 3. Parsing the handoff

The executor ends every return with this block (executor §10). Each field drives one coordinator decision:

| Field | What the coordinator does with it |
|---|---|
| `ANT` | confirms which ant this pass belonged to |
| `PASS` · `MODE` | sanity: pass 1 is never final; a VERIFY must exist before any close |
| `FINDINGS this pass` | nothing, informational |
| `CONFIDENCE moves` | nothing, the executor owns confidence |
| `STILL SUSPECT/PLAUSIBLE` | if non-empty, a close is not available yet |
| `ARTEFACTS caught/retracted` | nothing, informational (a retraction is the engine working) |
| `RUNG` · `DRY PASSES at this rung` · `CLIMBED this pass` | if dry passes are accumulating at one rung with no climb, the next doubt-auditor batch is the check for fabrication (auditor §3.3, §3.6) |
| `OSCILLATING (flips >=3)` | surface it to the human: oscillation means the question is underdetermined, and the confidence level alone hides it |
| `ANT STATUS` | `open` → fire another pass · `closeable-positive` / `closeable-negative-diagnostic` → RECONCILE and close |
| `PROPOSED_DEFINITION_UPDATES.md` | if N > 0, the coordinator reviews the proposals (§7) |
| `NEXT PASS SHOULD` | the executor's own honest call for the next heartbeat, and the default instruction for the next firing |

If the block is missing or malformed, that is a failed pass: re-fire with the handoff requirement restated. Do not reconstruct the state by guessing.

---

## 4. Who fires whom, and why the schedule is shaped this way

| Role | Cadence | Why that cadence |
|---|---|---|
| Executor | every tick | It is the only role that moves state forward. One pass per invocation, by its own definition. |
| Secretary | after each pass | Its deliverable is only useful if it is current, and it is cheap: it runs nothing and reads files. |
| Doubt auditor | every N passes | It is a check, not a participant. Running it every pass would make it part of the rhythm it is supposed to judge from outside, and the costly audit has nothing to audit until several passes exist. |
| Human director | on a genuine block, on an oscillating finding, on a definition proposal | Judgement, not content (`PROTOCOL.md` decision rule 9). |

**The asymmetry is the coordinator's responsibility to protect.** The auditor can only `KILL` or `SURVIVES`. If the coordinator ever asks it "so what should we doubt instead?", the control is destroyed: its incentive becomes the executor's, and two doubters that share a failure mode validate each other. That is theatre, not a check. The reason the pairing works is that the executor fails by fabricating doubts and the auditor fails by over-pruning them: opposite failure modes contain each other.

---

## 5. The rules the coordinator cannot break

1. **Do not stop the loop to ask permission**, and do not stop to confirm an intermediate finding. The loop stops only on a genuine block: data that is inaccessible, or something only the human knows.
2. **One ant at a time.** When an ant closes, generate the next one from `OPEN_QUESTIONS.md`: one, never five half-done (`PROTOCOL.md` decision rule 7).
3. **Never promote a finding.** If the coordinator decides a SUSPECT is good enough, the entire verification protocol is void.
4. **Never let one role do another's job.** The executor does not schedule; the auditor does not propose; the secretary does not verify science; the coordinator does not doubt.
5. **A dry pass is a result.** A pass that honestly reports "no gateable doubt remained at this rung, so I climbed" is a successful pass. The coordinator must not treat it as a failure, because pressure to produce is exactly what makes a doubter fabricate.
6. **Supply the date.** Agents have no clock. Every firing passes the current date, or the ledgers drift.

---

## 6. Incremental persistence (learned the hard way)

**If the parent process dies, in-flight subagents lose everything they have not written to disk.** This is not hypothetical: a ~18-minute pass and an entire audit were both lost at once because each was saving only at the end.

The coordinator's obligations:

- **Every firing instructs the agent to persist as it goes**, not at the close.
- **On resume, the first instruction is always "write to disk whatever you already have, before continuing."** When the harness supports sending a message to an existing agent, resuming it preserves its context, so use that rather than a cold restart.
- **The coordinator creates empty file skeletons.** Some harnesses block writing *new* report-shaped files, so the agents should edit files that already exist. `scripts/bootstrap.sh` creates the empty ledgers for exactly this reason.

---

## 7. Definition updates

The executor may append a structural proposal to `PROPOSED_DEFINITION_UPDATES.md` and flag it in the handoff. It does not edit its own definition (executor §14). The coordinator reviews the proposal, validates the YAML frontmatter and the logic, and applies it; the change takes effect at the next session start.

The coordinator **rejects** any proposal that weakens a TOP RULE, grants an agent its own scheduling or tool permissions, or permits believing on first look, reporting un-regenerable numbers, or inflating a null. Those are foundational. A proposal that touches one of them is routed to the human, not applied.

---

## 8. When to stop

| Signal | Action |
|---|---|
| `ANT STATUS: closeable-*` and `OPEN_QUESTIONS.md` is empty | Stop and report: the queue is genuinely empty. |
| `NEXT PASS SHOULD: BLOCKED: need <inaccessible data>` | Stop that ant, record it as future work, open the next one. Do not estimate around missing data. |
| `NEXT PASS SHOULD: human attention: <reason>` | Stop and surface it. |
| A finding at `flips >= 3` | Keep looping, but surface it: the engine is oscillating on an underdetermined question. |
| The auditor kills more than half a batch | Surface it as possible over-pruning (auditor §5), not as an executor failure. |
| Drought at a rung with no climb, several passes running | Let the next audit rule on it. Fabrication is the one failure this engine cannot survive. |

A dry pass is never a stopping condition. Running out of doubt at one rung means the boundary of that rung's frame was reached, not the truth.

---

## 9. Scale and cost

- **A few delegations per tick is subagent territory**, and that is the right shape for one ant with three roles.
- **Dozens or hundreds of agents ranking hypotheses is workflow-script territory**: move the orchestration out of the conversation's context. Do not reach for the heavy tool for what the light one does better.
- Agent-to-agent conversation is not free: the coordinator carries history into every call, so cost grows with roles × rounds. One well-structured session beats several badly coordinated agents.
- Do not build the plumbing. The methodology is the value; the harness already exists.

---

## 10. Heartbeat implementations

All three are the same contract, differing only in who holds the clock:

| Implementation | How the tick happens |
|---|---|
| **Manual** | A human fires each pass and reads the handoff. This is the honest baseline, and it is how the engine was first run end to end. |
| **Fixed interval** | A parent session fires a pass on a timer (in Claude Code, `/loop <interval>`). Simple, and it wastes ticks when a pass runs long. |
| **Self-paced** | The parent launches the pass in the background and re-arms its own wakeup each round, pacing the next tick to how long the work actually takes. This is what a long-running pass wants. |

Whichever is used, the parent is the heartbeat. The executor's definition forbids it from becoming one.
