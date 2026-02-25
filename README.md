## Public kit
- Audit prompt (two-shot): `prompts/audit_two_shot.txt`
- Public docs: `docs/`
  
stoppable-ai-control

Minimal Fail-Closed AI control loop demo (TG/WORM/IDF).

What this is

A minimal control pattern for AI systems that:
	•	STOP when uncertain (HOLD / FREEZE)
	•	Log reason codes and audit trails
	•	Resume only after verification (staged recovery)

Core idea

Most AI systems optimize for output.
This pattern optimizes for safe non-action.

Uncertainty → HOLD
Evidence verified → Controlled recovery (+stepwise)

Designed for
	•	Financial systems
	•	Governance workflows
	•	Compliance-heavy environments
	•	Safety-critical AI integration

Philosophy

This is not “smarter AI.”
This is controllable, auditable AI.
## Quick start
- Audit prompt templates: `prompts/`
- Minimal demo notes: `demo.txt`
- Docs (public): see PDFs in the root
