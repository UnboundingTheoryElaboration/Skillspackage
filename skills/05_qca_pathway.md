# Skill 05: Deterministic fsQCA and Enhanced Standard Analysis Pathway (`05_qca_pathway.md`)

## 1. Procedure
1. **Substantive Calibration**: Apply `cal_linear(1.0, 2.9, 5.0)`, `cal_logistic(1.0, 2.9, 5.0)`, and `cal_direct` via `control/oma_engines.py`. Verify matrix integrity via `oma_control.validate_matrix()`.
2. **Separate Necessity & Sufficiency for Outcomes and Negations**:
   - Evaluate necessity (`inclN >= 0.90, RoN >= 0.60, covN`) and sufficiency (`incl >= 0.80, PRI >= 0.60, n >= 1`) for every focal outcome (e.g., `DEC_AUTH`, `GEN_AUTH`) and its negation (`~DEC_AUTH`, `~GEN_AUTH`).
3. **Exhaustive Minimization & Enhanced Standard Analysis (ESA)**:
   - Identify and exclude Contradictory Simplifying Assumptions (CSAs—remainders used in both positive and negated parsimonious solutions) and document any blocked remainders.
   - Report all logically equivalent Conservative, Parsimonious, and Intermediate models (`exhaustive_search_completed: True`).
4. **Robustness & Rival Audit**:
   - Run threshold grids (`incl`, `PRI`, `n_cut`), orthogonal translation/missingness branches, discretionary-split exclusions, Leave-One-Study-Out (LOSO), and single-condition rival sufficiency tests.
