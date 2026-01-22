def mean_precision_at_k(all_retrieved_ids,all_relevant_ids,k:int)->float:
    """Mean Precison over k cutoff values"""
    assert len(all_retrieved_ids) == len(all_relevant_ids)
    total = 0.0
    for retrieved_ids,relevant_ids in zip(all_retrieved_ids,all_relevant_ids):
        if k == 0:
            continue
        retrieved_ids = retrieved_ids[:k]
        relevant_retrieved = sum(1 for doc_id in retrieved_ids if doc_id in relevant_ids)
        total = total+(relevant_retrieved/k)
    return total/len(all_retrieved_ids)
