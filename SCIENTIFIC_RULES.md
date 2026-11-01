# Consolidated Scientific Rules (`rules/SCIENTIFIC_RULES.md`)

Every module in the **Open Method Architecture Skill** enforces these seven methodological rules:

1. **Articles, Studies, Empirical Cases, and Conceptual Records Are Distinct**:
   - An **article** is a publication; a **study** is an empirical investigation; a **case** is a bounded organizational or actor-group unit with observable evidence on conditions and outcomes.
   - Conceptual papers, pre-deployment sensemaking studies, and cross-organizational interview surveys without bounded case units must be stored in the **Conceptual & Field-Level Synthesis Register**—never forced into fake case rows.
2. **Epistemic Basis Labeling**:
   - Every coded relationship or mechanism must carry one of four explicit labels: `empirically_reported`, `source_author_interpretation`, `conceptually_proposed`, or `synthesizer_conjecture`.
3. **Unambiguous Missingness (`NULL` Is Never `0`)**:
   - Unreported evidence is recorded strictly as `NULL` (`None` / `NaN`). Writing `0` in raw coding or silently converting `NULL` to `0.0` is prohibited.
4. **Orthogonal Aggregation vs. Missingness Rules**:
   - Combining first-order constructs into higher-order macro-conditions requires declaring **both** (a) the theoretical operator (`min`, `mean`, `max`, `single`) and (b) the incomplete-evidence policy (`complete_component_required`, `boolean_absorption_available`, `available_component_fallback`, `null_to_zero_imputation`, `null_to_one_stress`).
5. **Method Selection Is an Outcome of Synthesis, Not a Presupposition**:
   - The orchestrator must evaluate whether the evidence structure exhibits static conjunctural equifinality, longitudinal phase transitions (`T0 -> T1 -> T2 -> T3`), multi-dimensional regime clustering, or conceptual mechanisms before running an analytical engine.
6. **Production-Time Artifact Lineage (`produced_from`)**:
   - Every derived matrix, truth table, sequence model, or theory table records the SHA-256 hashes of the exact upstream artifacts from which it was computed. Editing upstream evidence or coding automatically invalidates downstream artifacts until they are recomputed.
7. **Three Levels of Inference & Adversarial Rivals**:
   - Reports must separate (1) Quantitative/Set-Analytic/Sequence Findings, (2) Within-Case Qualitative Process Interpretations, and (3) Generalizable Theoretical Propositions, and test at least two rival accounts (e.g., single-condition sufficiency, additive linear OLS net effects, and retrospective narrative halo bias).
