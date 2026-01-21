# BLEU Score (Batch Evaluation)

BLEU (Bilingual Evaluation Understudy) is a metric used to evaluate
text generation quality by measuring **n-gram overlap** between
model-generated text and reference text.

It is widely used in:

- Machine Translation
- Text Summarization
- Question Answering
- RAG answer evaluation

---

## What This Implementation Does

This implementation computes:

- Sentence-level BLEU for each sample
- Mean BLEU across all samples (batch)

Each `(reference, candidate)` pair is treated as one evaluation sample.

---

## BLEU Score Intuition

BLEU measures how similar the generated sentence is to the reference
based on overlapping word sequences (n-grams).

Higher BLEU → closer to reference wording  
Lower BLEU → more different wording

BLEU ranges from **0 to 1**.

---

references = ["the cat is on the mat","there is a dog in the park"]
candidates = ["cat is on mat","dog in the park"]
{"mean_bleu": 0.32,"per_sample": [0.28, 0.36]}

### Important Notes

This is sentence-level BLEU averaged over samples, not corpus BLEU.

Corpus BLEU is commonly used in research benchmarks.

Sentence BLEU is useful for:debugging,per-example evaluation,RAG answer scoring

### When to Use BLEU

Word-level overlap matters

Output phrasing is important

You want strict matching

### Not ideal when:

Paraphrasing is common

Answers are semantically correct but phrased differently

In such cases, combine with ROUGE or embedding-based metrics.
