"""
Open Method Architecture Skill — Epistemic Governance, Production Lineage,
Method-Open Router, and Numerical Validator (control/oma_control.py)

Key advances over v4.0:
1. Method-Open Routing: Supports QCA ('run_qca'), Process-Sequence ('run_process_sequence'),
   Regime Discriminant Clustering ('run_regime_clustering'), Hybrid Multi-Method ('run_hybrid_best_fit'),
   and Synthesis-Only / ABM Specification-Gap routes ('synthesize_theory') after a mandatory
   Method-Fit Assessment ('assess_method_fit').
2. Production-Time Artifact Lineage ('produced_from'): Derived artifacts record the exact SHA-256
   hashes of the upstream artifacts used when they were computed. Issuing a new packet after an
   upstream edit cannot launder an un-recomputed derived artifact.
3. Built-In Mandatory Task Prerequisites: The controller enforces required upstream artifacts
   for every task rather than trusting caller-supplied lists alone.
4. Orthogonal Aggregation vs. Missingness Semantics: Requires translation rules to declare
   theoretical aggregation ('min', 'mean', 'max', 'single') separately from incomplete-evidence
   handling ('complete_component_required', 'boolean_absorption_available', 'null_to_zero_imputation',
   'null_to_one_stress').
5. Three Execution Modes & Three Branch Levels: Distinguishes 'researcher_operated', 'scripted_demo',
   and 'computational_replay' modes, and tracks 'interpretive', 'analytical', and 'design' branches.
"""
import copy
import hashlib
import json
import math

KNOWN_TASKS = {
    "intake_cases",          # Optional upstream adapter (disabled by default unless intake_adapter_enabled=True)
    "propose_codebook",      # Synthesis Layer: first-order constructs & relational schema
    "code_evidence",         # Synthesis Layer: empirical & conceptual relational coding (NULL preserved)
    "translate_constructs",  # Synthesis Layer: cross-study equivalence & macro/relational mapping
    "assess_method_fit",     # Analytical Layer Gate: diagnose structure & select best analytical pathway(s)
    "prepare_calibration",   # Analytical Layer: prepare calibration & pathway specifications
    "run_qca",               # Pathway A: deterministic fsQCA execution
    "run_process_sequence",  # Pathway B: longitudinal Markov sequence & NMI information-gain execution
    "run_regime_clustering", # Pathway C: multi-dimensional regime clustering & Kruskal-Wallis / OLS audit
    "run_hybrid_best_fit",   # Combined execution of Pathways A + B + C
    "synthesize_theory",     # Theory Elaboration Register, reverse evidence lineage & rival critique
    "discover_literature",   # Expansion Layer (requires expansion_enabled=True)
    "validate_system",       # Evaluation Layer (requires expansion_enabled=True & independent_humans=True)
}

PROPOSAL_TASKS = {
    "propose_codebook",
    "translate_constructs",
    "assess_method_fit",
    "prepare_calibration",
}

EXPANSION_TASKS = {
    "discover_literature",
    "validate_system",
}

MANDATORY_PREREQS = {
    "intake_cases": [],
    "propose_codebook": ["case_registry", "evidence_passages"],
    "code_evidence": ["case_registry", "evidence_passages", "codebook"],
    "translate_constructs": ["raw_coding"],
    "assess_method_fit": ["raw_coding", "translation_rules"],
    "prepare_calibration": ["raw_coding", "translation_rules", "method_fit_assessment"],
    "run_qca": ["calibrated_matrix", "qca_spec", "provenance"],
    "run_process_sequence": ["raw_coding", "method_fit_assessment"],
    "run_regime_clustering": ["raw_coding", "method_fit_assessment"],
    "run_hybrid_best_fit": ["calibrated_matrix", "qca_spec", "provenance", "method_fit_assessment"],
    "synthesize_theory": ["evidence_passages"],
    "discover_literature": [],
    "validate_system": [],
}

VALID_EXECUTION_MODES = {"researcher_operated", "scripted_demo", "computational_replay"}
VALID_BRANCH_LEVELS = {"root", "interpretive", "analytical", "design"}
VALID_AGGREGATION_OPS = {"min", "mean", "max", "single", "mixed_declared"}
VALID_MISSINGNESS_POLICIES = {
    "complete_component_required",
    "boolean_absorption_available",
    "available_component_fallback",
    "null_to_zero_imputation",
    "null_to_one_stress",
}

def canonical_hash(value):
    raw = json.dumps(value, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()

def validate_translation_rules(rules):
    """Ensure theoretical aggregation and missing-evidence policy are explicitly separated."""
    blockers = []
    if not isinstance(rules, dict):
        return {"ok": False, "blockers": ["translation_rules_not_dict"]}
    agg = rules.get("aggregation_operator")
    miss = rules.get("missingness_policy")
    if agg not in VALID_AGGREGATION_OPS:
        blockers.append(f"invalid_or_missing_aggregation_operator:{agg}")
    if miss not in VALID_MISSINGNESS_POLICIES:
        blockers.append(f"invalid_or_missing_missingness_policy:{miss}")
    return {"ok": len(blockers) == 0, "blockers": blockers}

def validate_matrix(rows, conditions, outcome, crossover_policy_documented=False, crossover_handled=False):
    """Validate a calibrated set-membership matrix before QCA execution."""
    blockers = []
    warnings = []
    if not isinstance(rows, list) or len(rows) == 0:
        return {"ok": False, "blockers": ["empty_or_invalid_matrix"], "warnings": []}
    if not isinstance(conditions, list) or len(conditions) == 0 or not isinstance(outcome, str):
        return {"ok": False, "blockers": ["invalid_schema_spec"], "warnings": []}
    if outcome in conditions:
        blockers.append("outcome_in_conditions")

    expected_cols = {"case_id", outcome} | set(conditions)
    seen_ids = set()
    col_values = {c: [] for c in list(conditions) + [outcome]}
    has_exact_half = False

    for idx, r in enumerate(rows):
        if not isinstance(r, dict):
            blockers.append(f"row_{idx}_not_dict")
            continue
        cid = r.get("case_id")
        if cid is None or str(cid).strip() == "":
            blockers.append(f"row_{idx}_missing_case_id")
        elif cid in seen_ids:
            blockers.append(f"duplicate_case_id:{cid}")
        else:
            seen_ids.add(cid)

        extra = set(r.keys()) - expected_cols
        missing = expected_cols - set(r.keys())
        if extra:
            blockers.append(f"unexpected_columns:{sorted(extra)}")
        if missing:
            blockers.append(f"missing_columns:{sorted(missing)}")

        for c in list(conditions) + [outcome]:
            v = r.get(c)
            if isinstance(v, bool) or not isinstance(v, (int, float)):
                blockers.append(f"non_numeric:{cid}:{c}")
                continue
            if math.isnan(v) or math.isinf(v):
                blockers.append(f"nan_or_inf:{cid}:{c}")
                continue
            if v < 0.0 or v > 1.0:
                blockers.append(f"out_of_bounds:{cid}:{c}:{v}")
                continue
            if abs(v - 0.5) < 1e-9:
                has_exact_half = True
            col_values[c].append(float(v))

    if has_exact_half and not (crossover_policy_documented is True and crossover_handled is True):
        blockers.append("unresolved_0.5_crossover")

    for c, vals in col_values.items():
        if len(vals) > 1 and len(set(round(x, 6) for x in vals)) == 1:
            warnings.append(f"constant_column:{c}")

    return {"ok": len(blockers) == 0, "blockers": blockers, "warnings": warnings}


class OMAWorkflow:
    def __init__(
        self,
        execution_mode="researcher_operated",
        intake_adapter_enabled=False,
        expansion_enabled=False,
        tools_available=True,
        independent_humans=False,
    ):
        if execution_mode not in VALID_EXECUTION_MODES:
            raise ValueError(f"Invalid execution_mode: {execution_mode}")
        self.execution_mode = execution_mode
        self.intake_adapter_enabled = intake_adapter_enabled is True
        self.expansion_enabled = expansion_enabled is True
        self.tools_available = tools_available is True
        self.independent_humans = independent_humans is True
        self.branches = {
            "main": {
                "parent": None,
                "branch_level": "root",
                "commitment": "Baseline trajectory",
                "artifacts": {},
                "deps": {},
                "packets": {},
                "quarantined": False,
                "quarantine_reasons": [],
            }
        }

    def _branch(self, branch):
        if branch not in self.branches:
            raise ValueError(f"Unknown branch: {branch}")
        return self.branches[branch]

    def _has_cycle(self, deps, start, target):
        visited = set()
        stack = [target]
        while stack:
            curr = stack.pop()
            if curr == start:
                return True
            if curr in visited:
                continue
            visited.add(curr)
            stack.extend(deps.get(curr, []))
        return False

    def put_artifact(self, name, content, depends_on=None, branch="main", status="PROPOSED"):
        b = self._branch(branch)
        depends_on = list(depends_on or [])
        if name in depends_on:
            raise ValueError(f"Self-dependency on artifact: {name}")
        for d in depends_on:
            if d not in b["artifacts"]:
                raise ValueError(f"Missing dependency artifact: {d}")
            if self._has_cycle(b["deps"], name, d):
                raise ValueError(f"Dependency cycle involving: {name} -> {d}")
        copied = copy.deepcopy(content)
        # Record exact upstream hashes at the moment this artifact was produced
        produced_from = {d: b["artifacts"][d]["hash"] for d in depends_on}
        b["artifacts"][name] = {
            "content": copied,
            "hash": canonical_hash(copied),
            "status": status,
            "produced_from": produced_from,
            "execution_mode": self.execution_mode,
        }
        b["deps"][name] = depends_on
        return b["artifacts"][name]["hash"]

    def artifact_lineage_is_fresh(self, name, branch="main"):
        """Check recursively that 'name' and all its ancestors were produced from current upstream hashes."""
        b = self._branch(branch)
        if name not in b["artifacts"]:
            return False, f"missing_artifact:{name}"
        closure = self.transitive_closure([name], branch=branch)
        for art_name in closure:
            aobj = b["artifacts"][art_name]
            prod_map = aobj.get("produced_from", {})
            for parent_name, recorded_parent_hash in prod_map.items():
                cur_parent = b["artifacts"].get(parent_name)
                if not cur_parent or cur_parent["hash"] != recorded_parent_hash:
                    return False, f"stale_derived_artifact_lineage:{art_name}_from_{parent_name}"
        return True, "fresh_lineage"

    def transitive_closure(self, names, branch="main"):
        b = self._branch(branch)
        seen = []
        queue = list(names)
        while queue:
            n = queue.pop(0)
            if n in seen:
                continue
            if n not in b["artifacts"]:
                raise ValueError(f"Unknown artifact in closure: {n}")
            seen.append(n)
            for parent in b["deps"].get(n, []):
                if parent not in seen:
                    queue.append(parent)
        return seen

    def issue_packet(self, packet_id, task, required_artifacts=None, branch="main", contested=False):
        if task not in KNOWN_TASKS:
            raise ValueError(f"Unknown task: {task}")
        b = self._branch(branch)
        if packet_id in b["packets"]:
            raise ValueError(f"Duplicate packet_id: {packet_id}")
        # Merge caller required_artifacts with built-in mandatory prerequisites
        mandatory = MANDATORY_PREREQS.get(task, [])
        combined_reqs = []
        for r in list(mandatory) + list(required_artifacts or []):
            if r not in combined_reqs:
                combined_reqs.append(r)
        closure = self.transitive_closure(combined_reqs, branch=branch)
        snap = {n: b["artifacts"][n]["hash"] for n in closure}
        b["packets"][packet_id] = {
            "packet_id": packet_id,
            "task": task,
            "branch": branch,
            "required": combined_reqs,
            "closure": closure,
            "snapshot_hashes": snap,
            "contested": bool(contested),
            "decision": None,
            "actor": None,
            "execution_mode": self.execution_mode,
            "reason": None,
            "superseded_by": None,
        }
        return copy.deepcopy(b["packets"][packet_id])

    def supersede_packet(self, old_packet_id, new_packet_id, required_artifacts=None, branch="main", contested=None):
        b = self._branch(branch)
        if old_packet_id not in b["packets"]:
            raise ValueError(f"Unknown packet_id to supersede: {old_packet_id}")
        old_p = b["packets"][old_packet_id]
        if old_p["superseded_by"] is not None:
            raise ValueError(f"Packet {old_packet_id} already superseded by {old_p['superseded_by']}")
        reqs = required_artifacts if required_artifacts is not None else old_p["required"]
        cont = contested if contested is not None else old_p["contested"]
        new_p = self.issue_packet(new_packet_id, old_p["task"], reqs, branch=branch, contested=cont)
        old_p["superseded_by"] = new_packet_id
        return new_p

    def record_decision(self, packet_id, action, actor="human", reason="", branch="main"):
        b = self._branch(branch)
        if packet_id not in b["packets"]:
            return {"ok": False, "error": "unknown_packet"}
        p = b["packets"][packet_id]
        if p["superseded_by"] is not None:
            return {"ok": False, "error": "packet_superseded"}
        if p["decision"] is not None:
            return {"ok": False, "error": "packet_already_decided"}
        # Actor validation: must be 'human' (or 'scripted_demo' ONLY when workflow execution_mode == 'scripted_demo')
        allowed_actors = {"human"} if self.execution_mode != "scripted_demo" else {"human", "scripted_demo"}
        if actor not in allowed_actors:
            return {"ok": False, "error": "non_human_actor"}
        if action not in {"approve", "reject"}:
            return {"ok": False, "error": "invalid_or_conditional_action"}
        if p["contested"] and (not isinstance(reason, str) or len(reason.strip()) == 0):
            return {"ok": False, "error": "contested_requires_reason"}
        p["decision"] = "approved" if action == "approve" else "rejected"
        p["actor"] = actor
        p["reason"] = reason.strip() if isinstance(reason, str) else ""
        return {"ok": True, "status": p["decision"], "actor": actor, "execution_mode": self.execution_mode}

    def fork_branch(self, new_branch, from_branch="main", branch_level="analytical", commitment=""):
        if new_branch in self.branches:
            raise ValueError(f"Branch already exists: {new_branch}")
        if branch_level not in VALID_BRANCH_LEVELS:
            raise ValueError(f"Invalid branch_level: {branch_level}")
        src = self._branch(from_branch)
        self.branches[new_branch] = {
            "parent": from_branch,
            "branch_level": branch_level,
            "commitment": str(commitment),
            "artifacts": copy.deepcopy(src["artifacts"]),
            "deps": copy.deepcopy(src["deps"]),
            "packets": {},  # Never inherit execution approvals into a child branch
            "quarantined": False,
            "quarantine_reasons": [],
        }
        return new_branch

    def packet_is_fresh(self, packet_id, branch="main"):
        b = self._branch(branch)
        p = b["packets"].get(packet_id)
        if not p:
            return False, "unknown_packet"
        if p["superseded_by"] is not None:
            return False, "packet_superseded"
        for n, h in p["snapshot_hashes"].items():
            cur = b["artifacts"].get(n)
            if not cur or cur["hash"] != h:
                return False, "stale_upstream_artifact"
            ok_lin, lin_reason = self.artifact_lineage_is_fresh(n, branch=branch)
            if not ok_lin:
                return False, lin_reason
        return True, "fresh"

    def route_task(self, requested_task, branch="main"):
        if requested_task not in KNOWN_TASKS:
            return {"allowed_proposal": False, "reason": "unknown_task"}
        b = self._branch(branch)
        arts = b["artifacts"]
        if requested_task == "intake_cases" and not self.intake_adapter_enabled:
            return {"allowed_proposal": False, "reason": "intake_adapter_disabled_by_default"}
        if requested_task in EXPANSION_TASKS and not self.expansion_enabled:
            return {"allowed_proposal": False, "reason": "expansion_layer_disabled"}

        for req in MANDATORY_PREREQS.get(requested_task, []):
            if req not in arts:
                return {"allowed_proposal": False, "reason": f"missing_prerequisite:{req}"}

        if requested_task == "synthesize_theory":
            # Method-open theory synthesis: requires at least one VERIFIED analytical output
            # (qca_results, process_sequence_results, regime_cluster_results, hybrid_results, or synthesis_only_record)
            verified_outputs = [
                k for k in ("qca_results", "process_sequence_results", "regime_cluster_results", "hybrid_results", "synthesis_only_record")
                if arts.get(k, {}).get("status") == "VERIFIED"
            ]
            if not verified_outputs:
                return {"allowed_proposal": False, "reason": "no_verified_analytical_results"}
            return {"allowed_proposal": True, "skill": "07_theory_elaboration_and_critique.md", "verified_inputs": verified_outputs}

        skill_map = {
            "intake_cases": "00_optional_case_intake_adapter.md",
            "propose_codebook": "01_construct_and_relational_coding.md",
            "code_evidence": "01_construct_and_relational_coding.md",
            "translate_constructs": "02_cross_study_translation.md",
            "assess_method_fit": "03_method_fit_and_routing.md",
            "prepare_calibration": "05_qca_pathway.md",
            "run_qca": "05_qca_pathway.md",
            "run_process_sequence": "06_process_and_regime_pathway.md",
            "run_regime_clustering": "06_process_and_regime_pathway.md",
            "run_hybrid_best_fit": "06_process_and_regime_pathway.md",
            "discover_literature": "08_expansion_and_validation.md",
            "validate_system": "08_expansion_and_validation.md",
        }
        return {"allowed_proposal": True, "skill": skill_map[requested_task]}

    def authorize_execution(self, task, packet_id, branch="main"):
        if task not in KNOWN_TASKS:
            return {"allowed": False, "reason": "unknown_task"}
        if branch not in self.branches:
            return {"allowed": False, "reason": "unknown_branch"}
        b = self.branches[branch]
        if b.get("quarantined"):
            return {"allowed": False, "reason": "branch_quarantined"}
        if not self.tools_available:
            return {"allowed": False, "reason": "tools_unavailable"}
        if task == "intake_cases" and not self.intake_adapter_enabled:
            return {"allowed": False, "reason": "intake_adapter_disabled_by_default"}
        if task in EXPANSION_TASKS and not self.expansion_enabled:
            return {"allowed": False, "reason": "expansion_layer_disabled"}
        if task == "validate_system" and not self.independent_humans:
            return {"allowed": False, "reason": "independent_humans_required"}

        # Enforce mandatory prerequisites at execution time
        for req in MANDATORY_PREREQS.get(task, []):
            if req not in b["artifacts"]:
                return {"allowed": False, "reason": f"missing_prerequisite:{req}"}

        p = b["packets"].get(packet_id)
        if not p:
            return {"allowed": False, "reason": "wrong_task_or_branch"}
        if p["task"] != task or p["branch"] != branch:
            return {"allowed": False, "reason": "wrong_task_or_branch"}
        if p["superseded_by"] is not None:
            return {"allowed": False, "reason": "packet_superseded"}
        allowed_actors = {"human"} if self.execution_mode != "scripted_demo" else {"human", "scripted_demo"}
        if p["decision"] != "approved" or p["actor"] not in allowed_actors:
            return {"allowed": False, "reason": "not_approved"}

        fresh, reason = self.packet_is_fresh(packet_id, branch=branch)
        if not fresh:
            return {"allowed": False, "reason": reason}

        if task == "translate_constructs":
            tr = b["artifacts"].get("translation_rules", {}).get("content")
            vt = validate_translation_rules(tr)
            if not vt["ok"]:
                return {"allowed": False, "reason": "invalid_translation_rules", "blockers": vt["blockers"]}

        if task in ("run_qca", "run_hybrid_best_fit"):
            mat = b["artifacts"].get("calibrated_matrix", {}).get("content")
            spec = b["artifacts"].get("qca_spec", {}).get("content")
            if not isinstance(spec, dict):
                return {"allowed": False, "reason": "invalid_qca_spec"}
            v = validate_matrix(
                mat,
                spec.get("conditions", []),
                spec.get("outcome", ""),
                crossover_policy_documented=spec.get("crossover_policy_documented") is True,
                crossover_handled=spec.get("crossover_handled") is True,
            )
            if not v["ok"]:
                return {"allowed": False, "reason": "matrix_validation_failed", "blockers": v["blockers"]}

        if task == "synthesize_theory":
            verified_outputs = [
                k for k in ("qca_results", "process_sequence_results", "regime_cluster_results", "hybrid_results", "synthesis_only_record")
                if b["artifacts"].get(k, {}).get("status") == "VERIFIED"
            ]
            if not verified_outputs:
                return {"allowed": False, "reason": "no_verified_analytical_results"}

        return {"allowed": True, "reason": "authorized", "execution_mode": self.execution_mode}

    def to_json(self):
        return json.dumps(
            {
                "execution_mode": self.execution_mode,
                "intake_adapter_enabled": self.intake_adapter_enabled,
                "expansion_enabled": self.expansion_enabled,
                "tools_available": self.tools_available,
                "independent_humans": self.independent_humans,
                "branches": self.branches,
            },
            sort_keys=True,
        )

    @classmethod
    def from_json(cls, raw_str):
        try:
            data = json.loads(raw_str)
        except Exception as e:
            raise ValueError(f"Corrupted JSON state: {e}")
        if not isinstance(data, dict) or "branches" not in data or not isinstance(data["branches"], dict):
            raise ValueError("Invalid state structure")
        wf = cls(
            execution_mode=data.get("execution_mode", "researcher_operated"),
            intake_adapter_enabled=data.get("intake_adapter_enabled") is True,
            expansion_enabled=data.get("expansion_enabled") is True,
            tools_available=data.get("tools_available") is True,
            independent_humans=data.get("independent_humans") is True,
        )
        wf.branches = copy.deepcopy(data["branches"])
        for bname, b in wf.branches.items():
            reasons = []
            for aname, aobj in b.get("artifacts", {}).items():
                actual_h = canonical_hash(aobj.get("content"))
                if actual_h != aobj.get("hash"):
                    reasons.append(f"artifact_hash_mismatch:{aname}")
                    aobj["hash"] = actual_h
            for aname, aobj in b.get("artifacts", {}).items():
                for parent_name, rec_h in aobj.get("produced_from", {}).items():
                    cur_p = b.get("artifacts", {}).get(parent_name)
                    if not cur_p or cur_p.get("hash") != rec_h:
                        reasons.append(f"stale_derived_lineage:{aname}_from_{parent_name}")
            for pid, p in b.get("packets", {}).items():
                if p.get("decision") == "approved" and p.get("superseded_by") is None:
                    for n, sh in p.get("snapshot_hashes", {}).items():
                        cur = b.get("artifacts", {}).get(n)
                        if not cur or cur.get("hash") != sh:
                            reasons.append(f"stale_approved_packet:{pid}:{n}")
            if reasons:
                b["quarantined"] = True
                b["quarantine_reasons"] = reasons
        return wf

    def branch_dashboard(self):
        out = {}
        for bname, b in self.branches.items():
            if b.get("quarantined"):
                out[bname] = {
                    "status": "QUARANTINED",
                    "branch_level": b.get("branch_level", "root"),
                    "reasons": b.get("quarantine_reasons", []),
                }
                continue
            stale_packets = []
            for pid, p in b["packets"].items():
                if p["decision"] == "approved" and p["superseded_by"] is None:
                    fresh, _ = self.packet_is_fresh(pid, branch=bname)
                    if not fresh:
                        stale_packets.append(pid)
            out[bname] = {
                "status": "STALE" if stale_packets else "OK",
                "branch_level": b.get("branch_level", "root"),
                "execution_mode": self.execution_mode,
                "stale_packets": stale_packets,
                "n_artifacts": len(b["artifacts"]),
                "n_packets": len(b["packets"]),
            }
        return out
