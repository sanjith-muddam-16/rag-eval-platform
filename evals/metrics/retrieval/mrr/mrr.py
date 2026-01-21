def mean_reciprocal_rank(all_retrieved_documents, all_relevant_documents):
    assert len(all_retrieved_documents) == len(all_relevant_documents)

    total = 0.0
    for retrieved, relevant in zip(all_retrieved_documents, all_relevant_documents):
        for idx, doc in enumerate(retrieved):
            if doc in relevant:
                total += 1.0 / (idx + 1)
                break
    return total / len(all_retrieved_documents)
