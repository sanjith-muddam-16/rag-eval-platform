# ROUGE Score (Batch Evaluation)

ROUGE (Recall-Oriented Understudy for Gisting Evaluation) is a family of
metrics used to evaluate text generation quality based on **overlap of
n-grams and longest common subsequences**.

It is widely used in:

- Text Summarization
- Question Answering
- RAG answer evaluation

---

## What This Implementation Does

This implementation computes:

- ROUGE-1 F1 (unigram overlap)
- ROUGE-2 F1 (bigram overlap)
- ROUGE-L F1 (longest common subsequence)

For each sample and also returns:

- Mean scores across all samples

---

## ROUGE Variants Explained

| Metric  | Measures                                         |
| ------- | ------------------------------------------------ |
| ROUGE-1 | Unigram (word) overlap                           |
| ROUGE-2 | Bigram (2-word) overlap                          |
| ROUGE-L | Longest common subsequence (sequence similarity) |

All scores are reported using **F1 measure** (balance of precision and recall).

Scores range from **0 to 1**.

---

references = ["the cat is on the mat","there is a dog in the park"]
candidates = ["cat is on mat","dog in the park"]
{"mean": {"rouge1": 0.41,"rouge2": 0.28,"rougeL": 0.37},
"per_sample": [{"rouge1": 0.30, "rouge2": 0.10, "rougeL": 0.25},
{"rouge1": 0.50, "rouge2": 0.40, "rougeL": 0.45}]}

# When to Use ROUGE

ROUGE is better than BLEU when:

Paraphrasing is expected

Content coverage matters more than exact wording

Evaluating summaries or long answers

Especially useful for:

RAG answer evaluation

Document summarization

### Limitations

ROUGE does NOT measure:

Factual correctness

Logical consistency

Semantic equivalence

For modern LLM evaluation, combine with:

Embedding similarity

LLM-as-a-judge scoring
