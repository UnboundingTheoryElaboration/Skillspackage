# Skill 03: Method-Fit Diagnostic and Analytical Routing (`03_method_fit_and_routing.md`)

## 1. Scope
Executes `oma_engines.evaluate_method_fit()` after Cross-Study Translation (`Skill 02`) to diagnose the intrinsic structure of the evidence base and recommend the best analytical pathway(s) (`G3B_method_fit`).

## 2. Diagnostic Criteria & Routing Matrix
| Empirical Evidence Structure | Recommended Analytical Pathway | Engine Invoked |
|---|---|---|
| Comparable bounded cases (`N >= 15`), moderate outcome balance, cross-sectional end states | **Pathway A: Deterministic fsQCA** (`Skill 05`) | `oma_engines.truth_table`, `solve_all` |
| High share of longitudinal/ethnographic studies (`>= 40%`), explicit temporal phases (`T0 -> T1 -> T2 -> T3`), or static within-corner bifurcations | **Pathway B: Longitudinal Process-Sequence & Shannon/NMI Information-Gain Analysis** (`Skill 06`) | `oma_engines.analyze_process_sequences` |
| Multi-dimensional outcome space (e.g., `DEC_AUTH x EPI_GEN`) where single-dimension collapse conflates distinct regimes | **Pathway C: Multi-Dimensional Regime Clustering, Kruskal–Wallis `eta^2` & OLS Audit** (`Skill 06`) | `oma_engines.kruskal_eta2`, `ols_failure_audit` |
| Both cross-case conjunctural equifinality AND longitudinal breakdown/mobilization sequences (as in the 30-article AI authority corpus) | **Hybrid Best-Fit Strategy: Pathways A + B + C Triangulation** | All three deterministic engines in `oma_engines.py` |
| Purely conceptual/field corpus or unparameterized actor interaction rules | **Synthesis-Only Elaboration / ABM Specification-Gap Report** (`Skill 07`) | Qualitative relational synthesis without forced numerical calibration |
