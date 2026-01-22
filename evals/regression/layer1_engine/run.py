# evals/regression/run.py
from evals.regression.layer1_engine.similiarity import batch_semantic_drift
from evals.regression.layer1_engine.coverage import batch_coverage_drift
from evals.regression.layer1_engine.grounding import batch_grounding_drift
from evals.regression.layer1_engine.drift import detect_regression
from typing import List, Dict
import numpy as np

def run_batch_regression_eval(
    baseline_answers: List[str],
    new_answers: List[str],
    contexts: List[str],  # not used directly, but kept for future judge evals
    baseline_answer_embs: List[List[float]],
    new_answer_embs: List[List[float]],
    context_embs: List[List[float]],
    thresholds: Dict[str, float] | None = None,
):
    if thresholds is None:
        thresholds = {
            "semantic": 0.25,
            "coverage": 0.30,
            "grounding": 0.20,
        }

    sem_drifts = batch_semantic_drift(baseline_answer_embs, new_answer_embs)
    cov_drifts = batch_coverage_drift(baseline_answers, new_answers)
    grd_drifts = batch_grounding_drift(
        baseline_answer_embs, new_answer_embs, context_embs
    )

    results = []
    failures = 0

    for sem, cov, grd in zip(sem_drifts, cov_drifts, grd_drifts):
        regression = detect_regression(
            sem, cov, grd, thresholds=thresholds
        )

        if regression:
            failures += 1

        results.append({
            "semantic_drift": round(sem, 3),
            "coverage_drift": round(cov, 3),
            "grounding_drift": round(grd, 3),
            "regression": regression,
        })

    summary = {
        "num_samples": len(results),
        "num_failures": failures,
        "pass_rate": round(1 - failures / max(1, len(results)), 3),
        "mean_semantic_drift": round(float(np.mean(sem_drifts)), 3),
        "mean_coverage_drift": round(float(np.mean(cov_drifts)), 3),
        "mean_grounding_drift": round(float(np.mean(grd_drifts)), 3),
    }

    return {
        "summary": summary,
        "samples": results,
    }