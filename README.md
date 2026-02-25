# stoppable-ai-control

Minimal **fail-closed** AI control loop demo (**TG / WORM / IDF**).  
An audit-first pattern where the system **stops when uncertain** and **resumes only after verification**.

## What this is
A minimal control pattern for AI systems that:
- **STOP when uncertain** (HOLD / FREEZE)
- **Log reason codes and audit trails**
- **Resume only after verification** (staged recovery)

## What this is not
- Not an **accuracy benchmark**
- Not an **optimization** engine
- Not a medical / policy recommendation system  
This repo demonstrates a **controllable, auditable control loop**.

## Core idea
Most AI systems optimize for output. This pattern optimizes for **safe non-action**.

- Uncertainty → **HOLD**
- Evidence verified → **Controlled recovery** (stepwise)

## Public kit
- Audit prompt (two-shot): `prompts/audit_two_shot.txt`
- Prompt templates: `prompts/`
- Public docs: `docs/` (and PDFs in the repo root)
- Minimal demo notes: `demo.txt`
- Audit artifacts (ZIP): `covid_seed_audit_pack.zip` *(see “Audit artifacts” below)*

## Audit artifacts (ZIP)
`covid_seed_audit_pack.zip` includes:
- `run_manifest.json` (run config + dataset hash)
- `idf_timeline.csv` (FREEZE/RECOVER/NORMAL timeline)
- `miniMIL` Decision Packets (JSONL) with `input_hash` and `rule_hash`
- `tg_audit.jsonl` (PASS/HOLD with reason codes)
- `worm_log.jsonl` (hash-chain; tamper-evident audit trail)
- `metrics.json`, `conformance.json`, `undefined_report.json`

## Safety notes (important)
- The included COVID example uses a **simulated dataset** to demonstrate fail-closed audit behavior.  
  It is **not** intended for medical or policy decisions.
- The WORM “signature” in this demo is **illustrative**.  
  Production deployments require proper key management and standard digital signatures.

## Quick start
1) Read the public slide deck (PDF) to understand the story: **why it stops and why it’s safe**  
2) Check the audit pack (ZIP) files above to verify:
   - where HOLD happened
   - why it happened (reason codes)
   - that the trail is tamper-evident (hash-chain)

## License
Add a LICENSE file (MIT/Apache-2.0/etc.) if you want frictionless reuse.
