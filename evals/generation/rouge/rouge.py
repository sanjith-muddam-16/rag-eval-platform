from typing import List, Dict
from rouge_score import rouge_scorer
import statistics


def rouge_batch(
    references: List[str],
    candidates: List[str]
) -> Dict:
    """
    Computes ROUGE-1, ROUGE-2, ROUGE-L F1 scores for multiple samples.

    Returns:
        {
            "mean": {
                "rouge1": float,
                "rouge2": float,
                "rougeL": float
            },
            "per_sample": List[Dict]
        }
    """
    assert len(references) == len(candidates), "Mismatched input lengths"

    scorer = rouge_scorer.RougeScorer(
        ["rouge1", "rouge2", "rougeL"],
        use_stemmer=True
    )

    per_sample = []

    for ref, cand in zip(references, candidates):
        scores = scorer.score(ref, cand)

        per_sample.append({
            "rouge1": scores["rouge1"].fmeasure,
            "rouge2": scores["rouge2"].fmeasure,
            "rougeL": scores["rougeL"].fmeasure,
        })

    mean_scores = {
        "rouge1": statistics.mean(s["rouge1"] for s in per_sample),
        "rouge2": statistics.mean(s["rouge2"] for s in per_sample),
        "rougeL": statistics.mean(s["rougeL"] for s in per_sample),
    } if per_sample else {"rouge1": 0.0, "rouge2": 0.0, "rougeL": 0.0}

    return {
        "mean": mean_scores,
        "per_sample": per_sample
    }

"""
Sample Output:
{
  "mean": {
    "rouge1": 0.41,
    "rouge2": 0.28,
    "rougeL": 0.37
  },
  "per_sample": [
    {"rouge1": 0.3, "rouge2": 0.1, "rougeL": 0.25},
    {"rouge1": 0.5, "rouge2": 0.4, "rougeL": 0.45}
  ]
}
"""
def normalize_rouge_results(rouge_result: dict):
    records = []

    # aggregate
    for metric, score in rouge_result["mean"].items():
        records.append({
            "sample_id": "ALL",
            "metric": metric,
            "score": score,
            "group": "mean"
        })

    # per-sample
    for idx, sample_scores in enumerate(rouge_result["per_sample"]):
        for metric, score in sample_scores.items():
            records.append({
                "sample_id": idx,
                "metric": metric,
                "score": score,
                "group": "per_sample"
            })

    return records

