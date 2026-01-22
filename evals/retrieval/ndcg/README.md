# NDCG@K — Normalized Discounted Cumulative Gain

## What is NDCG?

NDCG (Normalized Discounted Cumulative Gain) is a ranking evaluation metric that measures:

- How relevant the retrieved documents are, and
- How high they appear in the ranked list

It supports **graded relevance** (not just relevant / not relevant) and rewards placing highly relevant documents at top ranks.

Commonly used in:

- Search engines
- Recommendation systems
- Information retrieval
- RAG (Retrieval-Augmented Generation) evaluation

---

### Discounted Cumulative Gain (DCG)

For the top **K** results:

DCG@K = Σ ( (2^relᵢ − 1) / log₂(i + 1) )

Where:

- `relᵢ` = relevance score at rank `i`
- `i` = rank position (starting from 1)

---

### Ideal Discounted Cumulative Gain (IDCG)

IDCG@K is DCG@K computed on the **ideal ranking** (documents sorted by highest relevance first).

---

### Normalized DCG

NDCG@K = DCG@K / IDCG@K

Final score range:

0 ≤ NDCG@K ≤ 1

---
