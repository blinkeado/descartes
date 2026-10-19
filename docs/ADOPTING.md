# Adopting the engine in your own project

The engine is four markdown agent definitions, a protocol document, and nine empty ledgers. There is no package to install and no service to run.

## 1. Copy the pieces in

```sh
scripts/install.sh /path/to/your/project
```

That copies `agents/` into `<project>/.claude/agents/`, the loop command into `<project>/.claude/commands/`, and `PROTOCOL.md` + `COORDINATOR.md` into the project root.

## 2. Create the empty ledgers

```sh
cd /path/to/your/project && /path/to/descartes/scripts/bootstrap.sh
```

This creates `.claude/agent-memory/<agent>/` with the nine headed-but-empty ledgers. Do this **before** the first pass: some harnesses refuse to create new report-shaped files, and the agents are instructed to edit files that already exist.

## 3. Pick the dataset and find the gap

Phase 0 of [`../PROTOCOL.md`](../PROTOCOL.md). Pick **one** dataset. Mine its own paper. Search in two passes — build, then refute. The gap you want is one the authors themselves reported and did not explain.

## 4. Freeze the hypothesis before touching data

Write the pre-registration into `ANT_REGISTRY.md`: the rationale, the universe, the frozen definitions, **what would falsify it**, and the power gate if the hypothesis compares groups. This is the step that makes everything downstream honest, and it is the easiest one to skip.

## 5. Start the loop

Fire the executor for one pass. Read the handoff. Fire again. See [`../COORDINATOR.md`](../COORDINATOR.md) — manual firing is a perfectly legitimate heartbeat, and it is how the engine was first run end to end.

---

## What you need to decide for your project

| Decision | Default | Note |
|---|---|---|
| Audit cadence `N` | every 3 passes | The auditor is a check, not a participant. |
| Drought threshold `K` before climbing a rung | 2–3 dry passes | Lower if your rungs are cheap. |
| Where analysis scripts live | `analysis/` | The secretary looks there for evidence. |
| Whether `PROTOCOL.md` needs project phases | usually not | If your domain needs different phases, write your own canonical document; the agents read it in preference to the shipped one. |

## What does not transfer

The phases are generic; **the domain layer is not.** Phase 7's translation step — turning a table into something that means something in your field — is the part no agent supplies. That is the human's contribution, and the engine is built on the assumption that it exists.
