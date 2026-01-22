from rogue_score import rogue_scorer
from typing import List,Tuple
scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)

def coverage_score(pairs:List[Tuple[str, str]])->List[float]:
    """
    Measures how much of baseline is preserved in new answers (ROUGE-L recall)
    for multiple (baseline, new) answer pairs.
    """
    scores = []
    for baseline_answer,new_answer in pairs:
        rouge = scorer.score(baseline_answer, new_answer)
        scores.append(rouge["rougeL"].recall)
    
    return scores

def coverage_drift( pairs: List[Tuple[str, str]])->List[float]:
    """Drift = 1 - coverage recall, per example."""
    return [1.0 - s for s in coverage_score(pairs)]
