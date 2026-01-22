import math
from typing import List, Dict

def dcg_at_k(relevances: List[int], k: int) -> float:
    """relevances: relevance scores in retrieved order k: cutoff rank"""
    return sum(
        (2 ** rel - 1) / math.log2(idx + 2)
        for idx, rel in enumerate(relevances[:k])
    )


def ndcg_at_k_single(retrieved_ids: List[str],relevance_map: Dict[str, int],k: int) -> float:
    """
    retrieved_ids : ranked list of retrieved document IDs
    relevance_map : {doc_id: relevance_score}
    k             : cutoff rank
    """

    relevances = [relevance_map.get(doc_id, 0) for doc_id in retrieved_ids]
    ideal_relevances = sorted(relevance_map.values(), reverse=True)
    dcg = dcg_at_k(relevances, k)
    idcg = dcg_at_k(ideal_relevances, k)
    return dcg / idcg if idcg > 0 else 0.0

def mean_ndcg_at_k(all_retrieved: List[List[str]],all_relevance_maps: List[Dict[str, int]],k: int) -> float:
    """
    all_retrieved       : list of retrieved lists (one per query)
    all_relevance_maps  : list of relevance maps (one per query)
    k                   : cutoff rank
    """

    assert len(all_retrieved) == len(all_relevance_maps), "Query count mismatch"
    total_ndcg = 0.0
    for retrieved, relevance_map in zip(all_retrieved, all_relevance_maps):
        total_ndcg += ndcg_at_k_single(retrieved, relevance_map, k)
    return total_ndcg / len(all_retrieved)
