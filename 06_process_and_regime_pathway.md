# Skill 06: Longitudinal Process-Sequence, Regime Discriminant, and OLS Audit Pathway (`06_process_and_regime_pathway.md`)

## 1. Activation
Invoked when the Method-Fit Diagnostic (`Skill 03`) identifies temporal phase sequences (`T0 -> T1 -> T2 -> T3`), static within-corner bifurcations, or multi-dimensional outcome regimes.

## 2. Three Deterministic Analytical Engines (`control/oma_engines.py`)
1. **Four-Stage Markov Process-Sequence & Information-Gain Engine (`analyze_process_sequences`)**:
   - Codes cases across sequential phases: `T0` (Initial Deployment & Mandate Structure), `T1` (Epistemic Encounter / Operational Breakdown Trigger), `T2` (Actor Mobilization Mode), and `T3` (Stabilized Authority Regime).
   - Computes stage Shannon entropies `H(Tk)`, Mutual Information `MI(T0..Tk; T3)`, Normalized Mutual Information `NMI` (% of final regime uncertainty explained at each stage), stage-to-stage Markov transition probability matrices `P(Tk+1 | Tk)`, and within-corner bifurcation tables.
2. **Multi-Dimensional Regime Typology & Kruskal–Wallis Discriminant Engine (`kruskal_eta2`)**:
   - Maps cases into the 2D/multi-dimensional outcome space (e.g., `DEC_AUTH x EPI_GEN -> Regimes I, II, III, IV`) and computes tie-corrected Kruskal–Wallis `H` and effect size `eta^2` across all first-order constructs.
3. **Additive Linear Net-Effects Failure Audit (`ols_failure_audit`)**:
   - Estimates standard OLS regressions on the same macro-conditions, reporting `beta, SE, t, R^2` and identifying specific cases where additive linear predictions commit crossover sign errors (`predicted > 0.50` vs. `actual < 0.50`).
