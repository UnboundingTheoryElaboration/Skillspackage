"""
Open Method Architecture Skill — Unified Deterministic Analytical Engines (control/oma_engines.py)
Contains:
1. Substantive Calibration & Orthogonal Set/Missingness Operators
2. Method-Fit Diagnostic Scorer (evaluate_method_fit)
3. Exact Quine-McCluskey fsQCA & Enhanced Standard Analysis (ESA) Engine (Raw & Aggregate Truth-Table Modes)
4. Longitudinal Markov Process-Sequence & Shannon/NMI Information-Theoretic Engine
5. Multi-Dimensional Regime Kruskal-Wallis Discriminant & Linear OLS Failure Audit Engine
"""
import itertools
import math
from collections import Counter, defaultdict
import numpy as np
import pandas as pd

# ---------------- 1. Substantive Calibration ----------------
def cal_linear(x, lo=1.0, co=2.9, hi=5.0):
    x = np.asarray(x, dtype=float)
    out = np.full(x.shape, np.nan)
    m = ~np.isnan(x)
    v = x[m]
    out[m] = np.where(
        v <= co,
        0.5 * (v - lo) / (co - lo),
        0.5 + 0.5 * (v - co) / (hi - co),
    )
    return np.clip(out, 0.0, 1.0)

def cal_logistic(x, lo=1.0, co=2.9, hi=5.0):
    x = np.asarray(x, dtype=float)
    out = np.full(x.shape, np.nan)
    m = ~np.isnan(x)
    v = x[m]
    lo_odds = np.where(v >= co, (v - co) * 3.0 / (hi - co), (v - co) * 3.0 / (co - lo))
    out[m] = 1.0 / (1.0 + np.exp(-lo_odds))
    return np.clip(out, 0.0, 1.0)

DIRECT_MAP = {1: 0.0, 2: 0.25, 3: 0.60, 4: 0.80, 5: 1.0}
def cal_direct(x):
    x = np.asarray(x, dtype=float)
    return np.array([np.nan if np.isnan(v) else DIRECT_MAP.get(int(round(v)), np.nan) for v in x], dtype=float)

# ---------------- 2. Orthogonal Set & Missingness Operators ----------------
def fmin_strict(*cols):
    """Complete-component conjunction: any NaN constituent returns NaN."""
    a = np.vstack(cols)
    any_nan = np.any(np.isnan(a), axis=0)
    safe = np.where(np.isnan(a), np.inf, a)
    res = np.min(safe, axis=0)
    res[any_nan] = np.nan
    return res

def fmin_avail(*cols):
    """Available-component conjunction (or Boolean absorption when observed=0.0)."""
    a = np.vstack(cols)
    all_nan = np.all(np.isnan(a), axis=0)
    safe = np.where(np.isnan(a), np.inf, a)
    res = np.min(safe, axis=0)
    res[all_nan] = np.nan
    return res

def fmean_avail(*cols):
    """Compensatory average over available non-NaN components."""
    a = np.vstack(cols)
    valid_counts = np.sum(~np.isnan(a), axis=0)
    safe_sum = np.nansum(a, axis=0)
    res = np.full(a.shape[1], np.nan, dtype=float)
    mask = valid_counts > 0
    res[mask] = safe_sum[mask] / valid_counts[mask]
    return res

def fmax_strict(*cols):
    """Complete-component union: any NaN constituent returns NaN."""
    a = np.vstack(cols)
    any_nan = np.any(np.isnan(a), axis=0)
    safe = np.where(np.isnan(a), -np.inf, a)
    res = np.max(safe, axis=0)
    res[any_nan] = np.nan
    return res

def fmax_avail(*cols):
    """Available-component union."""
    a = np.vstack(cols)
    all_nan = np.all(np.isnan(a), axis=0)
    safe = np.where(np.isnan(a), -np.inf, a)
    res = np.max(safe, axis=0)
    res[all_nan] = np.nan
    return res

def fuzzy_jaccard_matrix(cal_df, cols):
    n = len(cols)
    j_pos = np.zeros((n, n))
    j_neg = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            a = cal_df[cols[i]].values
            b = cal_df[cols[j]].values
            m = (~np.isnan(a)) & (~np.isnan(b))
            av, bv = a[m], b[m]
            dp = np.maximum(av, bv).sum()
            j_pos[i, j] = np.minimum(av, bv).sum() / dp if dp > 0 else np.nan
            dn = np.maximum(av, 1.0 - bv).sum()
            j_neg[i, j] = np.minimum(av, 1.0 - bv).sum() / dn if dn > 0 else np.nan
    return (
        pd.DataFrame(j_pos, index=cols, columns=cols).round(3),
        pd.DataFrame(j_neg, index=cols, columns=cols).round(3),
    )

# ---------------- 3. Method-Fit Diagnostic Scorer ----------------
def evaluate_method_fit(
    n_empirical_cases,
    n_longitudinal_cases,
    n_synthesis_only_studies,
    n_outcomes,
    outcome_positive_share,
    has_within_corner_bifurcation=False,
    has_parameterized_abm_rules=False,
):
    """
    Evaluates the empirical corpus structure before committing to an analytical engine.
    Computes genuine structure-dependent fit scores across candidate pathways, sorts
    candidates by fit_score descending, and assigns status dynamically so that the
    recommended pathway is determined by the corpus diagnostics rather than list order.
    """
    long_share = n_longitudinal_cases / max(1, n_empirical_cases)
    skew_warning = outcome_positive_share > 0.75 or outcome_positive_share < 0.25

    # 1. Static Single-Outcome fsQCA Alone
    if n_empirical_cases < 10:
        qca_score = 0.30
        qca_rationale = f"Insufficient bounded cases (N={n_empirical_cases} < 10) for reliable truth-table minimization."
    elif n_outcomes == 1 and long_share < 0.35 and not skew_warning and not has_within_corner_bifurcation:
        qca_score = 0.91
        qca_rationale = (
            f"Best fit: {n_empirical_cases} cross-sectional cases with a balanced single outcome "
            f"({outcome_positive_share*100:.1f}% positive), low longitudinal share ({long_share*100:.1f}%), "
            "and no unresolved within-corner trajectory contradictions."
        )
    else:
        penalties = 0.0
        if skew_warning:
            penalties += 0.10
        if long_share >= 0.40:
            penalties += 0.08
        if n_outcomes >= 2:
            penalties += 0.06
        if has_within_corner_bifurcation:
            penalties += 0.08
        qca_score = round(max(0.45, 0.90 - penalties), 2)
        qca_rationale = (
            f"Captures cross-case Boolean equifinality across {n_empirical_cases} cases, but static single-outcome QCA alone "
            f"is penalized by outcome skew ({outcome_positive_share*100:.1f}% positive={skew_warning}), "
            f"longitudinal process share ({long_share*100:.1f}%), n_outcomes={n_outcomes}, and "
            f"within-corner bifurcation={has_within_corner_bifurcation}."
        )

    # 2. Longitudinal Process-Sequence & Information-Theoretic Trajectory Analysis Alone
    if n_empirical_cases >= 6 and long_share >= 0.65 and n_outcomes == 1 and n_empirical_cases < 15:
        proc_score = 0.90
        proc_rationale = (
            f"Best fit: corpus is predominantly longitudinal ({n_longitudinal_cases}/{n_empirical_cases}, {long_share*100:.1f}%) "
            f"with N={n_empirical_cases} better suited to stage-transition (T0->T1->T2->T3) modeling than truth tables."
        )
    elif long_share >= 0.40:
        proc_score = 0.82
        proc_rationale = (
            f"Strong process signal ({n_longitudinal_cases}/{n_empirical_cases} longitudinal cases, {long_share*100:.1f}%): "
            "resolves temporal ordering and breakdown-triggered transitions, and complements cross-case set analysis."
        )
    else:
        proc_score = 0.40
        proc_rationale = (
            f"Low longitudinal coverage ({n_longitudinal_cases}/{n_empirical_cases}, {long_share*100:.1f}% < 40%) "
            "limits multi-stage transition estimation."
        )

    # 3. 2D Four-Regime Clustering & Non-Parametric Kruskal-Wallis Discriminant Analysis
    if n_empirical_cases >= 12 and n_outcomes >= 2 and long_share < 0.35:
        reg_score = 0.89
        reg_rationale = (
            f"Best fit for multi-dimensional cross-sectional corpus: {n_outcomes} distinct outcome dimensions across "
            f"{n_empirical_cases} cases with limited temporal stage data ({long_share*100:.1f}%)."
        )
    elif n_empirical_cases >= 12 and n_outcomes >= 2:
        reg_score = 0.84
        reg_rationale = (
            f"Disaggregates {n_outcomes} outcome dimensions across {n_empirical_cases} cases and ranks construct "
            "effect sizes (Kruskal-Wallis eta^2) without forcing single-dimension collapse."
        )
    else:
        reg_score = 0.42
        reg_rationale = f"Single outcome dimension (n_outcomes={n_outcomes}) or small sample (N={n_empirical_cases}) does not require 2D regime clustering."

    # 4. Hybrid Multi-Method Triangulation (Multi-Outcome fsQCA + Process-Sequence + 2D Regime Clustering)
    if n_empirical_cases >= 15 and long_share >= 0.40 and (n_outcomes >= 2 or has_within_corner_bifurcation):
        hyb_score = 0.94
        hyb_rationale = (
            f"Best fit: {n_empirical_cases} cases support cross-case Boolean minimization, while "
            f"{n_longitudinal_cases}/{n_empirical_cases} ({long_share*100:.1f}%) longitudinal cases and "
            f"n_outcomes={n_outcomes} (bifurcation={has_within_corner_bifurcation}) require combining multi-outcome fsQCA, "
            "Markov sequence analysis, and 2D regime discriminant analysis."
        )
    elif n_empirical_cases >= 15 and (long_share >= 0.40 or n_outcomes >= 2):
        hyb_score = 0.78
        hyb_rationale = "Feasible multi-method triangulation, though a simpler single-pathway design may suffice."
    else:
        hyb_score = 0.48
        hyb_rationale = (
            f"Hybrid 3-engine triangulation is over-parameterized for N={n_empirical_cases}, "
            f"longitudinal_share={long_share*100:.1f}%, n_outcomes={n_outcomes}."
        )

    # 5. Qualitative Relational Synthesis & Specification-Gap Report Only (Small-N / Conceptual)
    if n_empirical_cases < 10:
        qual_score = 0.92
        qual_rationale = (
            f"Best fit: with N={n_empirical_cases} bounded empirical cases and {n_synthesis_only_studies} synthesis-only studies, "
            "formal truth-table or Markov estimation is under-powered; use structured relational synthesis."
        )
    else:
        qual_score = 0.50
        qual_rationale = f"Corpus has sufficient bounded cases (N={n_empirical_cases}) to support formal cross-case analytical engines."

    # 6. Additive Linear Net-Effects Regression (OLS)
    ols_score = 0.25
    ols_rationale = (
        "Assumes symmetric additive marginal effects and independent observations; mis-specified for conjunctural, "
        "equifinal, or small-to-medium qualitative case corpora (retained only as a diagnostic contrast)."
    )

    # 7. Agent-Based Simulation (ABM)
    abm_score = 0.80 if has_parameterized_abm_rules else 0.20
    abm_rationale = (
        "Empirically calibrated transition rules available for simulation."
        if has_parameterized_abm_rules
        else "Qualitative studies describe actor interactions narratively without calibrated micro-transition parameters; "
             "running an ABM would require invented parameters."
    )

    candidates = [
        {"pathway": "Hybrid Multi-Method Triangulation (Multi-Outcome fsQCA + 4-Stage Process-Sequence + 2D Regime Clustering)", "fit_score": hyb_score, "rationale": hyb_rationale},
        {"pathway": "Static Single-Outcome fsQCA Alone", "fit_score": qca_score, "rationale": qca_rationale},
        {"pathway": "Longitudinal Process-Sequence & Information-Theoretic Trajectory Analysis Alone", "fit_score": proc_score, "rationale": proc_rationale},
        {"pathway": "2D Four-Regime Clustering & Non-Parametric Kruskal-Wallis Discriminant Analysis", "fit_score": reg_score, "rationale": reg_rationale},
        {"pathway": "Qualitative Relational Synthesis & Specification-Gap Report Only", "fit_score": qual_score, "rationale": qual_rationale},
        {"pathway": "Additive Linear Net-Effects Regression (OLS)", "fit_score": ols_score, "rationale": ols_rationale},
        {"pathway": "Agent-Based Simulation (ABM)", "fit_score": abm_score, "rationale": abm_rationale},
    ]

    # Sort descending by fit_score so candidates[0] is genuinely the highest-scoring pathway
    candidates.sort(key=lambda d: d["fit_score"], reverse=True)

    for idx, c in enumerate(candidates):
        s = c["fit_score"]
        if idx == 0:
            c["status"] = "RECOMMENDED_BEST_FIT"
        elif s >= 0.75:
            c["status"] = "COMPLEMENTARY_CORE_ENGINE"
        elif s >= 0.55:
            c["status"] = "DEFENSIBLE_BUT_INCOMPLETE"
        elif c["pathway"].startswith("Agent-Based"):
            c["status"] = "SPECIFICATION_GAP_ONLY"
        else:
            c["status"] = "REJECTED_MIS_SPECIFIED"

    return {
        "n_empirical_cases": n_empirical_cases,
        "n_longitudinal_cases": n_longitudinal_cases,
        "longitudinal_share": round(long_share, 3),
        "n_synthesis_only_studies": n_synthesis_only_studies,
        "outcome_positive_share": round(outcome_positive_share, 3),
        "outcome_skew_warning": skew_warning,
        "recommended_pathway": candidates[0]["pathway"],
        "candidates": candidates,
    }

# ---------------- 4. Exact Quine-McCluskey fsQCA & ESA Engine ----------------
ALLB = {}
def all_bits(k):
    if k not in ALLB:
        ALLB[k] = [tuple(b) for b in itertools.product([0, 1], repeat=k)]
    return ALLB[k]

def row_membership(X, bits):
    M = np.where(np.array(bits)[None, :] == 1, X, 1.0 - X)
    return M.min(axis=1)

def truth_table(X, Y, names, incl_cut=0.80, pri_cut=0.60, n_cut=1):
    k = X.shape[1]
    rows = []
    for idx, bits in enumerate(itertools.product([0, 1], repeat=k), 1):
        m = row_membership(X, bits)
        n = int((m > 0.5).sum())
        sm = float(m.sum())
        smy = float(np.minimum(m, Y).sum())
        smyn = float(np.minimum(np.minimum(m, Y), 1.0 - Y).sum())
        incl = smy / sm if sm > 0 else np.nan
        pri = (smy - smyn) / (sm - smyn) if (sm - smyn) > 0 else np.nan
        if n < n_cut:
            out = "?"
        else:
            out = 1 if (incl >= incl_cut - 1e-9 and pri >= pri_cut - 1e-9) else 0
        rows.append(
            dict(
                row=idx,
                bits=bits,
                n=n,
                incl=incl,
                pri=pri,
                OUT=out,
                cases=list(np.where(m > 0.5)[0]),
            )
        )
    return rows

def covers(term, b):
    return all(t is None or t == x for t, x in zip(term, b))

def minterms(term):
    return [b for b in all_bits(len(term)) if covers(term, b)]

def subsumes(a, b):
    return all(x is None or x == y for x, y in zip(a, b))

def nlit(t):
    return sum(v is not None for v in t)

def prime_implicants(P, allowed):
    if not P:
        return []
    k = len(next(iter(P)))
    valid = [
        t
        for t in itertools.product([None, 0, 1], repeat=k)
        if any(covers(t, p) for p in P) and all(m in allowed for m in minterms(t))
    ]
    return [t for t in valid if not any(u != t and subsumes(u, t) for u in valid)]

def cover_solutions(P, PIs):
    """Exhaustive Petrick/minimal-cover search without silent truncation."""
    if not P or not PIs:
        return []
    sols = []
    for k in range(1, len(PIs) + 1):
        for combo in itertools.combinations(PIs, k):
            if all(any(covers(t, p) for t in combo) for p in P):
                sols.append(combo)
        if sols:
            break
    if not sols:
        return []
    m = min(sum(nlit(t) for t in s) for s in sols)
    return [s for s in sols if sum(nlit(t) for t in s) == m]

def intermediate_PIs(P, R, names, direxp):
    cpi = prime_implicants(P, set(P))
    ppi = prime_implicants(P, set(P) | set(R))
    out = set()
    for c in cpi:
        for p in ppi:
            if not subsumes(p, c):
                continue
            t = list(c)
            for i, v in enumerate(c):
                if v is None or p[i] is not None:
                    continue
                e = direxp.get(names[i])
                if e is not None and v != e:
                    t[i] = None
            t = tuple(t)
            if all(m in (set(P) | set(R)) for m in minterms(t)):
                out.add(t)
    out = list(out)
    return [t for t in out if not any(u != t and subsumes(u, t) for u in out)]

def lit(t, names):
    s = [("" if v == 1 else "~") + names[i] for i, v in enumerate(t) if v is not None]
    return "*".join(s) if s else "1"

def solve_all(tt, names, direxp, esa_exclude=()):
    P = {r["bits"] for r in tt if r["OUT"] == 1}
    N = {r["bits"] for r in tt if r["OUT"] == 0}
    R = {r["bits"] for r in tt if r["OUT"] == "?"} - set(esa_exclude)
    if not P:
        return dict(P=P, N=N, R=R, complex=[], pars=[], inter=[], exhaustive_search_completed=True)
    cs = cover_solutions(P, prime_implicants(P, P))
    ps = cover_solutions(P, prime_implicants(P, P | R))
    ip = intermediate_PIs(P, R, names, direxp)
    isol = cover_solutions(P, ip)
    return dict(P=P, N=N, R=R, complex=cs, pars=ps, inter=isol, exhaustive_search_completed=True)

def remainders_used(sol_terms, P, R):
    used = set()
    for t in sol_terms:
        used |= {m for m in minterms(t) if m in R}
    return used

def term_membership(X, term):
    cols = [X[:, i] if v == 1 else 1.0 - X[:, i] for i, v in enumerate(term) if v is not None]
    return np.min(np.vstack(cols), axis=0) if cols else np.ones(X.shape[0])

def fit(T, Y):
    st = float(T.sum())
    sy = float(Y.sum())
    a = float(np.minimum(T, Y).sum())
    b = float(np.minimum(np.minimum(T, Y), 1.0 - Y).sum())
    incl = a / st if st > 0 else np.nan
    cov = a / sy if sy > 0 else np.nan
    pri = (a - b) / (st - b) if (st - b) > 0 else np.nan
    return incl, pri, cov

def solution_fit(X, Y, terms):
    Ts = [term_membership(X, t) for t in terms]
    S = np.max(np.vstack(Ts), axis=0)
    res = []
    tot_cov = fit(S, Y)[2]
    for i, T in enumerate(Ts):
        incl, pri, cov = fit(T, Y)
        others = [Ts[j] for j in range(len(Ts)) if j != i]
        cov_wo = fit(np.max(np.vstack(others), axis=0), Y)[2] if others else 0.0
        res.append(
            dict(
                incl=incl,
                pri=pri,
                cov=cov,
                ucov=tot_cov - cov_wo,
                n_cases=int((T > 0.5).sum()),
                cases=list(np.where(T > 0.5)[0]),
            )
        )
    si, sp, sc = fit(S, Y)
    return res, dict(incl=si, pri=sp, cov=sc), S

def necessity(Xc, Y):
    a = float(np.minimum(Xc, Y).sum())
    inclN = a / float(Y.sum()) if Y.sum() > 0 else np.nan
    covN = a / float(Xc.sum()) if Xc.sum() > 0 else np.nan
    denom = float((1.0 - np.minimum(Xc, Y)).sum())
    ron = float((1.0 - Xc).sum()) / denom if denom > 0 else np.nan
    return inclN, ron, covN

# ---------------- 5. Process-Sequence & Information-Theoretic Engine ----------------
def shannon_entropy(labels):
    c = Counter(labels)
    n = len(labels)
    return -sum((v / n) * math.log2(v / n) for v in c.values() if v > 0)

def mutual_information(x_labels, y_labels):
    n = len(x_labels)
    cx = Counter(x_labels)
    cy = Counter(y_labels)
    cxy = Counter(zip(x_labels, y_labels))
    mi = 0.0
    for (x, y), v in cxy.items():
        pxy = v / n
        px = cx[x] / n
        py = cy[y] / n
        mi += pxy * math.log2(pxy / (px * py))
    hy = shannon_entropy(y_labels)
    return mi, (mi / hy if hy > 0 else 0.0)

def analyze_process_sequences(df, stages=("T0", "T1", "T2", "T3")):
    s0, s1, s2, s3 = stages
    entropies = {s: round(shannon_entropy(df[s].tolist()), 3) for s in stages}
    mi_to_final = {}
    for s in [s0, s1, s2]:
        mi, nmi = mutual_information(df[s].tolist(), df[s3].tolist())
        mi_to_final[s] = {"MI_bits": round(mi, 3), "NMI_share": round(nmi, 3)}
    t01 = [f"{a}|{b}" for a, b in zip(df[s0], df[s1])]
    mi01, nmi01 = mutual_information(t01, df[s3].tolist())
    mi_to_final[f"{s0}_plus_{s1}"] = {"MI_bits": round(mi01, 3), "NMI_share": round(nmi01, 3)}
    t012 = [f"{a}|{b}|{c}" for a, b, c in zip(df[s0], df[s1], df[s2])]
    mi012, nmi012 = mutual_information(t012, df[s3].tolist())
    mi_to_final[f"{s0}_plus_{s1}_plus_{s2}"] = {"MI_bits": round(mi012, 3), "NMI_share": round(nmi012, 3)}

    transitions = {}
    for a, b in [(s0, s1), (s1, s2), (s2, s3), (s0, s3)]:
        ct = pd.crosstab(df[a], df[b])
        prob = ct.div(ct.sum(axis=1), axis=0).round(3)
        transitions[f"{a}_to_{b}"] = {"counts": ct.to_dict(), "probs": prob.to_dict()}

    seq_groups = defaultdict(list)
    for _, r in df.iterrows():
        seq_groups[(r[s0], r[s1], r[s2], r[s3])].append(r["case_id"])
    trajectories = [
        {s0: k[0], s1: k[1], s2: k[2], s3: k[3], "n": len(v), "cases": v}
        for k, v in sorted(seq_groups.items(), key=lambda x: (-len(x[1]), x[0]))
    ]
    return {
        "stage_entropies_bits": entropies,
        "information_gain_toward_final": mi_to_final,
        "transitions": transitions,
        "trajectories": trajectories,
    }

# ---------------- 6. Regime Discriminant & Linear OLS Failure Engine ----------------
def kruskal_eta2(df, group_col, val_col):
    sub = df[[group_col, val_col]].dropna()
    n = len(sub)
    if n <= 4:
        return np.nan, np.nan
    ranks = sub[val_col].rank(method="average")
    grand_mean = (n + 1) / 2.0
    vc = sub[val_col].value_counts()
    tie_sum = sum(t**3 - t for t in vc if t > 1)
    tie_corr = 1.0 - tie_sum / (n**3 - n) if (n**3 - n) > 0 else 1.0
    ss_between = 0.0
    for _, grp in sub.groupby(group_col):
        r_g = ranks.loc[grp.index]
        ss_between += len(r_g) * ((r_g.mean() - grand_mean) ** 2)
    H = (12.0 / (n * (n + 1))) * ss_between / (tie_corr if tie_corr > 0 else 1.0)
    k = sub[group_col].nunique()
    eta2 = max(0.0, (H - k + 1) / (n - k)) if (n - k) > 0 else np.nan
    return round(float(H), 3), round(float(eta2), 3)

def ols_failure_audit(df, conds, outcome_cols=("DEC_AUTH", "GEN_AUTH")):
    sub = df.dropna(subset=list(conds) + list(outcome_cols)).copy()
    X_raw = sub[list(conds)].values
    n, k = X_raw.shape
    X = np.column_stack([np.ones(n), X_raw])
    out = {}
    for ycol in outcome_cols:
        y = sub[ycol].values
        beta, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
        yhat = X @ beta
        resid = y - yhat
        ss_res = float(np.sum(resid ** 2))
        ss_tot = float(np.sum((y - y.mean()) ** 2))
        r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else np.nan
        adj_r2 = 1.0 - (1.0 - r2) * (n - 1) / (n - k - 1)
        sigma2 = ss_res / (n - k - 1)
        cov_b = sigma2 * np.linalg.inv(X.T @ X)
        se = np.sqrt(np.diag(cov_b))
        t_stats = beta / se
        coefs = [
            {"term": name, "beta": round(float(beta[i]), 3), "se": round(float(se[i]), 3), "t": round(float(t_stats[i]), 2)}
            for i, name in enumerate(["Intercept"] + list(conds))
        ]
        anomalies = []
        for cid, yi, yhi, ri in zip(sub["case_id"], y, yhat, resid):
            if (yi > 0.5) != (yhi > 0.5) or abs(ri) >= 0.23:
                anomalies.append({
                    "case_id": cid,
                    "actual": round(float(yi), 3),
                    "predicted": round(float(yhi), 3),
                    "residual": round(float(ri), 3),
                    "sign_error": bool((yi > 0.5) != (yhi > 0.5)),
                })
        out[ycol] = {"n": n, "R2": round(r2, 3), "adj_R2": round(adj_r2, 3), "coefs": coefs, "anomalies": anomalies}
    return out
