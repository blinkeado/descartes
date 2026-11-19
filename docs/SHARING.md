# Sharing workflow definitions and run records

## Identify the materials

The agent definitions, coordinator contract, protocol, command and empty templates describe the workflow. They can be inspected and reused without access to a project's private records.

A research run produces its own instructions, hypotheses, scripts, inputs, outputs, ledgers and corrections. These establish how the workflow was applied. The definitions alone do not establish that every rule was followed in a particular run.

Keep software definitions and project records separately identifiable. An example, excerpt or selection must state its scope and include the records needed to check it.

## Preserve the version used

For each run, record the engine commit, the project-specific instructions and any authorized departures from the protocol. Keep the original records and their file hashes. For an uncommitted artifact, record that status and its observed file hash instead of assigning it a commit it did not have.

Updates to the engine create a new version. They do not change the instructions under which an earlier pass ran. Record when a change took effect.

## Protect personal information

Check files, file metadata, commit messages and the history that would become accessible before sharing a repository. Remove credentials, private contact details, personal filesystem paths and private session identifiers from the copies intended for sharing. A file's extension does not determine whether it contains private information.

Use consistent markers for literal redactions. Retain the source commit or artifact identifier, original file hash, copy hash and the type of redaction. Keep the mapping to private values private. Do not expose the removed values in a public diff or redaction report.

Preserve scientific claims, observations, calculations, outcomes and their order. When a record contains an error, include its correction and current status so that an earlier claim is not presented as the final result. Identify corrections made by other roles or external contributors.

An anonymized copy has different bytes and a different hash from its original. Identify it as a derived copy. Preserve the original securely; an index or later summary can help navigate the records but does not replace them.

## State the access conditions

Workflow definitions and research records can have different access conditions. State which materials are public, restricted, available on request or not retained. Availability statements must describe the materials and access actually provided.

Keep the software license and attribution with the workflow. Identify the sources and applicable rights of separately supplied data and third-party materials.
