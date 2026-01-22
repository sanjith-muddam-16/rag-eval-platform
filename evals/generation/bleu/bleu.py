from typing import List,Dict
from nltk.translate.bleu_score import sentence_bleu,SmoothingFunction
import statistics

def bleu_score(references:List[str],candidates:List[str])->str:
    """
    Computes sentence level Bleau scores for multiple samples
    Args: references -> List of ground truth answers
          candidates -> List of model generated answers
    Returns :
        {
            "mean_bleu":float,
            "per_sample":List[float]
        }
    """
    assert len(references) == len(candidates),"Mismatched lengths"
    smooth = SmoothingFunction().method1
    scores = []
    for ref,can in zip(references,candidates):
        score = sentence_bleu([ref.split()],can.split(),smoothing_function=smooth)
        scores.append(score)
    return {
        "mean_bleu" : statistics.mean(scores) if scores else 0.0,
        'per_sample' : scores
    }

"""
Sample output: 

{
  "mean_bleu": 0.32,
  "per_sample": [0.1, 0.5, 0.36]
}

"""
def normalize_bleu_results(bleu_result: dict):
    records = []

    # aggregate
    records.append({
        "sample_id": "ALL",
        "metric": "bleu",
        "score": bleu_result["mean_bleu"],
        "group": "mean"
    })

    # per-sample
    for idx, score in enumerate(bleu_result["per_sample"]):
        records.append({
            "sample_id": idx,
            "metric": "bleu",
            "score": score,
            "group": "per_sample"
        })

    return records

