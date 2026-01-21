# Mean Reciprocal Rank (MRR)

## What is MRR?

Mean Reciprocal Rank (MRR) evaluates how early the first relevant document appears in a ranked list of retrieval results.

It is widely used in:

- Search engines
- Question answering systems
- Retrieval-Augmented Generation (RAG)
- Information retrieval evaluation

---

## 📐 Formula

**Reciprocal Rank (RR) for one query:**

RR = 1 / rank_of_first_relevant_document

**Mean Reciprocal Rank (MRR) over N queries:**

MRR = (RR₁ + RR₂ + ... + RRₙ) / N

---

## Example

### Retrieved Results

```python
all_retrieved = [
    ["D7", "D3", "D9", "D1"],
    ["D2", "D4", "D6"],
    ["D8", "D5", "D3"]
]
```

### Relevant Documents

```python
all_relevant = [
    {"D1", "D3"},
    {"D4"},
    {"D10"}
]
```

---

### Step-by-Step Scores

| Query | First Relevant Rank | RR  |
| ----- | ------------------- | --- |
| Q1    | 2                   | 0.5 |
| Q2    | 2                   | 0.5 |
| Q3    | Not Found           | 0.0 |

[
MRR = (0.5 + 0.5 + 0.0) / 3 = 0.3333
]

---

## ✅ When to Use MRR

Use MRR when:

- Only **one correct answer** is needed
- Top-ranked results are more important than lower-ranked ones

Typical use cases:

- FAQ retrieval
- Search ranking evaluation
- RAG chunk retrieval quality

---

## ⚠️ Limitations

MRR considers **only the first relevant document** and ignores:

- Total number of relevant documents retrieved
- Ranking quality beyond the first hit

---
