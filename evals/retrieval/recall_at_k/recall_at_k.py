def mean_recall_at_k(all_retrieved_ids,all_relevant_ids,k:int)->float:
    """Mean Recall@k over multiple queries"""
    assert len(all_retrieved_ids) == len(all_relevant_ids)
    total = 0.0
    for retrieved_docs,relevant_ids in zip(all_retrieved_ids,all_relevant_ids):
        if not relevant_ids:
            continue
        retrieved_docs = retrieved_docs[:k]
        relevant_retrieved = sum(1 for doc_id in retrieved_docs if doc_id in relevant_ids)
        total += relevant_retrieved/len(relevant_ids)
    return total/len(all_relevant_ids)