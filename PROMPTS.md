# Copy-Paste Prompts for the Open Method Architecture Skill (`PROMPTS.md`)

Use these short prompts with any LLM after loading `AGENT_INSTRUCTIONS.md` and `rules/SCIENTIFIC_RULES.md`.

### Prompt 1 — Start a New Method-Open Analysis (Recommended Default)
> Read `AGENT_INSTRUCTIONS.md` and `rules/SCIENTIFIC_RULES.md`. I have provided my article corpus [and/or case registry]. First reconcile articles, empirical studies, bounded cases, and synthesis-only conceptual/field papers. Propose construct definitions and a method-neutral relational coding schema, then run the Method-Fit Diagnostic (`Skill 03`) to recommend the best analytical approach (QCA, Process-Sequence, Regime Clustering, or Hybrid Triangulation). Stop at the first Review Card for my decision.

### Prompt 2 — Run a Forced QCA Replication of an Existing Model (Demo 1 Mode)
> Read `AGENT_INSTRUCTIONS.md` and `skills/05_qca_pathway.md`. Run a replication and sensitivity audit of the supplied QCA model using `control/oma_engines.py`. Separate theoretical aggregation (`min` vs. `mean`) from missingness handling (`complete_component_required`, `available_component_fallback`, `null_to_zero_imputation`), audit Enhanced Standard Analysis (ESA) remainder exclusions, and test single-condition rivals.

### Prompt 3 — Run an Independent Non-Replicating QCA-Only Analysis (Demo 2 Mode)
> Read `AGENT_INSTRUCTIONS.md`, `skills/01_construct_and_relational_coding.md`, `skills/02_cross_study_translation.md`, and `skills/05_qca_pathway.md`. Using the supplied articles, derive an independent outcome and first-order constructs bottom-up without replicating any prior manuscript codebook. Execute deterministic fsQCA across translation and calibration branches, and explicitly report what a QCA-only design can and cannot explain in this corpus.

### Prompt 4 — Run the Best-Fit Multi-Method Analysis (Demo 3 Mode)
> Read `AGENT_INSTRUCTIONS.md` and `skills/03_method_fit_and_routing.md`. Diagnose the empirical structure of the supplied studies and execute the best-fit multi-method strategy via `control/oma_engines.py`—combining multi-outcome fsQCA, longitudinal process-sequence and information-gain modeling (`T0 -> T1 -> T2 -> T3`), multi-dimensional regime discriminant analysis (`Kruskal-Wallis eta^2`), and an additive OLS mis-specification audit. Synthesize the results into a `theory_elaboration_register.csv` with full reverse evidence lineage.
