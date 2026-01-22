import numpy as np
from typing import List
from sklearn.metrics.pairwise import cosine_similarity

def batch_grounding_score(answer_embs: List[List[float]],context_embs: List[List[float]],) -> List[float]:
    if len(answer_embs) != len(context_embs):
        raise ValueError("answer_embs and context_embs must have same length")
    
    A = np.array(answer_embs, dtype=np.float32)   
    C = np.array(context_embs, dtype=np.float32)

    sims = cosine_similarity(A, C)  
    return np.diag(sims).tolist()

def batch_grounding_drift(baseline_answer_embs: List[List[float]],new_answer_embs: List[List[float]],
    context_embs: List[List[float]]) -> List[float]:
    #Drift = max(0, baseline_grounding - new_grounding) per sample.Penalizes only degradation in grounding.
    if not (len(baseline_answer_embs)== len(new_answer_embs)== len(context_embs)):
        raise ValueError("All input lists must have same length")

    base_scores = batch_grounding_score(baseline_answer_embs, context_embs)
    new_scores = batch_grounding_score(new_answer_embs, context_embs)

    drifts = [max(0.0, b - n) for b, n in zip(base_scores, new_scores)]
    return drifts

def batch_grounding_metrics(baseline_answer_embs: List[List[float]],new_answer_embs: List[List[float]],
    context_embs: List[List[float]]):
    base = batch_grounding_score(baseline_answer_embs, context_embs)
    new = batch_grounding_score(new_answer_embs, context_embs)
    drift = [max(0.0, b - n) for b, n in zip(base, new)]
    return base, new, drift


