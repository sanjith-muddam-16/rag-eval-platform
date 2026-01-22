# Mean Recall@K — Retrieval Evaluation Metric

Mean Recall@K is a standard metric used to evaluate **how well a retrieval system covers all relevant documents** within the top-K results across multiple queries.

It is widely used in:

- Search engines
- Recommendation systems
- RAG (Retrieval-Augmented Generation) pipelines

---

## What is Recall@K?

Recall@K measures the fraction of **total relevant documents that appear in the top-K retrieved results**.

It answers the question:

> Of all relevant documents that exist, how many did the system retrieve?

---

## Formula

### For a Single Query

Recall@K = (Relevant documents in top K) / (Total relevant documents)

### For Multiple Queries

Mean Recall@K = (Recall@K₁ + Recall@K₂ + ... + Recall@Kₙ) / N

Where:

- K = cutoff rank
- N = number of queries

---

all_retrieved_ids = [
["D1", "D3", "D5", "D7"],
["D2", "D4", "D6"]
]

all_relevant_ids = [
{"D1", "D5", "D9"},
{"D4"}
]

Calculation for K = 2
Query 1

Top-2 retrieved: [D1, D3]
Relevant in top-2: 1
Total relevant: 3

Recall@2 = 1 / 3 ≈ 0.33

Query 2

Top-2 retrieved: [D2, D4]
Relevant in top-2: 1
Total relevant: 1

Recall@2 = 1 / 1 = 1.0
Mean Recall@2 = (0.33 + 1.0) / 2 ≈ 0.67

---

### When to Use Mean Recall@K

Mean Recall@K is especially important when:

Missing relevant documents is costly

You want high coverage of relevant information

Building RAG retrievers where missing chunks leads to hallucinations

### Limitations

Recall@K does not consider ranking quality among relevant documents.

To evaluate ranking behavior, combine with:

Precision@K

Mean Reciprocal Rank (MRR)

NDCG@K
