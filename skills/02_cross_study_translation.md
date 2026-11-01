# Skill 02: Cross-Study Theoretical Translation (`02_cross_study_translation.md`)

## 1. Scope
Evaluates whether differently named phenomena across studies represent equivalent constructs, computes pairwise Fuzzy Jaccard similarity `J(A, B)`, and formulates parallel translation branches (`G3_translation`).

## 2. Orthogonal Specification Requirement
Every proposed macro-condition must explicitly separate two dimensions:
1. **Theoretical Relationship (`aggregation_operator`)**:
   - `min`: Weakest-link conjunction (all constituents jointly required).
   - `mean`: Compensatory family resemblance (constituents partially substitute).
   - `max`: Functional substitutability (any constituent suffices, e.g., formal professional licensure OR deep client relational embeddedness).
   - `single`: Single constituent construct.
2. **Incomplete-Evidence Policy (`missingness_policy`)**:
   - `complete_component_required`: Any `NULL` constituent produces `NaN` for the macro-condition (case excluded in complete-case runs).
   - `boolean_absorption_available`: Uses mathematical absorption (e.g., `min(0.0, NULL) = 0.0`).
   - `available_component_fallback`: Computes `min`/`mean`/`max` over observed constituents; requires reporting exact affected cell counts.
   - `null_to_zero_imputation` / `null_to_one_stress`: Explicit lower-bound and upper-bound sensitivity stress tests.
