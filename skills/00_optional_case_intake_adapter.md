# Skill 00: Optional Case and Evidence Intake Adapter (`00_optional_case_intake_adapter.md`)

## 1. Scope and Activation (`intake_adapter_enabled`)
This module is an **optional upstream adapter** (`disabled` by default in `control/oma_control.py`). The core Open Method Architecture workflow assumes researcher-verified case boundaries and locatable evidence excerpts as its entry contract. Activate this adapter only when the researcher supplies raw PDFs/bibliographies and explicitly asks for help drafting or auditing a Case Registry.

## 2. Procedure
1. **Reconcile Publications -> Studies -> Candidate Cases -> Synthesis-Only Records**:
   - Separate empirical studies with bounded organizational/occupational units from field-level interviews, pre-deployment studies, and conceptual papers.
   - Flag multi-paper overlaps (same dataset or organizational site across publications) and within-paper discretionary subgroup splits (`is_discretionary_split = True`).
2. **Extract Verbatim Boundary Quotes**:
   - Record `case_id`, `study_id`, `setting`, `actors`, `ai_system`, `pdf_page`, and a verbatim boundary quote (`<=45 words`).
3. **Stop at Gate `G1_cases`**:
   - Present the reconciliation table and wait for researcher ratification before coding.
