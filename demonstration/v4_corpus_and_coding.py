"""
QCMA Skill Package v4 — Independent Multi-Method Corpus, First-Order Coding,
Cross-Study Translation Rules, and Temporal Sequence Register.

Strictly independent of the UTD24 Journal submission:
- Focal phenomenon: Reconfiguration of Domain Experts' Epistemic Authority and
  Evaluative Practice When Confronting AI in Knowledge Work.
- Two distinct outcomes (1-5 scale):
  1. DEC_AUTH: Substantive Decision Authority over Case Judgments
  2. EPI_GEN:  Epistemic Generativity & Practice Renewal (whether AI engagement
               expands/deepens domain knowledge vs. hollowing, freezing, or monopolizing it)
- 10 First-Order Sociotechnical Constructs (1-5 scale; None = NULL / unreported):
  1. ALG_SUB  : Algorithmic Decision Substitution (design assigns decision execution to AI)
  2. MGT_CTRL : Managerial Efficiency & Control Mandate (top-down cost/productivity/surveillance drive)
  3. PROF_JUR : Institutionalized Professional Jurisdiction & Legal Accountability
  4. CLI_EMB  : Client-Facing Relational Embeddedness (continuous expert-client interaction & recognition)
  5. DEV_BRG  : Developer-Expert Co-Design & Boundary Bridging
  6. MED_BRK  : Dedicated Knowledge Brokerage / Translator Role
  7. GTG_AUD  : Ground-Truth Interrogation & In-Situ Auditing Practice
  8. SYS_MAL  : Technical Malleability & Local Reconfigurability (thresholds, features, prompts, feedback)
  9. EPI_OPA  : Experienced Algorithmic Opacity / Black-Box Inscrutability
  10. VIS_FAIL: Visible Operational Breakdown / Edge-Case Failure in Task Execution
"""

FIRST_ORDER = [
    "ALG_SUB", "MGT_CTRL", "PROF_JUR", "CLI_EMB",
    "DEV_BRG", "MED_BRK", "GTG_AUD", "SYS_MAL",
    "EPI_OPA", "VIS_FAIL"
]

OUTCOMES = ["DEC_AUTH", "EPI_GEN"]

MACRO_CONDITIONS = ["COERC", "INST_SHD", "BND_INF", "EPI_VAL"]

CODEBOOK = {
    "DEC_AUTH": {
        "name": "Substantive Decision Authority over Case Judgments",
        "anchor_5": "Experts hold and actively exercise recognized final discretion to shape, bound, or override AI-mediated judgments in core work.",
        "anchor_4": "Experts exercise substantial discretion or curatorial control over judgments, though contested, shared, or relocated to domain brokers.",
        "anchor_3": "More present than absent: experts retain partial or conditional discretion (e.g., supervising exceptions or reshaping client-facing decisions).",
        "anchor_2": "More absent than present: formal discretion is nominally present or claimed relationally, but substantive case decisions are largely steered by AI or management.",
        "anchor_1": "Experts cannot interact with, influence, or overrule AI-executed judgments; authority is fully displaced.",
        "separation_rule": "Never inferred from frequency of tool use, user satisfaction, or positive attitudes."
    },
    "EPI_GEN": {
        "name": "Epistemic Generativity & Practice Renewal",
        "anchor_5": "Sustained mutual learning: confronting AI expands experts' domain knowledge, surfaces tacit criteria, and creates new evaluative routines.",
        "anchor_4": "Substantial reflective refinement of domain criteria or client-facing explanatory repertoire, though bounded to part of the group.",
        "anchor_3": "Moderate adaptation: experts learn to work around or contextualize AI limits without deep transformation of domain knowledge.",
        "anchor_2": "Defensive stasis or narrow piloting: experts either ignore AI to protect existing know-how or narrow their role to routine monitoring.",
        "anchor_1": "Epistemic erosion or deskilling: unreflective dependency on AI accuracy or coercive compliance hollows out independent judgment.",
        "separation_rule": "Analytically distinct from DEC_AUTH: experts can retain full decision authority (DEC_AUTH=5) while exhibiting defensive stasis (EPI_GEN=2) by dismissing AI claims."
    },
    "ALG_SUB": {
        "name": "Algorithmic Decision Substitution",
        "anchor_5": "AI autonomously executes the core selection/decision; workflow precludes routine human override.",
        "anchor_4": "AI executes default decisions autonomously; human override requires exceptional escalation or post-hoc intervention.",
        "anchor_3": "Hybrid execution: AI automates sub-decisions or triage while humans handle complex or flagged cases.",
        "anchor_2": "Advisory recommendation or risk scoring; humans make every case decision.",
        "anchor_1": "Exploratory, generative, or compilative support tool with no autonomous decision execution.",
        "separation_rule": "Coded from implemented workflow architecture, not managerial rhetoric."
    },
    "MGT_CTRL": {
        "name": "Managerial Efficiency & Control Mandate",
        "anchor_5": "Top-down mandate driven by cost reduction, headcount savings, or worker surveillance/kpi enforcement.",
        "anchor_4": "Executive-led deployment prioritizing commercial efficiency/scale alongside secondary quality aims.",
        "anchor_3": "Balanced organizational initiative combining statutory/operational efficiency with professional quality.",
        "anchor_2": "Professionally or locally initiated deployment with light managerial efficiency expectations.",
        "anchor_1": "Bottom-up, experimental, or facilitator-led innovation with no managerial control mandate.",
        "separation_rule": "Separated from outcome displacement; high MGT_CTRL can co-occur with retained authority."
    },
    "PROF_JUR": {
        "name": "Institutionalized Professional Jurisdiction & Accountability",
        "anchor_5": "State-licensed profession with exclusive legal jurisdiction and personal malpractice/audit liability (physicians, partners in law/audit).",
        "anchor_4": "Public statutory mandate or specialized regulatory inspectorate authority.",
        "anchor_3": "Established occupational expertise inside organizations without state licensure (HR specialists, senior engineers, intelligence analysts).",
        "anchor_2": "Semi-professional or commercial advisory role with contested jurisdiction (loan consultants, media planners, seed sorters, non-specialist doctors outside specialty).",
        "anchor_1": "Low-discretion front-line or outsourced service role with weak occupational closure.",
        "separation_rule": "Coded from institutional and legal standing, not whether authority was retained."
    },
    "CLI_EMB": {
        "name": "Client-Facing Relational Embeddedness",
        "anchor_5": "Continuous, high-trust interaction with internal/external clients who depend on the expert's contextual interpretation.",
        "anchor_4": "Regular client or stakeholder interaction where experts translate or justify outputs.",
        "anchor_3": "Periodic or mediated client contact; client recognition is partial or contested.",
        "anchor_2": "One-off, transactional client contact with minimal relational feedback.",
        "anchor_1": "Purely internal processing role with no direct client-explanation relationship.",
        "separation_rule": "Captures relational structure with clients/stakeholders, not outcome success."
    },
    "DEV_BRG": {
        "name": "Developer-Expert Co-Design & Boundary Bridging",
        "anchor_5": "Continuous iterative co-development and mutual learning between AI developers and domain experts across deployment.",
        "anchor_4": "Substantial collaboration during design/calibration or scheduled periodic reconfiguration with developers.",
        "anchor_3": "Episodic consultation or partial involvement of a subset of users.",
        "anchor_2": "Minimal contact (one-way training or initial handoff only).",
        "anchor_1": "Zero contact between domain experts and developers (off-the-shelf vendor black box or isolated lab).",
        "separation_rule": "Defined by interaction structure across the developer-expert boundary, not by agreement."
    },
    "MED_BRK": {
        "name": "Dedicated Knowledge Brokerage / Translator Role",
        "anchor_5": "Formalized boundary-spanning broker or facilitator role continuously translating between algorithmic logic and domain practice.",
        "anchor_4": "Active internal champions, hybrid analyst-builders, or facilitators mediating interpretation.",
        "anchor_3": "Informal or emergent peer brokerage by tech-savvy domain members.",
        "anchor_2": "Weak or failed brokerage attempts (e.g., uncoordinated junior coaching).",
        "anchor_1": "No brokerage or translator role present.",
        "separation_rule": "Structural presence of a mediating actor/routine, independent of whether brokerage empowers or monopolizes."
    },
    "GTG_AUD": {
        "name": "Ground-Truth Interrogation & In-Situ Auditing",
        "anchor_5": "Systematic, institutionalized practices comparing AI outputs against independent expert know-how/ground truth and investigating divergences.",
        "anchor_4": "Regular mindful verification, triangulation, or 100%-test benchmarking in operational work.",
        "anchor_3": "Selective or pragmatic checking of outputs before action.",
        "anchor_2": "Superficial glance or initial curiosity followed by routine acceptance or dismissal.",
        "anchor_1": "No interrogation or auditing performed (either prohibited by workflow or neglected).",
        "separation_rule": "Measures the investigative activity of testing AI claims against domain knowledge, not final override power."
    },
    "SYS_MAL": {
        "name": "Technical Malleability & Local Reconfigurability",
        "anchor_5": "Experts or local teams can directly adjust thresholds, weights, prompts, rules, or features in situ.",
        "anchor_4": "System is regularly reconfigured or retrained in response to domain feedback.",
        "anchor_3": "Moderate configurability (report formatting, workflow wrappers, or coexisting rule layers).",
        "anchor_2": "Rigid core model with only minor workaround margins.",
        "anchor_1": "Completely locked, unmodifiable algorithmic system.",
        "separation_rule": "Technical and procedural modifiability of the tool/workflow."
    },
    "EPI_OPA": {
        "name": "Experienced Algorithmic Opacity",
        "anchor_5": "Deep black-box inscrutability: experts cannot see or reconstruct why specific predictions or classifications are generated.",
        "anchor_4": "Substantial opacity in model logic despite surface feature weights or scores.",
        "anchor_3": "Moderate opacity; general logic understood but case-level anomalies remain puzzling.",
        "anchor_2": "Mostly interpretable rule-based or transparent statistical logic.",
        "anchor_1": "Fully transparent deterministic rules.",
        "separation_rule": "Experienced epistemic inscrutability reported in the case."
    },
    "VIS_FAIL": {
        "name": "Visible Operational Breakdown / Edge-Case Failure",
        "anchor_5": "Severe, visible operational breakdowns or false predictions that disrupt work and expose algorithmic incompetence.",
        "anchor_4": "Frequent noticeable divergences from expert ground truth or domain realities in core cases.",
        "anchor_3": "Periodic edge-case errors or hallucinations requiring correction.",
        "anchor_2": "Minor occasional inaccuracies within acceptable tolerances.",
        "anchor_1": "High technical accuracy / no visible operational failures reported.",
        "separation_rule": "Observed task-level errors or breakdowns, not general skepticism."
    }
}

# 27 Empirical Cases across 20 Case-Contributing Articles
# Ratings: 1-5 ordinal scale; None = NULL (unreported in text).
# Temporal stages:
#   T0_entry: 'coercive_substitutive' | 'managed_hybrid' | 'advisory_professional' | 'participatory_codesign'
#   T1_trigger: 'operational_breakdown' | 'epistemic_divergence' | 'jurisdictional_threat' | 'smooth_complementarity'
#   T2_mobilization: 'co_design_and_audit' | 'jurisdictional_shielding' | 'curatorial_brokerage' | 'client_relational_enhancement' | 'compliance_or_drift'
#   T3_regime: 'R1_Generative_CoEvolution' | 'R2_Defensive_Curatorial_Shielding' | 'R3_Relational_Reconstruction' | 'R4_Displacement_or_Drift'

CASES_V4 = {
    "ASA": {
        "article_id": "A01", "study_id": "S01", "cite": "Asatiani et al. (2021)",
        "setting": "Danish Business Authority (ML Lab & case workers)",
        "actors": "Public registry case workers", "ai_system": "In-house ML fraud/risk flags",
        "is_discretionary_split": False, "resolution": "bounded",
        "ratings": {
            "DEC_AUTH": 5, "EPI_GEN": 5,
            "ALG_SUB": 2, "MGT_CTRL": 2, "PROF_JUR": 4, "CLI_EMB": 3,
            "DEV_BRG": 5, "MED_BRK": 4, "GTG_AUD": 4, "SYS_MAL": 5,
            "EPI_OPA": 5, "VIS_FAIL": 3
        },
        "temporal": {
            "T0": "participatory_codesign", "T1": "epistemic_divergence",
            "T2": "co_design_and_audit", "T3": "R1_Generative_CoEvolution"
        },
        "quotes": {
            "DEC_AUTH": "p.13: 'expert case workers are allowed to set thresholds for models'; p.17: 'Directly involved in the development of the AI'",
            "DEV_BRG": "p.13: 'ML Lab communicates with case workers regularly regarding the performance of the models'",
            "SYS_MAL": "p.13: 'case workers are allowed to set thresholds for models... enveloping process'",
            "EPI_OPA": "p.11: 'inscrutable models sometimes outperform explainable ones'"
        }
    },
    "EIN-D": {
        "article_id": "A04", "study_id": "S04", "cite": "Einola & Khoreva (2023)",
        "setting": "Wizz media agency — Digital media planning unit",
        "actors": "Digital media planners and specialists", "ai_system": "ML campaign optimization tools",
        "is_discretionary_split": True, "resolution": "bounded",
        "ratings": {
            "DEC_AUTH": 3, "EPI_GEN": 2,
            "ALG_SUB": 2, "MGT_CTRL": 4, "PROF_JUR": 2, "CLI_EMB": 4,
            "DEV_BRG": 2, "MED_BRK": 2, "GTG_AUD": 4, "SYS_MAL": 3,
            "EPI_OPA": 2, "VIS_FAIL": 2
        },
        "temporal": {
            "T0": "managed_hybrid", "T1": "smooth_complementarity",
            "T2": "compliance_or_drift", "T3": "R2_Defensive_Curatorial_Shielding"
        },
        "quotes": {
            "DEC_AUTH": "p.9: '[the solution] does it for me. I just pilot and keep an eye on what is happening'",
            "GTG_AUD": "p.12: 'I need to double check everything and present the results to the customer'",
            "MGT_CTRL": "p.12: 'top-down technology projects... executives and managers drove AI'"
        }
    },
    "EIN-T": {
        "article_id": "A04", "study_id": "S04", "cite": "Einola & Khoreva (2023)",
        "setting": "Wizz media agency — Traditional TV/print booking unit",
        "actors": "Traditional media planners/operators", "ai_system": "Automated slot-booking robot",
        "is_discretionary_split": True, "resolution": "bounded",
        "ratings": {
            "DEC_AUTH": 4, "EPI_GEN": 2,
            "ALG_SUB": 4, "MGT_CTRL": 5, "PROF_JUR": 2, "CLI_EMB": 3,
            "DEV_BRG": 1, "MED_BRK": 1, "GTG_AUD": 3, "SYS_MAL": 2,
            "EPI_OPA": 2, "VIS_FAIL": 5
        },
        "temporal": {
            "T0": "coercive_substitutive", "T1": "operational_breakdown",
            "T2": "jurisdictional_shielding", "T3": "R2_Defensive_Curatorial_Shielding"
        },
        "quotes": {
            "DEC_AUTH": "p.12: 'employees' tacit knowledge... became essential to solving deviations, making the automation solution look like a mixed application'",
            "DEV_BRG": "p.12: 'specialists... have no idea what our goals are (Operator 1)'",
            "VIS_FAIL": "p.9: 'quite stupid... bangs his head on the wall... requires more supervision than manual work'"
        }
    },
    "FAU-A": {
        "article_id": "A06", "study_id": "S06", "cite": "Faulconbridge et al. (2024)",
        "setting": "UK accounting professional service firms",
        "actors": "Accounting partners and auditors", "ai_system": "Supervised ML audit/tax extraction",
        "is_discretionary_split": True, "resolution": "field",
        "ratings": {
            "DEC_AUTH": 5, "EPI_GEN": 4,
            "ALG_SUB": 1, "MGT_CTRL": 2, "PROF_JUR": 5, "CLI_EMB": 5,
            "DEV_BRG": 4, "MED_BRK": 4, "GTG_AUD": 4, "SYS_MAL": 4,
            "EPI_OPA": 4, "VIS_FAIL": 2
        },
        "temporal": {
            "T0": "advisory_professional", "T1": "epistemic_divergence",
            "T2": "co_design_and_audit", "T3": "R1_Generative_CoEvolution"
        },
        "quotes": {
            "DEC_AUTH": "p.13: 'the final decision-making is always made at partner level'; p.16: 'you are totally in charge'",
            "GTG_AUD": "p.10: 'supervised training with professionals labelling and reviewing algorithm determinations'"
        }
    },
    "FAU-L": {
        "article_id": "A06", "study_id": "S06", "cite": "Faulconbridge et al. (2024)",
        "setting": "UK law professional service firms",
        "actors": "Law firm partners and associates", "ai_system": "ML document review (e.g., Relativity)",
        "is_discretionary_split": True, "resolution": "field",
        "ratings": {
            "DEC_AUTH": 5, "EPI_GEN": 4,
            "ALG_SUB": 1, "MGT_CTRL": 2, "PROF_JUR": 5, "CLI_EMB": 5,
            "DEV_BRG": 4, "MED_BRK": 4, "GTG_AUD": 4, "SYS_MAL": 4,
            "EPI_OPA": 4, "VIS_FAIL": 2
        },
        "temporal": {
            "T0": "advisory_professional", "T1": "epistemic_divergence",
            "T2": "co_design_and_audit", "T3": "R1_Generative_CoEvolution"
        },
        "quotes": {
            "DEC_AUTH": "p.16: 'partnership governance places decision authority in partners' hands'",
            "PROF_JUR": "p.13: 'what if it makes a mistake? ... professional accountability to clients'"
        }
    },
    "GIA-CRM": {
        "article_id": "A07", "study_id": "S07", "cite": "Giannitsas et al. (2026)",
        "setting": "AlphaAir — Customer Relationship Management department",
        "actors": "CRM analysts serving marketing", "ai_system": "In-house ML customer clustering",
        "is_discretionary_split": False, "resolution": "bounded",
        "ratings": {
            "DEC_AUTH": 4, "EPI_GEN": 4,
            "ALG_SUB": 2, "MGT_CTRL": 5, "PROF_JUR": 2, "CLI_EMB": 4,
            "DEV_BRG": 4, "MED_BRK": 4, "GTG_AUD": 5, "SYS_MAL": 4,
            "EPI_OPA": 4, "VIS_FAIL": 4
        },
        "temporal": {
            "T0": "managed_hybrid", "T1": "epistemic_divergence",
            "T2": "co_design_and_audit", "T3": "R1_Generative_CoEvolution"
        },
        "quotes": {
            "DEC_AUTH": "p.12: 'analysts reintroduced human oversight to contextualise insights while retaining automated clustering'",
            "GTG_AUD": "p.12: 'mindful evaluation, regularly scrutinising outputs' marketing fit; collaborative reviews'"
        }
    },
    "GIA-RM": {
        "article_id": "A07", "study_id": "S07", "cite": "Giannitsas et al. (2026)",
        "setting": "AlphaAir — Revenue Management department",
        "actors": "Revenue management pricing analysts", "ai_system": "Third-party ML pricing platform",
        "is_discretionary_split": False, "resolution": "bounded",
        "ratings": {
            "DEC_AUTH": 3, "EPI_GEN": 3,
            "ALG_SUB": 4, "MGT_CTRL": 5, "PROF_JUR": 2, "CLI_EMB": 2,
            "DEV_BRG": 2, "MED_BRK": 2, "GTG_AUD": 4, "SYS_MAL": 3,
            "EPI_OPA": 4, "VIS_FAIL": 3
        },
        "temporal": {
            "T0": "coercive_substitutive", "T1": "epistemic_divergence",
            "T2": "co_design_and_audit", "T3": "R2_Defensive_Curatorial_Shielding"
        },
        "quotes": {
            "DEC_AUTH": "p.9: 'became more cautious about fully delegating pricing authority; decision to override the platform on social-responsibility grounds'",
            "GTG_AUD": "p.12: 'AI-human comparisons and escalation pathways embedded'"
        }
    },
    "GIA-DSL": {
        "article_id": "A07", "study_id": "S07", "cite": "Giannitsas et al. (2026)",
        "setting": "AlphaAir — Data Science Lab & Cargo operations",
        "actors": "Cargo managers and DSL data scientists", "ai_system": "In-house cargo-space forecasting ML",
        "is_discretionary_split": False, "resolution": "bounded",
        "ratings": {
            "DEC_AUTH": 4, "EPI_GEN": 4,
            "ALG_SUB": 4, "MGT_CTRL": 5, "PROF_JUR": 2, "CLI_EMB": 3,
            "DEV_BRG": 4, "MED_BRK": 4, "GTG_AUD": 5, "SYS_MAL": 4,
            "EPI_OPA": 4, "VIS_FAIL": 5
        },
        "temporal": {
            "T0": "coercive_substitutive", "T1": "operational_breakdown",
            "T2": "co_design_and_audit", "T3": "R1_Generative_CoEvolution"
        },
        "quotes": {
            "DEC_AUTH": "p.11: 'There you want the human to intervene and feed this back to the algorithm'",
            "VIS_FAIL": "p.11: 'inaccurate forecasts caused operational disruptions (450 kg predicted; 350 kg could not be loaded)'",
            "GTG_AUD": "p.13: 'treated forecasts as hypotheses... compared predictions against actual cargo outcomes'"
        }
    },
    "GRA": {
        "article_id": "A11", "study_id": "S11", "cite": "Grange et al. (2025)",
        "setting": "Three human-centered design sprint projects (pooled)",
        "actors": "Innovation teams and sprint facilitators", "ai_system": "Generative AI (LLM) ideation/framing",
        "is_discretionary_split": False, "resolution": "pooled",
        "ratings": {
            "DEC_AUTH": 5, "EPI_GEN": 5,
            "ALG_SUB": 1, "MGT_CTRL": 1, "PROF_JUR": 2, "CLI_EMB": 4,
            "DEV_BRG": 4, "MED_BRK": 5, "GTG_AUD": 4, "SYS_MAL": 5,
            "EPI_OPA": 4, "VIS_FAIL": 4
        },
        "temporal": {
            "T0": "participatory_codesign", "T1": "operational_breakdown",
            "T2": "co_design_and_audit", "T3": "R1_Generative_CoEvolution"
        },
        "quotes": {
            "DEC_AUTH": "p.13: 'team members could modify or refine AI-generated material; empowered to feel more in control'",
            "MED_BRK": "p.13: 'facilitator's reflexive approach mediating GenAI use'",
            "VIS_FAIL": "p.13: 'garbage in, garbage out became evident in the first project'"
        }
    },
    "GRO": {
        "article_id": "A12", "study_id": "S12", "cite": "Grønsund & Aanestad (2020)",
        "setting": "International maritime trade analytics firm",
        "actors": "Shipbroker trade analysts and data scientists", "ai_system": "ML vessel/trade prediction algorithm",
        "is_discretionary_split": False, "resolution": "bounded",
        "ratings": {
            "DEC_AUTH": 5, "EPI_GEN": 5,
            "ALG_SUB": 2, "MGT_CTRL": 4, "PROF_JUR": 2, "CLI_EMB": 3,
            "DEV_BRG": 5, "MED_BRK": 4, "GTG_AUD": 5, "SYS_MAL": 5,
            "EPI_OPA": 4, "VIS_FAIL": 5
        },
        "temporal": {
            "T0": "managed_hybrid", "T1": "operational_breakdown",
            "T2": "co_design_and_audit", "T3": "R1_Generative_CoEvolution"
        },
        "quotes": {
            "DEC_AUTH": "p.1: 'new roles and redistribution of expertise to augment the algorithm (human-in-the-loop)'",
            "GTG_AUD": "p.1: 'auditing work = generation of ground truth and assessment of algorithmic output against it'",
            "DEV_BRG": "p.8: 'configuration of auditing and altering with data scientist'"
        }
    },
    "LEB-LUNG": {
        "article_id": "A16,A15", "study_id": "S16", "cite": "Lebovitz et al. (2022; 2021)",
        "setting": "US academic hospital — Lung cancer screening radiology",
        "actors": "Thoracic diagnostic radiologists", "ai_system": "Vendor ML lung nodule diagnostic tool",
        "is_discretionary_split": False, "resolution": "bounded",
        "ratings": {
            "DEC_AUTH": 5, "EPI_GEN": 5,
            "ALG_SUB": 1, "MGT_CTRL": 2, "PROF_JUR": 5, "CLI_EMB": 4,
            "DEV_BRG": 1, "MED_BRK": 1, "GTG_AUD": 5, "SYS_MAL": 2,
            "EPI_OPA": 5, "VIS_FAIL": 4
        },
        "temporal": {
            "T0": "advisory_professional", "T1": "epistemic_divergence",
            "T2": "co_design_and_audit", "T3": "R1_Generative_CoEvolution"
        },
        "quotes": {
            "DEC_AUTH": "p.2: 'professionals consistently incorporated AI results into their final judgments (engaged augmentation)'",
            "GTG_AUD": "p.2: 'invested in AI interrogation practices relating own knowledge claims to AI claims'",
            "EPI_OPA": "p.2: 'opacity increased uncertainty as AI results diverged without reasoning'"
        }
    },
    "LEB-BREAST": {
        "article_id": "A16,A15", "study_id": "S16", "cite": "Lebovitz et al. (2022; 2021)",
        "setting": "US academic hospital — Breast imaging radiology",
        "actors": "Breast imaging diagnostic radiologists", "ai_system": "Vendor ML mammography tool",
        "is_discretionary_split": False, "resolution": "bounded",
        "ratings": {
            "DEC_AUTH": 5, "EPI_GEN": 2,
            "ALG_SUB": 1, "MGT_CTRL": 2, "PROF_JUR": 5, "CLI_EMB": 4,
            "DEV_BRG": 1, "MED_BRK": 1, "GTG_AUD": 2, "SYS_MAL": 1,
            "EPI_OPA": 5, "VIS_FAIL": 4
        },
        "temporal": {
            "T0": "advisory_professional", "T1": "epistemic_divergence",
            "T2": "jurisdictional_shielding", "T3": "R2_Defensive_Curatorial_Shielding"
        },
        "quotes": {
            "DEC_AUTH": "p.15: 'unengaged augmentation: professionals largely ignored AI claims and kept their own judgment'",
            "GTG_AUD": "p.15: 'ceasing interrogation practices... dismissing the AI tool's knowledge claims'"
        }
    },
    "LEB-BONE": {
        "article_id": "A16", "study_id": "S16", "cite": "Lebovitz et al. (2022)",
        "setting": "US academic hospital — Pediatric bone age radiology",
        "actors": "Pediatric diagnostic radiologists", "ai_system": "Vendor ML bone-age assessment tool",
        "is_discretionary_split": False, "resolution": "bounded",
        "ratings": {
            "DEC_AUTH": 5, "EPI_GEN": 2,
            "ALG_SUB": 1, "MGT_CTRL": 2, "PROF_JUR": 5, "CLI_EMB": 4,
            "DEV_BRG": 1, "MED_BRK": 1, "GTG_AUD": 2, "SYS_MAL": 1,
            "EPI_OPA": 5, "VIS_FAIL": 4
        },
        "temporal": {
            "T0": "advisory_professional", "T1": "epistemic_divergence",
            "T2": "jurisdictional_shielding", "T3": "R2_Defensive_Curatorial_Shielding"
        },
        "quotes": {
            "DEC_AUTH": "p.15: 'unengaged augmentation path; radiologists kept final determination'",
            "GTG_AUD": "p.15: 'accepting or ignoring AI claims rather than interrogating them'"
        }
    },
    "LEE": {
        "article_id": "A17", "study_id": "S17", "cite": "Lee & Lee (2024)",
        "setting": "Korean Social Security Information Service & local governments",
        "actors": "Local government social-welfare officials", "ai_system": "ML welfare blind-spot identification",
        "is_discretionary_split": False, "resolution": "bounded_short",
        "ratings": {
            "DEC_AUTH": 4, "EPI_GEN": 3,
            "ALG_SUB": 2, "MGT_CTRL": 2, "PROF_JUR": 3, "CLI_EMB": 4,
            "DEV_BRG": 2, "MED_BRK": 3, "GTG_AUD": 4, "SYS_MAL": 3,
            "EPI_OPA": 4, "VIS_FAIL": 3
        },
        "temporal": {
            "T0": "managed_hybrid", "T1": "epistemic_divergence",
            "T2": "jurisdictional_shielding", "T3": "R2_Defensive_Curatorial_Shielding"
        },
        "quotes": {
            "DEC_AUTH": "p.1: 'human-driven heuristic method championed by local governments coexists with ML'",
            "GTG_AUD": "p.1: 'three methods compared on strengths and weaknesses'"
        }
    },
    "LI": {
        "article_id": "A18", "study_id": "S18", "cite": "Li et al. (2025)",
        "setting": "Chinese hospitals (physicians using AI-aided diagnosis)",
        "actors": "Hospital physicians", "ai_system": "Clinical AI-aided diagnostic systems",
        "is_discretionary_split": False, "resolution": "field",
        "ratings": {
            "DEC_AUTH": 5, "EPI_GEN": 2,
            "ALG_SUB": 1, "MGT_CTRL": None, "PROF_JUR": 5, "CLI_EMB": 4,
            "DEV_BRG": 1, "MED_BRK": 1, "GTG_AUD": 4, "SYS_MAL": 1,
            "EPI_OPA": 4, "VIS_FAIL": 3
        },
        "temporal": {
            "T0": "advisory_professional", "T1": "jurisdictional_threat",
            "T2": "jurisdictional_shielding", "T3": "R2_Defensive_Curatorial_Shielding"
        },
        "quotes": {
            "DEC_AUTH": "p.1: 'physicians' noncompliance use—not following AI recommendations; professional capital as boundary condition'",
            "PROF_JUR": "p.3: 'professional autonomy and clinical accountability over diagnostic decisions'"
        }
    },
    "MAY-BIO": {
        "article_id": "A19", "study_id": "S19b", "cite": "Mayer et al. (2025)",
        "setting": "Biotechnology firm — Seed sorting operations",
        "actors": "Seed-sorting experts serving supply-chain clients", "ai_system": "Predictive AI seed-selection system",
        "is_discretionary_split": False, "resolution": "bounded",
        "ratings": {
            "DEC_AUTH": 2, "EPI_GEN": 4,
            "ALG_SUB": 5, "MGT_CTRL": 5, "PROF_JUR": 2, "CLI_EMB": 5,
            "DEV_BRG": 2, "MED_BRK": 2, "GTG_AUD": 2, "SYS_MAL": 2,
            "EPI_OPA": 5, "VIS_FAIL": 3
        },
        "temporal": {
            "T0": "coercive_substitutive", "T1": "jurisdictional_threat",
            "T2": "client_relational_enhancement", "T3": "R3_Relational_Reconstruction"
        },
        "quotes": {
            "DEC_AUTH": "p.9: 'facing decisions generated by AI that could not easily be overruled'; p.16: 'perceived losing decision-making power'",
            "CLI_EMB": "p.10: 'continuous and deep exchanges with clients... expertise recognized as unique by clients'",
            "EPI_GEN": "p.24: 'experts who learned clients' needs enhanced AI outputs with expertise, reinforcing authority'"
        }
    },
    "MAY-REC": {
        "article_id": "A19", "study_id": "S19c", "cite": "Mayer et al. (2025)",
        "setting": "Large organization — Corporate recruitment function",
        "actors": "Recruiters serving hiring managers", "ai_system": "AI personality-based candidate selection",
        "is_discretionary_split": False, "resolution": "bounded",
        "ratings": {
            "DEC_AUTH": 2, "EPI_GEN": 4,
            "ALG_SUB": 5, "MGT_CTRL": 5, "PROF_JUR": 2, "CLI_EMB": 5,
            "DEV_BRG": 4, "MED_BRK": 3, "GTG_AUD": 3, "SYS_MAL": 4,
            "EPI_OPA": 5, "VIS_FAIL": 3
        },
        "temporal": {
            "T0": "coercive_substitutive", "T1": "jurisdictional_threat",
            "T2": "client_relational_enhancement", "T3": "R3_Relational_Reconstruction"
        },
        "quotes": {
            "DEC_AUTH": "p.10: 'Candidate selections are made by AI instead of recruiters'",
            "DEV_BRG": "p.24: 'recruiters engaged with AI developers in a 4-month exercise calibrating AI outputs'",
            "CLI_EMB": "p.10: 'Recruiters have continuous and deep exchanges with clients frequently'"
        }
    },
    "STR-BANK": {
        "article_id": "A24,A19", "study_id": "S19a", "cite": "Strich et al. (2021); Mayer et al. (2025)",
        "setting": "Main Finance bank — Retail loan consulting (CleverLoan)",
        "actors": "Loan consultants", "ai_system": "Substitutive loan-decision AI (CleverLoan)",
        "is_discretionary_split": False, "resolution": "bounded",
        "ratings": {
            "DEC_AUTH": 1, "EPI_GEN": 1,
            "ALG_SUB": 5, "MGT_CTRL": 5, "PROF_JUR": 2, "CLI_EMB": 2,
            "DEV_BRG": 1, "MED_BRK": 1, "GTG_AUD": 1, "SYS_MAL": 1,
            "EPI_OPA": 5, "VIS_FAIL": 3
        },
        "temporal": {
            "T0": "coercive_substitutive", "T1": "jurisdictional_threat",
            "T2": "compliance_or_drift", "T3": "R4_Displacement_or_Drift"
        },
        "quotes": {
            "DEC_AUTH": "Strich p.17: 'can neither influence the decision-making process nor change the final outcome'; Mayer p.15: 'masking backfired'",
            "ALG_SUB": "Strich p.2: 'eliminates employees' ability to interact with or overrule the system'",
            "CLI_EMB": "Mayer p.10: 'Loan consultants typically have one-off exchanges with clients'"
        }
    },
    "MIR": {
        "article_id": "A20", "study_id": "S20", "cite": "Mirkovski et al. (2025)",
        "setting": "Australian small e-retailer (Simply Headsets)",
        "actors": "Owner-managers and product innovation team", "ai_system": "GPT-based HAIAPI innovation framework",
        "is_discretionary_split": False, "resolution": "bounded_design",
        "ratings": {
            "DEC_AUTH": 5, "EPI_GEN": 5,
            "ALG_SUB": 1, "MGT_CTRL": 1, "PROF_JUR": 2, "CLI_EMB": 4,
            "DEV_BRG": 5, "MED_BRK": 5, "GTG_AUD": 4, "SYS_MAL": 5,
            "EPI_OPA": 2, "VIS_FAIL": 2
        },
        "temporal": {
            "T0": "participatory_codesign", "T1": "smooth_complementarity",
            "T2": "co_design_and_audit", "T3": "R1_Generative_CoEvolution"
        },
        "quotes": {
            "DEC_AUTH": "p.1: 'human experts retain problem selection and solution evaluation; AI augments articulation'",
            "MED_BRK": "p.8: 'researchers acted as facilitators translating prompts and outputs'"
        }
    },
    "MON": {
        "article_id": "A21", "study_id": "S21", "cite": "Monod et al. (2024)",
        "setting": "Alpha (Chinese service firm) — Customer-service sales unit",
        "actors": "Outsourced customer-service salespeople", "ai_system": "NLP AI Sales Assistant (AIA)",
        "is_discretionary_split": False, "resolution": "bounded",
        "ratings": {
            "DEC_AUTH": 1, "EPI_GEN": 1,
            "ALG_SUB": 4, "MGT_CTRL": 5, "PROF_JUR": 1, "CLI_EMB": 2,
            "DEV_BRG": 1, "MED_BRK": 1, "GTG_AUD": 1, "SYS_MAL": 1,
            "EPI_OPA": 3, "VIS_FAIL": 3
        },
        "temporal": {
            "T0": "coercive_substitutive", "T1": "jurisdictional_threat",
            "T2": "compliance_or_drift", "T3": "R4_Displacement_or_Drift"
        },
        "quotes": {
            "DEC_AUTH": "p.1: 'devolution of AI tools' intended positive implementation... into a tool to control and manage salespeople'",
            "MGT_CTRL": "p.4: 'launched to improve customer satisfaction and reduce costs; surveillance and flagging of performers'"
        }
    },
    "PIE-S": {
        "article_id": "A23", "study_id": "S23", "cite": "Pieper & Gleasure (2025)",
        "setting": "German medical care center — Radiology specialists",
        "actors": "Diagnostic radiology specialists", "ai_system": "AI-Rad Companion (Siemens Healthineers)",
        "is_discretionary_split": True, "resolution": "bounded",
        "ratings": {
            "DEC_AUTH": 5, "EPI_GEN": 5,
            "ALG_SUB": 1, "MGT_CTRL": 2, "PROF_JUR": 5, "CLI_EMB": 4,
            "DEV_BRG": 4, "MED_BRK": 3, "GTG_AUD": 5, "SYS_MAL": 4,
            "EPI_OPA": 4, "VIS_FAIL": 3
        },
        "temporal": {
            "T0": "advisory_professional", "T1": "epistemic_divergence",
            "T2": "co_design_and_audit", "T3": "R1_Generative_CoEvolution"
        },
        "quotes": {
            "DEC_AUTH": "p.16: 'specialists remain the validating authority... critique and triangulate recommendations'",
            "DEV_BRG": "p.6: 'developed in co-operation with the care centre; reconfigured twice a year with user feedback'"
        }
    },
    "PIE-N": {
        "article_id": "A23", "study_id": "S23", "cite": "Pieper & Gleasure (2025)",
        "setting": "German medical care center — Non-specialist referring physicians",
        "actors": "Non-specialist physicians interpreting scans", "ai_system": "AI-Rad Companion (Siemens Healthineers)",
        "is_discretionary_split": True, "resolution": "bounded",
        "ratings": {
            "DEC_AUTH": 2, "EPI_GEN": 1,
            "ALG_SUB": 1, "MGT_CTRL": 2, "PROF_JUR": 2, "CLI_EMB": 3,
            "DEV_BRG": 2, "MED_BRK": 1, "GTG_AUD": 1, "SYS_MAL": 2,
            "EPI_OPA": 4, "VIS_FAIL": 1
        },
        "temporal": {
            "T0": "advisory_professional", "T1": "smooth_complementarity",
            "T2": "compliance_or_drift", "T3": "R4_Displacement_or_Drift"
        },
        "quotes": {
            "DEC_AUTH": "p.16: 'growing dependency; less critical reflection; dependency on algorithmic accuracy substituted for human expertise'",
            "GTG_AUD": "p.16: 'non-specialists did not fear losing skills for independent evaluation because they felt they should not need them'"
        }
    },
    "VKR": {
        "article_id": "A28", "study_id": "S28", "cite": "van Krimpen & van der Voort (2025)",
        "setting": "Dutch national regulatory inspectorate",
        "actors": "Regulatory inspectors and ML developers", "ai_system": "ML risk-scoring for fraudulent online businesses",
        "is_discretionary_split": False, "resolution": "bounded",
        "ratings": {
            "DEC_AUTH": 4, "EPI_GEN": 4,
            "ALG_SUB": 1, "MGT_CTRL": 2, "PROF_JUR": 4, "CLI_EMB": 3,
            "DEV_BRG": 5, "MED_BRK": 4, "GTG_AUD": 4, "SYS_MAL": 4,
            "EPI_OPA": 4, "VIS_FAIL": 3
        },
        "temporal": {
            "T0": "participatory_codesign", "T1": "epistemic_divergence",
            "T2": "co_design_and_audit", "T3": "R1_Generative_CoEvolution"
        },
        "quotes": {
            "DEC_AUTH": "p.4: 'scores enable inspectors to decide follow-up'; p.11: 'engaged in joint learning'",
            "DEV_BRG": "p.11: 'co-creation brought developers and end-users closer; developers translating ML concepts'"
        }
    },
    "WAA": {
        "article_id": "A30", "study_id": "S30", "cite": "Waardenburg et al. (2022)",
        "setting": "Dutch national police — Predictive policing intelligence unit",
        "actors": "Intelligence officers (brokers) and police managers", "ai_system": "Crime Anticipation System (CAS) ML",
        "is_discretionary_split": False, "resolution": "bounded",
        "ratings": {
            "DEC_AUTH": 4, "EPI_GEN": 2,
            "ALG_SUB": 1, "MGT_CTRL": 4, "PROF_JUR": 3, "CLI_EMB": 4,
            "DEV_BRG": 3, "MED_BRK": 5, "GTG_AUD": 2, "SYS_MAL": 3,
            "EPI_OPA": 5, "VIS_FAIL": 4
        },
        "temporal": {
            "T0": "managed_hybrid", "T1": "epistemic_divergence",
            "T2": "curatorial_brokerage", "T3": "R2_Defensive_Curatorial_Shielding"
        },
        "quotes": {
            "DEC_AUTH": "p.2: 'brokers substituted the algorithmic predictions with their own judgments as curators (kings in the land of the blind)'",
            "MED_BRK": "p.2: 'intelligence officers tasked with brokering between ML community and user community'",
            "EPI_OPA": "p.2: 'impassable knowledge boundary yielded by black-boxed machine learning'"
        }
    },
    "VGI": {
        "article_id": "A27", "study_id": "S27", "cite": "van Giffen et al. (2025)",
        "setting": "Siemens Electronics Works Amberg — Lean quality management",
        "actors": "Quality engineers and factory operators", "ai_system": "Predictive X-ray solder quality ML",
        "is_discretionary_split": False, "resolution": "bounded",
        "ratings": {
            "DEC_AUTH": 5, "EPI_GEN": 5,
            "ALG_SUB": 2, "MGT_CTRL": 4, "PROF_JUR": 3, "CLI_EMB": 3,
            "DEV_BRG": 4, "MED_BRK": 4, "GTG_AUD": 5, "SYS_MAL": 4,
            "EPI_OPA": 5, "VIS_FAIL": 3
        },
        "temporal": {
            "T0": "managed_hybrid", "T1": "epistemic_divergence",
            "T2": "co_design_and_audit", "T3": "R1_Generative_CoEvolution"
        },
        "quotes": {
            "DEC_AUTH": "p.14: 'baseline expectation that workers oversee final quality; human-led inspections remain the fallback'",
            "GTG_AUD": "p.14: 'use cases where products are 100% tested allow AI predictions to be checked'"
        }
    },
    "VDB-HR": {
        "article_id": "A25", "study_id": "S25", "cite": "van den Broek et al. (2021)",
        "setting": "Multinational firm — HR recruitment ML development",
        "actors": "HR recruitment experts and ML developers", "ai_system": "ML candidate-assessment algorithm",
        "is_discretionary_split": True, "resolution": "bounded",
        "ratings": {
            "DEC_AUTH": 5, "EPI_GEN": 5,
            "ALG_SUB": 2, "MGT_CTRL": 4, "PROF_JUR": 3, "CLI_EMB": 4,
            "DEV_BRG": 5, "MED_BRK": 4, "GTG_AUD": 5, "SYS_MAL": 4,
            "EPI_OPA": 4, "VIS_FAIL": 4
        },
        "temporal": {
            "T0": "managed_hybrid", "T1": "operational_breakdown",
            "T2": "co_design_and_audit", "T3": "R1_Generative_CoEvolution"
        },
        "quotes": {
            "DEC_AUTH": "p.1: 'despite goal of getting experts out of the loop, hybrid practice relying on ML and domain expertise emerged'",
            "DEV_BRG": "p.10: 'mutual learning between developers and experts... iterations between excluding and including domain expertise'"
        }
    },
    "VDB-LM": {
        "article_id": "A26", "study_id": "S25", "cite": "van den Broek et al. (2025)",
        "setting": "Multinational firm — Line (hiring) managers in candidate selection",
        "actors": "Line / hiring managers", "ai_system": "Same ML candidate-assessment tool enforced by HR",
        "is_discretionary_split": True, "resolution": "bounded",
        "ratings": {
            "DEC_AUTH": 2, "EPI_GEN": 2,
            "ALG_SUB": 4, "MGT_CTRL": 4, "PROF_JUR": 2, "CLI_EMB": 2,
            "DEV_BRG": 2, "MED_BRK": 2, "GTG_AUD": 2, "SYS_MAL": 2,
            "EPI_OPA": 4, "VIS_FAIL": 3
        },
        "temporal": {
            "T0": "coercive_substitutive", "T1": "jurisdictional_threat",
            "T2": "compliance_or_drift", "T3": "R4_Displacement_or_Drift"
        },
        "quotes": {
            "DEC_AUTH": "p.1: 'AI crowded out line managers' expert practices of performing fairness, favouring HR's procedural version'",
            "MGT_CTRL": "p.12: 'HR mandate—right to define and enforce fair hiring—in symbiosis with AI procedures'"
        }
    }
}

# 10 Synthesis-Only Conceptual & Field-Level Studies (Separated from Empirical Case Pool per Skill v4 Rule)
SYNTHESIS_ONLY_RECORDS = [
    {
        "article_id": "A02", "cite": "Fernandez Cruz (2024)", "journal": "Information and Organization",
        "design": "42 cross-organizational interviews with recruitment professionals",
        "basis": "Source-author interpretation & field-level empirical pattern",
        "mechanism": "Organizational prioritization of AI and task-allocation structure condition whether experts intervene via oversight, correction, or deference.",
        "link_to_theory": "Corroborates COERC vs. EPI_VAL tension across unstructured HR settings."
    },
    {
        "article_id": "A03", "cite": "Dutta & Naveen (2025)", "journal": "Human Resource Management",
        "design": "43 HR leader interviews across Indian organizations",
        "basis": "Field-level empirical pattern (structuration lens)",
        "mechanism": "Discriminative and generative AI reshape signification, legitimation, and domination structures in recruitment.",
        "link_to_theory": "Explains why low-jurisdiction HR roles experience rapid norm shifts unless involved in configuring prompts/criteria."
    },
    {
        "article_id": "A05", "cite": "Ergün, Baer, & Plattfaut (2026)", "journal": "Journal of Information Technology",
        "design": "Qualitative study of team leaders managing GenAI-equipped teams",
        "basis": "Field-level leadership process",
        "mechanism": "Leaders recalibrate from task directive control toward epistemic coaching and boundary setting.",
        "link_to_theory": "Identifies managerial leadership recalibration (~MGT_CTRL) as an antecedent to team-level BND_INF."
    },
    {
        "article_id": "A08", "cite": "Goto (2021)", "journal": "Journal of Professions and Organization",
        "design": "Archival discourse + interviews in Japanese auditing profession",
        "basis": "Profession-level institutional mechanism",
        "mechanism": "Collective professional role identity is reconstructed macro-institutionally before firm-level AI deployment.",
        "link_to_theory": "Provides macro-institutional foundation for PROF_JUR as an anticipatory buffer."
    },
    {
        "article_id": "A09", "cite": "Goto (2022)", "journal": "Journal of Professions and Organization",
        "design": "Pre-deployment sensemaking interviews (2017-2019) in auditing",
        "basis": "Prospective sensemaking account",
        "mechanism": "Framing the future as 'ever-changing' enables professionals to normalize AI without surrendering core identity.",
        "link_to_theory": "Explains temporal pre-conditioning prior to Phase T0."
    },
    {
        "article_id": "A10", "cite": "Goto (2023)", "journal": "Research Policy",
        "design": "Field study of Big Four Japanese audit firms' AI R&D",
        "basis": "Field-level R&D governance",
        "mechanism": "Anticipatory innovation embeds practitioner audit logic into AI tools during R&D prior to rollout.",
        "link_to_theory": "Shows how high PROF_JUR fields pre-emptively build DEV_BRG upstream."
    },
    {
        "article_id": "A13", "cite": "Hopf et al. (2025)", "journal": "Journal of Information Technology",
        "design": "Hybrid human-agent team group-mind study",
        "basis": "Team-cognition mechanism",
        "mechanism": "Shared mental models and transactive memory between humans and intelligent agents require explicit representation of agent limits.",
        "link_to_theory": "Micro-cognitive foundation for why GTG_AUD + DEV_BRG generate EPI_GEN (Regime I)."
    },
    {
        "article_id": "A14", "cite": "Kellogg et al. (2025)", "journal": "Information and Organization",
        "design": "Post-experiment interviews at BCG on junior-to-senior GenAI coaching",
        "basis": "Empirical boundary failure mechanism",
        "mechanism": "'Novice risk work': juniors avoid coaching seniors on GenAI errors due to status anxiety, causing learning failures.",
        "link_to_theory": "Crucial negative mechanism showing why informal peer brokerage fails when hierarchical status blocks MED_BRK."
    },
    {
        "article_id": "A22", "cite": "Pemer & Werr (2025)", "journal": "Journal of Management Studies",
        "design": "Longitudinal interviews in Swedish Big Four PSFs",
        "basis": "Field-level institutional strategy",
        "mechanism": "'Creative accumulation': incumbents defuse digital disruption by absorbing new tech into partner-controlled advisory practices.",
        "link_to_theory": "Explains macro stability of Regime I in high-PROF_JUR partnership firms (FAU-A, FAU-L)."
    },
    {
        "article_id": "A29", "cite": "Vuori, Burkhard, & Pitkäranta (2025)", "journal": "Journal of Management Studies",
        "design": "Longitudinal study of internal AI expertise-profiling platform",
        "basis": "Within-organization behavioral mechanism",
        "mechanism": "High cognitive trust + low emotional trust (fear of exposure) triggers covert data hiding and manipulation, degrading AI quality.",
        "link_to_theory": "Parallels covert manipulation in STR-BANK and explains why coercive surveillance (MGT_CTRL) corrupts ground truth."
    }
]
