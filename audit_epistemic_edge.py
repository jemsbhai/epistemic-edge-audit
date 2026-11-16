#!/usr/bin/env python3
"""Independent artifact audit of the Epistemic Edge paper's three headline claims.

Recomputes every number from the released ground-truth artifacts in the public
repository (github.com/jemsbhai/epistemic-edge, experiments/results/) without
re-running any LLM or the BATADAL pipeline.

Conducted during the Apart Research AI x Epistemics Sprint, Nov 13-15, 2026.
Author: Muntaser Syed (auditing his own published work; see report for the
disclosure and the limitations of self-audit).

Usage: python3 audit_epistemic_edge.py <path-to-epistemic-edge-repo>
Writes audit_results.json next to this script.
"""
import bisect
import csv
import glob
import json
import os
import statistics
import sys

REPO = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/workspace/epistemic-edge-repo")
RES = os.path.join(REPO, "experiments", "results")
out = {}

# ---------------------------------------------------------------- Claim 1
# Paper: removing the epistemic layer collapses threshold-guardrail accuracy
# from 1.00 to exactly 0.40 across all seven models (2,800 trials).
# Audit: check EVERY released ablation run file, not only the published set.
CONDITIONS = ["C", "D", "E1", "E2", "G"]  # full, no_decay, no_fusion_vacuous, no_fusion_passthrough, no_epistemic
ablation = []
for f in sorted(glob.glob(os.path.join(RES, "02_ablation_*.json"))):
    d = json.load(open(f))
    cs = d.get("condition_summaries", {})
    row = {"file": os.path.basename(f), "model": d.get("model_size"),
           "total_trials": d.get("total_trials")}
    for c in CONDITIONS:
        s = cs.get(c)
        row[c] = s["threshold_guardrail_accuracy"] if s else None
    ablation.append(row)
out["claim1_ablation_runs"] = ablation
out["claim1_summary"] = {
    "runs_audited": len(ablation),
    "total_trials_all_runs": sum(r["total_trials"] for r in ablation),
    "runs_with_full_pipeline_1.00": sum(1 for r in ablation if r["C"] == 1.0),
    "runs_with_no_epistemic_0.40": sum(1 for r in ablation if r["G"] == 0.4),
    "runs_with_no_fusion_vacuous_0.40": sum(1 for r in ablation if r["E1"] == 0.4),
}

# ---------------------------------------------------------------- Claim 2
# Paper: BATADAL AUROC 0.9004 with no trained weights (422 configurations).
BD = os.path.join(RES, "batadal")
summaries = {}
for f in sorted(glob.glob(os.path.join(BD, "03_batadal_summary_*.json"))):
    d = json.load(open(f))
    summaries[os.path.basename(f)] = {
        "best_auroc": d.get("best_auroc"),
        "num_configurations": d.get("num_configurations"),
        "best_config": {k: d["best_config"].get(k) for k in
                        ("strategy", "k", "lambda", "fusion", "decay", "phys_mode", "anomaly_score", "smoothing")},
    }
out["claim2_summaries"] = summaries
repro_f = glob.glob(os.path.join(BD, "03_batadal_reproducibility_*.json"))[0]
out["claim2_reproducibility_record"] = json.load(open(repro_f))

heat = list(csv.DictReader(open(os.path.join(BD, "03_batadal_heatmap_20260416_044859.csv"))))
out["claim2_heatmap_rows"] = len(heat)

# Independent paired fusion analysis over the full grid (audit's own analysis,
# not the paper's Wilcoxon test): match configurations differing only in
# use_fusion and compare headline AUROC.
from collections import defaultdict
key = lambda r: (r["phase"], r["strategy"], r["window_k"], r["decay_lambda"], r["use_decay"],
                 r["physics_bounds_mode"], r["anomaly_score"], r["smoothing_window"], r["threshold_mode"])
pairs = defaultdict(dict)
for r in heat:
    pairs[key(r)][r["use_fusion"]] = float(r["auroc"])
diffs = [v["True"] - v["False"] for v in pairs.values() if "True" in v and "False" in v]
out["claim2_fusion_paired"] = {
    "matched_pairs": len(diffs),
    "mean_diff": round(statistics.mean(diffs), 4),
    "median_diff": round(statistics.median(diffs), 4),
    "frac_positive": round(sum(1 for x in diffs if x > 0) / len(diffs), 3),
    "frac_zero": round(sum(1 for x in diffs if x == 0) / len(diffs), 3),
}

# ---------------------------------------------------------------- Claim 3
# Paper: different BATADAL events are optimally detected by different
# SL-derived signals; no single signal wins on all five events.
sig_cols = ["auroc_fused_u", "auroc_fused_d", "auroc_max_d", "auroc_max_u", "auroc_mean_u", "auroc_composite_ud"]
out["claim3_signal_maxima"] = {
    c: round(max(float(r[c]) for r in heat if r[c]), 4) for c in sig_cols
}

# Per-event re-analysis from the released primary timeseries (audit protocol:
# event-window samples as positives, all non-attack samples as negatives,
# rank-based AUROC per signal).
ts = list(csv.DictReader(open(os.path.join(BD, "03_batadal_timeseries_20260416_044859.csv"))))
signals = ["fused_u", "fused_b", "fused_d", "max_u", "mean_u", "min_b", "mean_b", "max_d"]
labels = [int(r["is_attack"]) for r in ts]
events, i = [], 0
while i < len(labels):
    if labels[i] == 1:
        j = i
        while j < len(labels) and labels[j] == 1:
            j += 1
        events.append((i, j - 1)); i = j
    else:
        i += 1

def auroc(pos, neg):
    ns = sorted(neg)
    wins = 0.0
    for p in pos:
        lo = bisect.bisect_left(ns, p); hi = bisect.bisect_right(ns, p)
        wins += lo + 0.5 * (hi - lo)
    return wins / (len(pos) * len(neg))

neg = {s: [float(r[s]) for r, l in zip(ts, labels) if l == 0] for s in signals}
per_event = []
for idx, (a, b) in enumerate(events, 1):
    scores = {s: round(auroc([float(ts[k][s]) for k in range(a, b + 1)], neg[s]), 3) for s in signals}
    per_event.append({"event": idx, "rows": [a, b], "best_signal": max(scores, key=scores.get), "auroc": scores})
out["claim3_per_event"] = per_event

dest = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audit_results.json")
with open(dest, "w") as fh:
    json.dump(out, fh, indent=1)
print(json.dumps(out["claim1_summary"], indent=1))
print("BATADAL best_aurocs:", {k: v["best_auroc"] for k, v in summaries.items()})
print("fusion paired:", out["claim2_fusion_paired"])
print("signal maxima:", out["claim3_signal_maxima"])
print("per-event winners:", [(e["event"], e["best_signal"]) for e in per_event])
print("wrote", dest)
