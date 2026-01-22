from typing import List
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def batch_semantic_similarity(baseline_embs: List[List[float]],new_embs: List[List[float]]) -> List[float]:
    """
    Computes cosine similarity for multiple embedding pairs.[i] is compared with 
    new_embs[i].Returns list of similarities.
    """
    if len(baseline_embs) != len(new_embs):
        raise ValueError("baseline_embs and new_embs must have same length")

    A = np.array(baseline_embs, dtype=np.float32)  
    B = np.array(new_embs, dtype=np.float32)       
    sim_matrix = cosine_similarity(A, B)
    return np.diag(sim_matrix).tolist()

def batch_semantic_drift(baseline_embs: List[List[float]],new_embs: List[List[float]])->float:
    """Drift = 1 - similarity, per pair."""
    sims = batch_semantic_similarity(baseline_embs, new_embs)
    return [1.0 - s for s in sims]



