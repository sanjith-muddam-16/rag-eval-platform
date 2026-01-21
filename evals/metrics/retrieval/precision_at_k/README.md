# Mean Precision@K — Retrieval Evaluation Metric

## What is Precision@K?

Precision@K measures how many of the **top K retrieved documents are relevant**.

It answers the question:

> Of the top K results returned, what fraction are actually relevant?

---

## Formula (GitHub-Friendly)

For a single query:

Precision@K = (Number of relevant documents in top K) / K

For multiple queries:

Mean Precision@K = (Precision@K₁ + Precision@K₂ + ... + Precision@Kₙ) / N

Where:

- K = cutoff rank
- N = number of queries

---

all_retrieved_ids = [
["D1", "D3", "D5"],
["D2", "D4", "D6"]
]

all_relevant_ids = [
{"D1", "D5"},
{"D4"}
]

| Query | Top-2 Retrieved | Relevant in Top-2 | Precision@2 |
| ----- | --------------- | ----------------- | ----------- |
| Q1    | [D1, D3]        | 1                 | 1 / 2 = 0.5 |
| Q2    | [D2, D4]        | 1                 | 1 / 2 = 0.5 |

Mean Precision@2 = (0.5 + 0.5) / 2 = 0.5

## When to Use Precision@K

Use Precision@K when:

Showing irrelevant results is costly

You care about top-rank quality

Ranking systems must be accurate at early positions

## Common use cases:

Search ranking evaluation

Recommendation systems

RAG document re-ranking

## Limitations

Precision@K does NOT measure:

Whether all relevant documents were retrieved

How good the ordering is among relevant results
