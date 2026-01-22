from rogue_score import rogue_scorer
from typing import List, Tuple
scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)

def batch_coverage_score(baseline_answers: List[str],new_answers: List[str]) -> List[float]:
    """Pairwise coverage recall for multiple answers."""
    if len(baseline_answers) != len(new_answers):
        raise ValueError("baseline_answers and new_answers must have same length")
    results = []
    for b, n in zip(baseline_answers, new_answers):
        scores = scorer.score(b, n)
        results.append(scores["rougeL"].recall)
    return results

def batch_coverage_drift(baseline_answers: List[str],new_answers: List[str],) -> List[float]:
    """Drift = 1 - coverage recall, per sample."""
    scores = batch_coverage_score(baseline_answers, new_answers)
    return [1.0 - s for s in scores]

