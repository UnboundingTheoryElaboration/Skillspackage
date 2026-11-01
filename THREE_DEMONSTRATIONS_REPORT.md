# Open Method Architecture Skill — Three Executed Empirical Demonstrations

This report summarizes the three demonstrations recomputed from source matrices by `python3 control/run_three_demos.py`:

1. **Demonstration 1 — UTD24 Journal Submission AI-Integration QCA Replication & Reconstruction (`Forced QCA Mode`)**:
   - **Part 1A (55-Case / 64-Row Table A1)**: Verifies all 26 observed rows, proves that reproducing Paths 2 (`~KC*MA*IA*TE*EU`) and 3 (`ER*~MA*IA*TE`) requires blocking empty remainder rows `32` and `64` under Enhanced Standard Analysis (ESA), and shows that threshold invariance across `incl = 0.70–0.85` is an artifact of `PRI >= 0.60` being binding.
   - **Part 1B (53-Case / 30-Article Raw Dual-Coder Re-Execution)**: Separates theoretical aggregation (`min` vs. `mean`) from incomplete-evidence policies (`A0 Proposal Macro-Zero Fallback N=53: incl=0.923, PRI=0.748, cov=0.641`; `A1 Pure Available No-Impute N=49: incl=0.919, PRI=0.733, cov=0.643`; `C0 Strict Complete-Component Required N=7` due to 26 `NULL`s in `CEP` and 25 `NULL`s in `KWC`; `B Compensatory Mean N=49`; `C1 NULL->0.0 Imputed N=53`; `D No Discretionary Splits N=41`).

2. **Demonstration 2 — Independent (Non-UTD24 Journal Submission) QCA-Only Analysis (`Substantive Decision Authority DEC_AUTH`)**:
   - Derives 10 first-order constructs and 4 macro-conditions (`COERC, INST_SHD, BND_INF, EPI_VAL`) across 27 empirical cases (keeping 10 conceptual/field studies in a separate register).
   - Finds `~COERC*INST_SHD + EPI_VAL -> DEC_AUTH` (`incl = 0.912, PRI = 0.893, cov = 0.949`) and `COERC*~EPI_VAL -> ~DEC_AUTH` (`incl = 0.907, PRI = 0.860, cov = 0.636`), and diagnoses three blind spots of stopping at static QCA alone.

3. **Demonstration 3 — Method-Open Best-Fit Hybrid Analysis (`Recommended by Skill 03, Fit Score = 0.94`)**:
   - **Engine 3A (2D Outcome Disaggregation & Multi-Outcome `GEN_AUTH` fsQCA)**: Separates `Regime I (Generative Co-Evolution, n=13)`, `Regime II (Defensive/Curatorial Shielding, n=8)`, `Regime III (Relational Reconstruction, n=2)`, and `Regime IV (Displacement/Drift, n=4)`. Tightening the outcome from `DEC_AUTH` to `GEN_AUTH = min(DEC_AUTH, EPI_GEN)` flips Row `0100` (`LEB-BREAST, LEB-BONE, WAA`) from `OUT=1` (`incl=0.910`) to `OUT=0` (`incl=0.576, PRI=0.000`), while `~BND_INF*~EPI_VAL -> ~GEN_AUTH` holds across all branches (`incl = 0.925–0.974`).
   - **Engine 3B (4-Stage Markov Process-Sequence & Shannon/NMI Information-Gain Analysis)**: Shows that initial deployment `T0` explains only `27.9%` of final regime entropy `H(T3) = 1.714 bits`, `T0+T1` explains `64.6%`, and `T0+T1+T2` explains `100.0%`, resolving all 8 `T0 = coercive_substitutive` cases.
   - **Engine 3C (Kruskal–Wallis `eta^2` & Additive OLS Failure Audit)**: Shows that `GTG_AUD` (`eta^2=0.694`), `SYS_MAL` (`0.625`), and `DEV_BRG` (`0.568`) drive regime separation while `EPI_OPA` (`0.019`) is a scope constant, and demonstrates why additive OLS (`BND_INF beta = +0.012, p = 0.93`) commits crossover sign errors on `PIE-N`, `EIN-T`, `GIA-RM`, and `EIN-D`.
