# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.4.x   | ✅        |
| 0.3.x   | ⚠️ security fixes only |
| < 0.3   | ❌        |

## Reporting a vulnerability

Do **not** open a public issue for security problems. Email
`security@escape-room-puzzle-generator.dev` (or DM a maintainer on the
project Discord) with:

- A description of the issue
- Reproduction steps
- Affected version / commit hash
- Whether it's remotely triggerable

We aim to acknowledge within 72 hours and ship a patch within 14 days
for confirmed issues.

## Threat model

`escape-room-puzzle-generator` is a **local desktop tool**. It runs on
the operator's machine, reads local model weights, and writes room
bundles to `rooms/generated/`. It does not expose a network listener by
default.

Known non-issues:

- **Prompt injection via puzzle text.** Room text is untrusted input
  to the LLM. We sandbox generation prompts in
  `escape_room/services/llm/prompt_sandbox.py` and never let model
  output execute as code.
- **Malicious room bundles.** Room JSON is validated against
  `escape_room/models/room_schema.py` before load. Executable payloads
  in `custom_logic` fields are rejected.
- **Local file paths in bundles.** Bundles may reference local asset
  paths; the loader clamps to the configured `assets_root` and refuses
  traversal (`..`).

## Out of scope

- Denial of service against a user's own GPU by generating 10k rooms.
- Issues in third-party model weights you supply yourself.
- Anything requiring an attacker to already have code execution on the
  host.