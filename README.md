# Auditing Epistemic Guardrails From Their Own Artifacts

Independent artifact audit of the three headline claims of *Epistemic Edge:
Subjective Logic Guardrails for LLM-Driven IoT Actuation* (Syed & Silaghi,
IEEE IRI 2026), recomputed from the released ground-truth result files in
[epistemic-edge](https://github.com/jemsbhai/epistemic-edge) without
re-running any LLM or the BATADAL pipeline.

Conducted at the Apart Research **AI x Epistemics Research Sprint**,
November 13-15, 2026. The audited system and paper are preexisting work by
the audit's author, disclosed in the report; the audit, its analyses, and
this report are the sprint-period work.

- `audit_epistemic_edge.py` - the audit script (stdlib only)
- `audit_results.json` - its full output
- `report/` - the sprint report (LaTeX source + PDF)

Run: `python3 audit_epistemic_edge.py <path-to-epistemic-edge-repo>`

License: MIT
