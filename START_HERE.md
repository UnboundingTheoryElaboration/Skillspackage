# Open Method Architecture Skill (v4.1 Method-Open Edition)

> **Work-in-Progress Notice**: This skill package is an active research prototype developed for the *Organization Science* Special Issue (*AI-Enabled Frontiers in Organizational Science*). Its Synthesis Layer, Epistemic Governance Controller (`control/oma_control.py`), Deterministic fsQCA Engine (`control/oma_engines.py`), 4-Stage Markov Process-Sequence & Entropy Engine, and 2D Four-Regime Kruskal–Wallis Discriminant Engine are implemented and executable today. Automated multi-coder human panel benchmarking and parameterized Agent-Based Modeling (ABM) simulation remain Stage 2 development items. All AI-generated codings and analytical outputs are **provisional** until ratified by a human researcher.

---

## 1. What Makes This Package Different ("Method-Open Architecture")

Traditional literature-synthesis and QCMA workflows assume from the start that **fuzzy-set QCA (fsQCA)** is the only target method. When you only have a QCA hammer, every qualitative literature looks like a static truth table—even when the underlying studies describe temporal sequences, operational breakdowns, or multi-dimensional authority shifts.

The **Open Method Architecture Skill** separates **Synthesis** from **Method Selection**:
1. **Synthesis Layer (`Skills 01 & 02`)**: Reads researcher-approved cases and conceptual studies, codes constructs and **method-neutral relational statements** (who did what to whom, in what sequence, with what outcome), separates empirical observations from conceptual propositions, and preserves unreported evidence as explicit `NULL` (never guessing `0`).
2. **Method-Fit Diagnostic Gate (`Skill 03`)**: Before running any math engine, the system evaluates the empirical structure of your corpus (sample size, outcome skew, proportion of longitudinal/process studies, within-corner contradictions, and dimensionality) and recommends the **best-fit analytical strategy**:
   - **Pathway A (`Skill 05`)**: Deterministic Multi-Outcome & Multi-Branch fsQCA (with Enhanced Standard Analysis CSA exclusion).
   - **Pathway B (`Skill 06`)**: Longitudinal 4-Stage Process-Sequence & Shannon/Mutual-Information Trajectory Analysis (`T0 -> T1 -> T2 -> T3`).
   - **Pathway C (`Skill 06`)**: Multi-Dimensional Regime Clustering, Non-Parametric Kruskal–Wallis Effect Sizes (`eta^2`), and Additive Linear OLS Mis-Specification Auditing.
   - **Hybrid Best-Fit Triangulation**: Combining Pathways A + B + C when a literature contains both cross-case equifinality and longitudinal breakdown sequences.
   - **Synthesis-Only / Specification-Gap Report**: When evidence is purely conceptual or lacks calibrated parameters for simulation.
3. **Theory Elaboration & Reverse Lineage (`Skill 07`)**: Builds a structured `theory_elaboration_register.csv` and traces every proposition back to configurations, temporal trajectories, regime profiles, raw coder ratings, verbatim PDF quotes with page numbers, and human review decisions.

---

## 2. Quick Command Verification

To verify the governance controller and recompute all three empirical demonstrations from scratch:
```bash
python3 control/run_oma_checks.py
python3 control/run_three_demos.py
```
See **`STARTUP_MANUAL.md`** for a plain-language guide on using this package with Claude, ChatGPT, Gemini, Cursor/Windsurf, or local open-weight LLMs.
