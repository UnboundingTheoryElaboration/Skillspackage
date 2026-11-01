# Skill 04: Human Judgment, Production Lineage, and Three-Level Branching (`04_human_judgment_and_governance.md`)

## 1. Governance Invariants Enforced by `control/oma_control.py`
1. **Production-Time Lineage (`produced_from`)**: Every derived artifact stores the SHA-256 hashes of its parent artifacts at computation time. Mutating an upstream artifact blocks execution even if a new packet is issued, until the derived artifact is recomputed.
2. **Three Execution Modes**:
   - `researcher_operated`: Requires `actor="human"` for all approvals.
   - `scripted_demo`: Allows `actor="scripted_demo"` for automated benchmark demonstrations and labels all outputs as scripted demonstration traces.
   - `computational_replay`: Re-runs deterministic checks on previously approved states without claiming new human review.
3. **Three Branch Levels**:
   - `interpretive`: Competing readings of a construct or case outcome (e.g., relational authority vs. strict decision control).
   - `analytical`: Competing operationalizations within a method (e.g., weakest-link `min` vs. compensatory `mean`, or linear vs. logistic calibration).
   - `design`: Competing methodological pathways (e.g., QCA-Only vs. Best-Fit Hybrid Process + Regime + QCA).
